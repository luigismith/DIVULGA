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
    python commenti.py --tutti    # anche quelli già visti (per rileggere)
    python commenti.py --post 40  # quanti post guardare (default 12)

Gira anche da `commenti.yml` (lancio manuale, sola lettura): il token
sta solo nei secrets, quindi da una sessione si leggono così.
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
    tutti = "--tutti" in sys.argv
    quanti = MAX_POST_DA_CONTROLLARE
    if "--post" in sys.argv:
        quanti = int(sys.argv[sys.argv.index("--post") + 1])
    dati = leggi()
    visti = set(dati["visti"])

    token, _ = token_ig.token_corrente()
    me = api("GET", "me", token, fields="user_id,username")
    mio_nome = me.get("username")

    media = api("GET", "me/media", token,
                fields="id,permalink,comments_count,media_product_type",
                limit=quanti).get("data", [])

    if "--grezzo" in sys.argv:
        # Diagnosi (13/10/2026): comments_count > 0 ma /comments vuoto su
        # tutti i post, compresi i nostri primi commenti. Si stampa la
        # risposta dell'API così com'è, su tre forme della stessa domanda.
        for m in [m for m in media if m.get("comments_count")][:3]:
            print("==", m["permalink"])
            for desc, perc, par in (
                ("edge senza campi", f"{m['id']}/comments", {}),
                ("edge con campi", f"{m['id']}/comments",
                 {"fields": "id,text,username,timestamp"}),
                ("campo annidato", m["id"],
                 {"fields": "comments_count,comments{id,text,username,timestamp}"}),
            ):
                try:
                    print(f"  {desc}: {json.dumps(api('GET', perc, token, **par))[:600]}")
                except Exception as e:
                    print(f"  {desc}: ERRORE {str(e)[:400]}")
        # 16/10/2026: le stesse domande con la versione esplicita (senza
        # versione il Graph usa la più vecchia ancora attiva) e i permessi
        # del token, per capire se manca uno scope o se è la modalità app.
        conte = [m for m in media if m.get("comments_count")]
        if conte:
            mid = conte[0]["id"]
            for v in ("v21.0", "v22.0", "v23.0", "v24.0"):
                try:
                    r = api("GET", f"{v}/{mid}/comments", token, fields="id,text,username")
                    print(f"  {v}/comments: {json.dumps(r)[:300]}")
                except Exception as e:
                    print(f"  {v}/comments: ERRORE {str(e)[:300]}")
        for perc in ("me/permissions", "v23.0/me/permissions"):
            try:
                print(f"  {perc}: {json.dumps(api('GET', perc, token))[:600]}")
            except Exception as e:
                print(f"  {perc}: ERRORE {str(e)[:300]}")
        return

    nuovi = []
    for m in media:
        # Con --tutti non ci si fida di comments_count: il 13/10/2026 lo
        # script diceva «nessun commento» mentre il proprietario li leggeva
        # nell'app. Si chiedono sempre, e si stampa cosa risponde l'API.
        if not tutti and not m.get("comments_count"):
            continue
        commenti = api("GET", f"{m['id']}/comments", token,
                       fields="id,text,username,from{id,username},timestamp,like_count").get("data", [])
        if tutti:
            print(f"  · {m.get('permalink')} {m.get('media_product_type')}: "
                  f"comments_count={m.get('comments_count')}, letti={len(commenti)}")
        for c in commenti:
            # Con Instagram Login il nome sta in «from», non in «username»
            # (16/10/2026: la prima lettura vera usciva tutta «@None»).
            c["username"] = c.get("username") or (c.get("from") or {}).get("username")
            # I nostri stessi commenti (la menzione automatica) non sono
            # da presidiare: sono roba nostra.
            if c.get("username") == mio_nome:
                visti.add(c["id"])
                continue
            if tutti or c["id"] not in visti:
                c["post"] = f'{m["permalink"]} ({m.get("media_product_type", "?")})'
                nuovi.append(c)

    if not nuovi:
        print("[presidio] nessun commento nuovo.")
    else:
        print(f"[presidio] {len(nuovi)} commenti{'' if tutti else ' nuovi'}:\n")
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
