# -*- coding: utf-8 -*-
"""ELETTROFONI — il reel della scheda («formato 2», dal 07/10/2026).

PERCHÉ ESISTE. Il carosello lo vedono i follower; il reel è l'unico
formato che Instagram mostra a chi non ci segue (copertura mediana 22
contro 11 dei caroselli, misurata il 07/10/2026 su 45 + 45 contenuti con
`metriche.py`).

PERCHÉ È CAMBIATO TUTTO (07/10/2026). I numeri di `metriche/` dicevano
una cosa sola: su 45 reel il tempo medio di visione era 4 secondi su 28.
La gente se ne andava alla prima dissolvenza in nero, cioè alla fine
della prima scena. Il vecchio reel aveva:
  · il primo fotogramma NERO (dissolvenza in entrata) — e Instagram stima
    proprio la probabilità che uno scorra via entro 3 secondi;
  · sei scene su sette fatte di solo testo su fondo crema — e Instagram
    scrive nero su bianco che i reel «majority text» li mostra meno
    (about.instagram.com, «Instagram Ranking Explained», 2023);
  · il gancio piccolo in basso, sotto la didascalia di Instagram;
  · un nero ogni 4 secondi, cioè sei occasioni per andarsene.
Il formato 2 è l'opposto, punto per punto:
  · dal fotogramma 0 c'è la macchina che si muove e la frase più
    sorprendente della scheda (`reel_battute[0]`), niente nero, mai;
  · la foto riempie lo schermo; il testo sta in un pannello bruno che ne
    copre meno di un terzo, nella zona che l'interfaccia di Instagram non
    copre (sopra i 420px in basso, lontano dalla colonna dei bottoni);
  · 5 battute da 2,6 secondi che raccontano UNA storia in ordine, poi la
    chiamata a MANDARLO a qualcuno (gli invii pesano più di tutto per chi
    non ci segue: Mosseri, 21/01/2025), 15,6 secondi in tutto;
  · stacchi netti fra le battute, e l'ultima torna sulla prima
    inquadratura, così il giro ricomincia senza un salto.

SPECIFICHE (imparate a fatica, NON toccarle senza rileggerle):
720x1280 — a 1080x1920 i video lunghi vengono rifiutati; H.264 profilo
main; yuv420p; GOP chiuso (-g 60 -sc_threshold 0); niente B-frame
(-bf 0); AAC 44.1 kHz stereo; seconda passata di remux con
`-use_editlist 0`. Il testo si disegna a 1080x1920 e si riduce in ffmpeg:
rimpicciolire un testo già renderizzato a 720 lo rende impastato.

IL BUDGET È IL VERO VINCOLO. L'elaborazione video dell'account si
esaurisce dopo una dozzina di container, e anche i tentativi falliti la
consumano. Quindi: si costruisce e si verifica QUI, in locale, quante
volte serve; si pubblica UNA volta sola. Questo file non pubblica niente.
"""
import os
import pathlib
import re
import shutil
import subprocess
import sys

import contenuti
import genera_tavole as gt
import suoni

RADICE = pathlib.Path(__file__).resolve().parent
L, H = 1080, 1920          # come si disegna
LARG, ALT = 720, 1280      # come si esporta
FPS = 30
SEC_BATTUTA = 2.6
# Le zone che l'interfaccia di Instagram copre su un reel: in alto
# l'intestazione «Reel» e la fotocamera, in basso nome, didascalia e
# audio, a destra la colonna dei bottoni. Il testo vive fra le due.
PANNELLO_Y = 200           # dove comincia il pannello del testo
PANNELLO_MAX = 760         # dove deve finire, al massimo (autofit)
FASCIA_Y = 780             # dove comincia la foto orizzontale
FASCIA_MAX = 700           # quanto può essere alta, al massimo
TAG_MAX_X = 900            # oltre comincia la colonna dei bottoni
NOME_FILE = "reel2.mp4"    # il file del formato 2, accanto alle tavole


def _ff(nome="ffmpeg"):
    if shutil.which(nome):
        return nome
    raise RuntimeError(f"{nome} non trovato: il reel non si può montare")


def _esegui(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{cmd[0]} fallito:\n{r.stderr[-1500:]}")


# ---------------------------------------------------------- inquadratura ---

_PAROLE = {"left": 0.0, "top": 0.0, "center": 0.5, "right": 1.0, "bottom": 1.0}


def fuoco(posizione):
    """Da `object-position` CSS («top», «center 58%», «85% 100%») al
    punto di fuoco (fx, fy) fra 0 e 1, con la stessa semantica del CSS:
    fx=0.3 vuol dire che il ritaglio lascia fuori il 30% dell'eccedenza a
    sinistra e il 70% a destra.

    LEZIONE IMPARATA (07/10/2026): il prototipo ritagliava sempre al
    centro e al theremin tagliava la testa del suonatore. Le schede il
    punto giusto lo dicono già — è `posizione`, scelto guardando le
    tavole — e il reel deve usare lo stesso, non indovinarne un altro."""
    pezzi = (posizione or "center").split()
    if len(pezzi) == 1:
        p = pezzi[0]
        if p in ("top", "bottom"):
            pezzi = ["center", p]
        else:
            pezzi = [p, "center"]

    def val(p):
        if p in _PAROLE:
            return _PAROLE[p]
        m = re.fullmatch(r"(-?\d+(?:\.\d+)?)%", p)
        if not m:
            raise ValueError(f"posizione non capita: {posizione!r}")
        return max(0.0, min(1.0, float(m.group(1)) / 100))

    a, b = pezzi[:2]
    # «top center» e «center top» dicono la stessa cosa
    if a in ("top", "bottom") or b in ("left", "right"):
        a, b = b, a
    return val(a), val(b)


# Quattro movimenti a rotazione, tutti lenti: la foto non deve mai stare
# ferma (un'immagine ferma per 2,6 secondi sembra una diapositiva) ma
# nemmeno tagliare fuori la macchina. Lo zoom massimo è 1,22: si perde al
# più un sesto per lato.
def _moto(nome, fx, fy, n):
    t = f"on/{n}"
    if nome == "avanti":
        z = f"1.0+0.10*{t}"
        x, y = f"(iw-iw/zoom)*{fx}", f"(ih-ih/zoom)*{fy}"
    elif nome == "dentro":
        z = f"1.12+0.10*{t}"
        x, y = f"(iw-iw/zoom)*{fx}", f"(ih-ih/zoom)*{fy}"
    elif nome == "destra":
        z = "1.15"
        x = f"(iw-iw/zoom)*max(0,min(1,{fx}-0.35+0.7*{t}))"
        y = f"(ih-ih/zoom)*{fy}"
    else:  # sinistra
        z = "1.15"
        x = f"(iw-iw/zoom)*max(0,min(1,{fx}+0.35-0.7*{t}))"
        y = f"(ih-ih/zoom)*{fy}"
    return z, x, y


MOTI = ("avanti", "destra", "dentro", "sinistra")


def orientamento(path):
    """Il tag EXIF Orientation di un JPEG (1 = dritto).

    LEZIONE IMPARATA (07/10/2026): Chromium raddrizza da solo le foto
    girate col tag EXIF, ffmpeg no (o sì, a seconda della versione: la 7.1
    lo fa, la 6.1 dei runner Ubuntu no). Le tavole uscivano dritte e lo
    stesso file nel reel usciva coricato. Qui si legge il tag e si gira a
    mano, con -noautorotate perché nessuna versione lo giri due volte."""
    import struct
    d = pathlib.Path(path).read_bytes()
    if d[:2] != b"\xff\xd8":
        return 1
    i = 2
    while i + 4 < len(d):
        if d[i] != 0xFF:
            return 1
        m = d[i + 1]
        lung = struct.unpack(">H", d[i + 2:i + 4])[0]
        if m == 0xE1 and d[i + 4:i + 10] == b"Exif\0\0":
            t = i + 10
            bo = "<" if d[t:t + 2] == b"II" else ">"
            ifd = struct.unpack(bo + "I", d[t + 4:t + 8])[0]
            for k in range(struct.unpack(bo + "H", d[t + ifd:t + ifd + 2])[0]):
                e = t + ifd + 2 + 12 * k
                if struct.unpack(bo + "H", d[e:e + 2])[0] == 0x0112:
                    return struct.unpack(bo + "H", d[e + 8:e + 10])[0]
            return 1
        if m == 0xDA:
            return 1
        i += 2 + lung
    return 1


RADDRIZZA = {2: "hflip,", 3: "hflip,vflip,", 4: "vflip,", 5: "transpose=0,",
             6: "transpose=1,", 7: "transpose=3,", 8: "transpose=2,"}


# --------------------------------------------------------------- testo ---

def _css():
    return f"""
@font-face{{font-family:'Oswald';src:url({gt.FONTS}/Oswald-700.woff2) format('woff2');font-weight:700}}
@font-face{{font-family:'PlexMono';src:url({gt.FONTS}/IBMPlexMono-600.woff2) format('woff2');font-weight:600}}
html,body{{margin:0;background:transparent}}
body{{width:{L}px;height:{H}px;position:relative;font-family:'Oswald';color:{gt.CREMA}}}
/* Il pannello copre meno di un terzo dello schermo: il resto è la
   macchina. Il margine destro largo tiene il testo lontano dalla colonna
   dei bottoni di Instagram. */
.pannello{{position:absolute;left:0;right:0;top:{PANNELLO_Y}px;background:rgba(56,41,29,.94);
  padding:34px 150px 40px 64px;border-bottom:8px solid {gt.ARANCIO}}}
.kick{{font-family:'PlexMono';font-weight:600;font-size:30px;letter-spacing:.16em;color:{gt.ARANCIO}}}
.hook{{font-weight:700;text-transform:uppercase;font-size:88px;line-height:1.02;margin-top:14px}}
/* La targhetta non deve arrivare sotto la colonna dei bottoni (x>920):
   «New England Digital Synclavier» a 58px ci finiva dentro. */
.tag{{position:absolute;left:64px;bottom:440px;background:{gt.ARANCIO};color:{gt.BRUNO};
  font-weight:700;font-size:58px;padding:8px 24px;text-transform:uppercase;white-space:nowrap}}
.tag small{{font-family:'PlexMono';font-weight:600;font-size:30px;margin-left:16px;letter-spacing:.1em}}
.handle{{display:block;font-family:'PlexMono';font-weight:600;font-size:38px;letter-spacing:.12em;
  color:{gt.ARANCIO};margin-top:26px}}
"""


def _pagina(html):
    # L'autofit riduce la frase finché il pannello non rientra: una frase
    # più lunga del previsto diventa più piccola, non finisce sotto la foto.
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{_css()}</style></head>
<body>{html}
<script>document.fonts.ready.then(()=>{{
 for(const el of document.querySelectorAll('.hook')){{
   let s=parseFloat(getComputedStyle(el).fontSize);
   while(el.closest('.pannello').getBoundingClientRect().bottom>{PANNELLO_MAX} && s>44){{s-=2;el.style.fontSize=s+'px';}}
   if(el.closest('.pannello').getBoundingClientRect().bottom>{PANNELLO_MAX}) document.body.dataset.troppo='1';
 }}
 for(const el of document.querySelectorAll('.tag')){{
   let s=parseFloat(getComputedStyle(el).fontSize);
   while(el.getBoundingClientRect().right>{TAG_MAX_X} && s>30){{s-=2;el.style.fontSize=s+'px';}}
 }}
 document.body.dataset.pronto='1';}});</script></body></html>"""


def battute(scheda):
    """Le battute del reel: quelle scritte nella scheda, più la chiusura.

    Niente ripiego: una scheda senza `reel_battute` non ha un reel (lo
    impedisce già `valida_scheda`). Un reel costruito con testi di
    riserva uscirebbe con l'aria di funzionare, ed è esattamente la
    lezione del timbro «sega» in suoni.py."""
    righe = scheda.get("reel_battute")
    if not righe:
        raise ValueError(f"la scheda '{scheda['slug']}' non ha reel_battute")
    tag = f'<div class="tag">{scheda["strumento"]}<small>{scheda["anno"]}</small></div>'
    out = []
    for i, (kick, testo) in enumerate(righe):
        out.append({"foto": i, "moto": MOTI[i % len(MOTI)],
                    "html": f'<div class="pannello"><div class="kick">{kick}</div>'
                            f'<div class="hook">{testo}</div></div>{tag}'})
    # Chiusura: stessa foto e stesso movimento della prima battuta, così
    # quando il reel ricomincia non c'è uno stacco.
    out.append({"foto": 0, "moto": MOTI[0],
                "html": f'<div class="pannello"><div class="kick">ELETTROFONI · N. {scheda["numero"]:03d}</div>'
                        f'<div class="hook">{scheda["reel_cta"]}</div>'
                        f'<span class="handle">@ELETTROFONI</span></div>{tag}'})
    return out


# ------------------------------------------------------------ montaggio ---

def _filtro(foto, moto, n):
    """Il grafo ffmpeg di una battuta: foto in movimento + testo sopra.

    Foto verticali (o quasi): coprono tutto lo schermo. Foto orizzontali:
    una fascia a tutta larghezza alta quanto serve per mostrarle intere
    (al massimo FASCIA_MAX), sopra uno sfondo fatto della stessa foto
    sfocata e scurita. Niente cornici di colore pieno: Instagram mostra
    meno i reel «con i bordi»."""
    src = RADICE / foto["file"]
    dim = gt._dimensioni(src)
    if not dim:
        raise RuntimeError(f"dimensioni illeggibili: {src}")
    w, h = dim
    o = orientamento(src)
    if o >= 5:
        w, h = h, w
    giro = RADDRIZZA.get(o, "")
    asp = w / h
    fx, fy = fuoco(foto.get("posizione"))
    z, x, y = _moto(moto, fx, fy, n)
    # Si lavora al doppio della risoluzione finale: zoompan arrotonda le
    # coordinate al pixel, e a risoluzione piena il movimento tremola.
    if asp < 0.8:
        return (f"[0:v]{giro}scale={L*2}:{H*2}:force_original_aspect_ratio=increase,"
                f"crop={L*2}:{H*2}:(iw-ow)*{fx}:(ih-oh)*{fy},"
                f"zoompan=z='{z}':x='{x}':y='{y}':d={n}:s={L}x{H}:fps={FPS}[v0];"
                f"[v0][1:v]overlay=0:0:shortest=1[v1]")
    fh = min(FASCIA_MAX, round(L / asp / 2) * 2)
    return (f"[0:v]{giro}split=2[a][b];"
            f"[a]scale={L}:{H}:force_original_aspect_ratio=increase,crop={L}:{H},boxblur=40:4,"
            f"eq=brightness=-0.32:saturation=0.7,loop=loop={n}:size=1,setpts=N/{FPS}/TB[bg];"
            f"[b]scale={L*2}:{fh*2}:force_original_aspect_ratio=increase,"
            f"crop={L*2}:{fh*2}:(iw-ow)*{fx}:(ih-oh)*{fy},"
            f"zoompan=z='{z}':x='{x}':y='{y}':d={n}:s={L}x{fh}:fps={FPS}[fg];"
            f"[bg][fg]overlay=0:{FASCIA_Y + (FASCIA_MAX - fh) // 2}:shortest=1[v0];"
            f"[v0][1:v]overlay=0:0:shortest=1[v1]")


def _audio(scheda, wav, durata, ff):
    """La colonna sonora: la macchina vera se la scheda ne ha una
    registrazione libera (`reel_audio`), altrimenti la sigla sintetizzata.

    PERCHÉ (07/10/2026). Nella nicchia, chi cresce fa SENTIRE la macchina:
    il suono è il gancio (Synthet, 1,5 milioni di iscritti, apre con «you
    know this sound»; un Mellotron vero filmato col telefono a una fiera
    ha fatto 217.000 visualizzazioni su un canale da 890 iscritti). La
    sigla con lo stesso motivo per tutte le schede è il contrario.
    Il ripiego sulla sigla resta, ma si dichiara nel log: un ripiego che
    non si vede non lo controlla nessuno (lezione del timbro «sega»)."""
    a = scheda.get("reel_audio")
    if not a:
        print(f"[reel] audio: sigla sintetizzata ({scheda['slug']} non ha reel_audio)")
        # Attacco secco: il suono parte col primo fotogramma, come l'immagine.
        suoni.genera(scheda, wav, durata=durata, attacco=0.01)
        return
    src = RADICE / a["file"]
    print(f"[reel] audio: registrazione vera, {a['file']} da {a.get('inizio', 0)} s")
    # -stream_loop: se la registrazione è più corta del reel ricomincia.
    # Volume: loudnorm a -16 LUFS integrati, che è quanto suona forte la
    # sigla normalizzata sull'RMS (lezione del 28/08: si pareggia il volume
    # percepito, non il picco). Attacco di 10 ms, coda di 0,25 s.
    _esegui([ff, "-y", "-loglevel", "error", "-stream_loop", "-1",
             "-ss", str(a.get("inizio", 0)), "-i", str(src), "-t", f"{durata:.2f}",
             "-af", f"afade=t=in:d=0.01,afade=t=out:st={durata - 0.25:.2f}:d=0.25,"
                    "loudnorm=I=-16:TP=-1.5:LRA=11",
             "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le", str(wav)])


def costruisci(scheda, cartella=None):
    from playwright.sync_api import sync_playwright

    cartella = pathlib.Path(cartella or (RADICE / "docs" / "tavole" / scheda["slug"]))
    cartella.mkdir(parents=True, exist_ok=True)
    lavoro = cartella / "_reel"
    lavoro.mkdir(exist_ok=True)

    sequenza = battute(scheda)
    # Una foto che sulla tavola regge solo grazie alla didascalia («lo
    # stesso strumento visto dall'altro verso») nel reel, che didascalie
    # non ne ha, sembra un errore: la scheda la esclude con nel_reel=False.
    foto = contenuti.foto_del_reel(scheda)

    png = []
    exe = os.environ.get("ELETTROFONI_CHROMIUM")
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe, args=["--no-sandbox", "--force-color-profile=srgb"])
        pg = b.new_page(viewport={"width": L, "height": H})
        for i, bt in enumerate(sequenza):
            # LEZIONE IMPARATA (28/08/2026): con set_content() la pagina ha
            # origine about:blank e Chromium blocca i file:// — spariscono i
            # font senza un errore. Si scrive un file e si fa goto().
            tmp = lavoro / f"t{i}.html"
            tmp.write_text(_pagina(bt["html"]), encoding="utf-8")
            pg.goto(tmp.as_uri())
            pg.wait_for_selector("body[data-pronto='1']", timeout=20000)
            if pg.evaluate("document.body.dataset.troppo") == "1":
                raise RuntimeError(f"battuta {i + 1} troppo lunga anche a 44px: accorciarla")
            f = lavoro / f"t{i}.png"
            pg.screenshot(path=str(f), omit_background=True)
            png.append(f)
        b.close()

    ff = _ff()
    n = int(SEC_BATTUTA * FPS)
    clip = []
    for i, bt in enumerate(sequenza):
        f = foto[bt["foto"] % len(foto)]
        c = lavoro / f"c{i}.mp4"
        _esegui([ff, "-y", "-loglevel", "error",
                 "-noautorotate", "-i", str(RADICE / f["file"]),
                 "-loop", "1", "-framerate", str(FPS), "-i", str(png[i]),
                 "-filter_complex", _filtro(f, bt["moto"], n)
                 + f";[v1]scale={LARG}:{ALT},setsar=1,format=yuv420p[o]",
                 "-map", "[o]", "-frames:v", str(n), "-r", str(FPS),
                 "-c:v", "libx264", "-profile:v", "main", "-pix_fmt", "yuv420p",
                 "-g", str(FPS * 2), "-sc_threshold", "0", "-bf", "0",
                 "-preset", "medium", "-crf", "20", str(c)])
        clip.append(c)

    elenco = lavoro / "elenco.txt"
    elenco.write_text("".join(f"file '{c.name}'\n" for c in clip))
    muto = lavoro / "muto.mp4"
    _esegui([ff, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
             "-i", str(elenco), "-c", "copy", str(muto)])

    durata = SEC_BATTUTA * len(clip)
    wav = lavoro / "musica.wav"
    _audio(scheda, wav, durata, ff)

    grezzo = lavoro / "grezzo.mp4"
    _esegui([ff, "-y", "-loglevel", "error", "-i", str(muto), "-i", str(wav),
             "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2",
             "-shortest", str(grezzo)])

    # reel2.mp4, non reel.mp4: i reel del formato 1 restano dove sono, e
    # un nome nuovo non può essere servito dalla cache di Pages con il
    # file vecchio dentro (Pages tiene in cache fino a 10 minuti, e
    # Instagram scarica il video proprio in quei minuti).
    finale = cartella / NOME_FILE
    _esegui([ff, "-y", "-loglevel", "error", "-i", str(grezzo), "-c", "copy",
             "-movflags", "+faststart", "-use_editlist", "0", str(finale)])

    for f in lavoro.iterdir():
        f.unlink()
    lavoro.rmdir()
    return finale


def verifica(percorso):
    """Controlla il file finito. Senza ffprobe (nel container di sviluppo
    non c'e') si legge l'intestazione con ffmpeg -i: dice le stesse cose
    tranne i B-frame, che sono garantiti da -bf 0."""
    problemi = []
    if shutil.which("ffprobe"):
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries",
             "stream=codec_name,codec_type,profile,width,height,channels,sample_rate,has_b_frames",
             "-show_entries", "format=duration", "-of", "default=nw=1", str(percorso)],
            capture_output=True, text=True)
        d = r.stdout
        if "codec_type=audio" not in d: problemi.append("NESSUN AUDIO")
        if "codec_name=h264" not in d: problemi.append("video non H.264")
        if "codec_name=aac" not in d: problemi.append("audio non AAC")
        if f"width={LARG}" not in d or f"height={ALT}" not in d:
            problemi.append(f"non è {LARG}x{ALT}")
        if "has_b_frames=0" not in d: problemi.append("contiene B-frame")
        return d, problemi
    r = subprocess.run([_ff(), "-hide_banner", "-i", str(percorso)], capture_output=True, text=True)
    d = r.stderr
    if "Audio: aac" not in d: problemi.append("NESSUN AUDIO AAC")
    if "Video: h264 (Main)" not in d: problemi.append("video non H.264 main")
    if f"{LARG}x{ALT}" not in d: problemi.append(f"non è {LARG}x{ALT}")
    if "44100 Hz" not in d: problemi.append("audio non a 44.1 kHz")
    return d, problemi


if __name__ == "__main__":
    slug = sys.argv[1] if len(sys.argv) > 1 else "dx7"
    cartella = sys.argv[2] if len(sys.argv) > 2 else None
    if slug == "--prossima":
        import json
        stato = RADICE / "stato.json"
        gia = set()
        if stato.exists():
            gia = {x["slug"] for x in json.loads(stato.read_text())["pubblicati"]}
        prossima = contenuti.scheda_da_pubblicare(gia)
        if prossima is None:
            print("[reel] nessuna scheda in coda: niente da costruire")
            raise SystemExit(0)
        slug = prossima["slug"]
    scheda = next((s for s in contenuti.SCHEDE if s["slug"] == slug), None)
    if scheda is None:
        print(f"nessuna scheda '{slug}'"); raise SystemExit(1)
    out = costruisci(scheda, cartella)
    d, problemi = verifica(out)
    print(f"[reel] {slug}: {out.stat().st_size/1e6:.1f} MB — "
          + ("OK" if not problemi else "PROBLEMI: " + ", ".join(problemi)))
    if problemi:
        print(d)
        raise SystemExit(1)
