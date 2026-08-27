# -*- coding: utf-8 -*-
"""
ELETTROFONI — presidio dei commenti.

Scarica i commenti sui nostri post e segnala quelli MAI VISTI, così
nessuno resta senza risposta. NON risponde da solo: le risposte
automatiche a template si riconoscono lontano un miglio e fanno più
danni del silenzio. Qui si raccoglie; a rispondere, con giudizio, è la
sessione di presidio (una Routine la apre ogni giorno).

Uso:
    python commenti.py            # elenca i commenti nuovi
    python commenti.py --segna    # li marca come visti (commit su commenti.json)
"""
import datetime as dt
import json
import pathlib
import subprocess
import sys

import token_ig
from pubblica import api

RADICE = pathlib.Path(__file__).parent
FILE = RADICE / "commenti.json"
MAX_POST_DA_CONTROLLARE = 12   # gli ultimi: i vecchi non ricevono più commenti


def leggi():
    if FILE.exists():
        return json.loads(FILE.read_text())
    return {"visti": [], "ultimo_controllo": None}


def main():
    segna = "--segna" in sys.argv
    dati = leggi()
    visti = set(dati["visti"])

    token, _ = token_ig.token_corrente()
    me = api("GET", "me", token, fields="user_id,username")
    mio_nome = me.get("username")

    media = api("GET", "me/media", token,
                fields="id,permalink,comments_count",
                limit=MAX_POST_DA_CONTROLLARE).get("data", [])

    nuovi = []
    for m in media:
        if not m.get("comments_count"):
            continue
        commenti = api("GET", f"{m['id']}/comments", token,
                       fields="id,text,username,timestamp,like_count").get("data", [])
        for c in commenti:
            # I nostri stessi commenti (la menzione automatica) non sono
            # da presidiare: sono roba nostra.
            if c.get("username") == mio_nome:
                visti.add(c["id"])
                continue
            if c["id"] not in visti:
                c["post"] = m["permalink"]
                nuovi.append(c)

    if not nuovi:
        print("[presidio] nessun commento nuovo.")
    else:
        print(f"[presidio] {len(nuovi)} commenti nuovi:\n")
        for c in nuovi:
            print(f"  @{c.get('username')} — {c.get('timestamp')}")
            print(f"  «{c.get('text')}»")
            print(f"  su: {c['post']}")
            print(f"  id: {c['id']}\n")

    if segna:
        for c in nuovi:
            visti.add(c["id"])
        dati["visti"] = sorted(visti)
        dati["ultimo_controllo"] = dt.datetime.now(dt.timezone.utc).isoformat()
        FILE.write_text(json.dumps(dati, indent=1) + "\n")
        subprocess.run(["git", "add", str(FILE)], check=True, cwd=RADICE)
        diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=RADICE)
        if diff.returncode != 0:
            subprocess.run(["git", "commit", "-m", "presidio: commenti visti"], check=True, cwd=RADICE)
            subprocess.run(["git", "push"], check=True, cwd=RADICE)
        print("[presidio] segnati come visti.")


def rispondi(id_commento, testo):
    """Risponde a un commento. Usata dalla sessione di presidio, mai in
    automatico: la risposta la scrive qualcuno che ha letto il commento."""
    token, _ = token_ig.token_corrente()
    r = api("POST", f"{id_commento}/replies", token, message=testo)
    print(f"[presidio] risposta pubblicata: {r}")
    return r


if __name__ == "__main__":
    main()
