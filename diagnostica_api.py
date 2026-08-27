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
    main()
