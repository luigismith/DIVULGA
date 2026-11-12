# -*- coding: utf-8 -*-
"""ELETTROFONI — quale scheda merita il prossimo reel con HeyGen.

Il proprietario, 12/11/2026: «il reel esce solo 2 volte a settimana
basandosi sui post di maggior successo». Il reel HeyGen (formato 4,
genera_reel_heygen.py) costa ~45 crediti e i crediti non si ricaricano
fino all'11/11/2027: si spende sulle schede che hanno già dimostrato di
interessare, non sulla scheda del giorno a caso.

Il successo si misura sull'ultima fotografia in metriche/ (la più
recente), sommando tutti i contenuti della scheda (carosello e reel):
  punteggio = like + 2 × commenti + 3 × salvataggi + 3 × condivisioni
Salvataggi e condivisioni pesano di più perché sono i gesti che portano
il contenuto a chi non ci segue (vedi CLAUDE.md, «I numeri»).
Fuori: le schede che hanno già il loro reel HeyGen, quelle senza la
registrazione vera (`reel_audio`: il suono vero sta sotto la voce, regola
del 17/10) e i contenuti fuori catalogo.

    python scegli_heygen.py          # la prima, più la classifica dei primi 5
"""
import glob
import json
import pathlib

import contenuti

RADICE = pathlib.Path(__file__).resolve().parent
PESI = {"likes": 1, "comments": 2, "saved": 3, "shares": 3}


def classifica():
    foto = sorted(glob.glob(str(RADICE / "metriche" / "*.json")))[-1]
    dati = json.loads(pathlib.Path(foto).read_text(encoding="utf-8"))
    stato = json.loads((RADICE / "stato.json").read_text(encoding="utf-8"))
    pubblicati = {p["slug"] for p in stato["pubblicati"]}
    gia = {r["slug"] for r in stato.get("reel", []) if r.get("formato") == 4}
    schede = {s["slug"]: s for s in contenuti.SCHEDE}
    punti, dettaglio = {}, {}
    for m in dati["media"]:
        slug, ins = m.get("slug"), m.get("insights") or {}
        if not slug or slug not in schede or slug not in pubblicati or slug in gia:
            continue
        if not schede[slug].get("reel_audio"):
            continue
        p = sum(peso * (ins.get(k) or 0) for k, peso in PESI.items())
        punti[slug] = punti.get(slug, 0) + p
        d = dettaglio.setdefault(slug, {k: 0 for k in PESI})
        for k in PESI:
            d[k] += ins.get(k) or 0
    ordine = sorted(punti, key=lambda s: -punti[s])
    return pathlib.Path(foto).name, [(s, punti[s], dettaglio[s]) for s in ordine]


if __name__ == "__main__":
    foto, cl = classifica()
    if not cl:
        print("")
        raise SystemExit(0)
    print(cl[0][0])
    print(f"# da {foto}", file=__import__("sys").stderr)
    for s, p, d in cl[:5]:
        print(f"#  {s:14} {p:5}  like {d['likes']}, commenti {d['comments']}, "
              f"salvataggi {d['saved']}, condivisioni {d['shares']}", file=__import__("sys").stderr)
