# -*- coding: utf-8 -*-
"""ELETTROFONI — Dinamo che parla: la mascotte animata per il reel parlato.

PERCHÉ (21/10/2026). Il proprietario ha chiesto un reel PARLATO: Dinamo,
l'automa che compila il catalogo, racconta la scheda con una voce
sintetica mentre le scene scorrono. Una voce senza una faccia che si
muove è una voce fuori campo, e la voce fuori campo è proprio il tono da
documentario che «Come si scrive» (CLAUDE.md) vieta. Qui c'è la faccia:
lo stesso automa delle tavole (`AUTOMA_SVG` in genera_tavole.py), in un
tondo crema col bordo bruno come un timbro, che apre e chiude la bocca
seguendo il volume della registrazione della voce e ogni tanto sbatte le
palpebre. Dinamo è un automa: la bocca è una griglia da altoparlante che
si accende, non labbra. Una bocca a tre posizioni che segue l'inviluppo
basta e avanza per un automa; una sincronizzazione labiale «umana» sarebbe
il travestimento che il proprietario non vuole.

COME FUNZIONA. Ogni fotogramma ha uno stato (bocca 0..4, occhi, sguardo,
lancetta del VU 0..5, lampadina): per gli stati che il reel usa davvero
si fa uno sprite PNG con alfa, reso UNA volta con Chromium e tenuto in una
cartella cache. Per ogni fotogramma si scrive un link simbolico
f_00000.png, f_00001.png… allo sprite giusto: ffmpeg legge la cartella con
«-framerate FPS -i f_%05d.png» e la sovrappone al reel con `overlay`.
Niente Pillow, niente 900 copie dello stesso file: 900 link, che pesano
zero. La bocca si decide sull'RMS della voce a finestre di 1/FPS secondi,
normalizzato sul 95° percentile e con isteresi, così non sfarfalla.

DAL MONTAGGIO (genera_reel.py o chi per lui):

    import dinamo
    pattern = dinamo.sequenza(wav_voce, FPS, durata_s, inizio_s, lavoro / "dinamo")
    # poi, fra gli input di ffmpeg:  "-framerate", str(FPS), "-i", pattern
    # e nel filtro:  [k:v]format=rgba,scale=260:-2[d];[base][d]overlay=x=40:y=H-h-290+4*sin(2*PI*t/2.6)[o]

`inizio_s` è il secondo del video in cui la voce comincia: prima, bocca
chiusa. Se la sequenza finisce prima del video, `overlay` tiene l'ultimo
fotogramma (eof_action=repeat, il suo default): Dinamo resta, zitto.

    python dinamo.py prova.wav [demo.mp4]   # demo di 10 s, più foglio.png
                                            # e 4 fotogrammi da guardare

Se `prova.wav` non esiste lo genera ffmpeg (una sinusoide modulata a 3 Hz
con pause: non è una voce, ma fa muovere la bocca come una).
"""
import math
import os
import pathlib
import random
import shutil
import subprocess
import sys
import tempfile
import wave
import zlib

import numpy as np

import genera_tavole as gt

# 28/10/2026, il proprietario: «Migliora il personaggio nei reels parlati…
# fallo molto molto meglio e definito graficamente». Il primo Dinamo era
# l'icona al tratto delle tavole dentro un tondo, 187 px su 720, con 3 bocche
# e un battito di ciglia: da lontano un bollino. Ora è un busto a colori
# pieni (arancio, bruno, crema, come le tavole), contorno di 9 px e un bordo
# da adesivo crema con l'ombra, così si stacca da QUALUNQUE foto, chiara o
# scura. Stesso automa (antenna, testa quadrata, occhi tondi, bocca a
# griglia), più cose che si muovono e dicono «sta parlando»: la lampadina
# dell'antenna si accende, la lancetta del VU sul petto segue la voce con
# la balistica di uno strumento vero, la griglia della bocca ha 5 livelli,
# gli occhi ogni tanto guardano in alto a destra, verso il testo.
X0_SVG, LARG_SVG, ALT_SVG = 46, 308, 420   # viewBox del disegno: il busto più il bordo da adesivo
LATO = 400                       # larghezza dello sprite in px
BOCCHE = (0, 1, 2, 3, 4)         # barre accese della griglia
OCCHI = ("aperti", "socchiusi", "chiusi")

# Soglie della bocca sull'inviluppo (0..1): per salire di un livello serve
# la soglia piena, per scendere bisogna andare sotto il 75%. Così un valore
# che balla intorno a una soglia non fa battere la griglia.
SOGLIE_BOCCA = (0.12, 0.30, 0.50, 0.72)
TENUTA_MIN = 3
# VU: sale in 2 fotogrammi, scende in 10, come la lancetta vera.
VU_SALITA, VU_DISCESA = 0.55, 0.12
# Lampadina: accesa finché la voce è sopra 0,1 negli ultimi 0,3 s.
LAMPADA_TENUTA_S = 0.3
# Battito di ciglia: il primo presto (uno sguardo fisso di 5 s si nota),
# poi uno ogni 3-5 s; socchiuso-chiuso-chiuso-socchiuso.
BATTITO_PRIMO = (1.5, 3.5)
BATTITO_OGNI = (3.0, 5.0)
BATTITO = ("socchiusi", "chiusi", "chiusi", "socchiusi")
# Occhiate verso il testo: 1-2 s, ogni 4-7 s.
OCCHIATA_DURATA = (1.0, 2.0)
OCCHIATA_OGNI = (4.0, 7.0)

FPS = 30
DEMO_SEC = 10.0
DEMO_LATO = 260


# ------------------------------------------------------------- disegno ---

CREMA, BRUNO, ARANCIO = gt.CREMA, gt.BRUNO, gt.ARANCIO
OMBRA, LUCE, AVORIO, GIALLO = "#a9521d", "#f29a5c", "#fffaf0", "#ffc35a"


def svg_sprite(bocca=0, occhi="aperti", sguardo=0, ago=0, lampada=False, lato=LATO):
    """Dinamo in uno stato: bocca 0..4, occhi aperti/socchiusi/chiusi,
    sguardo 0 (avanti) o 1 (in alto a destra, verso il testo), ago 0..5
    (la lancetta del VU), lampada accesa o spenta. Fondo trasparente."""
    px = 5*sguardo; py = -3*sguardo
    o=[]
    o.append(f'''<defs>
<filter id="adesivo" x="-10%" y="-10%" width="120%" height="120%">
 <feMorphology in="SourceAlpha" operator="dilate" radius="7" result="d"/>
 <feFlood flood-color="{CREMA}"/><feComposite in2="d" operator="in" result="bordo"/>
 <feGaussianBlur in="d" stdDeviation="6" result="s0"/><feOffset in="s0" dx="0" dy="6" result="s1"/>
 <feComponentTransfer in="s1" result="ombra"><feFuncA type="linear" slope="0.45"/></feComponentTransfer>
 <feMerge><feMergeNode in="ombra"/><feMergeNode in="bordo"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<radialGradient id="alone"><stop offset="0" stop-color="{GIALLO}" stop-opacity=".9"/><stop offset="1" stop-color="{GIALLO}" stop-opacity="0"/></radialGradient>
</defs>''')
    g=[]
    # alone della lampadina (fuori dal filtro, sopra)
    # antenna
    g.append(f'<line x1="200" y1="84" x2="200" y2="44" stroke="{BRUNO}" stroke-width="9" stroke-linecap="round"/>')
    g.append(f'<rect x="186" y="74" width="28" height="14" rx="4" fill="{BRUNO}"/>')
    g.append(f'<circle cx="200" cy="34" r="15" fill="{GIALLO if lampada else OMBRA}" stroke="{BRUNO}" stroke-width="7"/>')
    g.append(f'<circle cx="195" cy="29" r="4" fill="{AVORIO}" opacity="{0.95 if lampada else 0.55}"/>')
    # busto
    g.append(f'<path d="M64 384 L64 318 Q64 262 120 262 L280 262 Q336 262 336 318 L336 384 Q336 406 314 406 L86 406 Q64 406 64 384 Z" fill="{ARANCIO}" stroke="{BRUNO}" stroke-width="9" stroke-linejoin="round"/>')
    g.append(f'<path d="M300 268 Q330 276 331 318 L331 384 Q331 400 316 401 L304 401 Z" fill="{OMBRA}"/>')
    # pannello del petto col VU
    g.append(f'<rect x="128" y="284" width="144" height="82" rx="12" fill="{CREMA}" stroke="{BRUNO}" stroke-width="7"/>')
    cx, cy, r = 200, 352, 52
    def pt(a, rr): return cx+rr*math.sin(math.radians(a)), cy-rr*math.cos(math.radians(a))
    x1,y1=pt(-55,r); x2,y2=pt(55,r)
    g.append(f'<path d="M{x1:.1f} {y1:.1f} A{r} {r} 0 0 1 {x2:.1f} {y2:.1f}" fill="none" stroke="{BRUNO}" stroke-width="4"/>')
    xr,yr=pt(25,r)
    g.append(f'<path d="M{xr:.1f} {yr:.1f} A{r} {r} 0 0 1 {x2:.1f} {y2:.1f}" fill="none" stroke="{ARANCIO}" stroke-width="8"/>')
    for a in range(-50,56,15):
        ax,ay=pt(a,r-2); bx,by=pt(a,r-11)
        g.append(f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{BRUNO}" stroke-width="3"/>')
    ang=-48+ago*19
    nx,ny=pt(ang,r-6)
    g.append(f'<line x1="{cx}" y1="{cy}" x2="{nx:.1f}" y2="{ny:.1f}" stroke="{BRUNO}" stroke-width="5" stroke-linecap="round"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="7" fill="{BRUNO}"/>')
    # targhetta col nome
    g.append(f'<rect x="146" y="372" width="108" height="24" rx="5" fill="{BRUNO}"/>')
    g.append(f'<text x="200" y="390" text-anchor="middle" font-family="PlexMono" font-weight="600" font-size="16" letter-spacing="3.5" fill="{CREMA}">DINAMO</text>')
    # bulloni del busto
    for x,y in ((88,300),(312,300)):
        g.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{CREMA}" stroke="{BRUNO}" stroke-width="4"/>')
    # collo
    g.append(f'<rect x="166" y="232" width="68" height="16" rx="5" fill="{BRUNO}"/>')
    g.append(f'<rect x="174" y="246" width="52" height="18" rx="5" fill="{OMBRA}" stroke="{BRUNO}" stroke-width="6"/>')
    # orecchie
    for x in (88, 290):
        g.append(f'<rect x="{x}" y="128" width="22" height="50" rx="7" fill="{OMBRA}" stroke="{BRUNO}" stroke-width="7"/>')
    # testa
    g.append(f'<rect x="104" y="84" width="192" height="152" rx="34" fill="{ARANCIO}" stroke="{BRUNO}" stroke-width="9"/>')
    g.append(f'<path d="M110 196 Q112 230 140 231 L262 231 Q290 230 291 196 Z" fill="{OMBRA}"/>')
    g.append(f'<path d="M126 104 Q140 94 170 94" fill="none" stroke="{LUCE}" stroke-width="7" stroke-linecap="round"/>')
    for x,y in ((122,104),(278,104),(122,216),(278,216)):
        g.append(f'<circle cx="{x}" cy="{y}" r="4.5" fill="{BRUNO}"/>')
    # visiera
    g.append(f'<rect x="128" y="106" width="144" height="106" rx="24" fill="{CREMA}" stroke="{BRUNO}" stroke-width="7"/>')
    # occhi
    for ex in (170, 230):
        g.append(f'<circle cx="{ex}" cy="146" r="21" fill="{AVORIO}" stroke="{BRUNO}" stroke-width="6"/>')
        if occhi != "chiusi":
            g.append(f'<circle cx="{ex+px}" cy="{146+py}" r="11" fill="{BRUNO}"/>')
            g.append(f'<circle cx="{ex+px-3.5}" cy="{146+py-3.5}" r="3" fill="{AVORIO}"/>')
        if occhi == "socchiusi":
            g.append(f'<path d="M{ex-21} 146 A21 21 0 0 1 {ex+21} 146 Z" fill="{ARANCIO}" stroke="{BRUNO}" stroke-width="6" stroke-linejoin="round"/>')
        if occhi == "chiusi":
            g.append(f'<circle cx="{ex}" cy="146" r="21" fill="{ARANCIO}" stroke="{BRUNO}" stroke-width="6"/>')
            g.append(f'<path d="M{ex-14} 148 Q{ex} 158 {ex+14} 148" fill="none" stroke="{BRUNO}" stroke-width="5" stroke-linecap="round"/>')
    # sopracciglia: dritte e tranquille; si alzano di 4 px quando la voce è forte
    alza = 4 if bocca >= 3 else 0
    for ex in (170, 230):
        g.append(f'<line x1="{ex-12}" y1="{118-alza}" x2="{ex+12}" y2="{118-alza}" stroke="{BRUNO}" stroke-width="5" stroke-linecap="round"/>')
    # bocca: griglia da altoparlante, barre che si accendono
    g.append(f'<rect x="160" y="176" width="80" height="26" rx="9" fill="{BRUNO}"/>')
    alt = [3, 7, 11, 15, 19][bocca]
    for i,x in enumerate((172,186,200,214,228)):
        h = max(3, alt - (abs(i-2)*3 if bocca>0 else 0))
        col = CREMA if bocca == 0 else (GIALLO if bocca >= 3 and i in (1,2,3) else LUCE)
        g.append(f'<line x1="{x}" y1="{189-h/2:.1f}" x2="{x}" y2="{189+h/2:.1f}" stroke="{col}" stroke-width="6" stroke-linecap="round" opacity="{0.55 if bocca==0 else 1}"/>')
    alone = f'<circle cx="200" cy="34" r="34" fill="url(#alone)"/>' if lampada else ''
    corpo = "\n".join(g)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{X0_SVG} 0 {LARG_SVG} {ALT_SVG}" '
            f'width="{lato}" height="{lato * ALT_SVG // LARG_SVG}">'
            + "".join(o) + f'<g filter="url(#adesivo)">{corpo}</g>{alone}</svg>')


def _pagina(corpo, larg, alt, sfondo="transparent", css=""):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:'PlexMono';src:url('{gt.FONTS}/IBMPlexMono-600.woff2');font-weight:600}}
html,body{{margin:0;padding:0;background:{sfondo}}}
body{{width:{larg}px;height:{alt}px;overflow:hidden}}
svg{{display:block}}
{css}
</style></head><body>{corpo}
<script>
Promise.all([document.fonts.ready,
             ...Array.from(document.images).map(i => i.decode().catch(() => null))])
  .then(() => requestAnimationFrame(() => {{ document.body.dataset.pronto = '1'; }}));
</script></body></html>"""


def _browser(p):
    # ELETTROFONI_CHROMIUM: override locale; in CI usa il chromium di Playwright
    exe = os.environ.get("ELETTROFONI_CHROMIUM")
    return p.chromium.launch(executable_path=exe, args=["--no-sandbox", "--force-color-profile=srgb"])


def _scatta(page, html, file, larg, alt, **kw):
    # LEZIONE (28/08/2026): mai set_content(): la pagina ha origine
    # about:blank e Chromium blocca i file:// senza dire niente. Si scrive
    # un file e si fa goto().
    tmp = file.with_suffix(".html")
    tmp.write_text(html, encoding="utf-8")
    page.set_viewport_size({"width": larg, "height": alt})
    page.goto(tmp.as_uri())
    page.wait_for_selector("body[data-pronto='1']", timeout=20000)
    page.screenshot(path=str(file), clip={"x": 0, "y": 0, "width": larg, "height": alt}, **kw)
    tmp.unlink()


def nome_sprite(st):
    b, o, g, a, l = st
    return f"d_b{b}_{o[0]}_g{g}_a{a}_l{int(l)}.png"


def rendi_sprite(cache, stati_usati, forza=False):
    """Un PNG per ogni stato che il reel usa davvero (di solito 100-200
    combinazioni, non tutte le 360 possibili), resi con UNA pagina di
    Chromium cambiando l'SVG dentro e fotografandolo. Tenuti in `cache`:
    il secondo reel riusa quelli già fatti. Torna {stato: Path}."""
    cache = pathlib.Path(cache)
    cache.mkdir(parents=True, exist_ok=True)
    file = {st: cache / nome_sprite(st) for st in set(stati_usati)}
    mancanti = [st for st, f in file.items() if forza or not f.exists()]
    if mancanti:
        from playwright.sync_api import sync_playwright
        alt = LATO * ALT_SVG // LARG_SVG
        with sync_playwright() as p:
            b = _browser(p)
            page = b.new_page(viewport={"width": LATO, "height": alt})
            base = cache / "_base.html"
            base.write_text(_pagina('<div id="d"></div>', LATO, alt), encoding="utf-8")
            page.goto(base.as_uri())
            page.wait_for_selector("body[data-pronto='1']", timeout=20000)
            for st in mancanti:
                page.evaluate("s => { document.getElementById('d').innerHTML = s; }", svg_sprite(*st))
                page.evaluate("() => document.fonts.ready")
                page.screenshot(path=str(file[st]), omit_background=True,
                                clip={"x": 0, "y": 0, "width": LATO, "height": alt})
            b.close()
            base.unlink()
        print(f"[dinamo] resi {len(mancanti)} sprite in {cache}")
    return file


def foglio(out, stati_scelti=None):
    """Un PNG con alcuni stati affiancati su tre foto diverse, per guardarli."""
    stati_scelti = stati_scelti or [(0, "aperti", 0, 0, False), (2, "aperti", 0, 2, True),
                                    (4, "aperti", 1, 5, True), (1, "socchiusi", 0, 1, True),
                                    (0, "chiusi", 0, 0, False)]
    out = pathlib.Path(out)
    file = rendi_sprite(out.parent / "_sprite_foglio", stati_scelti)
    alt = LATO * ALT_SVG // LARG_SVG
    celle = "".join(f'<div class="c"><img src="{file[st].resolve().as_uri()}"></div>' for st in stati_scelti)
    larg = len(stati_scelti) * (LATO + 20) + 20
    css = (f".f{{display:flex;gap:20px;padding:20px}}img{{display:block;width:{LATO}px}}")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = _browser(p)
        page = b.new_page(viewport={"width": larg, "height": alt + 40})
        _scatta(page, _pagina(f'<div class="f">{celle}</div>', larg, alt + 40, gt.BRUNO, css), out, larg, alt + 40)
        b.close()
    return out


# ------------------------------------------------------------- audio ---

def _ff():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        raise RuntimeError("ffmpeg non trovato (né in PATH né imageio-ffmpeg)")


def _esegui(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{cmd[0]} fallito:\n{r.stderr[-1500:]}")


def _campioni(percorso):
    """(frequenza, campioni mono in float -1..1). Col modulo wave della
    stdlib; se il file non è PCM intero (float a 32 bit, mp3…) ffmpeg lo
    converte in PCM 16 bit mono, e il log lo dice."""
    percorso = pathlib.Path(percorso)
    try:
        with wave.open(str(percorso), "rb") as w:
            sr, larg, can = w.getframerate(), w.getsampwidth(), w.getnchannels()
            grezzo = w.readframes(w.getnframes())
    except (wave.Error, EOFError) as e:
        print(f"[dinamo] {percorso.name}: non è un wav PCM intero ({e}), lo converte ffmpeg")
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as t:
            tmp = pathlib.Path(t.name)
        try:
            _esegui([_ff(), "-y", "-loglevel", "error", "-i", str(percorso),
                     "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(tmp)])
            return _campioni(tmp)
        finally:
            tmp.unlink(missing_ok=True)
    if larg == 1:
        x = (np.frombuffer(grezzo, np.uint8).astype(np.float32) - 128.0) / 128.0
    elif larg == 2:
        x = np.frombuffer(grezzo, "<i2").astype(np.float32) / 32768.0
    elif larg == 3:
        b = np.frombuffer(grezzo, np.uint8).reshape(-1, 3).astype(np.int32)
        x = (b[:, 0] | (b[:, 1] << 8) | (b[:, 2].astype(np.int8).astype(np.int32) << 16)).astype(np.float32) / 8388608.0
    elif larg == 4:
        x = np.frombuffer(grezzo, "<i4").astype(np.float32) / 2147483648.0
    else:
        raise RuntimeError(f"{percorso.name}: campioni da {larg} byte, non so leggerli")
    if can > 1:
        x = x.reshape(-1, can).mean(axis=1)
    return sr, x


def inviluppo(wav, fps):
    """Un valore 0..1 per fotogramma: RMS a finestre di 1/fps secondi,
    diviso per il 95° percentile delle finestre non mute (così i picchi
    non schiacciano tutto il resto a zero) e smussato su tre fotogrammi."""
    sr, x = _campioni(wav)
    n = int(math.ceil(len(x) * fps / sr))
    if n == 0:
        return []
    bordi = np.round(np.arange(n + 1) * sr / fps).astype(int)
    bordi[-1] = len(x)
    rms = np.array([math.sqrt(float(np.mean(x[a:b] ** 2))) if b > a else 0.0
                    for a, b in zip(bordi[:-1], bordi[1:])])
    attive = rms[rms > 1e-4]           # sotto -80 dBFS è silenzio
    if len(attive) == 0:
        return [0.0] * n
    v = np.minimum(rms / np.percentile(attive, 95), 1.0)
    v = np.convolve(v, [0.25, 0.5, 0.25], mode="same")
    return [float(a) for a in v]


def _livello(stato, v):
    """Il nuovo livello della bocca (0..4) con isteresi: si sale a soglia
    piena, si scende sotto il 75% della soglia."""
    su = sum(1 for t in SOGLIE_BOCCA if v >= t)
    if su > stato:
        return su
    giu = sum(1 for t in SOGLIE_BOCCA if v >= 0.75 * t)
    return min(stato, giu)


def stati(inviluppo, fps, inizio_s, n_fotogrammi, seme=0):
    """Per ogni fotogramma del video (bocca, occhi, sguardo, ago, lampada).
    La voce comincia a `inizio_s`: prima, e dopo la fine dell'inviluppo,
    bocca chiusa e lancetta a riposo. Battiti e occhiate dipendono solo dal
    seme: stessa scheda, stesso video, due volte."""
    scarto = int(round(inizio_s * fps))
    tenuta_l = max(1, int(round(LAMPADA_TENUTA_S * fps)))
    bocca, stato, tenuta = [], 0, TENUTA_MIN
    ago, vu = [], 0.0
    lampada, ultimo_suono = [], -10 ** 9
    for k in range(n_fotogrammi):
        j = k - scarto
        v = inviluppo[j] if 0 <= j < len(inviluppo) else 0.0
        nuovo = _livello(stato, v)
        if nuovo != stato and tenuta >= TENUTA_MIN:
            stato, tenuta = nuovo, 1
        else:
            tenuta += 1
        bocca.append(stato)
        vu += (VU_SALITA if v > vu else VU_DISCESA) * (v - vu)
        ago.append(min(5, int(round(vu * 5.4))))
        if v >= 0.1:
            ultimo_suono = k
        lampada.append(k - ultimo_suono <= tenuta_l)
    rng = random.Random(seme)
    occhi = ["aperti"] * n_fotogrammi
    t = rng.uniform(*BATTITO_PRIMO)
    while t * fps < n_fotogrammi:
        k0 = int(round(t * fps))
        for i, o in enumerate(BATTITO):
            if k0 + i < n_fotogrammi:
                occhi[k0 + i] = o
        t += rng.uniform(*BATTITO_OGNI)
    sguardo = [0] * n_fotogrammi
    t = rng.uniform(*OCCHIATA_OGNI) / 2
    while t * fps < n_fotogrammi:
        k0, d = int(round(t * fps)), int(round(rng.uniform(*OCCHIATA_DURATA) * fps))
        for k in range(k0, min(k0 + d, n_fotogrammi)):
            sguardo[k] = 1
        t += rng.uniform(*OCCHIATA_OGNI)
    return list(zip(bocca, occhi, sguardo, ago, lampada))


# ----------------------------------------------------------- sequenza ---

def _collega(sorgente, link):
    """Link simbolico; se il filesystem non li consente, hard link; se
    nemmeno quelli, copia. Torna come ha fatto, per il log."""
    if link.exists() or link.is_symlink():
        link.unlink()
    try:
        os.symlink(str(sorgente), str(link))
        return "link simbolici"
    except OSError:
        pass
    try:
        os.link(str(sorgente), str(link))
        return "hard link"
    except OSError:
        shutil.copyfile(sorgente, link)
        return "copie"


def sequenza(wav_voce, fps, durata_s, inizio_s, cartella, seme=None, cache=None):
    """Scrive in `cartella` f_00000.png … f_NNNNN.png, uno per fotogramma,
    come link agli sprite (che stanno in `cache`, default cartella/sprite),
    e stati.txt con la scelta di ogni fotogramma. Torna il pattern per
    ffmpeg («…/f_%05d.png»). Il seme, se non dato, viene dal nome del wav:
    deterministico, ma diverso da scheda a scheda."""
    cartella = pathlib.Path(cartella)
    cartella.mkdir(parents=True, exist_ok=True)
    # I resti di una sequenza più lunga vanno tolti: ffmpeg legge la
    # numerazione finché è continua, e si prenderebbe anche quelli.
    for vecchio in cartella.glob("f_*.png"):
        vecchio.unlink()
    n = int(round(durata_s * fps))
    if seme is None:
        seme = zlib.crc32(pathlib.Path(wav_voce).name.encode("utf-8"))
    env = inviluppo(wav_voce, fps)
    if not any(v >= SOGLIE_BOCCA[0] for v in env):
        # Un wav muto passato come voce è un errore a monte: con un
        # Dinamo a bocca chiusa per tutto il reel non se ne accorgerebbe
        # nessuno (vedi CLAUDE.md, «un ripiego che non lascia traccia»).
        raise RuntimeError(f"{wav_voce}: nessun suono sopra la soglia, non è una voce")
    seq = stati(env, fps, inizio_s, n, seme)
    sprite = rendi_sprite(cache or cartella / "sprite", seq)
    modo = "link simbolici"
    for k, st in enumerate(seq):
        modo = _collega(sprite[st].resolve(), cartella / f"f_{k:05d}.png")
    (cartella / "stati.txt").write_text(
        "".join(f"{k:05d} {b} {o} {g} {a} {int(l)}\n" for k, (b, o, g, a, l) in enumerate(seq)),
        encoding="utf-8")
    conta = {b: sum(1 for x in seq if x[0] == b) for b in BOCCHE}
    battiti = sum(1 for k in range(1, n) if seq[k][1] == "chiusi" and seq[k - 1][1] != "chiusi")
    print(f"[dinamo] {n} fotogrammi a {fps} fps ({modo}, {len(sprite)} sprite): bocca "
          + ", ".join(f"{b} {100 * c // max(n, 1)}%" for b, c in conta.items())
          + f"; {battiti} battiti di ciglia; lampada accesa {100 * sum(x[4] for x in seq) // max(n, 1)}%"
          + f"; voce da {inizio_s:.2f} s")
    return str(cartella / "f_%05d.png")


# --------------------------------------------------------------- demo ---

def wav_di_prova(percorso, ff, durata=DEMO_SEC):
    """Una «voce» finta: 220 Hz modulati in ampiezza a 3 Hz, frasi di 2 s
    con pause di 0,7 s, e muto per i primi 0,8 s (per vedere la bocca
    chiusa prima che parta)."""
    espr = "0.6*sin(2*PI*220*t)*(0.55+0.45*sin(2*PI*3*t))*gt(mod(t,2.7),0.7)*gt(t,0.8)"
    _esegui([ff, "-y", "-loglevel", "error", "-f", "lavfi",
             "-i", f"aevalsrc='{espr}':s=44100:d={durata}",
             "-c:a", "pcm_s16le", str(percorso)])


def demo(wav, out, durata=DEMO_SEC, inizio_s=0.0, sfondo=None):
    """Dieci secondi con Dinamo in basso a sinistra, che dondola appena e
    parla sul wav: su fondo bruno, o sopra la foto `sfondo` se data.
    Stesse specifiche del reel. Accanto: foglio.png e 4 fotogrammi."""
    ff = _ff()
    wav, out = pathlib.Path(wav), pathlib.Path(out)
    if not wav.exists():
        wav_di_prova(wav, ff, durata)
        print(f"[dinamo] wav di prova generato: {wav}")
    lavoro = out.parent / "_dinamo"
    pattern = sequenza(wav, FPS, durata, inizio_s, lavoro, seme=1)
    if sfondo:
        fondo = ["-loop", "1", "-framerate", str(FPS), "-t", str(durata), "-i", str(sfondo)]
        base = "[0:v]scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1[b];"
    else:
        fondo = ["-f", "lavfi", "-i", f"color=c={gt.BRUNO}:s=720x1280:r={FPS}:d={durata}"]
        base = "[0:v]null[b];"
    filtro = (base + f"[1:v]format=rgba,scale={DEMO_LATO}:-2[d];"
              f"[b][d]overlay=x=40:y=H-h-290+4*sin(2*PI*t/2.6),format=yuv420p[o]")
    _esegui([ff, "-y", "-loglevel", "error", *fondo,
             "-framerate", str(FPS), "-i", pattern,
             "-i", str(wav),
             "-filter_complex", filtro, "-map", "[o]", "-map", "2:a",
             "-c:v", "libx264", "-profile:v", "main", "-pix_fmt", "yuv420p",
             "-g", str(FPS * 2), "-sc_threshold", "0", "-bf", "0",
             "-preset", "medium", "-crf", "20",
             "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2",
             "-t", str(durata), "-movflags", "+faststart", str(out)])
    print(f"[dinamo] demo: {out}")
    foglio(out.with_name("foglio.png"))
    # Quattro fotogrammi da GUARDARE: bocca chiusa, media, piena, e un
    # battito di ciglia.
    seq = [r.split() for r in (lavoro / "stati.txt").read_text().split("\n") if r]
    scelti = []
    for prova in (lambda r: r[1] == "0" and r[2] == "aperti", lambda r: r[1] == "2",
                  lambda r: r[1] == "4", lambda r: r[2] == "chiusi"):
        for r in seq:
            k = int(r[0])
            if k > inizio_s * FPS + FPS // 2 and prova(r) and k not in scelti:
                scelti.append(k)
                break
    for k in scelti:
        f = out.with_name(f"demo_f{k:05d}.png")
        # Si cerca mezzo fotogramma PRIMA: con -ss a k/FPS arrotondato in su
        # ffmpeg scarta il fotogramma k e consegna il k+1 (visto il 21/10).
        _esegui([ff, "-y", "-loglevel", "error", "-ss", f"{(k - 0.5) / FPS:.4f}", "-i", str(out),
                 "-frames:v", "1", str(f)])
        print(f"[dinamo] fotogramma {k} ({' '.join(seq[k][1:])}): {f}")
    return out


def main():
    if len(sys.argv) < 2:
        print("uso: python dinamo.py prova.wav [demo.mp4]")
        raise SystemExit(2)
    wav = pathlib.Path(sys.argv[1])
    out = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else wav.with_name("demo.mp4")
    demo(wav, out)


if __name__ == "__main__":
    main()
