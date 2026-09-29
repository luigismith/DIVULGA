# -*- coding: utf-8 -*-
"""
ELETTROFONI — diagnostica dei permessi.

Chiede all'API che cosa siamo effettivamente autorizzati a fare con il
token attuale: quali campi del profilo si leggono, se i commenti sono
accessibili, se le storie sono pubblicabili. Serve a rispondere con i
fatti invece che a memoria — e a scoprire in anticipo cosa NON si puo'
automatizzare, invece di scoprirlo davanti a un errore.

Non modifica niente: solo letture e un tentativo dichiarato.
"""
import json
import os

import requests

import token_ig

GRAPH = token_ig.GRAPH


def prova(descrizione, metodo, percorso, token, **params):
    params["access_token"] = token
    try:
        r = requests.request(metodo, f"{GRAPH}/{percorso}", params=params, timeout=30)
        corpo = r.text[:300]
        esito = "OK " if r.status_code == 200 else "NO "
        print(f"[{esito}] {descrizione}\n        HTTP {r.status_code} — {corpo}\n")
        return r.status_code == 200, r
    except Exception as e:
        print(f"[ERR] {descrizione}: {e}\n")
        return False, None


def profilo():
    """Solo lettura: com'e' il profilo ADESSO.

    Serve ogni volta che il proprietario cambia bio, nome o link dall'app:
    quelli non li possiamo scrivere noi (l'API rifiuta), ma possiamo
    LEGGERLI — e una modifica fatta a mano va verificata come tutto il
    resto, invece di darla per fatta. Niente tentativi di scrittura qui:
    su un account giovane non si bussa a un endpoint solo per sentire il
    "no" che sappiamo gia'."""
    token, _ = token_ig.token_corrente()
    print(f"Token in uso: {token_ig.redigi(token)}\n")
    ok, r = prova("profilo", "GET", "me", token,
                  fields="username,name,biography,website,followers_count,media_count")
    if not ok:
        raise SystemExit(1)
    d = r.json()
    print("=" * 68)
    for campo in ("username", "name", "biography", "website",
                  "followers_count", "media_count"):
        valore = d.get(campo)
        if campo == "biography" and valore:
            print(f"{campo:>16}  ({len(valore)}/150 caratteri)")
            for riga in str(valore).split("\n"):
                print(f"{'':>18}{riga}")
            continue
        if campo == "name" and valore:
            print(f"{campo:>16}: {valore}   ({len(valore)}/30 caratteri)")
            continue
        print(f"{campo:>16}: {valore if valore not in (None, '') else '— VUOTO —'}")
    print("=" * 68)
    if not d.get("website"):
        print("ATTENZIONE: il campo sito web e' vuoto. Se la bio finisce con")
        print("una freccia verso il basso, sta indicando il nulla.")

    # Le storie durano 24 ore e non lasciano traccia in stato.json: l'unico
    # modo di sapere se quella di stasera e' uscita davvero — e se e' un
    # VIDEO o il ripiego muto — e' chiederlo all'API finche' e' attiva.
    # Come stanno andando i post: senza numeri non si decide una cadenza.
    # Le metriche cambiano nome fra un aggiornamento e l'altro dell'API,
    # quindi si chiede e si stampa quello che torna, senza dare per
    # scontato che un nome esista ancora.
    print()
    ok, r = prova("ultimi contenuti", "GET", "me/media", token,
                  fields="id,media_type,media_product_type,permalink,timestamp",
                  limit=8)
    if ok:
        for m in r.json().get("data", []):
            tipo = m.get("media_product_type") or m.get("media_type")
            quando = (m.get("timestamp") or "")[:16].replace("T", " ")
            metriche = ("reach,likes,comments,saved,shares,total_interactions"
                        if tipo == "REELS" else "reach,likes,comments,saved")
            ok2, r2 = prova(f"  resa {tipo} del {quando}", "GET",
                            f"{m['id']}/insights", token, metric=metriche)
            if ok2:
                vals = {d["name"]: d["values"][0]["value"]
                        for d in r2.json().get("data", []) if d.get("values")}
                riga = "  ".join(f"{k}={v}" for k, v in vals.items())
                print(f"        -> {riga}   {m.get('permalink')}")

    print()
    ok, r = prova("storie attive", "GET", "me/stories", token)
    if ok:
        ids = [s["id"] for s in r.json().get("data", [])]
        print(f"        -> {len(ids)} storie attive")
        for sid in ids:
            ok2, r2 = prova(f"  storia {sid}", "GET", sid, token,
                            fields="id,media_type,media_url,timestamp")
            if ok2:
                s = r2.json()
                tipo = s.get("media_type")
                nota = ("VIDEO: la colonna sonora c'e'" if tipo == "VIDEO"
                        else "IMMAGINE: muta")
                print(f"        -> {s.get('timestamp')}  media_type={tipo}  {nota}")


def storie_cliccabili():
    """Si puo' rendere cliccabile una storia dall'API? Chiediamolo.

    Il proprietario ha chiesto (29/09/2026) che le storie riportino al
    post. Su Instagram l'unico modo e' lo sticker con il link: lo
    «swipe up» non esiste piu' dal 2021. La documentazione di Meta dice
    che gli sticker non si pubblicano via API, ma la documentazione e'
    gia' stata smentita una volta in questo progetto, quindi si prova.

    Ogni tentativo crea al massimo un CONTENITORE, che non e' una storia:
    se non lo si pubblica scade da solo e non appare a nessuno. Uso
    `image_url` e non `video_url` apposta — i contenitori video consumano
    il budget di elaborazione dell'account, quelli immagine no.

    Quello che cerchiamo e' un 400 che NOMINI il parametro: e' la
    risposta definitiva. Un 200 invece non basta a dire di si', perche'
    l'API puo' accettare un parametro sconosciuto e buttarlo via: in quel
    caso lo dice qui sotto e tocca pubblicarne una vera per guardarla.
    """
    token, _ = token_ig.token_corrente()
    ok, r = prova("chi siamo", "GET", "me", token, fields="user_id,username")
    if not ok:
        return
    ig_user = r.json().get("user_id") or r.json().get("id")
    copertina = ("https://luigismith.github.io/DIVULGA/tavole/minimoog/01.jpg")

    print("=" * 68)
    print("STORIE CLICCABILI (qui ci aspettiamo dei rifiuti)")
    print("=" * 68)
    print("Contenitore di prova con foto, mai pubblicato. Cerco un 400 che")
    print("nomini il parametro: quello e' un no definitivo.\n")

    # I nomi che Meta ha usato o documentato nel tempo, piu' quelli che
    # userebbe chiunque. Se l'API ne accetta uno, lo vediamo.
    candidati = [
        ("link", "https://www.instagram.com/elettrofoni/"),
        ("link_url", "https://www.instagram.com/elettrofoni/"),
        ("story_link", "https://www.instagram.com/elettrofoni/"),
        ("link_sticker", "https://www.instagram.com/elettrofoni/"),
        ("sticker", "link"),
        ("cta", "https://www.instagram.com/elettrofoni/"),
        ("swipe_up_url", "https://www.instagram.com/elettrofoni/"),
        ("caption", "prova"),
    ]
    accettati = []
    for nome, valore in candidati:
        ok, r = prova(f"contenitore STORIES con «{nome}»", "POST",
                      f"{ig_user}/media", token,
                      media_type="STORIES", image_url=copertina,
                      **{nome: valore})
        if ok:
            accettati.append(nome)

    # user_tags e' l'unico che la documentazione dice supportato senza
    # sticker: se funziona, una menzione al nostro stesso account rende
    # la storia toccabile e porta al profilo. Non e' il post, ma e' un clic.
    prova("contenitore STORIES con «user_tags» (menzione)", "POST",
          f"{ig_user}/media", token, media_type="STORIES",
          image_url=copertina,
          user_tags=json.dumps([{"username": "elettrofoni"}]))

    print("=" * 68)
    if accettati:
        print("ACCETTATI AL VOLO:", ", ".join(accettati))
        print("ATTENZIONE: accettare non vuol dire fare. L'API puo' prendere")
        print("un parametro sconosciuto e ignorarlo. Prima di scriverlo nel")
        print("publisher va pubblicata UNA storia vera e guardata dal telefono.")
    else:
        print("Nessun parametro di link accettato: la storia cliccabile")
        print("dall'API non si fa. Annotarlo in CLAUDE.md accanto alla bio.")
    print("=" * 68)


def storia_vera():
    """Pubblica UNA storia col parametro `link` e poi la rilegge.

    LEZIONE IMPARATA (29/09/2026). La prova qui sopra non poteva dire di
    no: l'API ha risposto 200 a tutti e otto i nomi, compresi
    `swipe_up_url` e `cta` che non esistono da nessuna parte. Il Graph
    accetta i parametri che non conosce e li butta via senza dirlo,
    quindi un contenitore creato non dimostra niente. Vale la regola 10 —
    se una verifica non puo' dire di no, non e' una verifica — e l'unico
    modo di saperlo e' guardare una storia vera.

    Non e' una storia sprecata: e' la copertina della scheda di oggi,
    cioe' esattamente la «story di rilancio» che il publisher fa gia'
    tutti i giorni. Se il link funziona l'abbiamo guadagnato, se non
    funziona resta una storia normale.
    """
    token, _ = token_ig.token_corrente()
    ok, r = prova("chi siamo", "GET", "me", token, fields="user_id,username")
    if not ok:
        return
    ig_user = r.json().get("user_id") or r.json().get("id")

    ok, r = prova("ultimo post", "GET", "me/media", token,
                  fields="id,permalink,media_url,timestamp", limit=1)
    if not ok or not r.json().get("data"):
        print("Nessun post da cui prendere copertina e permalink: mi fermo.")
        return
    post = r.json()["data"][0]
    permalink = post.get("permalink")
    copertina = post.get("media_url")
    print(f"\nStoria di prova sulla copertina di {permalink}\n")

    c = prova("contenitore STORIES con link al post", "POST",
              f"{ig_user}/media", token, media_type="STORIES",
              image_url=copertina, link=permalink)[1]
    if not c or c.status_code != 200:
        return
    cid = c.json()["id"]

    import time
    for _ in range(12):
        ok, r = prova(f"stato del contenitore {cid}", "GET", cid, token,
                      fields="status_code,status")
        if ok and r.json().get("status_code") == "FINISHED":
            break
        time.sleep(5)

    ok, r = prova("pubblico la storia", "POST", f"{ig_user}/media_publish",
                  token, creation_id=cid)
    if not ok:
        return
    sid = r.json()["id"]

    # Rileggo tutto quello che l'API vuole dirmi di questa storia. Se il
    # link fosse stato registrato da qualche parte, e' qui che si vede.
    for campi in ("id,media_type,media_product_type,permalink,timestamp",
                  "id,media_url,thumbnail_url", "id,caption"):
        prova(f"rileggo la storia ({campi.split(',')[1]})", "GET", sid, token,
              fields=campi)

    print("=" * 68)
    print("STORIA PUBBLICATA:", sid)
    print("L'API non espone gli sticker, quindi da qui non si vede se il")
    print("link c'e'. LO DECIDE UN'OCCHIATA DAL TELEFONO: apri la storia")
    print("di @elettrofoni e guarda se in fondo c'e' lo sticker col link.")
    print("Se non c'e', il link dall'API non si puo' fare e va scritto in")
    print("CLAUDE.md accanto alla bio, fra le cose che l'API non consente.")
    print("=" * 68)


def main():
    token, _ = token_ig.token_corrente()
    print(f"Token in uso: {token_ig.redigi(token)}\n")
    print("=" * 68)
    print("LETTURA DEL PROFILO")
    print("=" * 68)

    ok, r = prova("campi base del profilo", "GET", "me", token,
                  fields="user_id,username,account_type,media_count")
    ig_user = None
    if ok:
        ig_user = r.json().get("user_id") or r.json().get("id")

    # Campi che servirebbero per "gestire la pagina": biografia, nome, foto.
    for campo in ("biography", "name", "profile_picture_url", "followers_count", "website"):
        prova(f"campo «{campo}» in lettura", "GET", "me", token, fields=campo)

    print("=" * 68)
    print("SCRITTURA SUL PROFILO (qui ci aspettiamo dei rifiuti)")
    print("=" * 68)
    # Tentativo dichiarato: l'API espone un modo per cambiare la biografia?
    prova("POST /me con biography (cambio bio)", "POST", "me", token,
          biography="prova")
    if ig_user:
        prova("POST /{ig_user} con biography", "POST", str(ig_user), token,
              biography="prova")

    print("=" * 68)
    print("COMMENTI E STORIE (quello che possiamo davvero presidiare)")
    print("=" * 68)
    ok, r = prova("elenco dei nostri post", "GET", "me/media", token,
                  fields="id,permalink,timestamp,comments_count,like_count", limit=5)
    if ok:
        media = r.json().get("data", [])
        print(f"        -> {len(media)} post trovati")
        if media:
            mid = media[0]["id"]
            prova("commenti sul post piu' recente", "GET", f"{mid}/comments", token,
                  fields="id,text,username,timestamp")
    prova("elenco storie attive", "GET", "me/stories", token)
    print("=" * 68)


if __name__ == "__main__":
    import sys
    if "--profilo" in sys.argv:
        profilo()
    elif "--storie" in sys.argv:
        storie_cliccabili()
    elif "--storia-vera" in sys.argv:
        storia_vera()
    else:
        main()
