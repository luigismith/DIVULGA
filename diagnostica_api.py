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
    else:
        main()
