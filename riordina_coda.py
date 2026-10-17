"""Riordina la coda: prima le schede col suono vero (`reel_audio`).

Regola del proprietario (17/10/2026): «Dobbiamo lavorare meglio sul suono
reale dello strumento. Voglio che ci sia in ogni prossimo post/storia/
reel». Il publisher prende la prima scheda verificata e non pubblicata
nell'ordine di SCHEDE, e il numero di scheda sta scritto nella scheda
stessa (`numero`) e nel kick della prima battuta del reel («ELETTROFONI ·
N. 056»). Quindi riordinare a mano vuol dire anche rinumerare a mano, e
un numero sbagliato esce stampato su tavole e reel. Questo script lo fa
sul testo di contenuti.py, senza toccare le schede già uscite:

    python riordina_coda.py          # mostra il nuovo ordine, non scrive
    python riordina_coda.py --scrivi # riscrive contenuti.py

Dopo, `python contenuti.py` deve passare: lo script lo controlla da solo
ricaricando il modulo e confrontando le schede campo per campo.
"""
import importlib
import json
import re
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent
FILE = RADICE / "contenuti.py"


def _blocchi(testo):
    """Divide la lista SCHEDE in blocchi di testo, uno per scheda, ognuno
    con i commenti che lo precedono. Restituisce (testa, blocchi, coda)."""
    inizio = testo.index("SCHEDE = [\n") + len("SCHEDE = [\n")
    # la lista finisce alla prima riga "]" a colonna 0 dopo l'inizio
    fine = re.search(r"^\]\s*$", testo[inizio:], re.M).start() + inizio
    corpo = testo[inizio:fine]
    righe = corpo.splitlines(keepends=True)
    tagli = []
    for i, r in enumerate(righe):
        if r == "    {\n" and i + 1 < len(righe) and righe[i + 1].lstrip().startswith('"slug"'):
            j = i
            while j > 0 and righe[j - 1].startswith("    #"):
                j -= 1
            tagli.append(j)
    blocchi = ["".join(righe[a:b]) for a, b in zip(tagli, tagli[1:] + [len(righe)])]
    testa = testo[:inizio] + "".join(righe[:tagli[0]])
    return testa, blocchi, testo[fine:]


def _slug(blocco):
    return re.search(r'"slug": "([^"]+)"', blocco).group(1)


def _rinumera(blocco, n):
    blocco = re.sub(r'"numero": \d+,', f'"numero": {n},', blocco, count=1)
    blocco = re.sub(r"ELETTROFONI · N\. \d{3}", f"ELETTROFONI · N. {n:03d}", blocco)
    blocco = re.sub(r"^(    # -{10,} )\d+$", rf"\g<1>{n}", blocco, count=1, flags=re.M)
    return blocco


def main():
    scrivi = "--scrivi" in sys.argv
    import contenuti
    per_slug = {s["slug"]: s for s in contenuti.SCHEDE}
    stato = json.loads((RADICE / "stato.json").read_text())
    usciti = {p["slug"] for p in stato["pubblicati"]}

    testo = FILE.read_text(encoding="utf-8")
    testa, blocchi, coda = _blocchi(testo)
    if [_slug(b) for b in blocchi] != [s["slug"] for s in contenuti.SCHEDE]:
        raise SystemExit("i blocchi di testo non corrispondono a SCHEDE: non tocco niente")

    fissi = [b for b in blocchi if _slug(b) in usciti]
    if [_slug(b) for b in blocchi[:len(fissi)]] != [_slug(b) for b in fissi]:
        raise SystemExit("le schede uscite non stanno tutte in testa: non tocco niente")
    in_coda = blocchi[len(fissi):]
    # stabile: dentro i due gruppi resta l'ordine di prima
    nuovo = ([b for b in in_coda if per_slug[_slug(b)].get("reel_audio")]
             + [b for b in in_coda if not per_slug[_slug(b)].get("reel_audio")])
    primo = max((per_slug[_slug(b)]["numero"] for b in fissi), default=0) + 1
    nuovo = [_rinumera(b, primo + i) for i, b in enumerate(nuovo)]

    for i, b in enumerate(nuovo):
        s = per_slug[_slug(b)]
        print(f"{primo + i:3d}  {s['slug']:<14} {'SUONO VERO' if s.get('reel_audio') else '-- senza suono'}"
              f"   (era {s['numero']})")
    if not scrivi:
        print("\nprova: niente scritto. Con --scrivi riscrive contenuti.py.")
        return

    FILE.write_text(testa + "".join(fissi) + "".join(nuovo) + coda, encoding="utf-8")
    # Verifica: stesse schede, stessi campi, cambiano solo numero e kick 1.
    vecchie = {s["slug"]: s for s in contenuti.SCHEDE}
    importlib.reload(contenuti)
    for s in contenuti.SCHEDE:
        v = dict(vecchie.pop(s["slug"]))
        a = dict(s)
        for d in (v, a):
            d.pop("numero")
            d["reel_battute"] = d["reel_battute"][1:]
        if v != a:
            raise SystemExit(f"{s['slug']}: cambiato qualcosa oltre al numero. Ripristina con git checkout contenuti.py")
    if vecchie:
        raise SystemExit(f"schede sparite: {list(vecchie)}")
    numeri = [s["numero"] for s in contenuti.SCHEDE]
    if numeri != list(range(numeri[0], numeri[0] + len(numeri))):
        raise SystemExit(f"numeri non consecutivi: {numeri}")
    print("\nscritto e verificato: stesse schede, numeri consecutivi.")


if __name__ == "__main__":
    main()
