# -*- coding: utf-8 -*-
"""ELETTROFONI — la slide del suono: un video in fondo al carosello.

PERCHÉ (20/10/2026, decisione del proprietario). Il 17/10 aveva chiesto
il suono vero della macchina «in ogni prossimo post/storia/reel», e il
reel ce l'ha. Il carosello no: sei tavole mute. Proposto di aggiungere
una settima slide video con la registrazione, risposta: «Sicuramente
metterei il video». Chi sfoglia il post sente la macchina di cui ha
appena letto, senza dover cercare il reel.

COS'È. Una tavola come le altre (testata, numerone 07, la foto della
macchina) con in basso un oscilloscopio: dentro, la forma d'onda vera
della registrazione disegnata da ffmpeg (`showwaves`) mentre suona, e
una barra che avanza. Sotto, cosa si sente e il credito della
registrazione, che è un obbligo di licenza come quello delle foto. Il
fondo è un'immagine ferma resa da Chromium come le tavole; si muove solo
l'oscilloscopio, che è la cosa da guardare mentre si ascolta.

SPECIFICHE. 864x1080: è 4:5 come le tavole, perché Instagram ritaglia
ogni elemento del carosello sul formato del primo, e resta sotto i
1080x1920 che con i video lunghi davano rifiuti (vedi genera_reel.py).
Per il resto le stesse del reel, che passano: H.264 main, yuv420p, GOP
chiuso, niente B-frame, AAC 44.1 kHz stereo, remux con -use_editlist 0.
Audio a -16 LUFS come il reel e il sito. Durata: quanto è lunga
l'estratto, fra 15 e 30 secondi; sotto i 15 si ripete.

Il file è `suono.mp4` (e `suono.jpg`, il fotogramma fermo), accanto alle
tavole. NON si chiama 07.jpg/07.mp4 apposta: il publisher prende le
tavole con il glob NN.jpg, e la slide del suono deve restare facoltativa.
Se manca, il carosello esce con sei tavole come prima.

    python genera_suono.py cz101 [cartella]   # una scheda
    python genera_suono.py --prossima         # quella che esce oggi
"""
import json
import os
import pathlib
import re
import sys

import contenuti
import genera_reel as gr
import genera_tavole as gt

RADICE = pathlib.Path(__file__).resolve().parent
L, H = 1080, 1350          # come si disegna (la tavola)
LARG, ALT = 864, 1080      # come si esporta: 4:5
FPS = 30
DURATA_MIN, DURATA_MAX = 15.0, 30.0
OSC_H = 200                # altezza dell'oscilloscopio, in px della tavola
NOME_VIDEO, NOME_FERMO = "suono.mp4", "suono.jpg"


def _frase(testo):
    testo = testo.strip()
    return testo[:1].upper() + testo[1:] + ("" if testo.endswith(".") else ".")


def slide_suono(scheda):
    a = scheda["reel_audio"]
    # La foto alta quanto le serve per stare intera a tutta larghezza
    # (fra 360 e 560 px): con un riquadro elastico una tastiera larga
    # restava in mezzo a due fasce di crema vuote, col credito staccato
    # sotto. Lo spazio che avanza lo prende l'oscilloscopio.
    altezza_foto = max(360, min(560, round(L / gt._aspetto(scheda["foto"]))))
    css = f"""
.ascolta{{flex:none;margin:22px 52px 0;display:flex;align-items:center;justify-content:space-between;
  font-family:'PlexMono';font-weight:600;font-size:15px;letter-spacing:.22em;color:{gt.ARANCIO}}}
.osc{{flex:1 1 auto;min-height:{OSC_H}px;position:relative;margin:10px 52px 0;background:{gt.BRUNO};
  border-left:16px solid {gt.ARANCIO}}}
/* Linea dello zero: il primo fotogramma (quello che Instagram mostra
   prima del tocco) non è un rettangolo vuoto ma uno strumento acceso. */
.osc::after{{content:'';position:absolute;left:0;right:0;top:50%;height:2px;background:{gt.ARANCIO};opacity:.55}}
.cosa{{flex:none;font-family:'PlexSerif';font-size:28px;line-height:1.45;margin:18px 52px 0;
  max-height:125px;overflow:hidden}}
.reg{{flex:none;font-family:'PlexMono';font-size:13px;line-height:1.5;color:#6b5138;margin:10px 52px 0}}
"""
    corpo = f"""
{gt._testata(scheda)}
{gt._intesta(7, "DA SENTIRE", "Il suono vero")}
{gt._banda(scheda, 0, altezza_foto, stile="margin-top:22px")}
<div class="ascolta"><span>▶ ALZATE IL VOLUME</span><span>{scheda['strumento'].upper()} · REGISTRAZIONE VERA</span></div>
<div class="osc" id="osc"></div>
<div class="cosa autofit" data-min="20">{_frase(a['cosa'])}</div>
<div class="reg">Registrazione: {a['autore']} · {a['licenza']} · {a['fonte']}</div>
{gt._pager(scheda, 7)}
"""
    return gt._pagina(corpo, css)


def _durata_file(percorso):
    """Durata in secondi letta dall'intestazione (ffprobe nel container
    di sviluppo non c'è, ffmpeg -i sì)."""
    import subprocess
    r = subprocess.run([gr._ff(), "-hide_banner", "-i", str(percorso)], capture_output=True, text=True)
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr)
    if not m:
        raise RuntimeError(f"durata illeggibile: {percorso}")
    return int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3])


def costruisci(scheda, cartella=None):
    from playwright.sync_api import sync_playwright

    a = scheda.get("reel_audio")
    if not a:
        raise RuntimeError(f"{scheda['slug']} non ha reel_audio: niente slide del suono")
    cartella = pathlib.Path(cartella or (RADICE / "docs" / "tavole" / scheda["slug"]))
    cartella.mkdir(parents=True, exist_ok=True)
    lavoro = cartella / "_suono"
    lavoro.mkdir(exist_ok=True)

    # 1. Il fondo fermo, con le stesse regole delle tavole (file + goto,
    #    mai set_content: vedi genera_tavole).
    fermo_png = lavoro / "fondo.png"
    exe = os.environ.get("ELETTROFONI_CHROMIUM")
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe, args=["--no-sandbox", "--force-color-profile=srgb"])
        pg = b.new_page(viewport={"width": L, "height": H})
        tmp = lavoro / "suono.html"
        tmp.write_text(slide_suono(scheda), encoding="utf-8")
        pg.goto(tmp.as_uri())
        pg.wait_for_selector("body[data-pronto='1']", timeout=20000)
        box = pg.evaluate("(() => {const r = document.getElementById('osc').getBoundingClientRect();"
                          "return [r.left, r.top, r.width, r.height];})()")
        pg.screenshot(path=str(fermo_png), clip={"x": 0, "y": 0, "width": L, "height": H})
        pg.screenshot(path=str(cartella / NOME_FERMO), type="jpeg", quality=90,
                      clip={"x": 0, "y": 0, "width": L, "height": H})
        b.close()
    # L'onda si disegna dentro il riquadro, lasciando fuori la costa arancio.
    x, y, w, h = (int(round(v)) for v in box)
    x, w = x + 16, w - 16
    if w <= 0 or h <= 0 or y + h > H:
        raise RuntimeError(f"oscilloscopio fuori tavola: {box}")

    # 2. L'audio: l'estratto della registrazione, a -16 LUFS.
    src = RADICE / a["file"]
    resto = _durata_file(src) - float(a.get("inizio", 0))
    durata = max(DURATA_MIN, min(DURATA_MAX, resto))
    ff = gr._ff()
    wav = lavoro / "audio.wav"
    gr._esegui([ff, "-y", "-loglevel", "error", "-stream_loop", "-1",
                "-ss", str(a.get("inizio", 0)), "-i", str(src), "-t", f"{durata:.2f}",
                "-af", f"afade=t=in:d=0.01,afade=t=out:st={durata - 1.5:.2f}:d=1.5,"
                       "loudnorm=I=-16:TP=-1.5:LRA=11",
                "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le", str(wav)])

    # 3. Il video: fondo fermo + forma d'onda vera + barra che avanza.
    #    La barra sta dentro l'oscilloscopio (si compone lì e poi si
    #    incolla), così non sborda sul margine.
    arancio = gt.ARANCIO.lstrip("#")
    bruno = gt.BRUNO.lstrip("#")
    n = round(durata * FPS)
    filtro = (
        f"color=c=0x{bruno}:s={w}x{h}:r={FPS}:d={durata:.2f}[o0];"
        f"[1:a]aformat=channel_layouts=mono,"
        f"showwaves=s={w}x{h - 12}:mode=cline:rate={FPS}:colors=0x{arancio}:scale=sqrt:draw=full,"
        f"format=rgba[onda];"
        f"color=c=0x{arancio}:s={w}x6:r={FPS}:d={durata:.2f}[barra];"
        f"[o0][onda]overlay=0:0:shortest=1[o1];"
        f"[o1][barra]overlay=x='-{w}+{w}*t/{durata:.2f}':y={h - 6}:shortest=1[osc];"
        f"[0:v][osc]overlay={x}:{y}:shortest=1,"
        f"scale={LARG}:{ALT}:flags=lanczos,setsar=1,format=yuv420p[v]"
    )
    grezzo = lavoro / "grezzo.mp4"
    gr._esegui([ff, "-y", "-loglevel", "error",
                "-loop", "1", "-framerate", str(FPS), "-i", str(fermo_png),
                "-i", str(wav),
                "-filter_complex", filtro,
                "-map", "[v]", "-map", "1:a", "-frames:v", str(n), "-r", str(FPS),
                "-c:v", "libx264", "-profile:v", "main", "-pix_fmt", "yuv420p",
                "-g", str(FPS * 2), "-sc_threshold", "0", "-bf", "0",
                "-preset", "medium", "-crf", "20",
                "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2",
                "-shortest", str(grezzo)])
    finale = cartella / NOME_VIDEO
    gr._esegui([ff, "-y", "-loglevel", "error", "-i", str(grezzo), "-c", "copy",
                "-movflags", "+faststart", "-use_editlist", "0", str(finale)])

    for f in lavoro.iterdir():
        f.unlink()
    lavoro.rmdir()
    print(f"[suono] {scheda['slug']}: {durata:.1f} s di {a['file']} da {a.get('inizio', 0)} s")
    return finale


def verifica(percorso):
    import subprocess
    r = subprocess.run([gr._ff(), "-hide_banner", "-i", str(percorso)], capture_output=True, text=True)
    d = r.stderr
    problemi = []
    if "Audio: aac" not in d: problemi.append("NESSUN AUDIO AAC")
    if "44100 Hz" not in d: problemi.append("audio non a 44.1 kHz")
    if "Video: h264 (Main)" not in d: problemi.append("video non H.264 main")
    if f"{LARG}x{ALT}" not in d: problemi.append(f"non è {LARG}x{ALT}")
    return d, problemi


if __name__ == "__main__":
    slug = sys.argv[1] if len(sys.argv) > 1 else None
    cartella = sys.argv[2] if len(sys.argv) > 2 else None
    if slug in (None, "--prossima"):
        stato = RADICE / "stato.json"
        gia = {x["slug"] for x in json.loads(stato.read_text())["pubblicati"]} if stato.exists() else set()
        prossima = contenuti.scheda_da_pubblicare(gia)
        if prossima is None:
            print("[suono] nessuna scheda in coda: niente da costruire")
            raise SystemExit(0)
        slug = prossima["slug"]
    scheda = next((s for s in contenuti.SCHEDE if s["slug"] == slug), None)
    if scheda is None:
        print(f"nessuna scheda '{slug}'"); raise SystemExit(1)
    if not scheda.get("reel_audio"):
        # Non è un errore: la scheda esce con sei tavole. Lo si dice.
        print(f"[suono] {slug} non ha una registrazione vera: il carosello resta di 6 tavole")
        raise SystemExit(0)
    out = costruisci(scheda, cartella)
    d, problemi = verifica(out)
    print(f"[suono] {slug}: {out.stat().st_size / 1e6:.1f} MB — "
          + ("OK" if not problemi else "PROBLEMI: " + ", ".join(problemi)))
    if problemi:
        print(d)
        raise SystemExit(1)
