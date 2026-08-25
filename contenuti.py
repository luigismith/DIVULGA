# -*- coding: utf-8 -*-
"""
ELETTROFONI — database dei contenuti.

Questo è l'UNICO posto dove vivono i testi delle schede: il generatore
grafico, il publisher e il sito-archivio leggono tutti da qui.
Non spargere testi nei template.

Ogni scheda è un dizionario con un campo per sezione (6 slide fisse):
  1. copertina   -> gancio + foto
  2. la_macchina -> cos'è
  3. inventore   -> chi la creò
  4. come_funziona
  5. chi_lusata  -> artisti e dischi (con menzioni @ verificate)
  6. aneddoto    -> chiusura + battuta di Dinamo + fonti

REGOLA EDITORIALE (fase 3): niente esce senza verifica su almeno 2 fonti
indipendenti; ogni fonte porta la data di verifica. Una scheda con
"verificata": False non viene MAI pubblicata (il publisher la salta) e
se una storia non regge la verifica si butta la scheda, non si ammorbidisce.
"""

FIRMA = "LE MACCHINE NON SUONANO DA SOLE. QUASI MAI."

# CTA fissa in didascalia (decisa in fase 0): genera commenti e suggerimenti.
CTA = (
    "Conosci qualcuno che ha suonato questa macchina? Taggalo. "
    "E dimmi quale macchina vuoi vedere nella prossima scheda."
)

# Vincoli dell'API Instagram, controllati PRIMA della pubblicazione
# (te ne accorgi in fase di scrittura, non davanti all'errore):
MAX_DIDASCALIA_UTF16 = 2200   # unità UTF-16: le emoji fuori dal BMP valgono 2
MAX_HASHTAG = 5
MAX_SLIDE = 10

# Limiti dei campi mostrati in tavola. LEZIONE IMPARATA (dal progetto
# precedente): qualunque testo che il template tronca a N caratteri va
# scritto SOTTO quella soglia, o la battuta finale sparisce dalla tavola
# pur restando nella didascalia. Quindi il limite si impone qui, a monte.
MAX_GANCIO = 110          # copertina, 3 righe grandi
MAX_BATTUTA = 150         # battuta di Dinamo, slide 6
MAX_TESTO_SLIDE = 620     # testo corrente di ogni slide interna

SCHEDE = [
    {
        "slug": "minimoog",
        "numero": 1,                      # numero di catalogo, appare in tavola
        "serie": "I SINTETIZZATORI",
        "strumento": "Minimoog Model D",
        "anno": "1970",
        "luogo": "Trumansburg, New York",
        "costruttore": "R.A. Moog Inc.",
        "specifiche": [                   # le 4 celle della copertina
            ("ANNO", "1970"),
            ("COSTRUTTORE", "R.A. Moog Inc."),
            ("SINTESI", "Sottrattiva"),
            ("VOCI", "Monofonico"),
        ],
        "gancio": "Prima di lui, per suonare un synth serviva una parete intera",
        "sottotitolo": "Il primo sintetizzatore che uscì dal laboratorio e salì su un palco.",
        "la_macchina": (
            "Fino al 1970 il sintetizzatore era un mobile: pareti di moduli, "
            "cavi da collegare a mano, roba da studio di registrazione. "
            "Il Minimoog mette tastiera e moduli già cablati in una sola "
            "valigetta di legno: niente cavi, si accende e suona. È il primo "
            "sintetizzatore portatile integrato pensato per il palco — quello "
            "che porta il synth fuori dal laboratorio."
        ),
        "inventore_nome": "Bill Hemsath e Bob Moog",
        "inventore": (
            "Il primo prototipo nasce quasi di nascosto, nell'autunno 1969: "
            "l'ingegnere Bill Hemsath lo assembla nelle pause pranzo, nella "
            "soffitta-«cimitero» della fabbrica Moog, con moduli di scarto — "
            "per sua stessa stima, un solo pezzo era nuovo. Bob Moog, il "
            "titolare, all'inizio è scettico: sarà il prodotto che salva "
            "l'azienda."
        ),
        "come_funziona": (
            "Tre oscillatori generano l'onda grezza (il terzo fa anche da "
            "LFO); il filtro «ladder» — brevetto US 3.475.623, il suono Moog "
            "per definizione — la scolpisce togliendo frequenze a 24 dB per "
            "ottava; l'inviluppo le dà forma nel tempo. Una nota alla volta: "
            "monofonico. E a sinistra della tastiera c'è una novità assoluta, "
            "la pitch wheel: la rotella per piegare le note che da qui in poi "
            "troverai su quasi ogni synth."
        ),
        "richiami": [
            ("FIG. 1", "3 oscillatori"),
            ("FIG. 2", "Filtro ladder 24 dB"),
            ("FIG. 3", "Pitch & mod wheel"),
        ],
        "chi_lusata": [
            # ATTENZIONE (regola fase 3): handle SOLO se verificati come
            # ufficiali (evidenza web salvata in fonti); si tagga l'autore,
            # mai il bersaglio. Se il profilo ufficiale non esiste si tagga
            # il non ufficiale più seguito dichiarandolo tale.
            # SCARTATI dopo verifica (2026-08-25): Keith Emerson per «Lucky
            # Man» (era il Moog MODULARE), Giorgio Moroder per «I Feel Love»
            # (Moog Modular 3P), Gary Numan «Cars» (non documentato su 2 fonti).
            {"artista": "Sun Ra", "nota": "primo in assoluto: «My Brother the Wind», 1970, col prototipo", "ig": None},
            {"artista": "Kraftwerk", "nota": "il basso di «Autobahn» (1974)", "ig": "kraftwerkofficial"},
            {"artista": "Bernie Worrell", "nota": "tre Minimoog insieme su «Flash Light» (Parliament, 1978)", "ig": None},
            {"artista": "Keith Emerson", "nota": "dal vivo con ELP, dal 1973", "ig": None},
        ],
        # Menzioni non-artista verificate (costruttore attuale del Model D)
        "menzioni_extra": [
            {"ig": "moogsynthesizers",
             "riga": "E il Model D, oltre mezzo secolo dopo, è ancora a listino da @moogsynthesizers."},
        ],
        "aneddoto": (
            "Nel 1969 Bob Moog prestò uno dei prototipi a Sun Ra, che lo "
            "portò sul palco e su disco prima ancora che il Minimoog fosse "
            "in vendita. Non lo restituì mai — e Moog non se ne preoccupò. "
            "Ne furono costruiti circa 12.000 fino al 1981; più di mezzo "
            "secolo dopo, il Model D è ancora a listino."
        ),
        "battuta_dinamo": "Anche io sono fatto di pezzi di ricambio. Non è un difetto, è un inizio.",
        "foto": {
            "file": "assets/foto/minimoog/principale.jpg",
            "autore": "Wolfgang Stief",
            "licenza": "CC BY 2.0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "«The Birth of the Minimoog» — Moogseum / Bob Moog Foundation",
             "url": "https://artsandculture.google.com/story/the-birth-of-the-minimoog-moogseum/BwWxC5g1sP9LAA",
             "data": "2026-08-25"},
            {"titolo": "«Instrumental Instruments: Minimoog» — Red Bull Music Academy Daily",
             "url": "https://daily.redbullmusicacademy.com/2017/10/instrumental-instruments-minimoog/",
             "data": "2026-08-25"},
            {"titolo": "Brevetto US 3.475.623 (filtro Moog) — Google Patents",
             "url": "https://patents.google.com/patent/US3475623A/en",
             "data": "2026-08-25"},
            {"titolo": "«Sun Ra & the Minimoog» — Bob Moog Foundation",
             "url": "https://moogfoundation.org/sun-ra-the-minimoog-by-historian-thom-holmes/",
             "data": "2026-08-25"},
        ],
        "hashtags": ["#minimoog", "#sintetizzatore", "#musicaelettronica", "#synth", "#storiadellamusica"],
        "verificata": True,   # verifica completata il 2026-08-25 (vedi fonti)
    },
    {
        "slug": "tr808",
        "numero": 2,
        "serie": "LE DRUM MACHINE",
        "strumento": "Roland TR-808",
        "anno": "1980",
        "luogo": "Giappone",
        "costruttore": "Roland",
        "specifiche": [
            ("ANNO", "1980"),
            ("COSTRUTTORE", "Roland"),
            ("SUONI", "Analogici"),
            ("LISTINO", "1.195 $"),
        ],
        "gancio": "Morì quando finirono i transistor difettosi",
        "sottotitolo": "La drum machine che da flop diventò il battito dell'hip hop, della house e della trap.",
        "la_macchina": (
            "Nel 1980 la TR-808 sembra un errore commerciale: suoni «finti» "
            "in un'epoca che vuole batterie vere. Fu un flop, e a metà anni "
            "'80 si trovava nei banchi dei pegni a meno di 100 dollari. La "
            "comprarono i ragazzi squattrinati di New York, Chicago e "
            "Detroit: da quelle camerette uscirono l'electro, la house e la "
            "techno. Oggi un originale supera i 4.000 dollari."
        ),
        "inventore_nome": "Ikutaro Kakehashi e Tadao Kikumoto",
        "inventore": (
            "Ikutaro Kakehashi, il fondatore di Roland, la volle; il capo "
            "ingegnere Tadao Kikumoto la progettò. La scelta chiave fu la "
            "sintesi analogica: niente costosi campioni digitali come la "
            "rivale Linn LM-1 da 5.000 dollari, ma circuiti che imitano i "
            "tamburi. Risultato: 1.195 dollari di listino."
        ),
        "come_funziona": (
            "Ogni suono è generato da un circuito, non registrato: il kick è "
            "un filtro «bridged-T» spinto a oscillare, una sinusoide smorzata "
            "che scende di tono. Il fruscio di rullante, clap e piatti viene "
            "invece da transistor 2SC828 FUORI SPECIFICA, scartati dalla "
            "fabbrica: Kakehashi li comprava apposta, perché quel difetto "
            "produceva il rumore giusto."
        ),
        "richiami": [
            ("FIG. 1", "16 suoni analogici"),
            ("FIG. 2", "Kick bridged-T"),
            ("FIG. 3", "Sequencer a step"),
        ],
        "chi_lusata": [
            # «Planet Rock» si cita come brano, accreditando il produttore:
            # niente tag né celebrazione di Bambaataa (accuse gravissime,
            # causa civile persa nel 2021 — regola: mai taggare figure
            # controverse, si racconta il disco).
            {"artista": "«Planet Rock»", "nota": "1982, prod. Arthur Baker: la pietra fondativa dell'electro", "ig": None},
            {"artista": "Marvin Gaye", "nota": "il battito di «Sexual Healing» (1982)", "ig": None},
            {"artista": "Whitney Houston", "nota": "«I Wanna Dance with Somebody» (1987)", "ig": None},
            {"artista": "Kanye West", "nota": "l'omaggio nel titolo: «808s & Heartbreak» (2008)", "ig": None},
        ],
        "menzioni_extra": [
            {"ig": "rolandglobal",
             "riga": "Oggi @rolandglobal la celebra ogni 8 agosto: è l'808 Day."},
        ],
        "aneddoto": (
            "La 808 morì di qualità: il suo fruscio veniva da lotti di "
            "transistor difettosi, e quando le fabbriche impararono a non "
            "sbagliarne più, Roland rimase senza ricambi. Produzione chiusa "
            "nel 1983, circa 12.000 unità. Le imitazioni digitali sono "
            "ovunque; i difetti originali, introvabili."
        ),
        "battuta_dinamo": "Difettosa per la fabbrica, perfetta per tutti gli altri.",
        "foto": {
            "file": "assets/foto/tr808/principale.jpg",
            "autore": "Brandon Daniel",
            "licenza": "CC BY-SA 2.0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "«The Strange Heart of the Roland TR-808» — Secret Life of Synthesizers",
             "url": "https://secretlifeofsynthesizers.com/the-strange-heart-of-the-roland-tr-808/",
             "data": "2026-08-25"},
            {"titolo": "«A Brief History of the TR-808» — Smithsonian Magazine",
             "url": "https://www.smithsonianmag.com/arts-culture/history-tr-808-drum-machine-180975205/",
             "data": "2026-08-25"},
            {"titolo": "«The History of the Roland TR-808» — Sweetwater",
             "url": "https://www.sweetwater.com/insync/history-roland-808/",
             "data": "2026-08-25"},
            {"titolo": "Documentario «808» (2015, regia A. Dunn) — con l'intervista a Kakehashi",
             "url": "https://en.wikipedia.org/wiki/808_(film)",
             "data": "2026-08-25"},
        ],
        "hashtags": ["#tr808", "#drummachine", "#musicaelettronica", "#hiphop", "#roland"],
        "verificata": True,   # verifica completata il 2026-08-25 (vedi fonti)
    },
    {
        "slug": "theremin",
        "numero": 3,
        "serie": "LE ORIGINI",
        "strumento": "Theremin",
        "anno": "1920",
        "luogo": "Pietrogrado, Russia",
        "costruttore": "Lev Termen",
        "specifiche": [
            ("ANNO", "1920"),
            ("INVENTORE", "Lev Termen"),
            ("PRINCIPIO", "Eterodina"),
            ("CONTATTO", "Nessuno"),
        ],
        "gancio": "L'unico strumento che si suona senza toccarlo",
        "sottotitolo": "Nato da un esperimento di fisica sovietico, finì a Hollywood. Il suo inventore, in un laboratorio-prigione.",
        "la_macchina": (
            "Due antenne: quella verticale decide la nota, l'anello "
            "orizzontale il volume. Le mani non toccano niente — è il corpo "
            "del musicista a entrare nel circuito, spostando la frequenza "
            "come farebbe un condensatore. Niente tasti e niente tacche: "
            "l'intonazione è tutta a orecchio, per questo è tra gli "
            "strumenti più difficili al mondo."
        ),
        "inventore_nome": "Lev Termen (Leon Theremin)",
        "inventore": (
            "Un fisico di Pietrogrado che nel 1920, lavorando a un misuratore "
            "di gas, si accorge che la sua mano cambia il suono. Nel 1922 lo "
            "mostra al Cremlino — secondo il suo racconto, Lenin arrivò a "
            "suonarci un'aria di Glinka. Brevetto americano nel 1928, e nel "
            "1929 la RCA ne produce circa 500 esemplari."
        ),
        "come_funziona": (
            "Dentro ci sono due oscillatori a frequenze altissime, quasi "
            "identiche: l'orecchio non li sente, ma sente la loro DIFFERENZA "
            "— il battimento — che cade nelle frequenze udibili. Avvicinando "
            "la mano all'antenna cambi la capacità del circuito, la "
            "differenza si sposta, la nota sale. L'altra mano, sull'anello, "
            "apre e chiude il volume: è così che il theremin «respira»."
        ),
        "richiami": [
            ("FIG. 1", "Antenna del tono"),
            ("FIG. 2", "Anello del volume"),
            ("FIG. 3", "Zero contatto"),
        ],
        "chi_lusata": [
            {"artista": "Clara Rockmore", "nota": "la virtuosa assoluta (Town Hall, New York, 1938)", "ig": None},
            {"artista": "Miklós Rózsa", "nota": "«Io ti salverò» di Hitchcock (1945), Oscar alla colonna sonora", "ig": None},
            {"artista": "Bernard Herrmann", "nota": "due theremin in «Ultimatum alla Terra» (1951)", "ig": None},
            {"artista": "Carolina Eyck", "nota": "la voce del theremin oggi", "ig": "carolinaeyck"},
        ],
        "menzioni_extra": [
            {"ig": "moogsynthesizers",
             "riga": "E si compra ancora: @moogsynthesizers ha a catalogo l'Etherwave, disegnato da Bob Moog."},
        ],
        "aneddoto": (
            "Termen tornò in URSS nel 1938 e finì arrestato: Kolyma, poi un "
            "laboratorio-prigione. Lì progettò «The Thing»: una cimice senza "
            "batterie nascosta nel Gran Sigillo di legno regalato "
            "all'ambasciatore USA a Mosca nel 1945. Funzionò, non scoperta, "
            "per sette anni. L'inventore dello strumento più etereo del "
            "mondo aveva costruito anche la spia perfetta."
        ),
        "battuta_dinamo": "Mai fidarsi dell'aria: a volte suona, a volte ascolta.",
        "foto": {
            "file": "assets/foto/theremin/principale.jpg",
            "autore": "Soundsweep",
            "licenza": "CC BY-SA 4.0",
            "fonte": "Wikimedia Commons",
            "posizione": "top",
        },
        "fonti": [
            {"titolo": "«The Theremin Turns 100» — Smithsonian Magazine",
             "url": "https://www.smithsonianmag.com/smart-news/theremin-100-years-anniversary-instrument-music-history-180976437/",
             "data": "2026-08-25"},
            {"titolo": "Brevetto US 1.661.058 (1928) — Google Patents",
             "url": "https://patents.google.com/patent/US1661058A/en",
             "data": "2026-08-25"},
            {"titolo": "«The Thing (listening device)» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/The_Thing_(listening_device)",
             "data": "2026-08-25"},
            {"titolo": "«The Sound of Early Sci-Fi: Samuel Hoffman's Theremin» — Reverb",
             "url": "https://reverb.com/news/the-sound-of-early-sci-fi-samuel-hoffmans-theremin",
             "data": "2026-08-25"},
        ],
        "hashtags": ["#theremin", "#musicaelettronica", "#storiadellamusica", "#synth", "#leontheremin"],
        "verificata": True,   # verifica completata il 2026-08-25 (vedi fonti)
    },
    {
        "slug": "mellotron",
        "numero": 4,
        "serie": "GLI ANTENATI",
        "strumento": "Mellotron",
        "anno": "1963",
        "luogo": "Birmingham, Inghilterra",
        "costruttore": "Bradmatic / Streetly",
        "specifiche": [
            ("ANNO", "1963"),
            ("COSTRUTTORE", "Bradmatic"),
            ("PRINCIPIO", "Nastri veri"),
            ("DURATA NOTA", "~8 secondi"),
        ],
        "gancio": "Sotto ogni tasto, otto secondi di orchestra vera",
        "sottotitolo": "Il campionatore prima del digitale: un registratore travestito da organo.",
        "la_macchina": (
            "Sotto ogni tasto c'è una striscia di nastro magnetico con una "
            "registrazione vera: flauti, archi, cori. Premi il tasto e il "
            "nastro scorre su una testina, come un registratore; dopo circa "
            "otto secondi la corsa finisce e una molla lo riporta indietro. "
            "Per tenere una nota lunga devi rilasciare e ripremere: i "
            "tastieristi impararono a respirare come i fiatisti."
        ),
        "inventore_nome": "I fratelli Bradley (e un segreto americano)",
        "inventore": (
            "1962: il venditore americano Bill Fransen porta a Birmingham "
            "due Chamberlin — senza dire che il progetto è del suo datore di "
            "lavoro, Harry Chamberlin. I fratelli Leslie, Frank e Norman "
            "Bradley li reingegnerizzano e nel 1963 nasce il Mellotron. "
            "Quando Chamberlin scopre la copia, la disputa si chiude solo "
            "nel 1966, con un accordo economico."
        ),
        "come_funziona": (
            "Una nota = un nastro. Non un anello continuo: una striscia con "
            "un inizio e una fine, per questo l'attacco di ogni nota è vivo "
            "come l'esecuzione originale. Ogni striscia porta più tracce — "
            "cambi suono spostando la testina — e la meccanica che preme "
            "nastro e rullo a ogni tasto è un piccolo miracolo di officina "
            "inglese. Fragile, pesante, meraviglioso."
        ),
        "richiami": [
            ("FIG. 1", "1 nastro per tasto"),
            ("FIG. 2", "~8 s per nota"),
            ("FIG. 3", "Ritorno a molla"),
        ],
        "chi_lusata": [
            {"artista": "Beatles", "nota": "l'intro di «Strawberry Fields Forever» (1967), flauti suonati da McCartney", "ig": "thebeatles"},
            {"artista": "Moody Blues", "nota": "«Nights in White Satin» (1967), al Mellotron Mike Pinder", "ig": None},
            {"artista": "King Crimson", "nota": "«In the Court of the Crimson King» (1969)", "ig": "kingcrimsonofficial"},
            {"artista": "Genesis", "nota": "l'intro di «Watcher of the Skies» (1972), Tony Banks", "ig": "genesis_band"},
        ],
        "menzioni_extra": [
            {"ig": "mellotronfactory",
             "riga": "Si costruisce ancora: a nastro dalla Streetly inglese, digitale da @mellotronfactory a Stoccolma."},
        ],
        "aneddoto": (
            "Prima di fondare i Moody Blues, Mike Pinder passò diciotto mesi "
            "nella fabbrica dei Bradley a collaudare Mellotron. Poi ne "
            "comprò uno usato e ci costruì «Nights in White Satin». Il "
            "collaudatore era diventato il miglior spot della ditta: nessuno "
            "conosceva quella macchina meglio di lui."
        ),
        "battuta_dinamo": "Otto secondi bastano a tutti, se sai quando premere il tasto.",
        "foto": {
            "file": "assets/foto/mellotron/principale.jpg",
            "autore": "Tobias Akerboom",
            "licenza": "CC BY 2.0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "«Did Mellotrons use tape loops or not?» — Sound On Sound",
             "url": "https://www.soundonsound.com/sound-advice/q-did-mellotrons-use-tape-loops-or-not",
             "data": "2026-08-25"},
            {"titolo": "«Blast from the past: Mellotron» — MusicRadar",
             "url": "https://www.musicradar.com/news/tech/blast-from-the-past-mellotron-612542",
             "data": "2026-08-25"},
            {"titolo": "«Mellotron / Mellotronics Manufacturing» — National Music Centre",
             "url": "https://collections.nmc.ca/people/419/mellotron-mellotronics-manufacturing",
             "data": "2026-08-25"},
            {"titolo": "«Strawberry Fields Forever» — Beatles Bible",
             "url": "https://www.beatlesbible.com/songs/strawberry-fields-forever/",
             "data": "2026-08-25"},
        ],
        "hashtags": ["#mellotron", "#beatles", "#storiadellamusica", "#rockprogressivo", "#musicaelettronica"],
        "verificata": True,   # verifica completata il 2026-08-25 (vedi fonti)
    },
    {
        "slug": "dx7",
        "numero": 5,
        "serie": "I SINTETIZZATORI",
        "strumento": "Yamaha DX7",
        "anno": "1983",
        "luogo": "Giappone",
        "costruttore": "Yamaha",
        "specifiche": [
            ("ANNO", "1983"),
            ("COSTRUTTORE", "Yamaha"),
            ("SINTESI", "FM digitale"),
            ("VENDUTI", "200.000+"),
        ],
        "gancio": "Un suo preset suonava nel 40% delle hit n.1 del 1986",
        "sottotitolo": "Il primo sintetizzatore digitale di successo: 1.995 dollari, e il suono degli anni '80 cambiò padrone.",
        "la_macchina": (
            "Nel 1983 un polifonico analogico costava come un'auto; il DX7 "
            "arriva a 1.995 dollari, la metà di un Jupiter-8, con un suono "
            "cristallino che gli analogici non sapevano fare. Oltre 150.000 "
            "ordini nel primo anno, più di 200.000 in totale: il "
            "sintetizzatore più venduto della sua epoca."
        ),
        "inventore_nome": "John Chowning e Yamaha",
        "inventore": (
            "La sintesi FM nasce a Stanford nel 1967, nel laboratorio di "
            "John Chowning. I costruttori americani di organi — Hammond, "
            "Wurlitzer, Lowrey — la vedono e passano la mano: non capiscono "
            "il digitale. Un ingegnere Yamaha la capisce in dieci minuti. "
            "Quel brevetto fruttò a Stanford oltre 20 milioni di dollari: "
            "per anni il più redditizio dell'università."
        ),
        "come_funziona": (
            "Niente filtri che scolpiscono: operatori che si modulano a "
            "vicenda, frequenza su frequenza, in 32 combinazioni chiamate "
            "algoritmi. Suoni impossibili per gli analogici — piani "
            "elettrici, campane, bassi vitrei — ma programmarlo era un "
            "incubo di membrane e sottomenu, senza una manopola. Disse "
            "Brian Eno: «Ce l'hanno tutti. Nessuno lo sa programmare»."
        ),
        "richiami": [
            ("FIG. 1", "Sintesi FM"),
            ("FIG. 2", "16 voci"),
            ("FIG. 3", "32 algoritmi"),
        ],
        "chi_lusata": [
            {"artista": "a-ha", "nota": "il basso di «Take On Me» (1985): preset BASS 1", "ig": None},
            {"artista": "Whitney Houston", "nota": "l'E.PIANO 1 delle grandi ballad", "ig": None},
            {"artista": "Phil Collins", "nota": "«One More Night» (1985)", "ig": None},
            {"artista": "Brian Eno", "nota": "tra i pochi a programmarlo davvero («Apollo», 1983)", "ig": "brianeno"},
        ],
        "menzioni_extra": [
            {"ig": "yamahasynths_official",
             "riga": "La casa madre, ieri e oggi: @yamahasynths_official."},
        ],
        "aneddoto": (
            "Nel 1986 il preset numero 11 — E.PIANO 1, il piano elettrico di "
            "fabbrica — suonava nel 40% dei singoli arrivati al numero 1 "
            "della Billboard Hot 100, e nel 61% di quelli R&B. Non il DX7: "
            "un suo SINGOLO preset. Nessun suono di fabbrica ha mai "
            "dominato le classifiche così."
        ),
        "battuta_dinamo": "Trentadue algoritmi e nessuna manopola: c'è chi lo chiama progresso.",
        "foto": {
            "file": "assets/foto/dx7/principale.jpg",
            "autore": "Leo-setä, iixorbiusii, Georgfotoart (mod. Pittigrilli)",
            "licenza": "CC BY 4.0",
            "fonte": "Wikimedia Commons",
            "posizione": "top",
        },
        "fonti": [
            {"titolo": "«The Yamaha DX7 was the most important release in synth history» — MusicRadar",
             "url": "https://www.musicradar.com/news/the-yamaha-dx7-was-the-most-important-release-in-synth-history",
             "data": "2026-08-25"},
            {"titolo": "«The Father of the Digital Synthesizer» — Priceonomics",
             "url": "https://priceonomics.com/the-father-of-the-digital-synthesizer/",
             "data": "2026-08-25"},
            {"titolo": "M. Lavengood, «What Makes It Sound '80s?» — Journal of Popular Music Studies (2019)",
             "url": "https://online.ucpress.edu/jpms/article-abstract/31/3/73/105979",
             "data": "2026-08-25"},
            {"titolo": "«Discovering Digital FM: John Chowning Remembers» — Yamaha Hub",
             "url": "https://hub.yamaha.com/keyboards/synthesizers/discovering-digital-fm-john-chowning-remembers/",
             "data": "2026-08-25"},
        ],
        "hashtags": ["#dx7", "#yamaha", "#synth", "#musicaelettronica", "#anni80"],
        "verificata": True,   # verifica completata il 2026-08-25 (vedi fonti)
    },
    {
        "slug": "fairlight",
        "numero": 6,
        "serie": "I CAMPIONATORI",
        "strumento": "Fairlight CMI",
        "anno": "1979",
        "luogo": "Sydney, Australia",
        "costruttore": "Fairlight",
        "specifiche": [
            ("ANNO", "1979"),
            ("ORIGINE", "Sydney"),
            ("CAMPIONI", "8 bit"),
            ("PREZZO UK", "£12-18.000"),
        ],
        "gancio": "Registrava il mondo e lo suonava sulla tastiera",
        "sottotitolo": "Il primo campionatore polifonico in commercio: un computer australiano con la penna ottica.",
        "la_macchina": (
            "Registri un suono vero — un cane, un vaso rotto, un'orchestra — "
            "e lo suoni su 73 tasti: è il primo sintetizzatore-campionatore "
            "digitale polifonico mai messo in vendita. Sul monitor a fosfori "
            "verdi disegni le forme d'onda con una penna ottica. Il nome "
            "viene dall'aliscafo che attraversava la baia di Sydney davanti "
            "alla casa dove i due inventori lavoravano."
        ),
        "inventore_nome": "Peter Vogel e Kim Ryrie",
        "inventore": (
            "Due giovani di Sydney. Nell'estate 1979 Vogel porta il "
            "prototipo a casa di Peter Gabriel, vicino Bath: è il primo "
            "Fairlight del Regno Unito, e Gabriel col cugino fonda "
            "l'importatore Syco. Kate Bush è tra i primissimi: lo usa su "
            "«Never for Ever» (1980) e ne fa lo strumento principale di "
            "«The Dreaming» (1982)."
        ),
        "come_funziona": (
            "Campiona a 8 bit, fino a circa 24 kHz: grezzo per gli standard "
            "di oggi, una rivoluzione allora. Nella libreria c'era ORCH5 — "
            "un accordo dell'«Uccello di fuoco» di Stravinskij, campionato "
            "da un disco — che da «Planet Rock» (1982) in poi diventò "
            "l'«orchestra hit» di mezzo pop anni '80. Un campione dentro un "
            "campionatore: la musica che cita sé stessa."
        ),
        "richiami": [
            ("FIG. 1", "Campioni a 8 bit"),
            ("FIG. 2", "Penna ottica"),
            ("FIG. 3", "Page R: sequencer"),
        ],
        "chi_lusata": [
            {"artista": "Peter Gabriel", "nota": "il primo in Gran Bretagna (1979)", "ig": "itspetergabriel"},
            {"artista": "Kate Bush", "nota": "«Never for Ever» (1980), «The Dreaming» (1982)", "ig": "katebushmusic"},
            {"artista": "Herbie Hancock", "nota": "l'era di «Rockit» (1983)", "ig": "herbiehancock"},
            {"artista": "Jan Hammer", "nota": "il tema di «Miami Vice», n. 1 USA nel 1985", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": (
            "1983, Sesame Street: Herbie Hancock campiona in diretta le voci "
            "dei bambini — tra cui la piccola Tatyana Ali, futura star di "
            "«Willy, il principe di Bel-Air» — e le suona sulla tastiera "
            "davanti a loro. Il campionamento spiegato meglio di qualunque "
            "manuale, in tre minuti di TV per l'infanzia."
        ),
        "battuta_dinamo": "Attento a cosa dici qui davanti: potrebbe finire in tastiera.",
        "foto": {
            # In attesa di scaricare la foto SMEM (rate limit Wikimedia):
            # File:Fairlight CMI at the SMEM Schaulager 09.jpg — CC BY 4.0
            "file": "assets/foto/fairlight/principale.jpg",
            "autore": "SMEM — Swiss Museum for Electronic Music Instruments",
            "licenza": "CC BY 4.0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "«Fairlight CMI (Retrozone)» — Sound On Sound",
             "url": "https://www.soundonsound.com/reviews/fairlight-cmi-retrozone",
             "data": "2026-08-25"},
            {"titolo": "R. Fink, «The story of ORCH5» — Popular Music, Cambridge UP",
             "url": "https://www.cambridge.org/core/journals/popular-music/article/story-of-orch5-or-the-classical-ghost-in-the-hiphop-machine/D87079C034B6E20504E0B59CCCFFFEB7",
             "data": "2026-08-25"},
            {"titolo": "«The Fairlight: the instrument that invented sampling» — NFSA (Australia)",
             "url": "https://www.nfsa.gov.au/latest/fairlight-instrument-invented-sampling",
             "data": "2026-08-25"},
            {"titolo": "«Herbie Hancock on Sesame Street, 1983» — herbiehancock.com",
             "url": "https://www.herbiehancock.com/2012/10/24/video-herbie-hancock-on-sesame-street-1983/",
             "data": "2026-08-25"},
        ],
        "hashtags": ["#fairlight", "#sampling", "#campionatore", "#musicaelettronica", "#anni80"],
        # Fatti verificati il 2026-08-25, ma la foto libera non è ancora nel
        # repo (rate limit sul download): resta False finché non c'è —
        # la regola della foto obbligatoria vale più della coda.
        "verificata": False,
    },
]


def _len_utf16(testo):
    """Lunghezza in unità UTF-16 (come conta Instagram): le emoji fuori
    dal BMP valgono 2 unità."""
    return len(testo.encode("utf-16-le")) // 2


def componi_didascalia(scheda):
    """Compone la didascalia del post a partire dai campi della scheda.

    Struttura fissa: gancio + racconto breve + artisti (con menzioni) +
    battuta di Dinamo + CTA + fonti con data + credito foto + firma + hashtag.
    """
    righe = []
    righe.append(f"{scheda['strumento'].upper()} · {scheda['anno']}")
    righe.append("")
    righe.append(scheda["gancio"] + ".")
    righe.append("")
    righe.append(scheda["la_macchina"])
    righe.append("")
    usi = []
    for u in scheda["chi_lusata"]:
        nome = f"@{u['ig']}" if u.get("ig") else u["artista"]
        usi.append(f"{nome} ({u['nota']})")
    if usi:
        righe.append("L'hanno resa leggenda: " + " · ".join(usi) + ".")
        righe.append("")
    for m in scheda.get("menzioni_extra", []):
        righe.append(m["riga"])
        righe.append("")
    righe.append(f"Dinamo dice: «{scheda['battuta_dinamo']}»")
    righe.append("")
    righe.append(CTA)
    righe.append("")
    if scheda["fonti"]:
        righe.append("Fonti (verificate il " + scheda["fonti"][0]["data"] + "):")
        for f in scheda["fonti"]:
            righe.append(f"· {f['titolo']}")
    foto = scheda["foto"]
    righe.append(f"Foto: {foto['autore']} · {foto['licenza']} · {foto['fonte']}")
    righe.append("")
    righe.append(FIRMA)
    righe.append("")
    righe.append(" ".join(scheda["hashtags"]))
    return "\n".join(righe)


def primo_commento(scheda):
    """Il primo commento ripete le menzioni: dentro una didascalia lunga,
    sul telefono, il tag resta nascosto dietro «... altro» — quindi la
    menzione va anche qui, dove la notifica parte sempre."""
    tags = [f"@{u['ig']}" for u in scheda["chi_lusata"] if u.get("ig")]
    tags += [f"@{m['ig']}" for m in scheda.get("menzioni_extra", [])]
    if not tags:
        return None
    return "In questa scheda: " + " ".join(tags)


def valida_scheda(scheda):
    """Controlli automatici: una scheda fuori misura viene rifiutata QUI,
    in fase di scrittura, non davanti all'errore dell'API."""
    errori = []
    did = componi_didascalia(scheda)
    n = _len_utf16(did)
    if n > MAX_DIDASCALIA_UTF16:
        errori.append(f"didascalia {n} unità UTF-16 (max {MAX_DIDASCALIA_UTF16})")
    if len(scheda["hashtags"]) > MAX_HASHTAG:
        errori.append(f"{len(scheda['hashtags'])} hashtag (max {MAX_HASHTAG})")
    if len(scheda["gancio"]) > MAX_GANCIO:
        errori.append(f"gancio {len(scheda['gancio'])} caratteri (max {MAX_GANCIO})")
    if len(scheda["battuta_dinamo"]) > MAX_BATTUTA:
        errori.append(f"battuta {len(scheda['battuta_dinamo'])} caratteri (max {MAX_BATTUTA})")
    for campo in ("la_macchina", "inventore", "come_funziona", "aneddoto"):
        if len(scheda[campo]) > MAX_TESTO_SLIDE:
            errori.append(f"{campo} {len(scheda[campo])} caratteri (max {MAX_TESTO_SLIDE})")
    if scheda["verificata"] and len(scheda["fonti"]) < 2:
        errori.append("scheda marcata verificata ma con meno di 2 fonti")
    for f in scheda["fonti"]:
        if not f.get("data") or not f.get("url") or not f.get("titolo"):
            errori.append(f"fonte incompleta: {f}")
    if not scheda["foto"].get("autore") or not scheda["foto"].get("licenza"):
        errori.append("credito foto incompleto (autore/licenza obbligatori)")
    return errori


def scheda_da_pubblicare(pubblicati_slug):
    """La prossima scheda in coda: la prima verificata e mai pubblicata.
    L'idempotenza si decide su stato.json, non interrogando l'API."""
    for s in SCHEDE:
        if s["slug"] not in pubblicati_slug and s["verificata"]:
            return s
    return None


if __name__ == "__main__":
    problemi = False
    for s in SCHEDE:
        errs = valida_scheda(s)
        stato = "OK " if not errs else "ERR"
        print(f"[{stato}] {s['slug']} — didascalia {_len_utf16(componi_didascalia(s))}/{MAX_DIDASCALIA_UTF16} UTF-16, verificata={s['verificata']}")
        for e in errs:
            print(f"      - {e}")
            problemi = True
    verificate = sum(1 for s in SCHEDE if s["verificata"])
    print(f"\nSchede totali: {len(SCHEDE)} — verificate e pubblicabili: {verificate}")
    raise SystemExit(1 if problemi else 0)
