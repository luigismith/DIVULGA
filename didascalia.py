# -*- coding: utf-8 -*-
"""ELETTROFONI — si può cambiare la didascalia di un post già uscito?

Domanda del proprietario (16/10/2026). La documentazione Meta descrive la
didascalia solo alla CREAZIONE del contenitore; un connettore di terzi
dice invece che si può aggiornare. Il Graph risponde 200 anche ai
parametri che non conosce (CLAUDE.md, 29/09/2026), quindi la prova vale
solo con la rilettura.

--prova MEDIA_ID: rimanda al post la sua STESSA didascalia (nessun cambio
visibile) e stampa la risposta grezza. Se l'API la rifiuta con un errore,
la risposta è no e ci si ferma qui. Se dice sì, non basta: serve una
modifica vera e la rilettura, che si fa solo col via del proprietario.
"""
import json
import sys

import requests

import token_ig
from pubblica import GRAPH


def main():
    if len(sys.argv) < 3 or sys.argv[1] != "--prova":
        print("uso: python didascalia.py --prova MEDIA_ID"); sys.exit(2)
    mid = sys.argv[2]
    token, _ = token_ig.token_corrente()
    prima = requests.get(f"{GRAPH}/{mid}", params={"fields": "caption,timestamp,permalink",
                                                   "access_token": token}, timeout=60).json()
    cap = prima.get("caption", "")
    print(f"[prova] post {prima.get('permalink')} — didascalia di {len(cap)} caratteri")
    for versione in ("", "v23.0/"):
        r = requests.post(f"{GRAPH}/{versione}{mid}", params={"caption": cap, "access_token": token},
                          timeout=60)
        print(f"[prova] POST {versione or '(senza versione) '}{{media}}?caption=<la stessa> → "
              f"HTTP {r.status_code}: {r.text[:400]}")
    dopo = requests.get(f"{GRAPH}/{mid}", params={"fields": "caption", "access_token": token},
                        timeout=60).json().get("caption", "")
    print(f"[prova] didascalia riletta identica: {dopo == cap}")


if __name__ == "__main__":
    main()
