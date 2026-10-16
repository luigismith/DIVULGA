# -*- coding: utf-8 -*-
"""ELETTROFONI — pubblica le risposte ai commenti APPROVATE dal proprietario.

Le risposte stanno in `risposte.json`, scritte dalla sessione di presidio
che ha letto i commenti e approvate una per una dal proprietario (regola
del 16/10/2026: «niente risposte senza il suo via»). Questo script non
scrive niente da solo: pubblica quelle voci e basta.

Ogni voce: {"id": <id commento>, "a": "@nome", "testo": "..."} per una
risposta, oppure {"id": ..., "a": ..., "nascondi": true} per nascondere
uno spam. Le voci fatte prendono "fatto": <data> e il file si committa,
così un secondo lancio non risponde due volte.

Fra una risposta e l'altra si aspetta PAUSA secondi: quindici risposte
nello stesso minuto sono il profilo di un bot.
"""
import datetime as dt
import json
import pathlib
import subprocess
import sys
import time

import token_ig
from pubblica import api

RADICE = pathlib.Path(__file__).parent
FILE = RADICE / "risposte.json"
PAUSA = 120


def salva(voci):
    FILE.write_text(json.dumps(voci, ensure_ascii=False, indent=1) + "\n")
    subprocess.run(["git", "add", str(FILE)], check=True, cwd=RADICE)
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=RADICE).returncode:
        subprocess.run(["git", "commit", "-q", "-m", "presidio: risposte pubblicate"], check=True, cwd=RADICE)
        for _ in range(5):
            if subprocess.run(["git", "push", "-q"], cwd=RADICE).returncode == 0:
                return
            subprocess.run(["git", "pull", "-q", "--rebase", "--autostash"], cwd=RADICE)
            time.sleep(5)
        print("[warn] push dello stato delle risposte fallito")


def main():
    voci = json.loads(FILE.read_text())
    da_fare = [v for v in voci if not v.get("fatto")]
    if not da_fare:
        print("[presidio] nessuna risposta in attesa.")
        return
    token, _ = token_ig.token_corrente()
    for n, v in enumerate(da_fare):
        if n:
            time.sleep(PAUSA)
        try:
            if v.get("nascondi"):
                api("POST", v["id"], token, hide="true")
                print(f"[ok] nascosto il commento di {v['a']}")
            else:
                r = api("POST", f"{v['id']}/replies", token, message=v["testo"])
                print(f"[ok] risposto a {v['a']}: {r.get('id')}")
            v["fatto"] = dt.datetime.now(dt.timezone.utc).isoformat()
        except Exception as e:
            # Su errore API ci si ferma (regola 6): niente tentativi in ciclo.
            print(f"[STOP] {v['a']}: {e}")
            salva(voci)
            sys.exit(1)
        salva(voci)


if __name__ == "__main__":
    main()
