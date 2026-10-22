# -*- coding: utf-8 -*-
"""ELETTROFONI — la voce di Dinamo.

PERCHÉ. Il proprietario ha chiesto un reel PARLATO: Dinamo, l'automa che
compila il catalogo, racconta la scheda mentre le scene scorrono. I
vincoli sono i soliti della pagina: strumenti gratuiti, tutto automatico
su un runner ubuntu-latest (4 CPU, niente GPU, niente apt), e lui non
deve fare niente. Dinamo è un automa: una voce un po' meccanica è il
personaggio; una voce che finge di essere umana e non ci riesce no.

COME SI È SCELTO (21/10/2026, misure in scratchpad/parlante). Due motori
open source su CPU con sola pip, quattro voci italiane, la stessa frase
di prova piena di nomi e sigle della pagina (Casio CZ-101, DX7, Vince
Clarke, Kuzmin, Ekaterinburg, Murzin, Skrjabin…). Nessuno qui può
ascoltare: si è misurato quanto ogni voce si capisce facendola
ritrascrivere da faster-whisper (modello medium, int8) e contando le
parole sbagliate (WER) sul testo atteso.
  · Kokoro-82M, voce if_sara:   WER 0,150   0,4-0,6 s di calcolo per s di audio
  · Kokoro-82M, voce im_nicola: WER 0,217   0,5 s/s
  · Piper it_IT-riccardo-x_low: WER 0,267   0,03 s/s  (16 kHz)
  · Piper it_IT-paola-medium:   WER 0,383   0,13 s/s  (22 kHz)
Col lessico di qui sotto if_sara scende a 0,133 senza nomi persi; whisper
medium ritrascrive 30 s in 22-25 s (il tetto era 60).
Piper è dieci volte più leggero (90 MB contro 1,5 GB di torch) e cento
volte più veloce, ma su una pagina che vive di nomi propri la metà degli
errori in più non si compra con i megabyte: Kokoro if_sara sbaglia solo
grafie che Whisper non può sapere (Clark/Clarke, Evgeny/Evgenij). Il
criterio 1 era l'intelligibilità, e lo decide lei.

COSA SERVE. `pip install kokoro soundfile faster-whisper` più torch CPU
(`--index-url https://download.pytorch.org/whl/cpu`, altrimenti pip
scarica 2 GB di CUDA inutili). espeak-ng arriva da pip con
`espeakng-loader`: niente apt. ATTENZIONE, provato: la libespeak-ng
dentro espeakng-loader 0.2.4 ignora la cartella dati che riceve e cerca
quella compilata dentro il wheel (`/home/runner/work/…`), che sul nostro
computer non esiste, e il processo MUORE (exit dalla C, nessuna
eccezione). Vuole una cartella che contenga sia `espeak-ng-data` sia i
suoi file: `_cartella_espeak()` la costruisce coi link simbolici nella
cache. Senza, Kokoro non parla italiano.

LICENZE. Kokoro-82M è Apache 2.0 (modello e voci), usabile per una
pagina pubblica senza condizioni. (Piper: repo MIT, voce paola su
dataset CC0; riccardo su M-AILABS, licenza «see URL» con URL che non
risponde: un'altra ragione per non sceglierlo.)

COSA FA. `normalizza` porta sigle e numeri in lettere (il motore legge
«CZ-101» come gli pare, «ci zeta cento uno» lo legge giusto; i nomi che
storpia si riscrivono come si pronunciano, con l'accento); `sintetizza`
produce il wav (mono, 24 kHz, livello normalizzato); `verifica` ri-
trascrive il wav con faster-whisper e dice se Dinamo ha storpiato un
nome: è il controllo che FERMA un reel, perché un nome sbagliato in voce
è peggio di un nome sbagliato scritto. Vedi le soglie accanto a
`SOGLIA_WER` e `SOGLIA_NOME`.

    python voce.py "Il DX7 di Yamaha costa 2.000 dollari."   # prova.wav
    python voce.py                                            # frase di prova
"""
import difflib
import json
import os
import pathlib
import re
import sys
import time
import unicodedata
import wave

import numpy as np

MOTORE = "kokoro"            # hexgrad/Kokoro-82M, Apache 2.0
VOCE = os.environ.get("ELETTROFONI_VOCE", "if_sara")   # if_sara: WER 0,150; im_nicola: 0,217
REPO_MODELLO = "hexgrad/Kokoro-82M"
FILE_MODELLO = "kokoro-v1_0.pth"
SR = 24000                   # Kokoro esce a 24 kHz mono
CACHE = pathlib.Path(os.environ.get("ELETTROFONI_CACHE_VOCE",
                                    "~/.cache/elettrofoni/voce")).expanduser()
MODELLO_WHISPER = "medium"   # int8 su 4 CPU: ~0,9 s per s di audio, 30 s di audio in meno di 60 s
PAUSA_FRASE = 0.30           # secondi di silenzio fra una frase e l'altra
RMS_DBFS = -18.0             # livello d'uscita; con -1 dBFS di picco massimo
PICCO_DBFS = -1.0

# SOGLIE DI `verifica`. Il WER misura anche gli errori di Whisper, non
# solo quelli della voce: sulla frase di prova (sei nomi stranieri in 57
# parole) la voce scelta fa 0,13, e su una frase con tredici nomi inglesi
# e russi 0,29, quasi tutto grafie (Prophet V, Harp 2600, Tarkovsky). Il
# WER è la rete di fondo contro una sintesi rotta o troncata (Kokoro
# tronca oltre ~500 fonemi: per questo `_frasi` spezza il testo): sopra
# 0,40 il reel non esce. Il controllo fine è quello dei nomi, sotto.
SOGLIA_WER = 0.40
# Un nome proprio è «mancante» se nessuna parola della trascrizione gli
# somiglia almeno per il 60% (rapporto di difflib): Katerinburg contro
# Ekaterinburg 0,92 e Skjabin/Skrjabin 0,93 passano, Azzurri/Erasure
# 0,43 e Kutsvine/Kuzmin 0,57 no. Un nome mancante ferma il reel da solo.
SOGLIA_NOME = 0.60

# ------------------------------------------------------------- lessico ---

# Le sigle della pagina, lette come le dice chi le usa. La chiave si
# scrive con il trattino dove c'è di solito; `normalizza` accetta anche
# la forma senza trattino o con lo spazio (CZ101, CZ 101).
LESSICO = {
    "CZ-101": "ci zeta centouno",
    "CZ-1000": "ci zeta mille",
    "DX7": "di ics sette",
    "DX7II": "di ics sette secondo",
    "DX100": "di ics cento",
    "TR-808": "ti erre ottocentotto",
    "TR-909": "ti erre novecentonove",
    "TR-606": "ti erre seicentosei",
    "TB-303": "ti bi trecentotré",
    "SH-101": "esse acca centouno",
    "MS-20": "emme esse venti",
    "M1": "emme uno",
    "D-50": "di cinquanta",
    "D-05": "di zero cinque",
    "JD-800": "gei di ottocento",
    "MC-202": "emme ci duecentodue",
    "MC-8": "emme ci otto",
    "MC-303": "emme ci trecentotré",
    "VCS3": "vu ci esse tre",
    "CS-80": "ci esse ottanta",
    "LM-1": "elle emme uno",
    "OB-Xa": "o bi ics a",
    "OB-X": "o bi ics",
    "Juno-106": "Juno centosei",
    "Juno-60": "Juno sessanta",
    "Jupiter-8": "Jupiter otto",
    "Jupiter-4": "Jupiter quattro",
    "ARP 2600": "arp duemilaseicento",
    "Minimoog": "Minimùg",
    "Moog": "Mùg",
    "Prophet-5": "Pròfet cinque",
    "PPG Wave": "pi pi gi uèiv",
    "H910": "acca novecentodieci",
    "VP-330": "vu pi trecentotrenta",
    "Synthi AKS": "Sìnti a kappa esse",
    "ANS": "a enne esse",
    "SP-1200": "esse pi milleduecento",
    "MPC60": "emme pi ci sessanta",
    "VL-1": "vu elle uno",
    "DS-2": "di esse due",
    "EP-3": "e pi tre",
    "OM-27": "o emme ventisette",
    "B-3": "bi tre",
    "C3": "ci tre",
    "TMS5100": "ti emme esse cinquemilacento",
    "SSM2045": "esse esse emme duemilaquarantacinque",
    "OP-1": "o pi uno",
    "A-100": "a cento",
    "CMI": "ci emme i",
    "DCO": "di ci o",
    "VCO": "vu ci o",
    "LFO": "elle effe o",
    "ADSR": "a di esse erre",
    "EMS": "e emme esse",
    "URSS": "u erre esse esse",
    "UK": "u kappa",
    "USA": "usa",
    "DJ": "di gei",
    "TV": "tivù",
    "MIDI": "midi",
    "RAI": "rai",
    "NAMM": "namm",
    "ARP": "arp",
    "ROM": "rom",
    "SEM": "sem",
    "Eurorack": "Iuroràc",
    "Wavestation": "Uèivsteiscion",
    "Nord Lead": "Nord Lid",
    "Auto-Tune": "Òtotiun",
    "Machinedrum": "Mascìndram",
    "Volca": "Volca",
    "Clavinet": "Clàvinet",
    "Rhodes": "Ròuds",
    "Wurlitzer": "Vùrlitser",
    "Mellotron": "Mèllotron",
    "Hammond": "Hàmmond",
    "Fairlight": "Fèrlait",
    "Omnichord": "Omnicòrd",
    "Optigan": "Òptigan",
    "Speak & Spell": "Spic end Spel",
    "Space Echo": "Spèis Eco",
    "Farfisa": "Farfìsa",
    "Synthex": "Sìntecs",
    "Synket": "Sìnchet",
    "Telharmonium": "Telarmònium",
    "II": "due",
    "III": "tre",
    "synth": "sint",
    "slide": "slaid",       # espeak-ng legge «zlìde»; così zlˈaɪd, e Whisper scrive «slide»
    "sampler": "sèmpler",
    "sequencer": "sìcuenser",
    "drum machine": "dram mascìn",
}

# Nomi propri che il motore storpia, riscritti come si pronunciano. Le
# vocali accentate portano l'accento tonico (espeak-ng in italiano le
# legge così). Si aggiunge una voce SOLO dopo averla provata con
# `verifica`: una riscrittura a orecchio può peggiorare la lettura.
NOMI = {
    "Kuzmin": "Kùsmin",              # da solo: «Kuzmina e Katerinburg»; così: «Kuzmin a Yekaterinburg»
    "Skrjabin": "Skriàbin",          # sentito «Skriabin»; da solo «Skjabin»
    "Ekaterinburg": "Iekaterinbùrg",
    "Evgenij": "Evghèni",            # sentito «Evgeny», come da solo: tiene il suono «gh»
    "Tarkovskij": "Tarkòvski",
    "Clarke": "Clark",
    # NON riscrivere: Erasure (da solo si capisce, «Irèisciur» diventa «E-Ration»),
    # Murzin (da solo esatto, «Mùrsin» diventa «Mursin»).
    "Buchla": "Bùcla",
    "Easel": "Ìsel",
    "Leslie": "Lèsli",
    "Circuits": "Sèrchits",
    "Yamaha": "Iamàha",
    "Korg": "Korg",
    "Roland": "Ròland",
    # Aggiunti il 21/10/2026 per i testi di Omnichord, JD-800 e D-50
    # (grafie provate con espeak-ng dai verificatori dello stile).
    "Deep Blue Day": "Dip Blu Dèi",
    "Lanois": "Lanuà",
    "Prince": "Prins",
    "Damn U": "Dam iu",
    "Watermark": "Uòtermark",
    "Persing": "Pèrsing",
    "Orinoco Flow": "Orinoco Flòu",
    "Casio": "Càsio",
    "Vince": "Vins",
    # NON riscrivere Depeche Mode: da solo si capisce, «Depèsc Mod» diventa «The Pesce Mod».
    "Kraftwerk": "Kràftverk",
    "Vangelis": "Vanghèlis",
    "Stevie Wonder": "Stìvi Uònder",
    "Herbie Hancock": "Hèrbi Hàncoc",
    "Bob Moog": "Bob Mùg",
    "Oberheim": "Òberhaim",
    "Sequential": "Sicuènscial",
    "Dave Smith": "Dèiv Smit",
    "Ketoff": "Kètof",
    "Termen": "Tèrmen",
    "Theremin": "Tèremin",
    "theremin": "tèremin",
}

# Unità dopo un numero (3 V, 24 dB, 44,1 kHz, 8 bit, 100.000 dollari…)
UNITA = {
    "kHz": "chilohertz", "Hz": "hertz", "MHz": "megahertz", "dB": "decibel",
    "V": "volt", "mV": "millivolt", "W": "watt", "kW": "chilowatt",
    "mm": "millimetri", "cm": "centimetri", "m": "metri", "km": "chilometri",
    "kg": "chili", "g": "grammi", "ms": "millisecondi", "s": "secondi",
    "KB": "chilobyte", "kB": "chilobyte", "MB": "megabyte", "GB": "gigabyte",
    "bit": "bit", "%": "per cento", "°": "gradi",
}
VALUTE = {"$": "dollari", "€": "euro", "£": "sterline", "¥": "yen"}

LETTERE = {"a": "a", "b": "bi", "c": "ci", "d": "di", "e": "e", "f": "effe", "g": "gi",
           "h": "acca", "i": "i", "j": "i lunga", "k": "kappa", "l": "elle", "m": "emme",
           "n": "enne", "o": "o", "p": "pi", "q": "cu", "r": "erre", "s": "esse", "t": "ti",
           "u": "u", "v": "vu", "w": "doppia vu", "x": "ics", "y": "ipsilon", "z": "zeta"}

UNITA_NUM = ["", "uno", "due", "tre", "quattro", "cinque", "sei", "sette", "otto", "nove",
             "dieci", "undici", "dodici", "tredici", "quattordici", "quindici", "sedici",
             "diciassette", "diciotto", "diciannove"]
DECINE = ["", "", "venti", "trenta", "quaranta", "cinquanta", "sessanta", "settanta",
          "ottanta", "novanta"]


def numero_in_lettere(n):
    """495 → quattrocentonovantacinque, 1984 → millenovecentottantaquattro."""
    n = int(n)
    if n < 0:
        return "meno " + numero_in_lettere(-n)
    if n < 20:
        return UNITA_NUM[n] if n else "zero"
    if n < 100:
        d, u = divmod(n, 10)
        base = DECINE[d]
        if u in (1, 8):            # ventuno, ventotto: cade la vocale
            base = base[:-1]
        parola = base + UNITA_NUM[u]
        return parola[:-1] + "é" if u == 3 else parola   # ventitré
    if n < 1000:
        c, r = divmod(n, 100)
        testa = "cento" if c == 1 else UNITA_NUM[c] + "cento"
        if 80 <= r < 90:           # centottanta
            testa = testa[:-1]
        return testa + (numero_in_lettere(r) if r else "")
    if n < 1_000_000:
        m, r = divmod(n, 1000)
        testa = "mille" if m == 1 else numero_in_lettere(m) + "mila"
        return testa + (numero_in_lettere(r) if r else "")
    if n < 1_000_000_000:
        M, r = divmod(n, 1_000_000)
        testa = "un milione" if M == 1 else numero_in_lettere(M) + " milioni"
        return testa + (" " + numero_in_lettere(r) if r else "")
    G, r = divmod(n, 1_000_000_000)
    testa = "un miliardo" if G == 1 else numero_in_lettere(G) + " miliardi"
    return testa + (" " + numero_in_lettere(r) if r else "")


def _sigla_in_lettere(sigla):
    """DMX → di emme ics; SSM2045 → esse esse emme duemilaquarantacinque."""
    pezzi = []
    for p in re.findall(r"[A-Za-z]+|\d+", sigla):
        if p.isdigit():
            pezzi.append(numero_in_lettere(int(p)))
        else:
            pezzi.extend(LETTERE[c] for c in p.lower())
    return " ".join(pezzi)


def _regex_sigla(chiave):
    """«CZ-101» → regex che prende anche CZ101 e CZ 101."""
    pezzi = re.findall(r"[A-Za-z]+|\d+|[^A-Za-z\d]+", chiave)
    out = []
    for p in pezzi:
        if re.fullmatch(r"[-\s]+", p):
            out.append(r"[-\s]?")
        else:
            out.append(re.escape(p))
    return r"(?<![A-Za-z\d])" + "".join(out) + r"(?![A-Za-z\d])"


_RE_LESSICO = [(re.compile(_regex_sigla(k)), v)
               for k, v in sorted(LESSICO.items(), key=lambda kv: -len(kv[0]))]
_RE_NOMI = [(re.compile(r"(?<![A-Za-z])" + re.escape(k) + r"(?![A-Za-z])"), v)
            for k, v in sorted(NOMI.items(), key=lambda kv: -len(kv[0]))]
_RE_UNITA = re.compile(r"(\d)\s*(" + "|".join(re.escape(u) for u in
                       sorted(UNITA, key=len, reverse=True)) + r")(?![A-Za-z])")


def _decimale(m):
    intero, dec = m.group(1), m.group(2)
    return numero_in_lettere(int(intero)) + " virgola " + " ".join(
        numero_in_lettere(int(c)) for c in dec)


def normalizza(testo):
    """Il testo come lo deve leggere il motore: sigle, nomi, numeri in lettere.

    L'ordine conta: prima le sigle del lessico (che contengono numeri),
    poi i nomi, poi valute e unità (che stanno attaccate ai numeri), poi
    i numeri stessi, e per ultime le sigle sconosciute lettera per
    lettera.
    """
    t = unicodedata.normalize("NFC", testo)
    t = t.replace("’", "'").replace("‑", "-").replace("–", "-").replace("—", ", ")
    for rx, letto in _RE_LESSICO:
        t = rx.sub(letto, t)
    for rx, letto in _RE_NOMI:
        t = rx.sub(letto, t)
    # decenni: anni '70, '80, anni 80 → anni settanta
    t = re.sub(r"(?i)\banni\s+'?(\d)0\b", lambda m: "anni " + DECINE[int(m.group(1))], t)
    t = re.sub(r"'(\d)0\b", lambda m: DECINE[int(m.group(1))], t)
    t = re.sub(r"'(\d\d)\b", lambda m: numero_in_lettere(int(m.group(1))), t)
    # separatore delle migliaia all'italiana: 1.200, 3.475.623
    t = re.sub(r"\b\d{1,3}(?:\.\d{3})+\b", lambda m: m.group(0).replace(".", ""), t)
    # valute prima del numero ($495) e dopo (495 $)
    for simbolo, nome in VALUTE.items():
        t = re.sub(re.escape(simbolo) + r"\s*(\d+(?:,\d+)?)", r"\1 " + nome, t)
        t = re.sub(r"(\d+(?:,\d+)?)\s*" + re.escape(simbolo), r"\1 " + nome, t)
    # ordinali: 1º, 2° (PRIMA delle unità: «°» è anche il grado, e la
    # regola delle unità li trasformava in «1 gradi»; trovato dal collaudo)
    t = re.sub(r"\b1[º°](?!\w)", "primo", t)
    t = re.sub(r"\b2[º°](?!\w)", "secondo", t)
    t = re.sub(r"\b3[º°](?!\w)", "terzo", t)
    t = _RE_UNITA.sub(lambda m: m.group(1) + " " + UNITA[m.group(2)], t)
    # intervalli e date con il trattino: 1983-84 → 1983 84
    t = re.sub(r"(\d)-(\d)", r"\1 \2", t)
    # sigle sconosciute con cifre dentro (D6, H3000, 200A): lettera per
    # lettera e il numero in cifre, PRIMA che i numeri diventino parole
    t = re.sub(r"(?<![A-Za-z\d])(?=[A-Za-z]*\d)(?=\d*[A-Za-z])[A-Za-z]*\d+[A-Za-z]*(?![A-Za-z\d])",
               lambda m: _sigla_in_lettere(m.group(0)), t)
    # decimali con la virgola: 44,1 → quarantaquattro virgola uno
    t = re.sub(r"\b(\d+),(\d+)\b", _decimale, t)
    # tutti gli altri numeri, anni compresi
    t = re.sub(r"\d+", lambda m: numero_in_lettere(int(m.group(0))), t)
    # sigle sconosciute di sole maiuscole: senza vocali (DMX, PCM, FM) si
    # leggono lettera per lettera; con le vocali sono parole (NAMM, ARP,
    # e le frasi in maiuscolo come la firma) e vanno al motore in minuscolo,
    # perché espeak-ng una parola tutta maiuscola può compitarla.
    def _sigla(m):
        s = m.group(0)
        if len(s) > 5 or re.search(r"[AEIOU]", s):
            return s.lower()
        return _sigla_in_lettere(s)
    t = re.sub(r"(?<![A-Za-z\d])[A-Z]{2,}(?![A-Za-z\d])", _sigla, t)
    # resti: trattini fra parole → spazio, spazi doppi
    t = re.sub(r"(?<=[A-Za-zàèéìòù])-(?=[A-Za-zàèéìòù])", " ", t)
    t = re.sub(r"[ \t]+", " ", t).strip()
    return t


# ------------------------------------------------------------- motore ---

_pipeline = None


def _scarica(nome_file):
    """Un file del modello dalla cache (CACHE/hf), scaricato solo se manca:
    prima si chiede alla cache senza rete, e solo se non c'è si scarica."""
    from huggingface_hub import hf_hub_download
    cache = str(CACHE / "hf")
    try:
        return hf_hub_download(repo_id=REPO_MODELLO, filename=nome_file,
                               cache_dir=cache, local_files_only=True)
    except Exception:
        print(f"voce: scarico {REPO_MODELLO}/{nome_file} in {cache}", flush=True)
        return hf_hub_download(repo_id=REPO_MODELLO, filename=nome_file, cache_dir=cache)


def _cartella_espeak():
    """La cartella dati che la libespeak-ng di espeakng-loader accetta.

    Provato il 21/10/2026 (sonda_espeak.py, 18 combinazioni): la libreria
    accetta un percorso P solo se esiste P/espeak-ng-data, e poi legge
    P/phontab, P/it_dict… cioè i file DIRETTAMENTE in P. Con la cartella
    dati vera (che non contiene un'altra espeak-ng-data) ignora il
    percorso e usa quello compilato nel wheel, che non esiste, e il
    processo esce senza eccezione. Qui si costruisce P con i link
    simbolici: P/espeak-ng-data → dati, P/<ogni file> → dati/<file>.
    """
    import espeakng_loader
    dati = pathlib.Path(espeakng_loader.get_data_path())
    P = CACHE / "espeak"
    P.mkdir(parents=True, exist_ok=True)
    for nome in ["espeak-ng-data"] + [f.name for f in dati.iterdir()]:
        bersaglio = dati if nome == "espeak-ng-data" else dati / nome
        link = P / nome
        if link.is_symlink() and link.resolve() == bersaglio.resolve():
            continue
        if link.exists() or link.is_symlink():
            link.unlink()
        link.symlink_to(bersaglio)
    if not (P / "phontab").exists():
        raise RuntimeError(f"cartella espeak incompleta: {P}")
    return P


def _carica():
    global _pipeline
    if _pipeline is not None:
        return _pipeline
    import torch
    from kokoro import KModel, KPipeline          # importa misaki, che fissa il percorso di espeak
    from phonemizer.backend.espeak.wrapper import EspeakWrapper
    EspeakWrapper.set_data_path(str(_cartella_espeak()))   # e qui lo si corregge, PRIMA della pipeline
    torch.set_num_threads(max(1, os.cpu_count() or 1))
    modello = KModel(repo_id=REPO_MODELLO, config=_scarica("config.json"),
                     model=_scarica(FILE_MODELLO)).to("cpu").eval()
    _pipeline = KPipeline(lang_code="i", repo_id=REPO_MODELLO, model=modello, device="cpu")
    _pipeline.voce = _scarica(f"voices/{VOCE}.pt")
    return _pipeline


def _frasi(testo):
    """Una frase per riga: con l'italiano Kokoro non spezza da solo i testi
    lunghi (lo dice lui: «Chunking logic not yet implemented»), e oltre
    ~500 fonemi tronca. Le battute sono corte, ma il racconto intero no."""
    pezzi = re.split(r"(?<=[.!?…])\s+", testo.strip())
    return [p for p in pezzi if p.strip()]


def _taglia_silenzio(a, soglia_dbfs=-45.0, margine=0.05):
    """Via il silenzio in testa e in coda a un pezzo (Kokoro ne lascia circa
    mezzo secondo per lato): la pausa fra le frasi la decide PAUSA_FRASE,
    e il silenzio in coda al file fa inventare parole a Whisper."""
    if not len(a):
        return a
    voce = np.flatnonzero(np.abs(a) > 10 ** (soglia_dbfs / 20))
    if not len(voce):
        return a[:0]
    m = int(SR * margine)
    return a[max(0, voce[0] - m):min(len(a), voce[-1] + m)]


def _normalizza_livello(a):
    """RMS a RMS_DBFS misurato sulle parti con voce (sopra -40 dBFS), picco
    non oltre PICCO_DBFS. Si misura sulla voce e non sul file intero
    perché le pause abbassano l'RMS e farebbero alzare troppo il guadagno."""
    if not len(a):
        return a
    blocco = SR // 50                                 # 20 ms
    n = len(a) // blocco
    rms_blocchi = np.sqrt(np.mean(a[:n * blocco].reshape(n, blocco) ** 2, axis=1)) if n else np.array([])
    voce = rms_blocchi[rms_blocchi > 10 ** (-40 / 20)]
    rms = np.sqrt(np.mean(voce ** 2)) if len(voce) else np.sqrt(np.mean(a ** 2))
    if rms <= 0:
        return a
    g = 10 ** (RMS_DBFS / 20) / rms
    picco = np.max(np.abs(a)) * g
    if picco > 10 ** (PICCO_DBFS / 20):
        g *= 10 ** (PICCO_DBFS / 20) / picco
    return a * g


def sintetizza(testo, wav_out, velocita=1.0):
    """Scrive `wav_out` (mono, 24 kHz, 16 bit) e torna la durata in secondi.

    `velocita` 1.0 è il passo del modello; 0.9 rallenta, 1.1 accelera. Il
    testo passa da `normalizza`: chi chiama scrive «CZ-101» e «1.200».
    """
    import torch
    pipe = _carica()
    pezzi = []
    pausa = np.zeros(int(SR * PAUSA_FRASE), dtype=np.float32)
    with torch.inference_mode():
        for frase in _frasi(normalizza(testo)):
            prima = len(pezzi)
            for _, _, audio in pipe(frase, voice=pipe.voce, speed=velocita, split_pattern=None):
                if audio is not None and len(audio):
                    pezzi.append(_taglia_silenzio(np.asarray(audio, dtype=np.float32)))
            if len(pezzi) == prima:
                # Kokoro salta in silenzio una frase senza fonemi: qui no.
                raise RuntimeError("frase senza audio dal motore: " + frase[:80])
            pezzi.append(pausa)
    if not pezzi:
        raise RuntimeError("sintesi vuota: " + testo[:60])
    a = _normalizza_livello(np.concatenate(pezzi[:-1]))   # senza la pausa finale
    a = np.clip(a, -1.0, 1.0)
    wav_out = pathlib.Path(wav_out)
    wav_out.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(wav_out), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((a * 32767).astype("<i2").tobytes())
    return len(a) / SR


# ---------------------------------------------------------- verifica ---

_whisper = None


def trascrivi(wav):
    """Il testo che faster-whisper sente nel wav (italiano, medium, int8)."""
    global _whisper
    if _whisper is None:
        from faster_whisper import WhisperModel
        _whisper = WhisperModel(MODELLO_WHISPER, device="cpu", compute_type="int8",
                                cpu_threads=max(1, os.cpu_count() or 1),
                                download_root=str(CACHE / "whisper"))
    # vad_filter toglie i silenzi, condition_on_previous_text=False impedisce
    # al decoder di «continuare» un testo: sono i due modi in cui Whisper
    # inventa frasi che non ci sono. La terza è la firma dei sottotitoli
    # («Sottotitoli creati dalla comunità Amara.org»), che sul silenzio in
    # coda è uscita alla prima prova: non può stare in una frase di
    # Dinamo, quindi si toglie senza rimpianti.
    segmenti, _ = _whisper.transcribe(str(wav), language="it", beam_size=5, vad_filter=True,
                                      condition_on_previous_text=False)
    testo = " ".join(s.text.strip() for s in segmenti)
    return _ALLUCINAZIONI.sub("", testo).strip()


_ALLUCINAZIONI = re.compile(r"(?i)sottotitoli (creati|e revisione|a cura)[^.]*\.?|grazie per aver guardato[^.]*\.?|"
                            r"iscriviti al canale[^.]*\.?")


_PEZZI_NUM = (r"(?:mille|mila|milion[ei]|miliard[oi]|cent[oi]|novant[ai]?|ottant[ai]?|settant[ai]?|"
              r"sessant[ai]?|cinquant[ai]?|quarant[ai]?|trent[ai]?|venti?|diciannove|diciotto|"
              r"diciassette|sedici|quindici|quattordici|tredici|dodici|undici|dieci|nove|otto|"
              r"sette|sei|cinque|quattro|tre|due|uno|un|zero)")
_RE_NUM = re.compile(rf"^{_PEZZI_NUM}+$")
_NOMI_LETTERA = {"bi": "b", "ci": "c", "effe": "f", "gi": "g", "acca": "h", "kappa": "k",
                 "elle": "l", "emme": "m", "enne": "n", "pi": "p", "cu": "q", "erre": "r",
                 "esse": "s", "ti": "t", "vu": "v", "vi": "v", "ics": "x", "ipsilon": "y",
                 "zeta": "z", "gei": "j"}
_AMBIGUE = {"a", "e", "i", "o", "u", "di"}


def _senza_accenti(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def _parole(testo):
    """Parole confrontabili: minuscole, senza punteggiatura né accenti;
    numeri e sigle portati alla stessa forma da entrambe le parti, così
    «CZ-101» e «ci zeta cento uno» (o «CZ 101») contano uguali."""
    t = _senza_accenti(testo.lower())
    t = re.sub(r"(?<=\d)\.(?=\d{3}\b)", "", t)
    t = re.sub(r"['’`]", " ", t)
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    t = re.sub(r"(?<=[a-z])(?=\d)|(?<=\d)(?=[a-z])", " ", t)
    toks = t.split()
    lettere = {**{c: c for c in "abcdefghijklmnopqrstuvwxyz"}, **_NOMI_LETTERA}
    out, i = [], 0
    while i < len(toks):
        j = i
        while j < len(toks) and toks[j] in lettere:
            j += 1
        serie = toks[i:j]
        if len(serie) >= 2 and any(s not in _AMBIGUE for s in serie):
            out.append("".join(lettere[s] for s in serie))
            i = j
            continue
        tok = toks[i]
        if tok.isdigit():
            tok = _senza_accenti(numero_in_lettere(int(tok))).replace(" ", "")
        elif tok == "vent":
            tok = "venti"
        out.append(tok)
        i += 1
    fuse = []
    for tok in out:
        if fuse and _RE_NUM.match(tok) and _RE_NUM.match(fuse[-1]):
            fuse[-1] += tok
        else:
            fuse.append(tok)
    return fuse


def _allinea(rif, ipo):
    """Levenshtein a parole con backtrace: (sostituzioni, omissioni,
    inserimenti, coppie (attesa, sentita) con None dove manca)."""
    n, m = len(rif), len(ipo)
    D = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        D[i][0] = i
    for j in range(m + 1):
        D[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            D[i][j] = min(D[i - 1][j] + 1, D[i][j - 1] + 1,
                          D[i - 1][j - 1] + (rif[i - 1] != ipo[j - 1]))
    i, j, S, O, I, coppie = n, m, 0, 0, 0, []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and D[i][j] == D[i - 1][j - 1] + (rif[i - 1] != ipo[j - 1]):
            if rif[i - 1] != ipo[j - 1]:
                S += 1
                coppie.append((rif[i - 1], ipo[j - 1]))
            i, j = i - 1, j - 1
        elif i > 0 and D[i][j] == D[i - 1][j] + 1:
            O += 1
            coppie.append((rif[i - 1], None))
            i -= 1
        else:
            I += 1
            coppie.append((None, ipo[j - 1]))
            j -= 1
    return S, O, I, list(reversed(coppie))


def wer(testo_atteso, trascrizione):
    rif, ipo = _parole(testo_atteso), _parole(trascrizione)
    S, O, I, _ = _allinea(rif, ipo)
    return (S + O + I) / max(1, len(rif))


def nomi_propri(testo):
    """Le parole del testo che devono arrivare intere: maiuscole non a
    inizio frase (Kuzmin, Moog), più le chiavi di NOMI e LESSICO ovunque."""
    nomi = set()
    for m in re.finditer(r"(?<![.!?…]\s)(?<!^)\b([A-Z][a-zà-ü]{2,})\b", testo):
        nomi.add(m.group(1))
    for k in list(NOMI) + list(LESSICO):
        if re.search(r"(?<![A-Za-z])" + re.escape(k) + r"(?![A-Za-z])", testo):
            nomi.add(k)
    return sorted(nomi)


def verifica(wav, testo_atteso, trascrizione=None):
    """(wer, parole_mancanti): i nomi propri che la trascrizione non contiene
    nemmeno storpiati. Chi chiama ferma il reel se `va_bene` è falso.
    `trascrizione` si passa quando il wav è già stato trascritto (Whisper
    medium costa quasi quanto l'audio dura)."""
    if trascrizione is None:
        trascrizione = trascrivi(wav)
    sentite = _parole(trascrizione)
    coppie = sentite + [a + b for a, b in zip(sentite, sentite[1:])]   # «a Ekaterinburg» sentito «al Katerinburg»
    mancanti = []
    for nome in nomi_propri(testo_atteso):
        for p in _parole(nome):
            if len(p) < 3 or _RE_NUM.match(p):
                continue
            migliore = max((difflib.SequenceMatcher(None, p, s).ratio() for s in coppie), default=0.0)
            if migliore < SOGLIA_NOME:
                mancanti.append(nome)
                break
    return wer(testo_atteso, trascrizione), mancanti


def va_bene(wer_misurato, mancanti):
    return wer_misurato <= SOGLIA_WER and not mancanti


# --------------------------------------------------------------- main ---

FRASE_DI_PROVA = ("Il Casio CZ-101 costa 495 dollari. Il DX7 di Yamaha quasi 2.000. "
                  "Vince Clarke degli Erasure ne tiene quattro. Vladimir Kuzmin, a "
                  "Ekaterinburg, vuole dare all'Unione Sovietica il suono di Moog, Korg e "
                  "Roland. Evgenij Murzin finisce l'ANS dopo vent'anni e gli dà le iniziali "
                  "di Skrjabin. Mandalo a chi lo chiama synth dei poveri.")

if __name__ == "__main__":
    frase = " ".join(sys.argv[1:]) or FRASE_DI_PROVA
    out = pathlib.Path("prova.wav")
    print("testo letto :", normalizza(frase))
    t0 = time.perf_counter()
    _carica()
    print(f"modello     : {MOTORE} {VOCE}, caricato in {time.perf_counter() - t0:.1f} s (cache {CACHE})")
    t0 = time.perf_counter()
    durata = sintetizza(frase, out)
    t_sintesi = time.perf_counter() - t0
    print(f"wav         : {out}  {durata:.2f} s  (sintesi {t_sintesi:.1f} s, "
          f"{t_sintesi / max(durata, 0.01):.2f} s di calcolo per s di audio)")
    t0 = time.perf_counter()
    trascrizione = trascrivi(out)
    print(f"trascrizione: {trascrizione}  (whisper {time.perf_counter() - t0:.1f} s)")
    e, mancanti = verifica(out, frase, trascrizione)
    print(f"WER         : {e:.3f}   nomi mancanti: {mancanti or 'nessuno'}   "
          f"→ {'VA BENE' if va_bene(e, mancanti) else 'FERMA IL REEL'}")
