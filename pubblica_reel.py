# -*- coding: utf-8 -*-
"""ELETTROFONI — pubblica UN reel. Uno solo, a comando.

PERCHÉ È UN FILE A PARTE. Il publisher quotidiano non deve toccare i
reel: il post è la missione e deve restare semplice. I reel si pubblicano
a mano, quando si decide, e uno per volta.

LA REGOLA CHE COMANDA QUI. Il budget di elaborazione video dell'account
si esaurisce dopo una dozzina di container, e lo consumano ANCHE i
tentativi falliti. Quindi: UN tentativo. Se fallisce ci si ferma, si
segnala e si aspetta un'ora prima di riprovare — a mano, dopo aver
capito il perché. Nessun ciclo di retry, per nessun motivo.

Il file lo si costruisce e verifica prima con `genera_reel.py`, che non
pubblica niente. Qui si pubblica e basta.
"""
import datetime as dt
import sys

import contenuti
import pubblica as P
import token_ig


def gia_pubblicati(stato):
    return {r["slug"] for r in stato.get("reel", [])}


def main(slug):
    scheda = next((s for s in contenuti.SCHEDE if s["slug"] == slug), None)
    if scheda is None:
        print(f"[stop] nessuna scheda '{slug}'"); return 1

    stato = P.leggi_stato()

    # Idempotenza: come per i post, sta nello stato, non nell'API.
    if slug in gia_pubblicati(stato):
        print(f"[stop] il reel di '{slug}' risulta già pubblicato: non lo rifaccio.")
        return 0
    # Un reel ha senso solo per una scheda già uscita nel feed.
    if slug not in {p["slug"] for p in stato["pubblicati"]}:
        print(f"[stop] la scheda '{slug}' non è ancora stata pubblicata come post.")
        return 1

    url = f"{P.BASE_PAGES}/tavole/{slug}/reel.mp4"
    P.verifica_immagini_online([url])          # HEAD: accetta anche video/

    token, _ = token_ig.token_corrente()
    me = P.api("GET", "me", token, fields="user_id,username")
    ig_user = me.get("user_id") or me.get("id")
    print(f"[api] account: @{me.get('username')} — token {token_ig.redigi(token)}")

    didascalia = contenuti.componi_didascalia(scheda)
    try:
        c = P.api("POST", f"{ig_user}/media", token,
                  media_type="REELS", video_url=url, caption=didascalia,
                  share_to_feed="true")
        # I video ci mettono molto più delle immagini. Questa NON è una
        # riprova su errore: è l'attesa del normale ciclo di vita del
        # container. Se torna ERROR ci si ferma subito.
        P.attendi_container(c["id"], token, tentativi=30)
        r = P.api("POST", f"{ig_user}/media_publish", token, creation_id=c["id"])
    except Exception as e:
        P.segnala_errore(f"reel '{slug}': pubblicazione fallita", str(e))
        print("[stop] UN SOLO TENTATIVO: non riprovo. Aspettare un'ora e capire prima.")
        return 1

    media_id = r["id"]
    v = P.api("GET", media_id, token, fields="id,permalink,media_type,timestamp")
    print(f"[ok] reel pubblicato: {v.get('permalink')} ({v.get('media_type')})")

    stato.setdefault("reel", []).append({
        "slug": slug,
        "quando": dt.datetime.now(dt.timezone.utc).isoformat(),
        "media_id": media_id,
        "permalink": v.get("permalink"),
    })
    P.scrivi_stato(stato, f"stato: reel {slug}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("uso: python pubblica_reel.py <slug>"); raise SystemExit(1)
    raise SystemExit(main(sys.argv[1]))
