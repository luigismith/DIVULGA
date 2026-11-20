# -*- coding: utf-8 -*-
"""ELETTROFONI — a quale indirizzo sta il sito OGGI.

20/11/2026, il proprietario: «ho il mio dominio luigimassari.com.
trasferisci tutto lì». Il sito resta servito da GitHub Pages di questo repo
(870 MB, ridistribuito a ogni uscita: dentro il repo di luigimassari.com
gli riempirebbe Pages), ma col sottodominio elettrofoni.luigimassari.com.
Il DNS (OVH) e il dominio personalizzato del repo li imposta chi ha le
credenziali del proprietario, cioè la sessione del sito sul suo PC, quando
può. Da qui non si sa QUANDO.

Per questo l'indirizzo non si cambia a mano in un commit da sincronizzare:
lo si chiede ogni volta. Se il dominio nuovo serve davvero i NOSTRI file
(logo.png, 200, image/png) si usa quello; altrimenti quello vecchio. Conta
per Instagram, che scarica tavole e video dall'indirizzo che gli diamo:
dopo il cambio il vecchio risponde 301 e il controllo HEAD di pubblica.py,
che non segue i redirect, fallirebbe. E conta per canonical e sitemap.

    python indirizzo.py      # stampa l'indirizzo da usare, senza / finale

Niente import pesanti: gira prima delle dipendenze (solo libreria standard).
"""
import urllib.error
import urllib.request

NUOVO = "https://elettrofoni.luigimassari.com"
VECCHIO = "https://luigismith.github.io/DIVULGA"


def risponde(base, timeout=15):
    """Vero solo se `base` serve il nostro logo, senza redirect: un 404 di
    GitHub (record DNS c'è, dominio non ancora impostato) o un certificato
    non ancora emesso dicono di no."""
    class SenzaRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None
    apri = urllib.request.build_opener(SenzaRedirect).open
    req = urllib.request.Request(f"{base}/logo.png", method="HEAD",
                                 headers={"User-Agent": "elettrofoni-indirizzo"})
    try:
        with apri(req, timeout=timeout) as r:
            return r.status == 200 and r.headers.get("content-type", "").startswith("image/")
    except (urllib.error.URLError, OSError, ValueError):
        return False


def base_attuale():
    return NUOVO if risponde(NUOVO) else VECCHIO


if __name__ == "__main__":
    print(base_attuale())
