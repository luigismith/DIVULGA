# -*- coding: utf-8 -*-
"""ELETTROFONI — la colonna sonora delle storie.

PERCHÉ ESISTE. Le storie erano immagini ferme, e una foto su Instagram
non ha audio: non era un guasto, era il formato. Per avere il suono la
storia deve diventare un video, e il suono dev'essere DENTRO al file —
l'API non permette di agganciare la musica del catalogo di Instagram.

REGOLA DEL PROGETTO: musica solo sintetizzata. Niente campioni, niente
brani, niente diritti da gestire. Qui non c'è nemmeno un file audio da
scaricare: le forme d'onda si calcolano.

L'IDEA. Un unico motivo, sempre lo stesso — è la sigla della pagina — ma
suonato ogni volta con il timbro della famiglia di macchine di cui parla
la scheda. Il DX7 lo fa in FM, l'Hammond a ruote foniche, la TB-303 col
filtro che spazza, la 808 a percussione. Chi segue la pagina riconosce
il motivo; chi guarda quella scheda sente di che macchina si parla.

Non usa numpy apposta: nessuna dipendenza nuova, solo la libreria
standard. Otto secondi di stereo a 44.1 kHz sono ~700.000 campioni,
calcolati in un paio di secondi — e si generano solo per la scheda del
giorno.
"""
import array
import math
import random
import struct
import wave

SR = 44100          # frequenza di campionamento
DURATA = 8.0        # secondi: quanto dura una storia guardata davvero
BPM = 96.0

# Il motivo: gradi di una scala minore, uno per movimento. È volutamente
# corto e un po' severo — siamo un catalogo, non una pubblicità.
SEMITONI = [0, 7, 3, 10, 0, 7, 3, 5]
BASE = 110.0        # LA2

# --------------------------------------------------------------- utilità ---

def _nota(semitoni, ottava=0):
    return BASE * (2 ** ((semitoni + 12 * ottava) / 12.0))


def _adsr(n, a=0.01, d=0.12, s=0.6, r=0.25):
    """Inviluppo campione per campione, in frazioni di durata."""
    att, dec, rel = int(n * a), int(n * d), int(n * r)
    sus = max(0, n - att - dec - rel)
    env = []
    for i in range(att):
        env.append(i / max(1, att))
    for i in range(dec):
        env.append(1.0 - (1.0 - s) * (i / max(1, dec)))
    env.extend([s] * sus)
    for i in range(rel):
        env.append(s * (1.0 - i / max(1, rel)))
    while len(env) < n:
        env.append(0.0)
    return env[:n]


def _passa_basso(campioni, taglio, risonanza=0.0):
    """Filtro a due poli, quel tanto che basta per sentire la differenza
    fra un synth e un'onda a dente di sega nuda."""
    out, y1, y2 = [], 0.0, 0.0
    for i, x in enumerate(campioni):
        f = taglio[i] if isinstance(taglio, list) else taglio
        f = max(30.0, min(f, SR * 0.45))
        c = 2.0 * math.sin(math.pi * f / SR)
        q = max(0.0, 1.0 - risonanza * 0.98)
        y1 += c * (x - y1 + (1.0 - q) * (y1 - y2) * 3.2)
        y2 += c * (y1 - y2)
        out.append(y2)
    return out


def _sat(x, quanto=1.6):
    return math.tanh(x * quanto) / math.tanh(quanto)


# ----------------------------------------------------------------- voci ---
# Ogni voce riceve la frequenza e la durata in campioni e restituisce
# una lista mono. Il carattere della macchina sta tutto qui dentro.

def voce_sega(f, n):
    """Sintetizzatore sottrattivo classico: dente di sega + filtro che
    si chiude. Minimoog, ARP 2600, MS-20."""
    fase, out = 0.0, []
    for i in range(n):
        fase = (fase + f / SR) % 1.0
        out.append(2.0 * fase - 1.0)
    taglio = [3000 * math.exp(-3.0 * i / n) + 180 for i in range(n)]
    filtrato = _passa_basso(out, taglio, risonanza=0.35)
    env = _adsr(n, 0.005, 0.2, 0.45, 0.35)
    return [_sat(s * e * 1.4) for s, e in zip(filtrato, env)]


def voce_acido(f, n):
    """TB-303: stessa sega, ma il filtro spazza e risuona. È il suono di
    una macchina usata al contrario di come dice il manuale."""
    fase, out = 0.0, []
    for i in range(n):
        fase = (fase + f / SR) % 1.0
        out.append(2.0 * fase - 1.0)
    taglio = [220 + 2600 * (0.5 + 0.5 * math.sin(2 * math.pi * i / n - 1.2))
              for i in range(n)]
    filtrato = _passa_basso(out, taglio, risonanza=0.62)
    env = _adsr(n, 0.002, 0.1, 0.7, 0.2)
    return [_sat(s * e * 1.15, 1.8) for s, e in zip(filtrato, env)]


def voce_fm(f, n):
    """DX7 e Fairlight: modulazione di frequenza, quel timbro vetroso da
    campanella che nessuno riusciva a programmare."""
    out = []
    for i in range(n):
        t = i / SR
        indice = 3.4 * math.exp(-4.0 * i / n)
        mod = math.sin(2 * math.pi * f * 2.0 * t) * indice
        out.append(math.sin(2 * math.pi * f * t + mod))
    env = _adsr(n, 0.002, 0.5, 0.18, 0.45)
    return [s * e for s, e in zip(out, env)]


def voce_organo(f, n):
    """Hammond e Farfisa: somma di armoniche, come le ruote foniche."""
    pesi = [(1, 1.0), (2, 0.55), (3, 0.35), (4, 0.22), (6, 0.16), (8, 0.1)]
    out = []
    for i in range(n):
        t = i / SR
        v = sum(p * math.sin(2 * math.pi * f * k * t) for k, p in pesi)
        out.append(v / 2.4)
    env = _adsr(n, 0.01, 0.05, 0.9, 0.12)
    return [_sat(s * e * 1.2) for s, e in zip(out, env)]


def voce_nastro(f, n):
    """Mellotron: tre voci scordate fra loro, con il pianto del nastro."""
    out = []
    for i in range(n):
        t = i / SR
        wow = 1.0 + 0.0035 * math.sin(2 * math.pi * 4.6 * t)
        v = (math.sin(2 * math.pi * f * wow * t)
             + 0.7 * math.sin(2 * math.pi * f * 1.004 * t)
             + 0.5 * math.sin(2 * math.pi * f * 0.995 * t))
        out.append(v / 2.2)
    env = _adsr(n, 0.06, 0.2, 0.75, 0.3)
    return [s * e for s, e in zip(out, env)]


def voce_onda(f, n):
    """Theremin, Ondes Martenot, Trautonium: una sinusoide che scivola da
    una nota all'altra e non sta mai ferma. Niente tasti, niente scatti."""
    out, fase, prec = [], 0.0, f * 0.84
    for i in range(n):
        t = i / SR
        gliss = prec + (f - prec) * min(1.0, i / (n * 0.35))
        vib = 1.0 + 0.012 * math.sin(2 * math.pi * 5.4 * t)
        fase = (fase + gliss * vib / SR) % 1.0
        out.append(math.sin(2 * math.pi * fase))
    env = _adsr(n, 0.14, 0.1, 0.85, 0.3)
    return [s * e for s, e in zip(out, env)]


def voce_giocattolo(f, n):
    """Stylophone: onda quadra e vibrato, tre soldi di elettronica."""
    out = []
    for i in range(n):
        t = i / SR
        vib = 1.0 + 0.02 * math.sin(2 * math.pi * 6.5 * t)
        out.append(1.0 if math.sin(2 * math.pi * f * vib * t) > 0 else -1.0)
    filtrato = _passa_basso(out, 2200.0)
    env = _adsr(n, 0.004, 0.1, 0.6, 0.25)
    return [s * e * 0.8 for s, e in zip(filtrato, env)]


def voce_studio(f, n):
    """Studio di Fonologia: onde pure e rumore, come uscivano dai
    generatori di Lietti prima di finire sotto la lametta."""
    rnd = random.Random(int(f))
    out = []
    for i in range(n):
        t = i / SR
        v = math.sin(2 * math.pi * f * t) + 0.5 * math.sin(2 * math.pi * f * 1.5 * t)
        if i > n * 0.7:
            v += 0.5 * (rnd.random() * 2 - 1)
        out.append(v / 1.8)
    env = _adsr(n, 0.002, 0.05, 0.8, 0.4)
    return [s * e for s, e in zip(out, env)]


VOCI = {
    "sega": voce_sega, "acido": voce_acido, "fm": voce_fm, "organo": voce_organo,
    "nastro": voce_nastro, "onda": voce_onda, "giocattolo": voce_giocattolo,
    "studio": voce_studio,
}

# Quale timbro per quale macchina. Le percussioni non sono una voce a sé:
# la 808 e la LM-1 hanno la batteria accesa e la voce tenuta bassa.
VOCE_SCHEDA = {
    "minimoog": "sega", "tr808": "sega", "theremin": "onda", "mellotron": "nastro",
    "dx7": "fm", "fairlight": "fm", "tb303": "acido", "hammond": "organo",
    "ondes": "onda", "arp2600": "sega", "vcs3": "studio", "farfisa": "organo",
    "trautonium": "onda", "fonologia": "studio", "stylophone": "giocattolo",
    "spaceecho": "sega", "ms20": "sega", "lm1": "sega",
}
CON_BATTERIA = {"tr808", "lm1", "tb303", "ms20", "spaceecho"}
CON_ECO = {"spaceecho", "vcs3", "fonologia", "theremin"}


# ------------------------------------------------------------ percussioni ---

def _batteria(n_tot, passo):
    """Cassa, rullante e charleston sintetizzati: la 808 li faceva così,
    con oscillatori e rumore, non con campioni."""
    rnd = random.Random(808)
    mix = [0.0] * n_tot
    def metti(inizio, campioni):
        for i, s in enumerate(campioni):
            j = inizio + i
            if 0 <= j < n_tot:
                mix[j] += s
    ncassa = int(SR * 0.28)
    cassa = [math.sin(2 * math.pi * (58 * math.exp(-9 * i / ncassa) + 34) * i / SR)
             * math.exp(-5.0 * i / ncassa) for i in range(ncassa)]
    nrull = int(SR * 0.16)
    rull = [((rnd.random() * 2 - 1) * 0.7 + math.sin(2 * math.pi * 190 * i / SR) * 0.5)
            * math.exp(-16.0 * i / nrull) for i in range(nrull)]
    nhat = int(SR * 0.05)
    hat = [(rnd.random() * 2 - 1) * math.exp(-45.0 * i / nhat) for i in range(nhat)]
    b = 0
    while b * passo < n_tot:
        if b % 4 in (0, 2):
            metti(b * passo, [s * 0.9 for s in cassa])
        if b % 4 == 2:
            metti(b * passo, [s * 0.5 for s in rull])
        metti(b * passo, [s * 0.28 for s in hat])
        metti(b * passo + passo // 2, [s * 0.18 for s in hat])
        b += 1
    return mix


def _eco(campioni, ritardo_s=0.375, ritorno=0.42):
    """L'eco a nastro: ogni ripetizione più bassa e più scura. Serve alla
    scheda dello Space Echo, e non solo a quella."""
    d = int(SR * ritardo_s)
    out = list(campioni)
    for i in range(d, len(out)):
        out[i] += out[i - d] * ritorno
    return out


# ------------------------------------------------------------------ mix ---

def genera(scheda, percorso_wav):
    """Scrive il WAV della sigla nel timbro della macchina della scheda."""
    slug = scheda["slug"] if isinstance(scheda, dict) else str(scheda)
    voce = VOCI[VOCE_SCHEDA.get(slug, "sega")]
    n_tot = int(SR * DURATA)
    passo = int(SR * 60.0 / BPM)          # un movimento
    n_nota = int(passo * 1.6)             # le note si sovrappongono un po'

    mix = [0.0] * n_tot
    for k in range(int(DURATA * BPM / 60.0)):
        gradi = SEMITONI[k % len(SEMITONI)]
        ott = 0 if k % 2 == 0 else 1
        campioni = voce(_nota(gradi, ott), n_nota)
        base = k * passo
        for i, s in enumerate(campioni):
            j = base + i
            if j < n_tot:
                mix[j] += s * 0.42

    # basso fisso sotto, per non lasciare il vuoto
    for i in range(n_tot):
        t = i / SR
        mix[i] += 0.16 * math.sin(2 * math.pi * (BASE / 2) * t) * min(1.0, i / (SR * 0.4))

    if slug in CON_BATTERIA:
        for i, s in enumerate(_batteria(n_tot, passo)):
            mix[i] += s * 0.55
    if slug in CON_ECO:
        mix = _eco(mix)

    # dissolvenze e normalizzazione: mai clip, mai partenze secche
    dis = int(SR * 0.25)
    for i in range(dis):
        mix[i] *= i / dis
        mix[n_tot - 1 - i] *= i / dis
    # LEZIONE IMPARATA (28/08/2026): normalizzare sul picco non basta.
    # La voce «acido» della TB-303, schiacciata dal filtro risonante,
    # usciva a -2,4 dB di media contro i -11 di tutte le altre: stesso
    # picco, volume percepito triplo. Su Instagram si sarebbe sentito uno
    # sbalzo di volume da una storia all'altra. Si normalizza sull'RMS —
    # quanto SUONA forte — e il picco fa solo da tetto anti-clip.
    picco = max(1e-6, max(abs(s) for s in mix))
    rms = math.sqrt(sum(s * s for s in mix) / max(1, len(mix))) or 1e-6
    guad = 0.18 / rms                      # circa -15 dBFS, uguale per tutte
    guad = min(guad, 0.95 / picco)         # ma senza mai toccare il tetto

    dati = array.array("h")
    for s in mix:
        v = int(max(-1.0, min(1.0, s * guad)) * 32767)
        dati.append(v)      # sinistra
        dati.append(v)      # destra (mono su due canali: l'audio è una sigla)

    with wave.open(str(percorso_wav), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(dati.tobytes())
    return percorso_wav


if __name__ == "__main__":
    import sys, pathlib
    slug = sys.argv[1] if len(sys.argv) > 1 else "dx7"
    out = pathlib.Path(f"/tmp/{slug}.wav")
    genera({"slug": slug}, out)
    print(f"[suoni] {slug}: {out} ({out.stat().st_size} byte, {DURATA}s, voce {VOCE_SCHEDA.get(slug)})")
