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
        # share_to_feed=false: il reel NON entra nella griglia del profilo
        # (regola del proprietario, 04/09/2026). Resta dove conta — nella
        # scheda Reel e nei feed di chi non ci segue, che e' da dove arriva
        # tutta la sua copertura — ma la griglia resta il catalogo: solo
        # caroselli, sei tavole l'uno, in ordine di scheda. Chi apre il
        # profilo deve vedere un catalogo, non un misto.
        # NOTA: si decide alla creazione del container e non si cambia
        # dopo. I dieci reel usciti prima di questa riga sono gia' nella
        # griglia e l'API non li puo' togliere: si fa a mano dall'app.
        c = P.api("POST", f"{ig_user}/media", token,
                  media_type="REELS", video_url=url, caption=didascalia,
                  share_to_feed="false")
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

    # Primo commento con le menzioni.
    #
    # LEZIONE IMPARATA (04/09/2026). Questo blocco c'era in pubblica.py e
    # NON qui: sette reel sono usciti con le menzioni solo in didascalia.
    # Su un reel la didascalia e' ancora meno visibile che su un carosello
    # — sta sotto il video, tagliata dopo due righe — quindi il tag c'era
    # ma la NOTIFICA all'account taggato non partiva. Cioe' esattamente
    # niente: taggare senza notificare non serve a nessuno.
    # La regola 3 diceva gia' «menzioni in didascalia E nel primo
    # commento»: era scritta, e valeva solo per meta' del codice.
    # REGOLA: quando due file pubblicano la stessa cosa in due modi, il
    # secondo non e' finito finche' non fa TUTTO quello che fa il primo.
    # Come nel carosello, il commento non e' critico: se fallisce il reel
    # resta pubblicato e si segnala soltanto.
    try:
        commento = contenuti.primo_commento(scheda)
        if commento:
            P.api("POST", f"{media_id}/comments", token, message=commento)
            print("[ok] primo commento con menzioni")
    except Exception as e:
        P.segnala_errore(f"primo commento fallito per il reel '{slug}'",
                         f"Il reel e' pubblicato ({media_id}); solo il commento e' fallito: {e}")

    stato.setdefault("reel", []).append({
        "slug": slug,
        "quando": dt.datetime.now(dt.timezone.utc).isoformat(),
        "media_id": media_id,
        "permalink": v.get("permalink"),
    })
    P.scrivi_stato(stato, f"stato: reel {slug}")
    return 0


def prossimo_reel():
    """La scheda piu' vecchia gia' uscita nel feed che non ha ancora avuto
    il suo reel. Si parte dalle vecchie apposta: hanno gia' esaurito la
    loro spinta nel feed, e il reel gliene da' una seconda."""
    stato = P.leggi_stato()
    fatti = gia_pubblicati(stato)
    for p in stato["pubblicati"]:
        if p["slug"] not in fatti:
            return p["slug"]
    return None


if __name__ == "__main__":
    slug = sys.argv[1] if len(sys.argv) > 1 else "--prossimo"
    if slug == "--prossimo":
        slug = prossimo_reel()
        if slug is None:
            print("[stop] tutte le schede pubblicate hanno gia' il loro reel.")
            raise SystemExit(0)
        print(f"[reel] scelto in automatico: {slug}")
    raise SystemExit(main(slug))
