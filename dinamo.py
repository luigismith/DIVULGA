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

COME FUNZIONA. Sei sprite PNG con alfa (3 bocche × 2 occhi), resi UNA
volta con Chromium e tenuti in una cartella cache. Per ogni fotogramma
del video si sceglie uno dei sei e si scrive un link simbolico
f_00000.png, f_00001.png… allo sprite giusto: ffmpeg legge la cartella
con «-framerate FPS -i f_%05d.png» e la sovrappone al reel con `overlay`.
Niente Pillow, niente 900 copie dello stesso file: 900 link, che pesano
zero. La bocca si decide sull'RMS della voce a finestre di 1/FPS secondi,
normalizzato sul 95° percentile e con isteresi, così non sfarfalla.

DAL MONTAGGIO (genera_reel.py o chi per lui):

    import dinamo
    pattern = dinamo.sequenza(wav_voce, FPS, durata_s, inizio_s, lavoro / "dinamo")
    # poi, fra gli input di ffmpeg:  "-framerate", str(FPS), "-i", pattern
    # e nel filtro:  [k:v]format=rgba,scale=300:300[d];[base][d]overlay=x=40:y=H-h-120+6*sin(2*PI*t/2.6)[o]

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

LATO = 320                       # lato dello sprite, in px
SCALA = 1.55                     # viewBox 200 -> sprite: l'automa riempie il tondo con margine
BOCCHE = ("chiusa", "mezza", "aperta")
OCCHI = ("aperti", "chiusi")
SPRITE = {(b, o): f"sprite_{b}_{o}.png" for b in BOCCHE for o in OCCHI}

# Soglie sull'inviluppo (0..1) con isteresi: per salire serve più volume
# che per scendere, così un valore che balla intorno alla soglia non fa
# battere la griglia. TENUTA_MIN: uno stato dura almeno 3 fotogrammi
# (100 ms a 30 fps). Misurato il 21/10/2026 su una voce Piper di 23 s:
# con 2 fotogrammi la bocca cambiava 5,9 volte al secondo e 56 stati su
# 139 duravano 67 ms (sfarfallio); con 3 cambia 5,3 volte al secondo,
# circa una per sillaba, e nessuno stato dura meno di 100 ms. Smussare
# di più (5-9 fotogrammi) la porta a 2-4 cambi al secondo con la bocca
# aperta il 60% del tempo: sembra incantata, non parlante.
SU_MEZZA, GIU_MEZZA = 0.15, 0.10
SU_APERTA, GIU_APERTA = 0.50, 0.40
TENUTA_MIN = 3
# Battito di ciglia: il primo presto (uno sguardo fisso di 5 s si nota),
# poi uno ogni 3-5 s, 4 fotogrammi l'uno.
BATTITO_PRIMO = (1.5, 3.5)
BATTITO_OGNI = (3.0, 5.0)
BATTITO_FOTOGRAMMI = 4

FPS = 30
DEMO_SEC = 10.0
DEMO_LATO = 300


# ------------------------------------------------------------- disegno ---

def _corpo():
    """Testa, antenna e orecchie presi da AUTOMA_SVG così come sono: una
    fonte sola per l'identità. Si tolgono occhi (cy=80) e bocca (y1=106),
    che qui cambiano; se AUTOMA_SVG cambia forma il conto non torna e ci
    si ferma, invece di disegnare due bocche senza dirlo."""
    svg = gt.AUTOMA_SVG
    dentro = svg[svg.index(">") + 1:svg.rindex("</svg>")]
    righe = [r.strip() for r in dentro.strip().splitlines() if r.strip()]
    occhi = [r for r in righe if 'cy="80"' in r]
    bocca = [r for r in righe if 'y1="106"' in r]
    if len(occhi) != 4 or len(bocca) != 4:
        raise RuntimeError("AUTOMA_SVG è cambiato (occhi/bocca non trovati): aggiornare dinamo.py")
    return [r for r in righe if r not in occhi and r not in bocca]


def _occhi(stato):
    if stato == "aperti":            # cerchio con pupilla, come sulle tavole
        return ['<circle cx="80" cy="80" r="14" stroke-width="7" stroke="{o}"/>',
                '<circle cx="120" cy="80" r="14" stroke-width="7" stroke="{o}"/>',
                '<circle cx="80" cy="80" r="4" fill="{o}" stroke="none"/>',
                '<circle cx="120" cy="80" r="4" fill="{o}" stroke="none"/>']
    return ['<line x1="66" y1="80" x2="94" y2="80" stroke-width="7" stroke-linecap="round" stroke="{o}"/>',
            '<line x1="106" y1="80" x2="134" y2="80" stroke-width="7" stroke-linecap="round" stroke="{o}"/>']


def _bocca(stato):
    """La griglia da altoparlante. Chiusa: lineette corte e basse. Mezza:
    com'è sulle tavole (106-120). Aperta: lineette lunghe dentro un
    rettangolo arrotondato aperto, l'altoparlante che si accende; il
    rettangolo resta 3 px dentro il bordo della testa."""
    if stato == "chiusa":
        y1, y2, cornice = 112, 118, ""
    elif stato == "mezza":
        y1, y2, cornice = 106, 120, ""
    else:
        y1, y2 = 99, 117
        cornice = '<rect x="62" y="92" width="76" height="32" rx="9" stroke-width="5"/>'
    righe = [cornice] if cornice else []
    righe += [f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke-width="6" stroke-linecap="round"/>'
              for x in (79, 93, 107, 121)]
    return righe


def svg_sprite(bocca, occhi, lato=LATO):
    """Il timbro: tondo crema con bordo bruno di 6 px, dentro Dinamo
    arancio con gli occhi bruni. Fondo trasparente, così si stacca da
    qualunque foto."""
    if bocca not in BOCCHE or occhi not in OCCHI:
        raise ValueError(f"stato sconosciuto: {bocca}/{occhi}")
    s = SCALA * lato / LATO
    # il centro ottico dell'automa sta a (100, 76): la testa, non l'antenna
    tx, ty = lato / 2 - 100 * s, lato / 2 - 76 * s
    r = lato / 2 - 4                 # il bordo da 6 px non tocca il margine
    dentro = "\n    ".join(_corpo() + _occhi(occhi) + _bocca(bocca))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {lato} {lato}" '
            f'width="{lato}" height="{lato}">\n'
            f'  <circle cx="{lato / 2}" cy="{lato / 2}" r="{r}" fill="{gt.CREMA}" '
            f'stroke="{gt.BRUNO}" stroke-width="6"/>\n'
            f'  <g transform="translate({tx:.2f} {ty:.2f}) scale({s:.4f})" fill="none" stroke="{{c}}">\n'
            f'    {dentro}\n  </g>\n</svg>').format(c=gt.ARANCIO, o=gt.BRUNO)


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


def rendi_sprite(cache, forza=False):
    """I sei PNG in `cache`, resi solo se mancano. Torna {(bocca, occhi): Path}."""
    cache = pathlib.Path(cache)
    cache.mkdir(parents=True, exist_ok=True)
    file = {st: cache / nome for st, nome in SPRITE.items()}
    mancanti = [st for st, f in file.items() if forza or not f.exists()]
    if mancanti:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = _browser(p)
            page = b.new_page(viewport={"width": LATO, "height": LATO})
            for st in mancanti:
                _scatta(page, _pagina(svg_sprite(*st), LATO, LATO), file[st], LATO, LATO,
                        omit_background=True)
            b.close()
        print(f"[dinamo] resi {len(mancanti)} sprite in {cache}")
    return file


def foglio(cache, out):
    """Un PNG con i sei sprite affiancati su fondo crema, per guardarli."""
    file = rendi_sprite(cache)
    passo, bordo = LATO + 20, 20
    celle = "".join(
        f'<div class="c"><img src="{f.resolve().as_uri()}"><div class="e">{b} / {o}</div></div>'
        for (b, o), f in file.items())
    larg, alt = 6 * passo - 20 + 2 * bordo, LATO + 70 + 2 * bordo
    css = (f".f{{display:flex;gap:20px;padding:{bordo}px}}.c{{width:{LATO}px}}img{{display:block;width:{LATO}px}}"
           f".e{{font-family:'PlexMono';font-weight:600;font-size:18px;letter-spacing:.14em;"
           f"color:{gt.BRUNO};text-align:center;margin-top:20px}}")
    from playwright.sync_api import sync_playwright
    out = pathlib.Path(out)
    with sync_playwright() as p:
        b = _browser(p)
        page = b.new_page(viewport={"width": larg, "height": alt})
        _scatta(page, _pagina(f'<div class="f">{celle}</div>', larg, alt, gt.CREMA, css), out, larg, alt)
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


def _prossima_bocca(stato, v):
    if stato == "chiusa":
        return "aperta" if v >= SU_APERTA else "mezza" if v >= SU_MEZZA else "chiusa"
    if stato == "mezza":
        return "aperta" if v >= SU_APERTA else "chiusa" if v < GIU_MEZZA else "mezza"
    return "chiusa" if v < GIU_MEZZA else "mezza" if v < GIU_APERTA else "aperta"


def stati(inviluppo, fps, inizio_s, n_fotogrammi, seme=0):
    """Per ogni fotogramma del video (bocca, occhi). La voce comincia a
    `inizio_s`: prima, e dopo la fine dell'inviluppo, bocca chiusa. I
    battiti di ciglia dipendono solo dal seme: stessa scheda, stesso
    video, due volte."""
    scarto = int(round(inizio_s * fps))
    bocca, stato, tenuta = [], "chiusa", TENUTA_MIN
    for k in range(n_fotogrammi):
        j = k - scarto
        v = inviluppo[j] if 0 <= j < len(inviluppo) else 0.0
        nuovo = _prossima_bocca(stato, v)
        if nuovo != stato and tenuta >= TENUTA_MIN:
            stato, tenuta = nuovo, 1
        else:
            tenuta += 1
        bocca.append(stato)
    occhi = ["aperti"] * n_fotogrammi
    rng = random.Random(seme)
    t = rng.uniform(*BATTITO_PRIMO)
    while t * fps < n_fotogrammi:
        k0 = int(round(t * fps))
        for k in range(k0, min(k0 + BATTITO_FOTOGRAMMI, n_fotogrammi)):
            occhi[k] = "chiusi"
        t += rng.uniform(*BATTITO_OGNI)
    return list(zip(bocca, occhi))


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
    ffmpeg («…/f_%05d.png»). Il seme dei battiti, se non dato, viene dal
    nome del wav: deterministico, ma diverso da scheda a scheda."""
    cartella = pathlib.Path(cartella)
    cartella.mkdir(parents=True, exist_ok=True)
    # I resti di una sequenza più lunga vanno tolti: ffmpeg legge la
    # numerazione finché è continua, e si prenderebbe anche quelli.
    for vecchio in cartella.glob("f_*.png"):
        vecchio.unlink()
    sprite = rendi_sprite(cache or cartella / "sprite")
    n = int(round(durata_s * fps))
    if seme is None:
        seme = zlib.crc32(pathlib.Path(wav_voce).name.encode("utf-8"))
    env = inviluppo(wav_voce, fps)
    if not any(v >= SU_MEZZA for v in env):
        # Un wav muto passato come voce è un errore a monte: con un
        # Dinamo a bocca chiusa per tutto il reel non se ne accorgerebbe
        # nessuno (vedi CLAUDE.md, «un ripiego che non lascia traccia»).
        raise RuntimeError(f"{wav_voce}: nessun suono sopra la soglia, non è una voce")
    seq = stati(env, fps, inizio_s, n, seme)
    modo = "link simbolici"
    for k, st in enumerate(seq):
        modo = _collega(sprite[st].resolve(), cartella / f"f_{k:05d}.png")
    (cartella / "stati.txt").write_text(
        "".join(f"{k:05d} {b} {o}\n" for k, (b, o) in enumerate(seq)), encoding="utf-8")
    conta = {b: sum(1 for x, _ in seq if x == b) for b in BOCCHE}
    battiti = sum(1 for k in range(1, n) if seq[k][1] == "chiusi" and seq[k - 1][1] == "aperti")
    print(f"[dinamo] {n} fotogrammi a {fps} fps ({modo}): bocca "
          + ", ".join(f"{b} {100 * c // max(n, 1)}%" for b, c in conta.items())
          + f"; {battiti} battiti di ciglia; voce da {inizio_s:.2f} s")
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


def demo(wav, out, durata=DEMO_SEC, inizio_s=0.0):
    """Dieci secondi su fondo bruno con Dinamo in basso a sinistra, che
    dondola appena e parla sul wav. Stesse specifiche del reel."""
    ff = _ff()
    wav, out = pathlib.Path(wav), pathlib.Path(out)
    if not wav.exists():
        wav_di_prova(wav, ff, durata)
        print(f"[dinamo] wav di prova generato: {wav}")
    lavoro = out.parent / "_dinamo"
    pattern = sequenza(wav, FPS, durata, inizio_s, lavoro, seme=1)
    filtro = (f"[1:v]format=rgba,scale={DEMO_LATO}:{DEMO_LATO}[d];"
              f"[0:v][d]overlay=x=40:y=H-h-120+6*sin(2*PI*t/2.6),format=yuv420p[o]")
    _esegui([ff, "-y", "-loglevel", "error",
             "-f", "lavfi", "-i", f"color=c={gt.BRUNO}:s=720x1280:r={FPS}:d={durata}",
             "-framerate", str(FPS), "-i", pattern,
             "-i", str(wav),
             "-filter_complex", filtro, "-map", "[o]", "-map", "2:a",
             "-c:v", "libx264", "-profile:v", "main", "-pix_fmt", "yuv420p",
             "-g", str(FPS * 2), "-sc_threshold", "0", "-bf", "0",
             "-preset", "medium", "-crf", "20",
             "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2",
             "-t", str(durata), "-movflags", "+faststart", str(out)])
    print(f"[dinamo] demo: {out}")
    foglio(lavoro / "sprite", out.with_name("foglio.png"))
    # Quattro fotogrammi da GUARDARE: uno per bocca (a occhi aperti, dopo
    # che la voce è partita) e uno a occhi chiusi.
    righe = (lavoro / "stati.txt").read_text().split("\n")
    seq = [r.split() for r in righe if r]
    scelti = []
    for cerca in (("chiusa", "aperti"), ("mezza", "aperti"), ("aperta", "aperti"), (None, "chiusi")):
        for k, b, o in seq:
            k = int(k)
            if k > inizio_s * FPS + FPS // 2 and (cerca[0] in (None, b)) and o == cerca[1] and k not in scelti:
                scelti.append(k)
                break
    for k in scelti:
        b, o = seq[k][1:]
        f = out.with_name(f"demo_f{k:05d}_{b}_{o}.png")
        # Si cerca mezzo fotogramma PRIMA: con -ss a k/FPS arrotondato in su
        # ffmpeg scarta il fotogramma k e consegna il k+1 (visto il 21/10).
        _esegui([ff, "-y", "-loglevel", "error", "-ss", f"{(k - 0.5) / FPS:.4f}", "-i", str(out),
                 "-frames:v", "1", str(f)])
        print(f"[dinamo] fotogramma {k} ({b}/{o}): {f}")
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
