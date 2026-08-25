# -*- coding: utf-8 -*-
"""
ELETTROFONI — gestione del token Instagram.

REGOLE DI SICUREZZA (non negoziabili):
- il token lo incolla l'utente nei GitHub secrets, una volta sola;
- da quel momento NON si stampa più in nessun log: se uno script deve
  nominarlo, lo redige (vedi redigi());
- il rinnovo è automatico: il token corrente vive CIFRATO nel repo
  (token.enc, AES-256-GCM con chiave derivata dal secret STATE_KEY),
  così nessun umano deve mai rigenerarlo a mano.

Ciclo di vita:
- bootstrap: se token.enc non esiste, si parte dal secret IG_ACCESS_TOKEN;
- rinnovo: dopo 25 giorni si chiama /refresh_access_token (il token
  di lunga durata vale 60 giorni ed è rinnovabile da quando ha 24 ore).
"""
import base64
import datetime as dt
import json
import os
import pathlib

import requests
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

RADICE = pathlib.Path(__file__).parent
FILE_TOKEN = RADICE / "token.enc"

# graph.instagram.com: percorso "Instagram API with Instagram Login",
# NON il percorso che passa dalla Pagina Facebook.
GRAPH = "https://graph.instagram.com"
GIORNI_PRIMA_DEL_RINNOVO = 25


def redigi(token):
    """Rappresentazione sicura del token nei log: mai il valore."""
    return f"<token redatto, {len(token)} caratteri>"


def _chiave(passphrase, salt):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=600_000)
    return kdf.derive(passphrase.encode("utf-8"))


def _salva(token, passphrase, emesso_il=None):
    salt = os.urandom(16)
    nonce = os.urandom(12)
    payload = json.dumps({
        "token": token,
        "salvato_il": dt.datetime.now(dt.timezone.utc).isoformat(),
        "emesso_il": emesso_il or dt.datetime.now(dt.timezone.utc).isoformat(),
    }).encode("utf-8")
    ct = AESGCM(_chiave(passphrase, salt)).encrypt(nonce, payload, None)
    FILE_TOKEN.write_text(json.dumps({
        "v": 1,
        "salt": base64.b64encode(salt).decode(),
        "nonce": base64.b64encode(nonce).decode(),
        "ct": base64.b64encode(ct).decode(),
    }, indent=1))


def _leggi(passphrase):
    blob = json.loads(FILE_TOKEN.read_text())
    salt = base64.b64decode(blob["salt"])
    nonce = base64.b64decode(blob["nonce"])
    ct = base64.b64decode(blob["ct"])
    return json.loads(AESGCM(_chiave(passphrase, salt)).decrypt(nonce, ct, None))


def token_corrente():
    """Restituisce (token, rinnovato: bool). Bootstrap dal secret se serve,
    rinnovo automatico se il token ha più di GIORNI_PRIMA_DEL_RINNOVO."""
    passphrase = os.environ.get("STATE_KEY")
    if not passphrase:
        raise SystemExit("STATE_KEY mancante nell'ambiente (GitHub secret).")

    if not FILE_TOKEN.exists():
        seme = os.environ.get("IG_ACCESS_TOKEN")
        if not seme:
            raise SystemExit("token.enc assente e IG_ACCESS_TOKEN mancante: serve il bootstrap (fase 1).")
        _salva(seme.strip(), passphrase)
        print(f"[token] bootstrap da IG_ACCESS_TOKEN: {redigi(seme)} cifrato in token.enc")

    dati = _leggi(passphrase)
    emesso = dt.datetime.fromisoformat(dati["emesso_il"])
    eta = dt.datetime.now(dt.timezone.utc) - emesso
    if eta < dt.timedelta(days=GIORNI_PRIMA_DEL_RINNOVO):
        return dati["token"], False

    print(f"[token] età {eta.days} giorni: rinnovo…")
    r = requests.get(f"{GRAPH}/refresh_access_token", params={
        "grant_type": "ig_refresh_token",
        "access_token": dati["token"],
    }, timeout=30)
    if r.status_code != 200:
        # Ci si ferma e si segnala: NIENTE retry in loop (è così che si
        # finisce bloccati). Il corpo della risposta non contiene il token.
        raise RuntimeError(f"rinnovo token fallito: HTTP {r.status_code} — {r.text[:300]}")
    nuovo = r.json()["access_token"]
    _salva(nuovo, passphrase)
    print(f"[token] rinnovato: {redigi(nuovo)}")
    return nuovo, True
