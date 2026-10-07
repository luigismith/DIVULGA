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


import genera_reel

# I reel usciti prima del 07/10/2026 non hanno il campo «formato»: sono
# tutti del formato 1 (sette scene di testo, 28 secondi).
FORMATO = 2


def gia_pubblicati(stato, formato=None):
    """Gli slug che hanno già un reel; con `formato`, solo di quel formato."""
    return {r["slug"] for r in stato.get("reel", [])
            if formato is None or r.get("formato", 1) == formato}


def main(slug):
    scheda = next((s for s in contenuti.SCHEDE if s["slug"] == slug), None)
    if scheda is None:
        print(f"[stop] nessuna scheda '{slug}'"); return 1

    stato = P.leggi_stato()

    # Idempotenza: come per i post, sta nello stato, non nell'API.
    if slug in gia_pubblicati(stato, FORMATO):
        print(f"[stop] il reel di '{slug}' (formato {FORMATO}) risulta già pubblicato: non lo rifaccio.")
        return 0
    # Un reel ha senso solo per una scheda già uscita nel feed.
    if slug not in {p["slug"] for p in stato["pubblicati"]}:
        print(f"[stop] la scheda '{slug}' non è ancora stata pubblicata come post.")
        return 1
    # RIFACIMENTO: una scheda che ha già il reel del formato 1 può averne
    # uno nuovo nel formato 2 (altre frasi, altre foto, altro ritmo: un
    # video diverso, non lo stesso ripubblicato). Succede SOLO se lo si
    # chiede per nome o con --rifacimento: la cadenza dei rifacimenti è
    # una decisione del proprietario, non di questo file.
    rifacimento = slug in gia_pubblicati(stato)
    if rifacimento:
        print(f"[reel] '{slug}' ha già un reel del formato 1: questo è il rifacimento")

    url = f"{P.BASE_PAGES}/tavole/{slug}/{genera_reel.NOME_FILE}"
    P.verifica_immagini_online([url])          # HEAD: accetta anche video/

    token, _ = token_ig.token_corrente()
    me = P.api("GET", "me", token, fields="user_id,username")
    ig_user = me.get("user_id") or me.get("id")
    print(f"[api] account: @{me.get('username')} — token {token_ig.redigi(token)}")

    # Nei rifacimenti niente @: gli account taggati sono già stati avvisati
    # dal carosello e dal primo reel. Una terza notifica per la stessa
    # scheda, da una pagina piccola, è il profilo di un bot (stessa
    # ragione per cui non si sono recuperati i commenti dei reel vecchi).
    didascalia = contenuti.componi_didascalia_reel(scheda, menzioni=not rifacimento)
    try:
        # share_to_feed=TRUE — decisione del proprietario del 07/10/2026
        # («share_to_feed true, i reel vanno anche nella griglia»), che
        # sostituisce la regola del 04/09/2026 (false, griglia = solo
        # caroselli).
        # Perché: la documentazione Meta dice che con false il reel può
        # apparire SOLO nella scheda Reel, quindi mai nel feed dei follower
        # (dove arrivano i primi «mi piace») e mai fra i reel suggeriti nel
        # feed di chi non ci segue. Dopo il 04/09 la copertura mediana dei
        # reel era scesa da 39 a 17 (anche i caroselli erano calati, da 15
        # a 8: non è tutta colpa di questo parametro, ma nessun numero
        # diceva che aiutasse).
        # NOTA: si decide alla creazione del container e non si cambia
        # dopo. I reel usciti col false restano fuori dalla griglia.
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
        commento = None if rifacimento else contenuti.primo_commento(scheda)
        if rifacimento:
            print("[ok] nessun commento: rifacimento, gli account sono già stati avvisati")
        elif commento:
            P.api("POST", f"{media_id}/comments", token, message=commento)
            print("[ok] primo commento con menzioni")
        else:
            # LEZIONE IMPARATA (26/09/2026): con l'Ondioline il log non ha
            # scritto niente, perche' quella scheda non tagga nessuno e
            # `commento` era None. Ma chi controlla il run cerca proprio la
            # riga «primo commento con menzioni», e la sua assenza voleva
            # dire due cose opposte: «non c'era nessuno da avvisare» e «il
            # commento non e' partito». Un controllo che non sa distinguere
            # le due non e' un controllo. Adesso il silenzio lo dice il log.
            print("[ok] nessun commento: questa scheda non tagga nessuno")
    except Exception as e:
        P.segnala_errore(f"primo commento fallito per il reel '{slug}'",
                         f"Il reel e' pubblicato ({media_id}); solo il commento e' fallito: {e}")

    stato.setdefault("reel", []).append({
        "slug": slug,
        "formato": FORMATO,
        "quando": dt.datetime.now(dt.timezone.utc).isoformat(),
        "media_id": media_id,
        "permalink": v.get("permalink"),
    })
    P.scrivi_stato(stato, f"stato: reel {slug}")
    return 0


def prossimo_reel(stato=None):
    """La scheda piu' vecchia gia' uscita nel feed che non ha ancora avuto
    nessun reel (di norma quella di ieri sera)."""
    stato = stato or P.leggi_stato()
    fatti = gia_pubblicati(stato)
    for p in stato["pubblicati"]:
        if p["slug"] not in fatti:
            return p["slug"]
    return None


def prossimo_rifacimento(stato=None):
    """La scheda piu' vecchia che ha solo il reel del formato 1."""
    stato = stato or P.leggi_stato()
    nuovi = gia_pubblicati(stato, FORMATO)
    for p in stato["pubblicati"]:
        if p["slug"] not in nuovi:
            return p["slug"]
    return None


if __name__ == "__main__":
    slug = sys.argv[1] if len(sys.argv) > 1 else "--prossimo"
    if slug == "--quale":
        # Per reel.yml: dice quale scheda toccherebbe, senza pubblicare.
        modo = sys.argv[2] if len(sys.argv) > 2 else "--prossimo"
        if modo == "--rifacimento":
            print(prossimo_rifacimento() or "")
        elif modo == "--prossimo":
            print(prossimo_reel() or "")
        else:
            print(modo)
        raise SystemExit(0)
    if slug == "--rifacimento":
        slug = prossimo_rifacimento()
        if slug is None:
            print("[stop] tutte le schede pubblicate hanno gia' il reel del formato 2.")
            raise SystemExit(0)
        print(f"[reel] rifacimento scelto in automatico: {slug}")
    if slug == "--prossimo":
        slug = prossimo_reel()
        if slug is None:
            print("[stop] tutte le schede pubblicate hanno gia' il loro reel.")
            raise SystemExit(0)
        print(f"[reel] scelto in automatico: {slug}")
    raise SystemExit(main(slug))
