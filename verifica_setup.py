# -*- coding: utf-8 -*-
"""
ELETTROFONI — verifica del setup (workflow manuale, da lanciare dopo la
fase 1). Controlla i secrets, valida il token contro l'API (senza MAI
stamparlo), esegue il bootstrap di token.enc e valida tutte le schede.
"""
import subprocess
import sys
import pathlib

import requests

import contenuti
import token_ig

RADICE = pathlib.Path(__file__).parent


def main():
    ok = True

    # 1. token: bootstrap + validazione contro l'API
    try:
        token, _ = token_ig.token_corrente()
        r = requests.get(f"{token_ig.GRAPH}/me",
                         params={"fields": "user_id,username,account_type",
                                 "access_token": token}, timeout=30)
        if r.status_code == 200:
            dati = r.json()
            print(f"[ok] token valido — account @{dati.get('username')} "
                  f"(tipo: {dati.get('account_type')}) — {token_ig.redigi(token)}")
        else:
            print(f"[ERR] l'API rifiuta il token: HTTP {r.status_code} — {r.text[:300]}")
            ok = False
    except SystemExit as e:
        print(f"[ERR] {e}"); ok = False
    except Exception as e:
        print(f"[ERR] verifica token fallita: {e}"); ok = False

    # 2. token.enc appena creato dal bootstrap? va committato
    stato = subprocess.run(["git", "status", "--porcelain", "token.enc"],
                           capture_output=True, text=True, cwd=RADICE)
    if stato.stdout.strip():
        subprocess.run(["git", "add", "token.enc"], check=True, cwd=RADICE)
        subprocess.run(["git", "commit", "-m", "token: bootstrap cifrato"], check=True, cwd=RADICE)
        subprocess.run(["git", "push"], check=True, cwd=RADICE)
        print("[ok] token.enc cifrato e committato")

    # 3. validazione schede
    for s in contenuti.SCHEDE:
        errs = contenuti.valida_scheda(s)
        if errs:
            print(f"[ERR] scheda {s['slug']}: {errs}"); ok = False
    print(f"[ok] schede valide: {sum(1 for s in contenuti.SCHEDE if not contenuti.valida_scheda(s))}"
          f"/{len(contenuti.SCHEDE)} — verificate: {sum(1 for s in contenuti.SCHEDE if s['verificata'])}")

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
