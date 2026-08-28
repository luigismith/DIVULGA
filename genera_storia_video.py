# -*- coding: utf-8 -*-
"""ELETTROFONI — la storia come video, con l'audio dentro.

PERCHÉ. Le storie erano `story.jpg`, un'immagine ferma: su Instagram una
foto non ha audio, e non è un difetto da riparare ma il formato. L'unico
modo per avere il suono è pubblicare un video — e il suono dev'essere
DENTRO il file, perché l'API non consente di agganciare la musica del
catalogo di Instagram (quella la si sceglie solo dall'app, a mano).

Da qui: stessa tavola 1080x1920 di prima, otto secondi, colonna sonora
sintetizzata da `suoni.py` nel timbro della macchina di cui parla la
scheda. Nessun campione, nessun diritto, nessun file da scaricare.

SPECIFICHE VIDEO (le stesse imparate a fatica per i reel): H.264 profilo
main, yuv420p, GOP chiuso, niente B-frame, AAC 44.1 kHz stereo, e una
seconda passata di remux con `-use_editlist 0` — senza quella alcuni
lettori partono con un fotogramma nero.

Sulla risoluzione: la regola scritta per i reel dice 720x1280, perché a
1080x1920 i video LUNGHI venivano rifiutati. Qui restiamo a 1080x1920
apposta: otto secondi non sono un video lungo, e la storia ha in basso
il credito della foto in corpo piccolo, che a 720 diventa illeggibile.
Se un giorno una storia venisse rifiutata, questa è la prima cosa da
provare a cambiare.
"""
import pathlib
import shutil
import subprocess
import sys

import contenuti
import suoni

RADICE = pathlib.Path(__file__).resolve().parent
FPS = 30


def _ffmpeg():
    for c in ("ffmpeg", "/usr/bin/ffmpeg"):
        if shutil.which(c) or pathlib.Path(c).exists():
            return c
    raise RuntimeError("ffmpeg non trovato: il video della storia non si può fare")


def _esegui(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"ffmpeg fallito:\n{r.stderr[-1500:]}")


def costruisci(scheda):
    cartella = RADICE / "docs" / "tavole" / scheda["slug"]
    foto = cartella / "story.jpg"
    if not foto.exists():
        raise RuntimeError(f"manca {foto}: genera prima le tavole")

    wav = cartella / "story.wav"
    suoni.genera(scheda, wav)

    ff = _ffmpeg()
    grezzo = cartella / "_story_grezzo.mp4"
    finale = cartella / "story.mp4"

    _esegui([
        ff, "-y", "-loglevel", "error",
        "-loop", "1", "-framerate", str(FPS), "-i", str(foto),
        "-i", str(wav),
        "-c:v", "libx264", "-profile:v", "main", "-pix_fmt", "yuv420p",
        "-r", str(FPS), "-g", str(FPS * 2), "-sc_threshold", "0", "-bf", "0",
        "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2",
        "-t", str(suoni.DURATA), "-shortest",
        str(grezzo),
    ])
    # Seconda passata: senza -use_editlist 0 alcuni lettori mostrano un
    # fotogramma nero all'avvio. +faststart mette l'indice in testa, così
    # Instagram non deve scaricare tutto il file prima di iniziare.
    _esegui([ff, "-y", "-loglevel", "error", "-i", str(grezzo),
             "-c", "copy", "-movflags", "+faststart", "-use_editlist", "0",
             str(finale)])
    grezzo.unlink(missing_ok=True)
    wav.unlink(missing_ok=True)   # il WAV non va su Pages: pesa e non serve
    return finale


def verifica(percorso):
    """Non ci si fida di ffmpeg che esce con zero: si guarda il file."""
    ff = _ffmpeg().replace("ffmpeg", "ffprobe")
    r = subprocess.run(
        [ff, "-v", "error", "-show_entries",
         "stream=codec_name,codec_type,width,height,channels,sample_rate,profile",
         "-show_entries", "format=duration,size", "-of", "default=nw=1", str(percorso)],
        capture_output=True, text=True)
    dati = r.stdout
    problemi = []
    if "codec_type=audio" not in dati:
        problemi.append("NESSUNA TRACCIA AUDIO")
    if "codec_name=h264" not in dati:
        problemi.append("video non H.264")
    if "codec_name=aac" not in dati:
        problemi.append("audio non AAC")
    return dati, problemi


if __name__ == "__main__":
    slug = sys.argv[1] if len(sys.argv) > 1 else None
    if slug == "--prossima":
        # stessa logica di genera_tavole.py: solo la scheda del giorno
        import json
        stato = RADICE / "stato.json"
        gia = set()
        if stato.exists():
            gia = {x["slug"] for x in json.loads(stato.read_text())["pubblicati"]}
        prossima = contenuti.scheda_da_pubblicare(gia)
        if prossima is None:
            print("[storia] nessuna scheda in coda: niente video"); raise SystemExit(0)
        slug = prossima["slug"]
    schede = [s for s in contenuti.SCHEDE if slug in (None, s["slug"])]
    if not schede:
        print(f"nessuna scheda '{slug}'"); raise SystemExit(1)
    for s in schede:
        out = costruisci(s)
        dati, problemi = verifica(out)
        mb = out.stat().st_size / 1e6
        voce = suoni.VOCE_SCHEDA.get(s["slug"], "sega")
        stato = "OK" if not problemi else "PROBLEMI: " + ", ".join(problemi)
        print(f"[storia] {s['slug']}: {mb:.1f} MB, voce «{voce}» — {stato}")
        if problemi:
            print(dati); raise SystemExit(1)
