# -*- coding: utf-8 -*-
"""ELETTROFONI — legge i messaggi diretti (sola lettura, 16/10/2026).

Richiesta del proprietario: «puoi anche leggere i direct?». Stampa le
conversazioni più recenti con gli ultimi messaggi. Non risponde: come per
i commenti, si risponde solo col via del proprietario.

Serve il permesso instagram_business_manage_messages sul token; se manca,
l'API lo dice nell'errore e lo si stampa così com'è.
"""
import json
import sys

import token_ig
from pubblica import api


def main():
    quante = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    token, _ = token_ig.token_corrente()
    me = api("GET", "me", token, fields="user_id,username")
    io = me.get("username")
    try:
        conv = api("GET", "me/conversations", token, platform="instagram",
                   fields="updated_time,participants,messages.limit(10){message,from,created_time}",
                   limit=quante).get("data", [])
    except Exception as e:
        print(f"[direct] l'API non li dà: {e}")
        sys.exit(1)
    print(f"[direct] {len(conv)} conversazioni\n")
    for c in conv:
        altri = [p.get("username") for p in (c.get("participants") or {}).get("data", [])
                 if p.get("username") != io]
        print(f"== con @{', @'.join(a for a in altri if a)} — ultimo: {c.get('updated_time')}")
        for m in reversed((c.get("messages") or {}).get("data", [])):
            chi = (m.get("from") or {}).get("username")
            print(f"   {m.get('created_time')} @{chi}: {m.get('message')}")
        print()


if __name__ == "__main__":
    main()
