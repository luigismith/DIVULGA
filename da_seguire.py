# -*- coding: utf-8 -*-
"""ELETTROFONI — chi seguire PRIMA che esca la scheda che lo tagga.

REGOLA DEL PROPRIETARIO (31/08/2026): le pagine che taggheremo si
seguono prima, non dopo. Un tag da un account che non ti segue e' una
richiesta; un tag da un account che ti segue e' una conversazione — e
chi riceve la notifica va a vedere chi sei.

PERCHE' NON LO FA IL PROGRAMMA. L'API di Instagram non espone nessun
endpoint per seguire un account: non e' un permesso mancante, non
esiste. Ed e' voluto — automatizzare i «segui» viola le regole d'uso di
Instagram ed e' uno dei comportamenti che fanno scattare i blocchi.
Quindi questo file non segue nessuno: prepara la lista, in ordine di
uscita, e il proprietario tocca cinque volte lo schermo.

La lista si pulisce da sola: gli handle di una scheda spariscono appena
la scheda viene pubblicata, quindi resta sempre solo cio' che serve.
"""
import datetime as dt
import json
import pathlib
import zoneinfo

import contenuti

RADICE = pathlib.Path(__file__).resolve().parent
ROMA = zoneinfo.ZoneInfo("Europe/Rome")


def handle_di(scheda):
    """Tutti gli account che quella scheda taggherà, senza doppioni."""
    fuori = []
    for u in scheda["chi_lusata"]:
        if u.get("ig"):
            fuori.append((u["ig"], u["artista"]))
    for m in scheda.get("menzioni_extra", []):
        if m.get("ig"):
            fuori.append((m["ig"], "menzione in didascalia"))
    visti, unici = set(), []
    for h, chi in fuori:
        if h not in visti:
            visti.add(h)
            unici.append((h, chi))
    return unici


def main(giorni=10):
    stato = json.loads((RADICE / "stato.json").read_text())
    gia = {p["slug"] for p in stato["pubblicati"]}
    coda = [s for s in contenuti.SCHEDE if s["verificata"] and s["slug"] not in gia]

    oggi = dt.datetime.now(ROMA).date()
    # LEZIONE IMPARATA (23/09/2026): la prima scheda della coda usciva
    # «domani» per definizione (days=i+1). Ma prima delle 18 la giornata di
    # oggi non ha ancora pubblicato, quindi la prima scheda esce OGGI, e
    # questa lista diceva al proprietario di seguire un account entro
    # domani mentre il tag partiva fra cinque ore. Una lista di preavviso
    # che arriva tardi e' peggio di nessuna lista: sembra di essere a posto.
    # Adesso la prima data si deduce dall'ultimo post, non si presume.
    ultimo = max((dt.datetime.fromisoformat(p["quando"]).astimezone(ROMA).date()
                  for p in stato["pubblicati"]), default=None)
    primo = oggi + dt.timedelta(days=1) if ultimo == oggi else oggi

    # Un account si segue UNA volta sola, anche se lo taggano tre schede:
    # la lista utile e' quella senza doppioni, ordinata per quando serve.
    visti, elenco = set(), []
    for i, s in enumerate(coda[:giorni]):
        quando = primo + dt.timedelta(days=i)
        for h, chi in handle_di(s):
            if h in visti:
                continue
            visti.add(h)
            elenco.append((quando, h, chi, s["strumento"]))

    print("DA SEGUIRE PRIMA CHE ESCA LA SCHEDA CHE LI TAGGA")
    print("=" * 72)
    for quando, h, chi, strumento in elenco:
        # «OGGI» e non una data: fra la scheda di oggi e quella di domani
        # c'e' tutta la differenza che questa lista serve a segnalare.
        etichetta = "OGGI " if quando == oggi else f"{quando:%d/%m}"
        print(f"  {etichetta}  https://www.instagram.com/{h}/")
        print(f"         {chi} — scheda «{strumento}»")
    print("=" * 72)
    print(f"{len(elenco)} account da seguire, uno per riga, nessun doppione.")
    print("Le schede che non compaiono non taggano nessuno: si tagga solo")
    print("quando l'account ufficiale e' stato verificato.")


if __name__ == "__main__":
    import sys
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 10)
