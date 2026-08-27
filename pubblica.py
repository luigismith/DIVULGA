# -*- coding: utf-8 -*-
"""
ELETTROFONI — publisher.

Pubblica su Instagram la prossima scheda in coda (carosello di 6 immagini
servite da GitHub Pages), poi salva lo stato, mette il primo commento con
le menzioni e verifica che il post esista davvero.

Principi (tutti imparati sbagliando, sul progetto precedente):
- l'idempotenza vive in stato.json, NON nell'API: è già successo che
  l'API non restituisse un contenuto pubblicato trenta secondi prima e
  che il post si prendesse un doppione;
- lo stato si salva (commit+push) SUBITO dopo la pubblicazione, prima di
  qualunque altro passaggio: se la run muore sul commento successivo, la
  corsa dopo NON deve ripubblicare lo stesso post;
- massimo 2 post al giorno, mai due a distanza di pochi minuti (4
  pubblicazioni ravvicinate = soft-block già preso);
- se una chiamata fallisce o l'account si comporta in modo strano ci si
  ferma e si apre una segnalazione: NIENTE retry in loop;
- dopo ogni pubblicazione si confronta ciò che l'API dice di avere con
  stato.json: un post è già stato dato per pubblicato — con tanto di id —
  senza esistere davvero.
"""
import datetime as dt
import json
import os
import pathlib
import subprocess
import sys
import time

import requests

import contenuti
import token_ig

RADICE = pathlib.Path(__file__).parent
FILE_STATO = RADICE / "stato.json"
GRAPH = token_ig.GRAPH

MAX_POST_AL_GIORNO = 2
DISTANZA_MINIMA_ORE = 6

# Le immagini vengono servite da GitHub Pages (l'API di Instagram non
# accetta upload di file: scarica da un URL pubblico).
BASE_PAGES = os.environ.get("BASE_PAGES", "https://luigismith.github.io/DIVULGA")


# -------------------------------------------------------------- stato ---

def leggi_stato():
    if FILE_STATO.exists():
        return json.loads(FILE_STATO.read_text())
    return {"pubblicati": [], "ultimo_errore": None}


def scrivi_stato(stato, messaggio_commit):
    FILE_STATO.write_text(json.dumps(stato, indent=1, ensure_ascii=False) + "\n")
    # Il salvataggio dello stato è un commit: sopravvive alla morte della run.
    subprocess.run(["git", "add", str(FILE_STATO)], check=True, cwd=RADICE)
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=RADICE)
    if diff.returncode != 0:
        subprocess.run(["git", "commit", "-m", messaggio_commit], check=True, cwd=RADICE)
        subprocess.run(["git", "push"], check=True, cwd=RADICE)


def segnala_errore(titolo, corpo):
    """Apre una issue sul repo (il proprietario riceve la notifica) e
    lascia traccia in stato.json. Poi la run fallisce: nessun retry."""
    stato = leggi_stato()
    stato["ultimo_errore"] = {
        "quando": dt.datetime.now(dt.timezone.utc).isoformat(),
        "titolo": titolo,
    }
    try:
        scrivi_stato(stato, f"stato: errore — {titolo}")
    except Exception as e:  # anche se il push fallisce, la issue parte
        print(f"[warn] salvataggio stato errore fallito: {e}")
    tok = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if tok and repo:
        requests.post(
            f"https://api.github.com/repos/{repo}/issues",
            headers={"Authorization": f"Bearer {tok}"},
            json={"title": f"🔴 ELETTROFONI: {titolo}", "body": corpo, "labels": ["pubblicazione"]},
            timeout=30,
        )
    print(f"[ERRORE] {titolo}\n{corpo}")


# ---------------------------------------------------------------- API ---

def api(metodo, percorso, token, **params):
    params["access_token"] = token
    r = requests.request(metodo, f"{GRAPH}/{percorso}", params=params, timeout=60)
    if r.status_code != 200:
        # Il token non compare mai nei log: qui si stampa solo il corpo
        # della risposta dell'API, che non lo contiene.
        raise RuntimeError(f"{metodo} /{percorso} → HTTP {r.status_code}: {r.text[:400]}")
    return r.json()


def verifica_immagini_online(urls):
    """HEAD su ogni immagine prima di chiamare l'API: Pages impiega un
    minuto a distribuire. Attesa di cortesia, non retry su errore."""
    for url in urls:
        for tentativo in range(24):           # max ~4 minuti
            r = requests.head(url, timeout=20)
            if r.status_code == 200 and r.headers.get("content-type", "").startswith("image/"):
                break
            time.sleep(10)
        else:
            raise RuntimeError(f"immagine mai apparsa online: {url}")
        print(f"[pages] online: {url}")


def attendi_container(cid, token):
    """Attesa del processing del container (non è un retry su errore:
    è il normale ciclo di vita del media)."""
    for _ in range(10):
        st = api("GET", cid, token, fields="status_code")
        if st.get("status_code") == "FINISHED":
            return
        if st.get("status_code") == "ERROR":
            raise RuntimeError(f"container {cid} in ERROR")
        time.sleep(6)
    raise RuntimeError(f"container {cid} mai FINISHED")


# --------------------------------------------------------------- main ---

def main():
    stato = leggi_stato()
    ora = dt.datetime.now(dt.timezone.utc)

    # Guardie anti-soft-block: mai più di 2 post al giorno, mai ravvicinati.
    recenti = [p for p in stato["pubblicati"]
               if dt.datetime.fromisoformat(p["quando"]).date() == ora.date()]
    if len(recenti) >= MAX_POST_AL_GIORNO:
        print("[stop] già pubblicati 2 post oggi: niente da fare."); return
    if stato["pubblicati"]:
        ultimo = dt.datetime.fromisoformat(stato["pubblicati"][-1]["quando"])
        if ora - ultimo < dt.timedelta(hours=DISTANZA_MINIMA_ORE):
            print("[stop] ultimo post troppo recente: niente da fare."); return

    gia = {p["slug"] for p in stato["pubblicati"]}

    # ALLARME PREVENTIVO (aggiunto il 27/08/2026). Prima qui si segnalava
    # solo la coda VUOTA: cioè quando il danno era già fatto e la pagina
    # taceva. È così che è morta la pagina precedente — nove giorni di
    # silenzio. A un post al giorno servono sette schede a settimana:
    # sotto le SETTE rimaste restano meno di sette giorni di margine, il
    # tempo esatto perché la Routine di rifornimento (mar+ven) rimedi.
    rimaste = sum(1 for s in contenuti.SCHEDE
                  if s["verificata"] and s["slug"] not in gia)
    if 0 < rimaste < 7:
        segnala_errore(
            f"coda bassa: restano {rimaste} schede ({rimaste} giorni)",
            f"A un post al giorno la coda si esaurisce tra {rimaste} giorni.\n"
            "La sessione di rifornimento (martedì e venerdì) deve riportarla "
            "ad almeno 14 schede verificate.\n\n"
            "Questa non è un'emergenza: è il preavviso perché non diventi tale.")

    scheda = contenuti.scheda_da_pubblicare(gia)
    if scheda is None:
        # La coda vuota è un'emergenza editoriale (9 giorni di silenzio sul
        # progetto precedente): si segnala forte.
        segnala_errore("coda vuota: nessuna scheda verificata da pubblicare",
                       "Aggiungere e verificare nuove schede in contenuti.py.")
        sys.exit(1)

    errs = contenuti.valida_scheda(scheda)
    if errs:
        segnala_errore(f"scheda '{scheda['slug']}' non valida", "\n".join(errs))
        sys.exit(1)

    slide_dir = RADICE / "docs" / "tavole" / scheda["slug"]
    files = sorted(slide_dir.glob("[0-9][0-9].jpg"))
    if len(files) != 6:
        segnala_errore(f"tavole mancanti per '{scheda['slug']}'",
                       f"attese 6 slide in {slide_dir}, trovate {len(files)}. "
                       "Eseguire genera_tavole.py prima del publish.")
        sys.exit(1)

    token, _ = token_ig.token_corrente()
    me = api("GET", "me", token, fields="user_id,username")
    ig_user = me.get("user_id") or me.get("id")
    print(f"[api] account: @{me.get('username')} — token {token_ig.redigi(token)}")

    urls = [f"{BASE_PAGES}/tavole/{scheda['slug']}/{f.name}" for f in files]
    try:
        verifica_immagini_online(urls)

        figli = []
        for n, url in enumerate(urls, start=1):
            # alt_text: accessibilità E indicizzazione. Google legge l'alt
            # dei post pubblici degli account professionali (dal 2025), quindi
            # qui passa il contenuto vero della slide, non un'etichetta.
            c = api("POST", f"{ig_user}/media", token, image_url=url,
                    is_carousel_item="true",
                    alt_text=contenuti.alt_slide(scheda, n)[:1000])
            attendi_container(c["id"], token)
            figli.append(c["id"])
        carosello = api("POST", f"{ig_user}/media", token,
                        media_type="CAROUSEL", children=",".join(figli),
                        caption=contenuti.componi_didascalia(scheda))
        attendi_container(carosello["id"], token)
        pubblicato = api("POST", f"{ig_user}/media_publish", token, creation_id=carosello["id"])
        media_id = pubblicato["id"]
    except Exception as e:
        segnala_errore(f"pubblicazione fallita per '{scheda['slug']}'", str(e))
        sys.exit(1)

    # >>> PRIMA DI QUALUNQUE ALTRA COSA: stato salvato e pushato. <<<
    stato["pubblicati"].append({
        "slug": scheda["slug"],
        "quando": ora.isoformat(),
        "media_id": media_id,
    })
    stato["ultimo_errore"] = None
    scrivi_stato(stato, f"stato: pubblicata scheda {scheda['slug']} ({media_id})")
    print(f"[ok] pubblicato {scheda['slug']} → media {media_id}")

    # Primo commento con le menzioni (il tag in didascalia lunga resta
    # nascosto dietro «… altro»: la notifica parte dal commento).
    try:
        commento = contenuti.primo_commento(scheda)
        if commento:
            api("POST", f"{media_id}/comments", token, message=commento)
            print("[ok] primo commento con menzioni")
    except Exception as e:
        segnala_errore(f"primo commento fallito per '{scheda['slug']}'",
                       f"Il post è pubblicato ({media_id}); solo il commento è fallito: {e}")
        sys.exit(1)

    # Verifica finale: l'API deve confermare che il post ESISTE.
    try:
        ultimi = api("GET", "me/media", token, fields="id,permalink,timestamp", limit=5)
        ids = [m["id"] for m in ultimi.get("data", [])]
        if media_id not in ids:
            raise RuntimeError(f"media {media_id} assente dagli ultimi post dell'account: {ids}")
        permalink = next(m.get("permalink") for m in ultimi["data"] if m["id"] == media_id)
        stato = leggi_stato()
        stato["pubblicati"][-1]["permalink"] = permalink
        scrivi_stato(stato, f"stato: permalink {scheda['slug']}")
        print(f"[ok] verificato: {permalink}")
    except Exception as e:
        segnala_errore(f"verifica post-pubblicazione fallita per '{scheda['slug']}'", str(e))
        sys.exit(1)

    # Rilancio come STORIA. È facoltativa PER SCELTA: il post è la missione,
    # la storia il megafono. Se fallisce si annota e si tira dritto — non
    # vale la pena far fallire una run (e allarmare il proprietario) per un
    # megafono. Formato dedicato 1080x1920: story.jpg.
    try:
        story_url = f"{BASE_PAGES}/tavole/{scheda['slug']}/story.jpg"
        verifica_immagini_online([story_url])
        c = api("POST", f"{ig_user}/media", token,
                image_url=story_url, media_type="STORIES")
        attendi_container(c["id"], token)
        s = api("POST", f"{ig_user}/media_publish", token, creation_id=c["id"])
        print(f"[ok] storia pubblicata: {s['id']}")
    except Exception as e:
        print(f"[warn] storia non pubblicata (non blocca il post): {e}")

    # Story di rilancio: la copertina ripubblicata come storia, per dare al
    # post il doppio di occasioni di essere visto. È facoltativa PER SCELTA:
    # se fallisce si annota nel log e basta — niente issue, niente retry —
    # perché il post è la missione, la story solo il megafono.
    try:
        st = api("POST", f"{ig_user}/media", token,
                 media_type="STORIES", image_url=urls[0])
        attendi_container(st["id"], token)
        api("POST", f"{ig_user}/media_publish", token, creation_id=st["id"])
        print("[ok] story di rilancio pubblicata")
    except Exception as e:
        print(f"[warn] story di rilancio non pubblicata (non blocca): {e}")


if __name__ == "__main__":
    main()
