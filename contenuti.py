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
        "verificata": True,   # verifica 2026-08-25; foto SMEM scaricata via workflow scarica-foto
    },
    {
        "slug": "tb303",
        "numero": 7,
        "serie": "I SINTETIZZATORI",
        "strumento": "Roland TB-303",
        "anno": "1981",
        "luogo": "Giappone",
        "costruttore": "Roland",
        "specifiche": [
            ("ANNO", "1981"),
            ("COSTRUTTORE", "Roland"),
            ("VOCI", "1 oscillatore"),
            ("LISTINO", "395 $"),
        ],
        "gancio": "Doveva imitare un basso. Ha inventato l'acid house",
        "sottotitolo": "Il flop per chitarristi senza bassista, rinato nei banchi dei pegni di Chicago.",
        "la_macchina": (
            "Nel 1981 Roland la vende come «basso computerizzato» per chi "
            "prova senza bassista, in coppia con la drum machine TR-606. Ma "
            "il suono non somiglia a nessun basso, e il manuale è "
            "incomprensibile: circa 10.000 unità, produzione chiusa nel "
            "1984, e la 303 finisce nei banchi dei pegni a prezzi "
            "stracciati. Oggi un originale costa migliaia di euro."
        ),
        "inventore_nome": "Tadao Kikumoto (Roland)",
        "inventore": (
            "Lo stesso capo ingegnere della TR-808 e della TR-909. Progettò "
            "una macchina seria per un pubblico serio: chitarristi da "
            "studio. Il destino decise diversamente, e la colpa fu del suo "
            "difetto più famoso: NESSUNO riusciva a programmarla. Nemmeno "
            "quelli che, anni dopo, ci avrebbero inventato un genere."
        ),
        "come_funziona": (
            "Un solo oscillatore — dente di sega o quadra — dentro un "
            "filtro risonante, con cutoff, resonance, envelope e decay; "
            "accent e slide su ogni nota del sequencer. Il trucco che ha "
            "fatto la storia: girare cutoff e resonance MENTRE il pattern "
            "corre. Ne esce uno «squelch» liquido, gommoso, ipnotico, che "
            "non somiglia a niente. Solo a sé stesso."
        ),
        "richiami": [
            ("FIG. 1", "1 oscillatore"),
            ("FIG. 2", "Filtro risonante"),
            ("FIG. 3", "Accent & slide"),
        ],
        "chi_lusata": [
            {"artista": "Phuture", "nota": "«Acid Tracks» (Trax, 1987): il manifesto dell'acid house", "ig": None},
            {"artista": "DJ Pierre", "nota": "le mani sulle manopole di quella 303", "ig": "djpierrephuture"},
            {"artista": "Ron Hardy", "nota": "la impose al Music Box di Chicago: alla quarta passata, all'alba, la pista capì", "ig": None},
            {"artista": "Marshall Jefferson", "nota": "la fece rallentare a 120 BPM", "ig": None},
        ],
        "menzioni_extra": [
            {"ig": "rolandglobal",
             "riga": "Roland l'ha rifatta nel 2016 come TB-03: @rolandglobal."},
        ],
        "aneddoto": (
            "Spanky dei Phuture la comprò usata — Pierre ricorda 40 "
            "dollari, lui il suo ultimo centesimo, 200. Non sapevano "
            "programmarla: Pierre si mise a girare le manopole mentre il "
            "pattern suonava, e Spanky disse «continua così». «We didn't "
            "know how to program it»: è per questo che ha funzionato."
        ),
        "battuta_dinamo": "Se non sai programmarla, forse stai per inventare qualcosa.",
        "foto": {
            "file": "assets/foto/tb303/principale.jpg",
            "autore": "Alexandre Dulaunoy",
            "licenza": "CC BY-SA 2.0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "Intervista a DJ Pierre — Red Bull Music Academy Daily",
             "url": "https://daily.redbullmusicacademy.com/2012/12/dj-pierre-interview/",
             "data": "2026-08-26"},
            {"titolo": "«Roland TB-303» (Hardware Focus) — Attack Magazine",
             "url": "https://www.attackmagazine.com/technique/hardware-focus/roland-tb-303/",
             "data": "2026-08-26"},
            {"titolo": "«Lifetime Achievement: DJ Pierre and Phuture» — Roland Articles",
             "url": "https://articles.roland.com/lifetime-achievement-dj-pierre-and-phuture/",
             "data": "2026-08-26"},
            {"titolo": "«Acid Tracks» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Acid_Tracks",
             "data": "2026-08-26"},
        ],
        "hashtags": ["#tb303", "#acidhouse", "#roland", "#musicaelettronica", "#synth"],
        "verificata": True,   # verifica completata il 2026-08-26 (vedi fonti)
    },
    {
        "slug": "hammond",
        "numero": 8,
        "serie": "GLI ELETTROMECCANICI",
        "strumento": "Hammond B-3",
        "anno": "1954",
        "luogo": "Chicago, USA",
        "costruttore": "Hammond Organ Co.",
        "specifiche": [
            ("ORGANO HAMMOND", "1935"),
            ("MODELLO B-3", "1954"),
            ("GENERATORE", "91 ruote"),
            ("PESO", "193 kg"),
        ],
        "gancio": "Il suo inventore non sapeva suonare una nota",
        "sottotitolo": "91 ruote dentate davanti a calamite: l'organo di Chicago che conquistò le chiese, il jazz e il rock.",
        "la_macchina": (
            "Nasce nel 1935 come alternativa economica all'organo a canne: "
            "entro il 1966 lo suonano cinquantamila chiese americane. Il "
            "B-3 del 1954, con la percussione al tocco, è IL modello: 193 "
            "chili con panca e pedaliera, più una sessantina di Leslie. Ne "
            "furono costruiti circa 270.000, fino all'ultimo esemplare "
            "elettromeccanico del 1975."
        ),
        "inventore_nome": "Laurens Hammond",
        "inventore": (
            "Un ingegnere di Chicago che costruiva orologi elettrici — e "
            "non sapeva suonare. Per giudicare i suoni si fece prestare le "
            "orecchie del contabile della ditta, W.L. Lahey, organista "
            "diplomato. Il cuore dell'organo è lo stesso motore sincrono "
            "dei suoi orologi: precisione da cronometro, prestata alla "
            "musica."
        ),
        "come_funziona": (
            "Il suono non nasce da valvole o da oscillatori: nasce da 91 "
            "ruote dentate che girano davanti a pickup magnetici — "
            "elettromeccanica pura, l'anello tra il carillon e il synth. I "
            "nove drawbar dosano fondamentale e armonici come i registri di "
            "un organo a canne. E il colpo di scena è l'altoparlante: il "
            "Leslie, che ruota davvero e mette il suono in orbita."
        ),
        "richiami": [
            ("FIG. 1", "91 ruote foniche"),
            ("FIG. 2", "9 drawbar"),
            ("FIG. 3", "Leslie rotante"),
        ],
        "chi_lusata": [
            {"artista": "Le chiese gospel", "nota": "il primo pubblico, e la prima scuola", "ig": None},
            {"artista": "Jimmy Smith", "nota": "la svolta jazz: Newport 1957, «Back at the Chicken Shack»", "ig": None},
            {"artista": "Jon Lord", "nota": "Deep Purple: un C3 (il gemello del B-3) dentro i Marshall", "ig": "deeppurple_official"},
            {"artista": "Booker T.", "nota": "«Green Onions» (1962) — su un M3, il fratello piccolo", "ig": None},
        ],
        "menzioni_extra": [
            {"ig": "officialhammondorgan",
             "riga": "Il marchio suona ancora: @officialhammondorgan."},
        ],
        "aneddoto": (
            "1940: Don Leslie presenta il suo altoparlante rotante alla "
            "Hammond. Laurens ascolta la demo per telefono da Chicago e "
            "dice no. Poi fa cambiare i connettori degli organi per "
            "renderli «a prova di Leslie» e vieta ai rivenditori di "
            "trattarlo. Non servì a niente: i musicisti li vollero insieme "
            "per quarant'anni. I marchi si riunirono solo nel 1980, a "
            "fondatori usciti di scena."
        ),
        "battuta_dinamo": "Anche le macchine hanno storie d'amore complicate.",
        "foto": {
            "file": "assets/foto/hammond/principale.jpg",
            "autore": "bobistraveling",
            "licenza": "CC BY 2.0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "«Hammond organ» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Hammond_organ",
             "data": "2026-08-26"},
            {"titolo": "«The Hammond Story» — hammondorganco.com (sito ufficiale)",
             "url": "https://hammondorganco.com/the-hammond-story-2",
             "data": "2026-08-26"},
            {"titolo": "«Leslie speaker» / «Donald Leslie» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Leslie_speaker",
             "data": "2026-08-26"},
            {"titolo": "«The History of Hammond» — Sound On Sound",
             "url": "https://www.soundonsound.com/people/history-hammond",
             "data": "2026-08-26"},
        ],
        "hashtags": ["#hammond", "#organo", "#b3", "#storiadellamusica", "#musicaelettronica"],
        "verificata": True,   # verifica completata il 2026-08-26 (vedi fonti)
    },
    {
        "slug": "ondes",
        "numero": 9,
        "serie": "LE ORIGINI",
        "strumento": "Ondes Martenot",
        "anno": "1928",
        "luogo": "Parigi, Francia",
        "costruttore": "Maurice Martenot",
        "specifiche": [
            ("ANNO", "1928"),
            ("INVENTORE", "M. Martenot"),
            ("COSTRUITE", "Meno di 300"),
            ("ULTIMA", "1988"),
        ],
        "gancio": "Quel suono che credi un theremin, spesso non lo è",
        "sottotitolo": "Il cugino francese, con tastiera e anello: l'unico elettrofono entrato stabilmente in orchestra.",
        "la_macchina": (
            "Stesso principio del theremin — due frequenze altissime che si "
            "sottraggono — ma con i comandi di uno strumento vero: una "
            "tastiera e un anello da infilare al dito. Per questo i "
            "compositori l'hanno adottata sul serio, mentre il theremin "
            "restava un prodigio da concerto. Ne furono costruite meno di "
            "trecento, a mano, fino al 1988."
        ),
        "inventore_nome": "Maurice Martenot",
        "inventore": (
            "Violoncellista e radiotelegrafista nella Grande Guerra. Tra un "
            "messaggio e l'altro sentiva i battimenti delle valvole radio e "
            "gli parevano bellissimi: passò dieci anni a trasformarli in "
            "musica. Il 20 aprile 1928 li porta all'Opéra di Parigi, "
            "solista lui stesso, con un poema sinfonico scritto apposta da "
            "Dimitrios Levidis."
        ),
        "come_funziona": (
            "La mano destra sceglie l'altezza: sui tasti, oppure facendo "
            "scorrere l'anello lungo il nastro — ed è lì che nascono i "
            "glissandi che sembrano una voce. La sinistra sta nel cassetto, "
            "sulla «touche d'intensité»: preme, e il suono nasce; molla, e "
            "muore. Gli altoparlanti sono strumenti a sé: la Palme ha corde "
            "che risuonano da sole, il Métallique un gong al posto della "
            "membrana."
        ),
        "richiami": [
            ("FIG. 1", "Tastiera + anello"),
            ("FIG. 2", "Touche d'intensité"),
            ("FIG. 3", "Palme e gong"),
        ],
        "chi_lusata": [
            {"artista": "Olivier Messiaen", "nota": "«Turangalîla» (1949), diretta da Bernstein: alle onde, Ginette Martenot", "ig": None},
            {"artista": "Maurice Jarre", "nota": "il deserto di «Lawrence d'Arabia» (1962)", "ig": None},
            {"artista": "Elmer Bernstein", "nota": "«Ghostbusters» (1984): non è un theremin, è un'onda", "ig": None},
            {"artista": "Jonny Greenwood", "nota": "Radiohead, da «Kid A» in poi", "ig": "radiohead"},
        ],
        "menzioni_extra": [],
        "aneddoto": (
            "Esposizione di Parigi 1937: Messiaen scrive «Fête des belles "
            "eaux» per SEI onde Martenot. Non è un concerto da sala — è la "
            "colonna sonora dei giochi d'acqua sulla Senna, diffusa dagli "
            "altoparlanti lungo il fiume, sincronizzata con fontane, luci e "
            "fuochi. L'ultimo movimento disegna in musica il razzo che sale "
            "e le scintille che ricadono."
        ),
        "battuta_dinamo": "Trecento esemplari in un secolo. Anche le macchine possono essere rare.",
        "foto": {
            "file": "assets/foto/ondes/principale.jpg",
            "autore": "andrew garton",
            "licenza": "CC BY-SA 2.0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "«Ondes Martenot» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Ondes_Martenot",
             "data": "2026-08-26"},
            {"titolo": "«The Ondes Martenot» — 120 Years of Electronic Music",
             "url": "https://120years.net/the-ondes-martenotmaurice-martenotfrance1928/",
             "data": "2026-08-26"},
            {"titolo": "«Turangalîla-Symphonie» — Boston Symphony Orchestra",
             "url": "https://www.bso.org/works/messiaen-turangalila-symphonie",
             "data": "2026-08-26"},
            {"titolo": "«Fête des belles eaux» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/F%C3%AAte_des_belles_eaux",
             "data": "2026-08-26"},
        ],
        "hashtags": ["#ondesmartenot", "#musicaelettronica", "#messiaen", "#radiohead", "#storiadellamusica"],
        "verificata": True,   # verifica completata il 2026-08-26 (vedi fonti)
    },
    {
        "slug": "arp2600",
        "numero": 10,
        "serie": "I SINTETIZZATORI",
        "strumento": "ARP 2600",
        "anno": "1971",
        "luogo": "Massachusetts, USA",
        "costruttore": "ARP Instruments",
        "specifiche": [
            ("ANNO", "1971"),
            ("COSTRUTTORE", "ARP"),
            ("OSCILLATORI", "3 VCO"),
            ("LISTINO", "2.600 $"),
        ],
        "gancio": "La valigia che ha dato la voce a R2-D2",
        "sottotitolo": "Semi-modulare, con gli altoparlanti dentro: il synth pensato anche per le scuole.",
        "la_macchina": (
            "Una valigia che si apre e diventa un laboratorio. È "
            "semi-modulare: i moduli sono già collegati fra loro, e i cavi "
            "servono solo se vuoi cambiare le regole. Ha gli altoparlanti "
            "incorporati e un riverbero a molla, perché ARP lo vendeva "
            "anche a scuole e università: bastava aprirlo sulla cattedra e "
            "l'aula sentiva."
        ),
        "inventore_nome": "Alan R. Pearlman",
        "inventore": (
            "Le sue iniziali sono il nome della ditta: A.R.P. Ingegnere "
            "elettronico con un passato nei circuiti per la NASA, progettò "
            "il 2600 con Dennis Colin. Il primo filtro, il 4012, ricalcava "
            "da vicino il ladder brevettato da Moog: sotto minaccia di "
            "azione legale — mai una causa vera in tribunale — ARP dovette "
            "riprogettarlo da capo."
        ),
        "come_funziona": (
            "Tre oscillatori, filtro, inviluppi e amplificatore già cablati "
            "in fila: si accende e suona, senza toccare un cavo. Ma sopra "
            "ogni modulo ci sono i jack, e lì comincia il gioco: puoi far "
            "comandare il filtro dall'inviluppo, o dal rumore, o da sé "
            "stesso. Il sample & hold e il filtro in auto-oscillazione sono "
            "le due manopole da cui è uscita mezza fantascienza."
        ),
        "richiami": [
            ("FIG. 1", "3 VCO"),
            ("FIG. 2", "Semi-modulare"),
            ("FIG. 3", "Altoparlanti interni"),
        ],
        "chi_lusata": [
            {"artista": "Edgar Winter", "nota": "«Frankenstein» (1972): se lo mise a tracolla, inventando il keytar", "ig": None},
            {"artista": "Joe Zawinul", "nota": "due ARP 2600 nei Weather Report di «Black Market» (1976)", "ig": None},
            {"artista": "Jean-Michel Jarre", "nota": "il tema di «Oxygène IV» (1976)", "ig": "jeanmicheljarre"},
            {"artista": "Stevie Wonder", "nota": "tra i primi: il suo pannello era etichettato in Braille", "ig": None},
        ],
        "menzioni_extra": [
            {"ig": "korgofficial",
             "riga": "Oggi lo rifà @korgofficial, con la supervisione di un fondatore ARP."},
        ],
        "aneddoto": (
            "1977: Ben Burtt deve dare una voce a un robot che non parla. "
            "Prende un ARP 2600, ci mescola la propria voce e ottiene un "
            "suono «per metà elettronico e per metà umano». Quel pianto "
            "acuto che tutti riconoscono — R2-D2 — è mezzo circuito e mezzo "
            "essere umano. Ci mise sei mesi."
        ),
        "battuta_dinamo": "Metà macchina e metà persona. Come tutte le voci migliori.",
        "foto": {
            "file": "assets/foto/arp2600/principale.jpg",
            "autore": "Ville Hyvönen",
            "licenza": "CC BY-SA 2.0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "«ARP 2600» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/ARP_2600",
             "data": "2026-08-26"},
            {"titolo": "«Hardware Wars: the gear behind Star Wars» — Attack Magazine",
             "url": "https://www.attackmagazine.com/technique/hardware-focus/hardware-wars-the-gear-behind-the-sounds-of-star-wars/",
             "data": "2026-08-26"},
            {"titolo": "«The ARP 2600: Evolution and Revolution» — Alan R. Pearlman Foundation",
             "url": "https://artsandculture.google.com/story/the-arp-2600-evolution-and-revolution-alanrpearlmanfoundation/xAVxhDm7Hp9CaA",
             "data": "2026-08-26"},
            {"titolo": "«Frankenstein» (Edgar Winter) — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Frankenstein_(instrumental)",
             "data": "2026-08-26"},
        ],
        "hashtags": ["#arp2600", "#synth", "#starwars", "#musicaelettronica", "#r2d2"],
        "verificata": True,   # verifica completata il 2026-08-26 (vedi fonti)
    },
    {
        "slug": "vcs3",
        "numero": 11,
        "serie": "I SINTETIZZATORI",
        "strumento": "EMS VCS3",
        "anno": "1969",
        "luogo": "Putney, Londra",
        "costruttore": "EMS",
        "specifiche": [
            ("ANNO", "1969"),
            ("COSTRUTTORE", "EMS"),
            ("PATCH", "Matrice 16×16"),
            ("LISTINO", "£330"),
        ],
        "gancio": "Vendette la tiara della moglie per comprare un computer",
        "sottotitolo": "«The Putney»: il primo synth compatto ed economico d'Europa, nato in un capanno sul Tamigi.",
        "la_macchina": (
            "Mentre in America i sintetizzatori erano armadi da migliaia di "
            "dollari, a Londra esce una scatola di legno da 330 sterline. "
            "Niente foresta di cavi: una matrice di fori dove infili degli "
            "spinotti, e ogni spinotto è un collegamento. Piccolo, "
            "trasportabile, alla portata di una band: è il primo synth "
            "compatto ed economico d'Europa."
        ),
        "inventore_nome": "Peter Zinovieff e soci",
        "inventore": (
            "Zinovieff, figlio di aristocratici russi fuggiti dalla "
            "rivoluzione, teneva in un capanno del giardino di casa a "
            "Putney due computer PDP-8 battezzati Sofka e Leo, come i suoi "
            "genitori. L'elettronica del VCS3 è di David Cockerell, il "
            "mobile di Tristram Cary, compositore che scriveva musiche per "
            "Doctor Who."
        ),
        "come_funziona": (
            "Due oscillatori più un terzo lento, filtro, generatore di "
            "inviluppo, ring modulator e un riverbero a molla. Il cuore è "
            "la matrice: sedici righe per sedici colonne, e ogni spinotto "
            "decide chi comanda chi. Ci si perde volentieri — è uno "
            "strumento che si esplora più che suonarlo, e infatti è finito "
            "più negli effetti e nei paesaggi sonori che nelle melodie."
        ),
        "richiami": [
            ("FIG. 1", "Matrice a spinotti"),
            ("FIG. 2", "3 oscillatori"),
            ("FIG. 3", "Ring modulator"),
        ],
        "chi_lusata": [
            {"artista": "Franco Battiato", "nota": "«Fetus» (1972) e «Pollution»: tra i primi in Italia, andò a Londra a prenderlo", "ig": None},
            {"artista": "Brian Eno", "nota": "Roxy Music: non lo suonava, ci passava dentro gli altri", "ig": "brianeno"},
            {"artista": "White Noise", "nota": "«An Electric Storm» (1969), con Delia Derbyshire", "ig": None},
            {"artista": "BBC Radiophonic Workshop", "nota": "gli effetti di mezza fantascienza britannica", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": (
            "Per pagarsi il primo computer, Zinovieff vendette la tiara "
            "nuziale della moglie: quattromila sterline, finite in un "
            "calcolatore installato nel capanno del giardino. Sosteneva "
            "fosse il primo computer al mondo in una casa privata. Poi "
            "un'alluvione del Tamigi si prese lo studio."
        ),
        "battuta_dinamo": "Una tiara per un computer. Ognuno ha i suoi gioielli.",
        "foto": {
            "file": "assets/foto/vcs3/principale.jpg",
            "autore": "Alexander Baxevanis",
            "licenza": "CC BY 2.0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "«All About EMS» (parti 1-2) — Sound On Sound",
             "url": "https://www.soundonsound.com/music-business/all-about-ems-part-1",
             "data": "2026-08-26"},
            {"titolo": "«Peter Zinovieff» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Peter_Zinovieff",
             "data": "2026-08-26"},
            {"titolo": "«Fetus» (Franco Battiato) — Wikipedia (IT)",
             "url": "https://it.wikipedia.org/wiki/Fetus",
             "data": "2026-08-26"},
            {"titolo": "«Wonderful Things: VCS3 synthesiser» — Science Museum",
             "url": "https://blog.sciencemuseum.org.uk/wonderful-things-vcs3-synthesiser/",
             "data": "2026-08-26"},
        ],
        "hashtags": ["#vcs3", "#ems", "#battiato", "#synth", "#musicaelettronica"],
        "verificata": True,   # verifica completata il 2026-08-26 (vedi fonti)
    },
    {
        "slug": "farfisa",
        "numero": 12,
        "serie": "GLI ORGANI",
        "strumento": "Farfisa Compact",
        "anno": "1964",
        "luogo": "Camerano, Ancona",
        "costruttore": "Farfisa",
        "specifiche": [
            ("ANNO", "1964"),
            ("ORIGINE", "Ancona"),
            ("TECNOLOGIA", "Transistor"),
            ("DIPENDENTI", "1.600 nel '66"),
        ],
        "gancio": "Nato dalle fisarmoniche marchigiane, finito nei dischi che conosci",
        "sottotitolo": "L'organo portatile di Camerano: dal beat al soul, con quel timbro che taglia come una lama.",
        "la_macchina": (
            "Un organo che sta su due gambe pieghevoli e si carica in "
            "furgone: nel 1964 è quello che ogni gruppo cerca. Costa la "
            "metà del rivale inglese e ha un timbro nasale, tagliente, che "
            "buca qualsiasi muro di chitarre. Il segreto è nella "
            "provenienza: gli stessi tecnici che elettrificavano le "
            "fisarmoniche marchigiane."
        ),
        "inventore_nome": "FAbbriche Riunite FISArmoniche",
        "inventore": (
            "Il nome è un acronimo: nel 1946, a Camerano in provincia di "
            "Ancona, si fondono tre storiche fabbriche di fisarmoniche — "
            "Settimio Soprani, Scandalli, Frontalini. Vent'anni dopo la "
            "Farfisa ha 1.600 dipendenti e manda negli Stati Uniti il "
            "settanta per cento della produzione: per un periodo è il più "
            "grande costruttore europeo di strumenti elettronici."
        ),
        "come_funziona": (
            "Non ha ruote che girano come l'Hammond: qui il suono nasce da "
            "oscillatori a transistor, uno per nota, filtrati dalle "
            "linguette dei registri — flauto, oboe, tromba. E c'è il "
            "«Multi-Tone Booster», il circuito che accende il timbro e lo "
            "rende ronzante. Curiosità: nei primi Compact il riverbero era "
            "ancora a valvole."
        ),
        "richiami": [
            ("FIG. 1", "Oscillatori a transistor"),
            ("FIG. 2", "Multi-Tone Booster"),
            ("FIG. 3", "Portatile e pieghevole"),
        ],
        "chi_lusata": [
            {"artista": "Pink Floyd", "nota": "Rick Wright, «Interstellar Overdrive» (1967): un Compact Duo", "ig": "pinkfloyd"},
            {"artista": "Percy Sledge", "nota": "«When a Man Loves a Woman» (1966): l'organo è un Farfisa, non un Hammond", "ig": None},
            {"artista": "B-52s", "nota": "Kate Pierson in «Rock Lobster»: il suo Compact è al Metropolitan", "ig": None},
            {"artista": "Blondie", "nota": "Jimmy Destri lo fece diventare il colore della band", "ig": "blondieofficial"},
        ],
        "menzioni_extra": [
            {"ig": "museofisarmonicacastelfidardo",
             "riga": "La storia comincia lì: @museofisarmonicacastelfidardo."},
        ],
        "aneddoto": (
            "L'intro d'organo di «When a Man Loves a Woman» — numero uno in "
            "America nel 1966, la ballata soul per definizione — la "
            "credono tutti un maestoso Hammond. È invece un piccolo Farfisa "
            "rosso lucido, fatto in provincia di Ancona. Disse Spooner "
            "Oldham che lo suonò: quel booster «suonava come mille "
            "calabroni». Oggi il marchio sopravvive sui citofoni."
        ),
        "battuta_dinamo": "Made in Marche, suonato ovunque. Nessuno se n'è accorto.",
        "foto": {
            "file": "assets/foto/farfisa/principale.jpg",
            "autore": "TheTankman",
            "licenza": "CC BY-SA 4.0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "Farfisa — SIUSA, Sistema Informativo Unificato Soprintendenze Archivistiche",
             "url": "https://siusa-archivi.cultura.gov.it/cgi-bin/pagina.pl?TipoPag=prodente&Chiave=50568",
             "data": "2026-08-26"},
            {"titolo": "«La storia della Farfisa» — Il Post",
             "url": "https://www.ilpost.it/2024/08/30/farfisa-storia/",
             "data": "2026-08-26"},
            {"titolo": "«When a Man Loves a Woman» (crediti) — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/When_a_Man_Loves_a_Woman_(song)",
             "data": "2026-08-26"},
            {"titolo": "«Dan Penn and Spooner Oldham: Old Souls» — No Depression",
             "url": "https://nodepression.org/dan-penn-and-spooner-oldham-old-souls/",
             "data": "2026-08-26"},
        ],
        "hashtags": ["#farfisa", "#organo", "#madeinitaly", "#storiadellamusica", "#musicaelettronica"],
        "verificata": True,   # verifica completata il 2026-08-26 (vedi fonti)
    },
    # NOTA EDITORIALE (27/08/2026, scheda "stylophone"): la faccia della
    # campagna pubblicitaria dello Stylophone nel Regno Unito fu un noto
    # presentatore televisivo, poi condannato per reati sessuali. Il fatto
    # storico e' vero ma non entra nella scheda: non serve a spiegare la
    # macchina e trascinerebbe la pagina dove non deve andare. Non e' una
    # dimenticanza — se una prossima sessione lo "scopre", sappia che la
    # scelta e' stata presa apposta.
    # ---------------------------------------------------------------- 13
    {
        "slug": "trautonium",
        "numero": 13,
        "serie": "LE ORIGINI",
        "strumento": "Trautonium",
        "anno": "1930",
        "luogo": "Berlino",
        "costruttore": "Friedrich Trautwein",
        "specifiche": [
            ("ANNO", "1930"),
            ("ORIGINE", "Berlino"),
            ("TASTIERA", "Nessuna: un filo"),
            ("VENDUTI", "Poche centinaia"),
        ],
        "gancio": "Gli uccelli di Hitchcock non sono uccelli: sono questa macchina",
        "sottotitolo": "Niente tasti: un filo teso sopra una barra di metallo, e il dito che sceglie la nota.",
        "la_macchina": "Una cassa di legno con sopra un filo teso su una barra metallica. Si preme il filo con il dito: dove lo premi, quella è la nota. Non ci sono tasti, quindi non ci sono note fisse — il quarto di tono, il glissando e il vibrato non sono effetti, sono il modo normale di suonarlo. La Telefunken provò a venderne una versione domestica dal 1933, il Volkstrautonium: ne uscirono poche centinaia e fu un fiasco. Trautwein lasciò perdere.",
        "inventore_nome": "Friedrich Trautwein",
        "inventore": "Trautwein lo costruisce nel 1930 alla Rundfunkversuchsstelle, il laboratorio di radio e musica della Musikhochschule di Berlino. Paul Hindemith ci scrive sopra dei pezzi e lo porta in concerto; un suo allievo di composizione, Oskar Sala, se ne innamora, va a studiare fisica per capirlo meglio e ci passerà i settant'anni successivi. Nel 1948 lo trasforma nel Mixtur-Trautonium, che a differenza dell'originale può suonare più voci insieme.",
        "come_funziona": "Il filo è una resistenza. Premendolo contro la barra si chiude il circuito in quel punto preciso: più avanti premi, meno resistenza, più alta la nota. La pressione del dito, in più, regola il volume. La trovata di Sala sono le subarmoniche: invece di sommare multipli della frequenza fondamentale, come fa qualsiasi organo, il Mixtur ne genera le frazioni. È un modo di costruire il timbro che non assomiglia a niente — e infatti il risultato non assomiglia a niente.",
        "richiami": [
            ("FIG. 1", "Filo su barra metallica"),
            ("FIG. 2", "Pressione = volume"),
            ("FIG. 3", "Subarmoniche"),
        ],
        "chi_lusata": [
            {"artista": "Paul Hindemith", "nota": "Ci scrisse un concerto e dei trii: fu lui a portarlo in sala da concerto", "ig": None},
            {"artista": "Oskar Sala", "nota": "Fisico e compositore: di fatto l'unico al mondo che sapesse suonarlo", "ig": None},
            {"artista": "Alfred Hitchcock", "nota": "«Gli uccelli» (1963): nessuna colonna sonora, solo questa macchina", "ig": None},
        ],
        "menzioni_extra": [
            {"ig": "deutschesmuseum",
             "riga": "Il fondo Oskar Sala oggi sta al @deutschesmuseum di Monaco."},
        ],
        "aneddoto": "«Gli uccelli» di Hitchcock non ha colonna sonora. Non una nota: Bernard Herrmann, il compositore di tutti i suoi film, compare nei titoli solo come «consulente del suono». Ogni stormire, ogni stridio, ogni ala che sbatte è Oskar Sala a Berlino, sul suo Mixtur-Trautonium, insieme a Remi Gassmann. Hitchcock quello strumento lo aveva sentito da giovane alla radio tedesca e se l'era ricordato per trent'anni.",
        "battuta_dinamo": "Il film più spaventoso del secolo non ha musica. Ha una macchina che urla.",
        "foto": {
            "file": "assets/foto/trautonium/principale.jpg",
            "autore": "Morn the Gorn",
            "licenza": "CC BY-SA 3.0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "«Trautonium» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Trautonium", "data": "2026-08-27"},
            {"titolo": "«Oskar Sala» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Oskar_Sala", "data": "2026-08-27"},
            {"titolo": "«The Birds» (suono e musica) — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/The_Birds_(film)", "data": "2026-08-27"},
            {"titolo": "«How the Bird Sound Effects in The Birds Were Created» — Open Culture",
             "url": "https://www.openculture.com/2026/08/how-the-bird-sound-effects-in-alfred-hitchcocks-the-birds-were-created-with-a-pioneering-electronic-instrument-the-trautonium.html",
             "data": "2026-08-27"},
        ],
        "hashtags": ["#trautonium", "#oskarsala", "#hitchcock", "#storiadellamusica", "#musicaelettronica"],
        "verificata": True,
    },
    # ---------------------------------------------------------------- 14
    {
        "slug": "fonologia",
        "numero": 14,
        "serie": "GLI STUDI",
        "strumento": "Studio di Fonologia della RAI",
        "anno": "1955",
        "luogo": "Milano, corso Sempione",
        "costruttore": "RAI",
        "specifiche": [
            ("ANNO", "1955"),
            ("ORIGINE", "Milano"),
            ("OSCILLATORI", "Nove"),
            ("CHIUSO", "1983"),
        ],
        "gancio": "La terza officina elettronica d'Europa stava in una stanza della RAI di Milano",
        "sottotitolo": "Nove oscillatori, un tecnico paziente e mezzo Novecento della musica passato di lì.",
        "la_macchina": "Non uno strumento: una stanza intera. Generatori di onde sinusoidali e quadre, un generatore di impulsi, uno di rumore bianco, modulatori d'ampiezza e di frequenza, filtri d'ottava e passabanda, apparecchi per l'eco. Quasi tutto costruito lì dentro, perché sul mercato non esisteva. Il vanto erano i nove oscillatori: un numero enorme per il 1955, e la ragione per cui a Milano si poteva fare ciò che altrove no.",
        "inventore_nome": "Berio, Maderna e Lietti",
        "inventore": "Lo vollero due compositori, Luciano Berio e Bruno Maderna, e la RAI pagò. A progettarlo e costruirlo fu l'ingegnere Alfredo Lietti, che inventava gli apparecchi man mano che i musicisti chiedevano cose impossibili. Alla console stava il tecnico Marino Zuccheri, le mani che per ventotto anni trasformarono le idee dei compositori in nastro. Prima di Milano esistevano solo Colonia e Parigi.",
        "come_funziona": "Non si suona: si costruisce. Si genera una frequenza, la si incide su nastro magnetico, si taglia il nastro con la lametta, si incolla, si sovrappone. Un secondo di musica può voler dire un pomeriggio di forbici. I nove oscillatori permettono di impilare nove frequenze insieme; il selettore d'ampiezza disegna l'attacco e la coda di ogni suono; i filtri scavano il timbro togliendo quello che non serve.",
        "richiami": [
            ("FIG. 1", "Nove oscillatori"),
            ("FIG. 2", "Filtri e selettore"),
            ("FIG. 3", "Nastro e lametta"),
        ],
        "chi_lusata": [
            {"artista": "Luciano Berio", "nota": "«Thema (Omaggio a Joyce)», 1958: la voce di Cathy Berberian che legge l'Ulisse, fatta a pezzi", "ig": None},
            {"artista": "Bruno Maderna", "nota": "Con Berio firma «Ritratto di città» (1955), il primo lavoro uscito dallo Studio", "ig": None},
            {"artista": "Luigi Nono", "nota": "Ci porta la politica: le voci degli operai dentro il nastro", "ig": None},
            {"artista": "John Cage", "nota": "Invitato da Berio, ci realizza «Fontana Mix» fra il novembre 1958 e il 1959", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": "Mentre montava «Fontana Mix» a Milano, John Cage andò a «Lascia o raddoppia?». Non come musicista: come esperto di funghi. Cinque puntate fra il gennaio e il febbraio 1959, con Mike Bongiorno che lo interrogava sulla micologia, e fra una domanda e l'altra Cage eseguiva i suoi pezzi in prima serata. Vinse cinque milioni di lire. L'avanguardia europea, finanziata da un quiz televisivo italiano.",
        "battuta_dinamo": "Il futuro della musica pagato da un quiz sui funghi. Non chiedetemi di spiegarlo.",
        "foto": {
            "file": "assets/foto/fonologia/principale.jpg",
            "autore": "Stefano Stabile (mod. Clusternote)",
            "licenza": "CC BY-SA 3.0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "Studio di Fonologia Musicale di Milano della RAI — LIM, Università degli Studi di Milano",
             "url": "https://fonologia.lim.di.unimi.it/introduzione.php", "data": "2026-08-27"},
            {"titolo": "«Studio di fonologia musicale di Radio Milano» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Studio_di_fonologia_musicale_di_Radio_Milano", "data": "2026-08-27"},
            {"titolo": "Cage in Italia, cronologia 1958-1959 — johncage.it",
             "url": "https://www.johncage.it/en/chronology.html", "data": "2026-08-27"},
            {"titolo": "«La volta che John Cage andò a Lascia o raddoppia?» — Il Post",
             "url": "https://www.ilpost.it/2012/09/05/john-cage-mike-bongiorno-lascia-o-raddoppia/", "data": "2026-08-27"},
        ],
        "hashtags": ["#studiodifonologia", "#lucianoberio", "#johncage", "#milano", "#musicaelettronica"],
        "verificata": True,
    },
    # ---------------------------------------------------------------- 15
    {
        "slug": "stylophone",
        "numero": 15,
        "serie": "I GIOCATTOLI",
        "strumento": "Stylophone",
        "anno": "1968",
        "luogo": "Londra",
        "costruttore": "Dubreq",
        "specifiche": [
            ("ANNO", "1968"),
            ("ORIGINE", "Londra"),
            ("VOCI", "Una sola"),
            ("VENDUTI", "3 milioni"),
        ],
        "gancio": "Un giocattolo per bambini. Ci è nato sopra il pezzo che ha lanciato Bowie",
        "sottotitolo": "Tastiera di rame stampata, una penna al posto delle dita, tre milioni di pezzi.",
        "la_macchina": "Sta in una mano. Una scatoletta con un altoparlante, una manopola di accordatura, un interruttore per il vibrato e una tastiera che non è una tastiera: è un circuito stampato, con i tasti disegnati in rame. Si suona con un pennino legato alla scatola. Una nota per volta, nessuna dinamica, intonazione che va per conto suo. Venduto come giocattolo: tre milioni di pezzi in sette anni, poi fuori produzione nel 1975 e di nuovo in commercio dal 2007.",
        "inventore_nome": "Brian Jarvis",
        "inventore": "Brian Jarvis lavorava alla Dubreq, a Londra. Nel 1967 stava riparando il pianoforte giocattolo della nipote quando gli venne l'idea: e se al posto dei tasti meccanici ci mettessi dell'elettronica? Un anno dopo lo Stylophone era in produzione. Non nasce in un laboratorio di ricerca né in un conservatorio: nasce su un tavolo di casa, da un giocattolo rotto.",
        "come_funziona": "Ogni tasto di rame è collegato all'oscillatore attraverso una resistenza di valore diverso. Il pennino chiude il circuito: appoggiandolo su un tasto scegli quale resistenza entra in gioco, e quindi quale nota esce. Tutto qui. L'unica espressione disponibile è l'interruttore del vibrato. Il timbro ronzante e sporco che riconosci non è una scelta di progetto: è quello che succede quando un oscillatore così semplice non sta perfettamente in accordatura.",
        "richiami": [
            ("FIG. 1", "Tastiera in rame stampato"),
            ("FIG. 2", "Pennino = interruttore"),
            ("FIG. 3", "Una resistenza per nota"),
        ],
        "chi_lusata": [
            {"artista": "David Bowie", "nota": "«Space Oddity»: la melodia la compose sullo Stylophone, poi lo suonò sul disco", "ig": "davidbowie"},
            {"artista": "Marc Bolan", "nota": "Fu lui a metterglielo in mano: «Ti piacciono queste cose, fanne qualcosa»", "ig": None},
            {"artista": "Kraftwerk", "nota": "Fra i primi a prendere sul serio un giocattolo da tre soldi", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": "Tony Visconti, il produttore di Bowie, si rifiutò di produrre «Space Oddity»: la chiamò una trovata per lucrare sullo sbarco sulla Luna. Il pezzo lo produsse Gus Dudgeon; Visconti fece il resto dell'album. Registrata il 20 giugno 1969, uscì l'11 luglio: cinque giorni prima che l'Apollo 11 partisse davvero. Fu il primo successo di Bowie, e c'è dentro un giocattolo suonato con una penna.",
        "battuta_dinamo": "Il produttore la chiamò una trovata pubblicitaria. Aveva ragione. Ha perso lo stesso.",
        "foto": {
            "file": "assets/foto/stylophone/principale.jpg",
            "autore": "Alex Ashbourne",
            "licenza": "CC BY-SA 3.0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "«Stylophone» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Stylophone", "data": "2026-08-27"},
            {"titolo": "History — Stylophone / Dubreq (sito ufficiale)",
             "url": "https://stylophone.com/history/", "data": "2026-08-27"},
            {"titolo": "«Space Oddity» (registrazione e crediti) — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Space_Oddity", "data": "2026-08-27"},
        ],
        "hashtags": ["#stylophone", "#davidbowie", "#spaceoddity", "#storiadellamusica", "#musicaelettronica"],
        "verificata": True,
    },
    # ---------------------------------------------------------------- 16
    {
        "slug": "spaceecho",
        "numero": 16,
        "serie": "GLI EFFETTI",
        "strumento": "Roland RE-201 Space Echo",
        "anno": "1974",
        "luogo": "Osaka",
        "costruttore": "Roland",
        "specifiche": [
            ("ANNO", "1974"),
            ("ORIGINE", "Osaka"),
            ("TESTINE", "Tre in lettura"),
            ("RIVERBERO", "A molla"),
        ],
        "gancio": "Un nastro che gira a vuoto in una scatola: così il dub ha imparato a rimbombare",
        "sottotitolo": "Non uno strumento ma una macchina per lo spazio: tre testine, un anello di nastro, tre molle.",
        "la_macchina": "Un anello di nastro da un quarto di pollice che non sta su bobine: viene lasciato cadere sciolto dentro una camera, senza tensione, e gira all'infinito. Sopra ci sono tre testine di lettura a distanze diverse e un selettore a undici posizioni che le combina, più un riverbero a tre molle e i controlli di tono. Esce nel 1974 e rimane in catalogo per anni: quasi ogni studio del mondo ne ha avuto uno.",
        "inventore_nome": "Ikutaro Kakehashi",
        "inventore": "Kakehashi aveva già costruito eco a nastro alla Ace Tone prima di fondare la Roland a Osaka, nel 1972. Il problema di tutte le macchine precedenti era lo stesso: il nastro, teso e tirato, si consumava in fretta e la macchina moriva. La soluzione fu smettere di tirarlo. Nastro lento, lasco, in un cassetto: dura, e nel frattempo suona meglio.",
        "come_funziona": "Una testina incide il suono sul nastro. Poco dopo la prima testina di lettura lo ritrova, poi la seconda, poi la terza: la distanza fra la testina che scrive e quelle che leggono è il tempo dell'eco. Alzando il ritorno, l'eco si rimangia se stessa e cresce invece di spegnersi, fino a partire in oscillazione. Quel fischio che sale è il difetto della macchina — ed è esattamente il motivo per cui la comprano ancora.",
        "richiami": [
            ("FIG. 1", "Anello di nastro senza bobine"),
            ("FIG. 2", "Tre testine di lettura"),
            ("FIG. 3", "Riverbero a molla"),
        ],
        "chi_lusata": [
            {"artista": "King Tubby", "nota": "A Kingston lo usa come strumento, non come effetto: nasce il dub", "ig": None},
            {"artista": "Lee «Scratch» Perry", "nota": "Al Black Ark ci costruisce sopra un intero modo di mixare", "ig": None},
            {"artista": "Pink Floyd", "nota": "David Gilmour: l'eco che allarga la chitarra fino all'orizzonte", "ig": "pinkfloyd"},
            {"artista": "Portishead", "nota": "Trent'anni dopo, la stessa scatola per lo stesso motivo: il nastro sporca", "ig": None},
        ],
        "menzioni_extra": [
            {"ig": "rolandglobal",
             "riga": "Chi l'ha costruita esiste ancora: @rolandglobal."},
        ],
        "aneddoto": "In Giamaica non lo trattarono da effetto. King Tubby e Lee Perry ci mettevano le mani sopra mentre il mix andava: alzavano il ritorno finché la macchina non partiva a ululare, poi lo riabbassavano al momento giusto. Il dub non è un genere suonato, è un genere mixato — ed è nato da quello che questa scatola fa quando la spingi oltre il punto in cui dovrebbe funzionare.",
        "battuta_dinamo": "Mi hanno comprato per fare l'eco. Ho finito per inventare un genere musicale.",
        "foto": {
            "file": "assets/foto/spaceecho/principale.jpg",
            "autore": "1904.CC",
            "licenza": "CC BY 4.0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "«Why the RE-201 Space Echo Remains a Classic» — BOSS/Roland",
             "url": "https://articles.boss.info/why-the-re-201-space-echo-remains-a-classic/", "data": "2026-08-27"},
            {"titolo": "«Studio Icons: Roland RE-201 Space Echo» — MusicTech",
             "url": "https://musictech.com/reviews/roland-re201-space-echo/", "data": "2026-08-27"},
            {"titolo": "«Roland Space Echo» — Attack Magazine",
             "url": "https://www.attackmagazine.com/technique/hardware-focus/roland-space-echo/", "data": "2026-08-27"},
        ],
        "hashtags": ["#spaceecho", "#roland", "#dub", "#kingtubby", "#musicaelettronica"],
        "verificata": True,
    },
    # ---------------------------------------------------------------- 17
    {
        "slug": "ms20",
        "numero": 17,
        "serie": "I SINTETIZZATORI",
        "strumento": "Korg MS-20",
        "anno": "1978",
        "luogo": "Tokyo",
        "costruttore": "Korg",
        "specifiche": [
            ("ANNO", "1978"),
            ("ORIGINE", "Tokyo"),
            ("FILTRI", "Due, in serie"),
            ("USCITA", "1978-1983"),
        ],
        "gancio": "Il sintetizzatore che si fa suonare dalla tua voce, se gliela colleghi",
        "sottotitolo": "Semimodulare ed economico: il pannello di patch che ha insegnato la sintesi a una generazione.",
        "la_macchina": "Due oscillatori, due filtri in serie — uno passa-alto e uno passa-basso — e a destra un pannello di prese con i cavetti. È semimodulare: suona anche senza collegare niente, ma ogni collegamento interno si può interrompere e rifare a mano. Costava poco e finì nelle scuole di mezzo Giappone. In produzione dal 1978 al 1983; nel 2013 la Korg lo ha rifatto all'86% delle dimensioni originali.",
        "inventore_nome": "Fumio Mieda",
        "inventore": "Mieda alla Korg aveva già firmato l'Uni-Vibe, il pedale che fa girare il suono. Con l'MS-20 guida un progetto con un'idea precisa: prendere il pannello di patch dei modulari — roba da università e da studi ricchi — e metterlo su uno strumento che uno studente possa permettersi. Non è un modulare in miniatura: è un modulare per chi non ne avrà mai uno.",
        "come_funziona": "La parte che nessuno si aspetta è l'ESP, il processore di segnale esterno. Ci colleghi una chitarra, un microfono, un rullante: l'ESP estrae l'altezza del suono e la trasforma in tensione di controllo, e l'attacco in un impulso di innesco. A quel punto il sintetizzatore suona quello che hai cantato. In più i due filtri, con quella risonanza sporca e stridula che è la sua impronta digitale.",
        "richiami": [
            ("FIG. 1", "Pannello di patch"),
            ("FIG. 2", "Due filtri in serie"),
            ("FIG. 3", "ESP: audio in tensione"),
        ],
        "chi_lusata": [
            {"artista": "Aphex Twin", "nota": "Uno dei suoi strumenti di partenza, e si sente da quale filtro arriva", "ig": None},
            {"artista": "Daft Punk", "nota": "Nel corredo francese degli anni Novanta c'è quasi sempre", "ig": None},
            {"artista": "The Chemical Brothers", "nota": "Bassi e stridori: l'MS-20 dà il meglio quando lo maltratti", "ig": None},
            {"artista": "Vangelis", "nota": "Dall'altra parte del catalogo: lo stesso strumento, tutt'altra musica", "ig": None},
        ],
        "menzioni_extra": [
            {"ig": "korgofficial",
             "riga": "Lo ha rifatto uguale trentacinque anni dopo: @korgofficial."},
        ],
        "aneddoto": "L'MS-20 nasce come strumento didattico: costa poco, il pannello di patch mostra a occhio come è fatta la sintesi, entra nelle scuole. Poi passa di moda e finisce nei negozi dell'usato a prezzi da svendita — ed è lì che se lo comprano quelli che stanno inventando la techno. Nel 2013 la Korg lo rimette in produzione partendo dai disegni originali, e poi lo vende perfino in kit, da montare a mano.",
        "battuta_dinamo": "Collegami la voce e ti rispondo. Non sempre in modo gentile.",
        "foto": {
            "file": "assets/foto/ms20/principale.jpg",
            "autore": "Wilfredor",
            "licenza": "CC0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "«Korg MS-20» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Korg_MS-20", "data": "2026-08-27"},
            {"titolo": "«The Story of the KORG MS-20 Synthesizer» — Guitar Center Riffs",
             "url": "https://www.guitarcenter.com/riffs/gear-tips/keyboards--midi/korg-ms-20-history-overview", "data": "2026-08-27"},
            {"titolo": "MS-20 Kit, funzioni dell'External Signal Processor — Korg (sito ufficiale)",
             "url": "https://www.korg.com/us/products/dj/ms_20kit/page_1.php", "data": "2026-08-27"},
            {"titolo": "MS-20 mini (86% dell'originale, 1978) — Korg (sito ufficiale)",
             "url": "https://www.korg.com/us/products/synthesizers/ms_20mini/", "data": "2026-08-27"},
        ],
        "hashtags": ["#korgms20", "#korg", "#sintetizzatore", "#storiadellamusica", "#musicaelettronica"],
        "verificata": True,
    },
    # ---------------------------------------------------------------- 18
    {
        "slug": "lm1",
        "numero": 18,
        "serie": "LE DRUM MACHINE",
        "strumento": "Linn LM-1",
        "anno": "1980",
        "luogo": "Los Angeles",
        "costruttore": "Linn Electronics",
        "specifiche": [
            ("ANNO", "1980"),
            ("ORIGINE", "Los Angeles"),
            ("CAMPIONI", "8 bit / 28 kHz"),
            ("COSTRUITI", "Circa 500"),
        ],
        "gancio": "La prima drum machine con dentro una batteria vera. Costava come un'automobile",
        "sottotitolo": "Dodici suoni campionati, nessun piatto, cinquecento esemplari: il suono degli anni Ottanta.",
        "la_macchina": "Dodici suoni presi da una batteria vera, registrati in digitale a 8 bit e messi in memoria: cassa, rullante, charleston aperto e chiuso, tom, congas, cabasa, tamburello, campanaccio, claves, battimani. Programmabile, con un'uscita separata per ogni suono così il fonico può trattarli uno per uno. Cinquemila dollari nel 1980. Ne furono costruite circa cinquecento.",
        "inventore_nome": "Roger Linn",
        "inventore": "Roger Linn era un chitarrista e un tecnico di Los Angeles, stufo di drum machine che facevano rumori da organetto. La sua idea non era sintetizzare la batteria: era registrarla. Chiamò un amico batterista, Art Wood, lo mise a suonare colpo per colpo, campionò quei colpi e li chiuse dentro la memoria della macchina. Nello stesso anno, a Osaka, la Roland faceva l'esatto contrario con la TR-808.",
        "come_funziona": "Ogni suono è una registrazione digitale: 8 bit di risoluzione, 28.000 campioni al secondo. Sembra poco ed è pochissimo, ma nel 1980 la memoria costava una fortuna — ed è tutta lì la storia. Bastava per una cassa, un rullante, delle percussioni. Non bastava per un piatto, che ha una coda lunga e quindi occupa troppo. Per questo su quei dischi il crash non c'è: non è gusto, è il prezzo dei chip.",
        "richiami": [
            ("FIG. 1", "Campioni a 8 bit"),
            ("FIG. 2", "Un'uscita per suono"),
            ("FIG. 3", "Niente piatti"),
        ],
        "chi_lusata": [
            {"artista": "Prince", "nota": "«1999», «Little Red Corvette», «When Doves Cry»: la accordava verso il basso finché non era sua", "ig": None},
            {"artista": "The Human League", "nota": "Il synth-pop inglese del 1981 passa da qui", "ig": "humanleaguehq"},
            {"artista": "Gary Numan", "nota": "Fra i primi in Europa a metterci le mani", "ig": None},
            {"artista": "Stevie Wonder", "nota": "Anche chi la batteria la sa suonare davvero se la comprò", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": "L'assenza dei piatti non è una scelta estetica: è il prezzo della memoria nel 1980. Un crash dura troppo, e quei secondi in RAM costavano più di quanto valesse il suono. Il risultato è che un decennio intero di dischi si ferma di colpo invece di aprirsi — e quella brusca chiusura, nata da un vincolo di bilancio, è diventata uno dei suoni riconoscibili del pop degli anni Ottanta.",
        "battuta_dinamo": "Niente piatti: la memoria costava troppo. Dieci anni di musica senza un crash.",
        "foto": {
            "file": "assets/foto/lm1/principale.jpg",
            "autore": "Forat Electronics",
            "licenza": "CC BY-SA 3.0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "«Linn LM-1» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Linn_LM-1", "data": "2026-08-27"},
            {"titolo": "«Roger Linn Electronics LM-1» — Polynominal",
             "url": "https://www.polynominal.com/Roger-Linn-lm1/", "data": "2026-08-27"},
            {"titolo": "«Roger Linn on Drum Samples, Prince…» (Art Wood, il batterista campionato) — Reverb",
             "url": "https://reverb.com/news/roger-linn-on-drum-samples-prince-and-unlocking-virtuosity-in-electronic-music", "data": "2026-08-27"},
        ],
        "hashtags": ["#linnlm1", "#drummachine", "#prince", "#anni80", "#musicaelettronica"],
        "verificata": True,
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


def alt_slide(scheda, n):
    """Testo alternativo di ogni slide del carosello.

    NON è solo accessibilità: da metà 2025 Google indicizza i post
    pubblici degli account professionali e legge ESPLICITAMENTE l'alt
    text (oltre alla didascalia). Il campo `alt_text` esiste sull'API
    dal marzo 2025 — usarlo è gratis e ci fa trovare da chi cerca
    «chi ha inventato il minimoog» su Google, non solo su Instagram.
    Quindi qui si scrivono frasi vere, con dentro le parole che una
    persona digiterebbe.
    """
    nome, anno = scheda["strumento"], scheda["anno"]
    costruttore = scheda["costruttore"]
    if n == 1:
        # Niente acrobazie sul plurale della serie: una frase semplice con
        # dentro le parole che uno cerca davvero (nome, anno, costruttore).
        return (f"{nome}: fotografia dello strumento del {anno}, "
                f"costruito da {costruttore}. {scheda['gancio']}.")
    # LEZIONE IMPARATA (27/08/2026). Qui c'era l'articolo «il» scritto a
    # mano davanti al nome dello strumento, e usciva «il Hammond B-3»,
    # «il Ondes Martenot», «il ARP 2600», «il Stylophone». È lo stesso
    # errore del plurale sbagliato nella serie: appena provi a declinare
    # qualcosa che dipende dal nome, sbagli su qualche nome. Google e i
    # lettori di schermo leggono questo testo davvero.
    # REGOLA: nell'alt text nessun articolo e nessun participio che debba
    # accordarsi col nome dello strumento. Il nome va da solo, e ciò che
    # segue si accorda con «macchina», che è sempre femminile singolare.
    if n == 2:
        return f"{nome} ({anno}) — che cos'è. {scheda['la_macchina'][:600]}"
    if n == 3:
        return (f"{nome} ({anno}) — chi ha progettato questa macchina: "
                f"{scheda['inventore_nome']}. {scheda['inventore'][:500]}")
    if n == 4:
        return f"{nome} ({anno}) — come funziona. {scheda['come_funziona'][:600]}"
    if n == 5:
        artisti = ", ".join(f"{u['artista']} ({u['nota']})" for u in scheda["chi_lusata"])
        return f"{nome} ({anno}) — chi ha usato questa macchina: {artisti}"[:900]
    return f"{nome} ({anno}) — la storia. {scheda['aneddoto'][:600]}"


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
