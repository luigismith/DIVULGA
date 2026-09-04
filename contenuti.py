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

# CHIAMATA ALL'AZIONE — una sola richiesta per scheda, a rotazione.
#
# LEZIONE IMPARATA (04/09/2026). La CTA di fase 0 chiedeva due cose in una
# riga: «Conosci qualcuno che ha suonato questa macchina? Taggalo. E dimmi
# quale macchina vuoi vedere nella prossima scheda.» In undici schede non
# ha prodotto un solo commento. Due richieste in una frase obbligano chi
# legge a scegliere quale fare, e nel dubbio non ne fa nessuna.
#
# REGOLA: una richiesta per scheda, e deve essere una a cui si risponde
# senza pensarci. Le tre forme ruotano sul numero della scheda, quindi la
# stessa scheda ha SEMPRE la stessa CTA — in didascalia, sulla tavola e
# nel reel devono coincidere, e la tavola vive per sempre nell'archivio.
#
# PERCHE' NON C'E' «la prossima scheda: A o B?», che pure funzionerebbe
# meglio (si risponde con una parola): la didascalia di Instagram e la
# tavola nell'archivio sono permanenti, e una domanda su «la prossima»
# diventa falsa il giorno dopo. Una CTA deve restare vera quanto il posto
# in cui e' scritta.
CTA_FORME = (
    "Conosci qualcuno che ha suonato questa macchina? Taggalo qui sotto.",
    "Quale macchina vuoi nella prossima scheda? Scrivila qui sotto.",
    "Qual è la prima macchina elettronica che hai riconosciuto in un disco? Raccontala qui sotto.",
)


def cta(scheda):
    """La chiamata all'azione di questa scheda: sempre la stessa, per
    sempre. Deriva dal numero, cosi' didascalia, tavola e reel non possono
    divergere neanche se generati in momenti diversi."""
    return CTA_FORME[(scheda["numero"] - 1) % len(CTA_FORME)]

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
MAX_BATTUTA = 150         # battuta di Dinamo, slide 6 (solo schede 1-4)
MAX_AVVERTENZA = 150      # riga di chiusura in forma di avvertenza, slide 6
MAX_ASCOLTO = 180         # riga «da ascoltare», in fondo alla slide 5
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
        "avvertenza": "Contiene trentadue algoritmi. Non è previsto che l'acquirente sappia cosa sia un algoritmo.",
        "da_ascoltare": {"brano": 'Take On Me', "artista": 'a-ha',
                          "anno": '1985',
                          "cosa": 'Quel basso è il preset BASS 1 del DX7, uscito così dalla fabbrica e mai modificato.'},
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
        "avvertenza": 'Registra qualunque suono e lo rende suonabile sulla tastiera. Non distingue una nota da un colpo di tosse.',
        "da_ascoltare": {"brano": 'The Dreaming', "artista": 'Kate Bush',
                          "anno": '1982',
                          "cosa": 'I suoni che non riesci ad attribuire a nessuno strumento sono campioni suonati sul Fairlight.'},
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
        "avvertenza": 'Non suona come un basso. Il manuale sostiene il contrario.',
        "da_ascoltare": {"brano": 'Acid Tracks', "artista": 'Phuture',
                          "anno": '1987',
                          "cosa": "La 303 non accompagna niente: dall'inizio alla fine è lei il pezzo."},
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
        "avvertenza": 'Peso: centonovantatré chili. Prevedere quattro persone e una rampa, non un ripensamento.',
        "da_ascoltare": {"brano": 'Back at the Chicken Shack', "artista": 'Jimmy Smith',
                          "anno": '1960',
                          "cosa": "Nel quartetto non c'è un bassista: quel basso lo fanno i piedi di Smith sui pedali."},
        "foto": {
            "file": "assets/foto/hammond/principale.jpg",
            "autore": "bobistraveling",
            "licenza": "CC BY 2.0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": '«Back at the Chicken Shack» (registrato il 25/04/1960, senza bassista) — Wikipedia (EN)',
             "url": 'https://en.wikipedia.org/wiki/Back_at_the_Chicken_Shack', "data": '2026-08-28'},
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
        "avvertenza": 'Ne esistono circa trecento in tutto il mondo. In caso di guasto, mettersi comodi.',
        "da_ascoltare": {"brano": 'Turangalîla-Symphonie', "artista": 'Olivier Messiaen',
                          "anno": '1949',
                          "cosa": "La voce che sale sopra l'orchestra e sembra un soprano non è un soprano."},
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
        "avvertenza": 'Funziona senza collegare un solo cavo. Diventa interessante solo quando ne colleghi qualcuno.',
        "da_ascoltare": {"brano": 'Frankenstein', "artista": 'Edgar Winter',
                          "anno": '1972',
                          "cosa": "Il synth che Winter si mise a tracolla per suonarlo in piedi: quel riff è un ARP 2600."},
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
        "avvertenza": 'I collegamenti si fanno con spilli infilati in una matrice. Con gli spilli sbagliati si ottiene comunque qualcosa.',
        "da_ascoltare": {"brano": 'Fetus', "artista": 'Franco Battiato',
                          "anno": '1972',
                          "cosa": 'Il VCS3 che Battiato era andato a prendersi a Londra, su un disco uscito a gennaio.'},
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
        "avvertenza": 'Il timbro non si può addolcire. È stato progettato per passare attraverso un muro di chitarre.',
        "da_ascoltare": {"brano": 'When a Man Loves a Woman', "artista": 'Percy Sledge',
                          "anno": '1966',
                          "cosa": "L'organo dell'introduzione non è un Hammond: è un Farfisa fatto in provincia di Ancona."},
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
        "avvertenza": "Non ha tasti. Ogni nota stonata è esattamente dove l'avete messa.",
        "da_ascoltare": {"brano": 'Gli uccelli', "artista": 'Alfred Hitchcock',
                          "anno": '1963',
                          "cosa": "Non c'è musica in tutto il film: ogni stridio e ogni battito d'ali è questa macchina."},
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
        "avvertenza": 'Un secondo di musica può richiedere un pomeriggio di forbici. Non è un guasto.',
        "da_ascoltare": {"brano": 'Thema (Omaggio a Joyce)', "artista": 'Luciano Berio',
                          "anno": '1958',
                          "cosa": "È soltanto la voce di Cathy Berberian che legge l'Ulisse, tagliata e rimontata su nastro."},
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
        "avvertenza": 'Si suona con un pennino legato alla scatola. Perso il pennino, lo strumento è finito.',
        "da_ascoltare": {"brano": 'Space Oddity', "artista": 'David Bowie',
                          "anno": '1969',
                          "cosa": 'Il ronzio sotto le strofe non è un sintetizzatore: è un giocattolo per bambini.'},
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
        "avvertenza": 'Oltre metà corsa il ritorno si rimangia se stesso e la macchina ulula. Non è un difetto, è il motivo.',
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
        "avvertenza": "L'ingresso ESP accetta qualsiasi segnale e lo trasforma in note. Anche quando cantate stonato.",
        "da_ascoltare": {"brano": 'Da Funk', "artista": 'Daft Punk',
                          "anno": '1995',
                          "cosa": 'Quel lead sporco e saturo è un MS-20: il pezzo è nato su questa macchina.'},
        "foto": {
            "file": "assets/foto/ms20/principale.jpg",
            "autore": "Wilfredor",
            "licenza": "CC0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": '«The Korg MS-20: the unfinished story of a legendary monosynth» — Happy Mag',
             "url": 'https://happymag.tv/the-korg-ms-20-the-unfinished-story-of-a-legendary-monosynth/', "data": '2026-08-28'},
            {"titolo": '«How the Korg MS-20 and the MS-20 Mini became a powerhouse» (Da Funk) — MusicTech',
             "url": 'https://musictech.com/features/opinion-analysis/korg-ms-20-mini-history/', "data": '2026-08-28'},
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
        "avvertenza": 'Non contiene piatti. Non è un errore di imballaggio: la memoria costava troppo.',
        "da_ascoltare": {"brano": 'When Doves Cry', "artista": 'Prince',
                          "anno": '1984',
                          "cosa": 'Niente basso e nessun piatto: quel che resta è la LM-1 accordata verso il basso.'},
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
    # ---------------------------------------------------------------- 19
    {
        "slug": "buchlaeasel",
        "numero": 19,
        "serie": "I SINTETIZZATORI",
        "strumento": "Buchla Music Easel",
        "anno": "1973",
        "luogo": "Berkeley, California",
        "costruttore": "Buchla and Associates",
        "specifiche": [
            ("ANNO", "1973"),
            ("COSTRUTTORE", "Buchla and Associates"),
            ("SINTESI", "Wavefolding"),
            ("VOCI", "Monofonico"),
        ],
        "gancio": "Un intero studio elettronico chiuso in una valigetta, senza un solo tasto bianco o nero",
        "sottotitolo": "Il synth-valigetta con cui Don Buchla portò la musica elettronica fuori dal laboratorio, dritta sul palco.",
        "la_macchina": "Il Music Easel è un sintetizzatore semi-modulare portatile progettato da Don Buchla nel 1973: un intero studio elettronico chiuso in una valigetta rigida apribile a libro, con da un lato la sezione sonora e dall'altro una tastiera a piastre sensibili al tocco, senza tasti bianchi e neri. Nato dall'ambiente sperimentale del San Francisco Tape Music Center, fu tra i primi sintetizzatori pensati per essere suonati dal vivo fuori dal laboratorio, non solo programmati in studio: bastava una presa elettrica.",
        "inventore_nome": "Don Buchla",
        "inventore": "Don Buchla (1937-2016) iniziò a costruire moduli elettronici nel 1963 su commissione dei compositori Morton Subotnick e Ramon Sender del San Francisco Tape Music Center, con un finanziamento della Rockefeller Foundation. Fondò poi Buchla and Associates a Berkeley, California. A differenza di Bob Moog, escluse per principio la tastiera pianistica: «Una tastiera è dittatoriale», disse, «con una tastiera bianca e nera è difficile suonare qualcosa che non sia musica da tastiera».",
        "come_funziona": "Il cuore del Music Easel è un oscillatore complesso con wavefolder incorporato, che ripiega la forma d'onda su se stessa per generare armonici via via più ricchi all'aumentare del livello, affiancato da un oscillatore di modulazione indipendente. Il suono passa poi in due Low Pass Gate, moduli ibridi che uniscono filtro e VCA in un solo controllo, pensati per imitare il modo in cui uno strumento acustico si smorza naturalmente. La tastiera a piastre capacitive restituisce pressione e velocity del dito, non solo l'attacco della nota.",
        "richiami": [
            ("FIG. 1", "Oscillatore complesso con wavefolder"),
            ("FIG. 2", "Tastiera a piastre capacitive"),
            ("FIG. 3", "Doppio Low Pass Gate (filtro+VCA)"),
        ],
        "chi_lusata": [
            {"artista": "Kaitlyn Aurelia Smith", "nota": "usato per gran parte dell'album «EARS», 2016, intrecciato a un quartetto di fiati", "ig": None},
            {"artista": "Alessandro Cortini", "nota": "possiede il primo prototipo di Music Easel mai costruito da Buchla; ci ha registrato la trilogia «Forse», 2013", "ig": None},
            {"artista": "Jimmy Tamborello (Dntel)", "nota": "l'album strumentale «Hate In My Heart» nasce da session quotidiane col Music Easel in salotto", "ig": None},
        ],
        "menzioni_extra": [
            {"ig": "buchlausa",
             "riga": "Il produttore attuale, Buchla Electronic Musical Instruments, è @buchlausa."},
        ],
        "aneddoto": "Alessandro Cortini ha cercato per anni il suo Music Easel prima di trovarlo, scoprendo che si trattava del primissimo prototipo mai costruito da Don Buchla in persona: «Quando l'ho trovato ho pianto», ha raccontato. Su quella macchina, in un mese, ha scritto e suonato dal vivo l'intero doppio album «Forse Vol. 1 & 2» (2013), pubblicato da Important Records, un pezzo alla volta, senza sovraincisioni: esattamente come lo strumento era stato pensato per essere suonato.",
        "avvertenza": "Le piastre della tastiera non premono tasti: misurano la pressione del dito. Il vibrato è nel vostro polso, non nello strumento.",
        "foto": {
            "file": "assets/foto/buchlaeasel/principale.jpg",
            "autore": "Captnapalm",
            "licenza": "Pubblico dominio",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "«Music Easel» — pagina ufficiale Buchla",
             "url": "https://buchla.com/music-easel/", "data": "2026-09-04"},
            {"titolo": "«Buchla Music Easel» review — Sound on Sound",
             "url": "https://www.soundonsound.com/reviews/buchla-music-easel", "data": "2026-09-04"},
            {"titolo": "«Alessandro Cortini on Falling in Love with Synthesizers» — Red Bull Music Academy Daily",
             "url": "https://daily.redbullmusicacademy.com/2017/03/alessandro-cortini-interview/", "data": "2026-09-04"},
            {"titolo": "«Don Buchla, inventor of electronic music instruments, dies at 79» — SFGate/San Francisco Chronicle",
             "url": "https://www.sfgate.com/music/article/Don-Buchla-inventor-of-electronic-music-9235035.php", "data": "2026-09-04"},
        ],
        "hashtags": ["#buchla", "#musicaelettronica", "#synth", "#sintetizzatore", "#modularsynth"],
        "verificata": True,
    },
    # ---------------------------------------------------------------- 20
    {
        "slug": "synthex",
        "numero": 20,
        "serie": "I SINTETIZZATORI",
        "strumento": "Elka Synthex",
        "anno": "1982",
        "luogo": "Castelfidardo (AN), Italia",
        "costruttore": "Elka, su progetto di Mario Maggi",
        "specifiche": [
            ("ANNO", "1982"),
            ("COSTRUTTORE", "Elka (Castelfidardo)"),
            ("SINTESI", "Sottrattiva, oscillatori DCO"),
            ("VOCI", "8 voci polifoniche"),
        ],
        "gancio": "Il synth italiano che sfidò Prophet e Oberheim, e finì tra le mani di Jarre e Stevie Wonder",
        "sottotitolo": "Nato da un progettista indipendente, diventò il polifonico analogico più ambizioso mai costruito in Italia.",
        "la_macchina": "Progettato in proprio dall'ingegnere Mario Maggi e prodotto dall'italiana Elka dal 1982, il Synthex è un polifonico analogico a 8 voci con 16 oscillatori DCO controllati digitalmente: a differenza dei rivali americani restava perfettamente accordato. Filtro CEM a 4 poli multimodo, joystick al posto delle rotelle, sequencer interno a 4 tracce da 128 passi — tra i primi sequencer multitimbrici della storia. Costava meno del Prophet-5 ma offriva più voci: fu considerato il vertice dell'industria italiana dei sintetizzatori. Ne furono costruiti circa 1.850 in tre serie.",
        "inventore_nome": "Mario Maggi",
        "inventore": "Mario Maggi lavorava da anni per conto proprio quando, dopo i rifiuti di Galanti/GEM, EKO e della stessa Crumar, portò il prototipo alla Elka di Castelfidardo tramite un amico che doveva riparare un organo in fabbrica: direzione e consiglio ne rimasero folgorati. Il nome nacque dopo notti insonni: Maggi voleva un nome corto che finisse in X, tra le suggestioni dei fumetti di Tex Willer. Il Synthex debuttò al Musikmesse di Francoforte nel 1982: i distributori aspettavano di ascoltarlo ancora prima che Maggi arrivasse in albergo.",
        "come_funziona": "Ogni voce ha due oscillatori digitali (DCO): 16 in tutto, generati con circuiti TTL invece che con i soliti VCO analogici, quindi restano intonati senza bisogno di accordarli di continuo. Il segnale passa in un filtro Curtis a 4 poli commutabile fra passa-basso 24dB, passa-alto e due modalità passa-banda. Il joystick sostituisce le rotelle pitch/mod e in modalità split controlla in tempo reale due LFO indipendenti. Il sequencer integrato registra 4 tracce fino a 128 passi ciascuna, con lunghezze diverse per creare poliritmi che si intrecciano ad ogni giro.",
        "richiami": [
            ("FIG. 1", "16 oscillatori DCO (2 per voce)"),
            ("FIG. 2", "Filtro CEM 4 poli multimodo"),
            ("FIG. 3", "Joystick al posto delle wheel"),
        ],
        "chi_lusata": [
            {"artista": "Jean-Michel Jarre", "nota": "Synthex e laser harp protagonisti dell'album «Rendez-Vous», 1986", "ig": "jeanmicheljarre"},
            {"artista": "Stevie Wonder", "nota": "l'ultimo Synthex mai assemblato fu montato apposta per lui: il basso di «Skeletons», 1987", "ig": None},
            {"artista": "Keith Emerson", "nota": "lo usò dal vivo per «Fanfare for the Common Man» quando il suo Yamaha GX-1 lo tradì", "ig": None},
            {"artista": "Nick Rhodes (Duran Duran)", "nota": "apprezzava i suoi campanelli morbidi, presenti in più album della band", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": "Prima di dire sì, Elka era stata la terza scelta di Maggi: Galanti/GEM e la stessa Crumar (fondata da un ex socio Elka) lo avevano già respinto. L'ultimo Synthex mai assemblato uscì dalla fabbrica pochi mesi prima della chiusura, costruito su misura per Stevie Wonder: è quello strumento a fornire il suono di basso di «Skeletons», singolo del 1987 dall'album «Characters». Un altro esemplare accompagnò Keith Emerson sul palco quando il suo enorme Yamaha GX-1 lo tradì durante l'esecuzione live di «Fanfare for the Common Man».",
        "avvertenza": "Il joystick non sta a fianco della tastiera, come le rotelle pitch/mod: vive in mezzo al pannello di programmazione, tra i comandi.",
        "da_ascoltare": {"brano": "Second Rendez-Vous", "artista": "Jean-Michel Jarre",
                          "anno": "1986",
                          "cosa": "Synthex e laser harp sono i protagonisti sonori del brano, eseguito anche dal vivo a Houston nello stesso anno."},
        "foto": {
            "file": "assets/foto/synthex/principale.jpg",
            "autore": "Matt Friedman",
            "licenza": "CC BY 3.0",
            "fonte": "Wikimedia Commons (originariamente pubblicata su vintagesynth.com)",
        },
        "fonti": [
            {"titolo": "«Elka Synthex» — Sound on Sound (Retrozone)",
             "url": "https://www.soundonsound.com/reviews/elka-synthex-retrozone", "data": "2026-09-04"},
            {"titolo": "«Dedicated to Mario Maggi (third part)» — Classic2Vintage",
             "url": "https://www.classic2vintage.com/en/dedicated-to-mario-maggi-third-part/", "data": "2026-09-04"},
            {"titolo": "«ELKA Synthex — analog Classic and vintage Workstation» — GreatSynthesizers",
             "url": "https://greatsynthesizers.com/en/review/elka-synthex-polyphonic-classic/", "data": "2026-09-04"},
            {"titolo": "«Elka Synthex» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Elka_Synthex", "data": "2026-09-04"},
        ],
        "hashtags": ["#elkasynthex", "#sintetizzatore", "#madeinitaly", "#synth", "#musicaelettronica"],
        "verificata": True,
    },
    # ---------------------------------------------------------------- 21
    {
        "slug": "tr909",
        "numero": 21,
        "serie": "LE DRUM MACHINE",
        "strumento": "Roland TR-909",
        "anno": "1983",
        "luogo": "Hamamatsu, Giappone",
        "costruttore": "Roland Corporation",
        "specifiche": [
            ("ANNO", "1983"),
            ("COSTRUTTORE", "Roland Corporation"),
            ("SINTESI", "Analogica + campioni PCM"),
            ("VOCI", "11 suoni"),
        ],
        "gancio": "Un flop commerciale che vendette 10.000 pezzi e poi, da usato, costruì techno e house",
        "sottotitolo": "La drum machine che Roland ritirò dopo un anno e che il ballo elettronico non ha più smesso di suonare.",
        "la_macchina": "La TR-909 Rhythm Composer, uscita nel 1983 a 1.195 dollari, fu la prima drum machine Roland a unire sintesi analogica e campioni digitali: cassa, rullante, tom e clap sono generati elettronicamente, mentre charleston, ride e crash sono campioni PCM a 6 bit. Ha 11 voci, uscite individuali per ogni suono e, prima nella serie TR, sia il MIDI sia lo step sequencer con shuffle e accent programmabili voce per voce. Vendette così male che Roland la tolse dal listino dopo appena un anno.",
        "inventore_nome": "Tadao Kikumoto",
        "inventore": "Tadao Kikumoto, già ingegnere capo sulla precedente TR-808 e poi progettista della TB-303, guidò lo sviluppo della TR-909 insieme al capo progetto Makoto Muroi; il software fu scritto da Atsushi Hoshiai e i circuiti voce da Yoshiro Oue. Roland puntava a inseguire il mercato che preferiva suoni «realistici» campionati come la LinnDrum: la 909 fu il primo tentativo Roland di un ibrido fra analogico e digitale, un compromesso che all'epoca non convinse quasi nessuno.",
        "come_funziona": "I piatti (hi-hat, ride, crash) sono campioni digitali a 6 bit: Atsushi Hoshiai li registrò lui stesso di notte in ufficio, spostando i microfoni per settimane, usando i suoi piatti personali spaiati — un Paiste sopra e uno Zildjian sotto — per ottenere l'attacco giusto. Cassa, rullante, tom e clap restano invece sintesi analogica sottrattiva pura, motivo per cui la 909 suona più aggressiva e secca della 808, che era invece interamente analogica.",
        "richiami": [
            ("FIG. 1", "Sintesi ibrida: analogica + campioni a 6 bit"),
            ("FIG. 2", "Uscite individuali per ogni voce"),
            ("FIG. 3", "Sequencer con shuffle e accent"),
        ],
        "chi_lusata": [
            {"artista": "Larry Heard (Mr. Fingers)", "nota": "«Can You Feel It», 1986, registrato pochi giorni dopo aver comprato una 909 e un Juno-60", "ig": None},
            {"artista": "Daft Punk", "nota": "il brano «Revolution 909» (Homework, 1997) prende il nome dalla macchina; la loro 909 originale è stata poi venduta all'asta", "ig": None},
            {"artista": "Jeff Mills", "nota": "tra i primi DJ/producer di Detroit a farne uno strumento da performance dal vivo, fine anni '80", "ig": None},
        ],
        "menzioni_extra": [
            {"ig": "rolandglobal",
             "riga": "Il produttore originale, Roland Corporation, è ancora @rolandglobal."},
        ],
        "aneddoto": "Per registrare charleston, ride e crash, il tecnico del suono Atsushi Hoshiai portò i propri piatti da batterista jazz in ufficio e per notti intere spostò i microfoni cercando il punto giusto vicino alla scrivania di un collega, prima di campionarli a 6 bit. Anni dopo ha raccontato di usare ancora la stessa combinazione di piatti spaiati quando suona dal vivo nella sua big band acustica: il suono più campionato della musica da ballo elettronica nasce da un hobby personale portato in ufficio fuori orario.",
        "avvertenza": "Charleston, ride e crash sono campioni dei piatti jazz personali di un tecnico Roland, registrati di notte in ufficio. Il resto è sintesi.",
        "foto": {
            "file": "assets/foto/tr909/principale.png",
            "autore": "Clusternote (derivato da una foto di Brandon Daniel)",
            "licenza": "CC BY-SA 2.0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "«Roland TR-909» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Roland_TR-909", "data": "2026-09-04"},
            {"titolo": "«Roland Engineering: Atsushi Hoshiai and the TR-909» — Roland Articles",
             "url": "https://articles.roland.com/atsushi-hoshiai-tr-909/", "data": "2026-09-04"},
            {"titolo": "Roland designer Atsushi Hoshiai on the origin of the TR-909's sounds — MusicRadar",
             "url": "https://www.musicradar.com/news/909-hi-hats", "data": "2026-09-04"},
            {"titolo": "«Sound Behind the Song: Can You Feel It» — Roland Articles",
             "url": "https://articles.roland.com/can-you-feel-it-mr-fingers/", "data": "2026-09-04"},
        ],
        "hashtags": ["#tr909", "#roland", "#drummachine", "#techno", "#musicaelettronica"],
        "verificata": True,
    },
    # ---------------------------------------------------------------- 22
    {
        "slug": "optigan",
        "numero": 22,
        "serie": "I GIOCATTOLI",
        "strumento": "Mattel Optigan",
        "anno": "1971",
        "luogo": "El Segundo, California",
        "costruttore": "Optigan Corporation (Mattel)",
        "specifiche": [
            ("ANNO", "1971"),
            ("COSTRUTTORE", "Optigan Corporation (Mattel)"),
            ("LETTURA", "Dischi ottici in celluloide"),
            ("TASTIERA", "37 tasti + 21 accordi"),
        ],
        "gancio": "Un giocattolo Mattel che leggeva la musica con un fascio di luce, come una colonna sonora di celluloide",
        "sottotitolo": "L'organo giocattolo che, invece delle note, faceva girare vere registrazioni d'orchestra su un disco di plastica.",
        "la_macchina": "L'Optigan è un organo elettronico per famiglie, venduto da Mattel come elettrodomestico da salotto: al posto di generare elettronicamente le note, faceva girare un disco trasparente di celluloide da 12 pollici su cui erano incise, in piste concentriche, vere registrazioni di strumenti e piccole orchestre. Premendo un tasto si illuminava una pista diversa e si sentiva quel suono già registrato. È un antenato ingenuo e fragile del campionatore: stesso principio del Fairlight o dell'Emulator, dieci anni prima, ma con la tecnologia economica del cinema sonoro al posto dei computer.",
        "inventore_nome": "Optigan Corporation (Mattel)",
        "inventore": "L'Optigan nacque come costola di Mattel: la ricerca tecnica iniziò nel 1968 e i primi brevetti arrivarono nel 1970, sotto l'etichetta Optigan Corporation, con sede a El Segundo e fabbrica a Compton, in California. Fu presentato ufficialmente il 27 gennaio 1971 al Century Plaza Hotel di Los Angeles, seguito l'anno dopo da una delle prime grandi campagne pubblicitarie televisive mai dedicate a uno strumento musicale. Le colonne sonore dei dischi furono arrangiate dal direttore musicale Johnny Largo.",
        "come_funziona": "Ogni disco Optigan («Program Disc») contiene 57 tracce ottiche concentriche: una lampadina illumina il disco in rotazione e una fila di fotodiodi legge le variazioni di luce come farebbe un lettore di colonna sonora ottica al cinema, trasformandole in segnale audio. 37 piste sono note sostenute suonate con la tastiera a destra; 21 sono accordi (in stile fisarmonica) per la mano sinistra; le restanti 5 sono percussioni ed effetti su interruttori a bilico. Il limite: nessuna nota ha un vero attacco o rilascio, perché la traccia gira in loop continuo.",
        "richiami": [
            ("FIG. 1", "Disco ottico 12\", 57 piste"),
            ("FIG. 2", "Lampadina + fotodiodi"),
            ("FIG. 3", "37 tasti + 21 pulsanti accordo"),
        ],
        "chi_lusata": [
            {"artista": "Bruce Haack", "nota": "dischi Optigan tra cui «Nashville Country» usati in «Captain Entropy», 1973", "ig": None},
            {"artista": "Steve Hackett", "nota": "«Sentimental Institution» (Defector, 1980), registrato con l'Optigan nel bagno degli Wessex Studios", "ig": None},
            {"artista": "David Lynch", "nota": "campionò «Big Band Beat» per «The Air is on Fire» (2007), poi in «Twin Peaks: The Return» (2017)", "ig": None},
            {"artista": "Mark Mothersbaugh (Devo)", "nota": "un remix del singolo Devo «Beautiful World» (1981) usa il disco «Banjo Sing-Along»", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": "L'Optigan non poteva suonare in tutte le tonalità: per risparmiare spazio, gli accordi di La maggiore e Mi maggiore condividevano la stessa pista ottica di alcuni accordi diminuiti, rendendo impossibile accompagnarsi con la mano sinistra in quelle due tonalità. Un secondo difetto, altrettanto documentato, è il crosstalk fra tracce vicine: si sente in sottofondo l'accordo diminuito della traccia adiacente.",
        "avvertenza": "Gli accordi di La e Mi maggiore condividono la pista ottica dei diminuiti. In quelle due tonalità, la mano sinistra è meglio tenerla in tasca.",
        "da_ascoltare": {"brano": "Sentimental Institution", "artista": "Steve Hackett",
                          "anno": "1980",
                          "cosa": "Registrato con un solo Optigan e il disco «Big Band Beat», nel bagno degli Wessex Studios per un suono volutamente vecchio e sporco."},
        "foto": {
            "file": "assets/foto/optigan/principale.jpg",
            "autore": "PMDrive1061",
            "licenza": "CC BY-SA 3.0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "«Optigan» — Wikipedia (EN), sezioni Production history / Use in the music industry",
             "url": "https://en.wikipedia.org/wiki/Optigan", "data": "2026-09-04"},
            {"titolo": "«Optigan» — Optigan.com (archivio storico dedicato)",
             "url": "https://optigan.com/info/optigan/", "data": "2026-09-04"},
            {"titolo": "Bruce Haack, «Captain Entropy» — Discogs (crediti dischi Optigan usati in registrazione)",
             "url": "https://www.discogs.com/release/3020912-Bruce-Haack-Captain-Entropy", "data": "2026-09-04"},
            {"titolo": "Steve Hackett, «Sentimental Institution» (Defector, 1980) — registrazione con Optigan a Wessex Studios",
             "url": "https://paul-pearson.blogspot.com/2014/03/song-of-day-3142014-steve-hackett.html", "data": "2026-09-04"},
        ],
        "hashtags": ["#optigan", "#mattel", "#organoelettronico", "#vintagesynth", "#musicaelettronica"],
        "verificata": True,
    },
    # ---------------------------------------------------------------- 23
    {
        "slug": "emulator",
        "numero": 23,
        "serie": "I CAMPIONATORI",
        "strumento": "E-mu Emulator II",
        "anno": "1984",
        "luogo": "Santa Cruz, California",
        "costruttore": "E-mu Systems",
        "specifiche": [
            ("ANNO", "1984"),
            ("COSTRUTTORE", "E-mu Systems"),
            ("CAMPIONAMENTO", "8 bit, 27,7 kHz"),
            ("VOCI", "8 voci, 8 parti MIDI"),
        ],
        "gancio": "Registra un violino vero, lo intona su tutta la tastiera: l'orchestra finisce dentro una scatola",
        "sottotitolo": "Il campionatore che negli anni '80 mise un'intera orchestra dentro 61 tasti, spesso senza che nessuno se ne accorgesse.",
        "la_macchina": "L'Emulator II è il campionatore che portò suoni reali — archi, ottoni, un flauto giapponese, un vetro rotto — dentro una tastiera musicale, a un prezzo che uno studio professionale poteva permettersi. Si registrava un suono a 8 bit e lo si intonava automaticamente su tutti i tasti: bastava premere per risuonare quel violino o quel corno campionato. Con le sue librerie di suoni su floppy disk diventò lo strumento invisibile dietro decine di hit pop e colonne sonore della seconda metà degli anni '80, spesso senza che l'ascoltatore se ne accorgesse.",
        "inventore_nome": "Dave Rossum e Scott Wedge",
        "inventore": "E-mu Systems nacque nel 1971 a Santa Cruz, in California, per costruire sintetizzatori modulari su misura per altri musicisti. Fu la vista del Fairlight CMI e della Linn LM-1 al NAMM del 1979 a convincere i fondatori Dave Rossum e Scott Wedge che il campionamento digitale poteva costare molto meno dei 30.000 dollari del Fairlight australiano. Nel 1981 uscì il primo Emulator; tre anni dopo l'Emulator II ne perfezionò il suono aggiungendo i filtri analogici risonanti SSM2045, che restano la firma sonora della macchina.",
        "come_funziona": "Il suono viene campionato a 8 bit con una frequenza di 27,7 kHz e salvato su floppy disk da 5 pollici e un quarto, poi distribuito automaticamente sui 61 tasti sensibili a velocity e aftertouch. A valle del campionamento agisce un filtro analogico risonante a 4 poli, 24 dB/ottava, costruito attorno al chip SSM2045: è lui a scaldare e modellare il suono altrimenti crudo del campione digitale. La macchina ha 8 voci di polifonia, 8 parti multitimbriche via MIDI e un sequencer interno a 8 tracce.",
        "richiami": [
            ("FIG. 1", "Campionamento 8 bit, 27,7 kHz"),
            ("FIG. 2", "Filtro risonante SSM2045, 24 dB/oct"),
            ("FIG. 3", "61 tasti velocity + floppy 5¼\""),
        ],
        "chi_lusata": [
            {"artista": "Pet Shop Boys", "nota": "«West End Girls» (1986): archi, tromba e cassa sono campioni Emulator I/II stratificati", "ig": "petshopboys"},
            {"artista": "Peter Gabriel", "nota": "«Sledgehammer» (1986): lo shakuhachi sintetico dell'intro nasce da un campione E-mu Emulator II", "ig": None},
            {"artista": "Sade", "nota": "«Love Is Stronger Than Pride»: stesso campione shakuhachi della libreria sonora Emulator II", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": "Il campione «Shakuhachi» della libreria sonora dell'Emulator II — un flauto giapponese registrato per uso generico — finì per aprire «Sledgehammer» di Peter Gabriel nel 1986 e ricomparve, identico, in brani di Enigma e in «Love Is Stronger Than Pride» di Sade: lo stesso suono, uscito dallo stesso floppy disk, girava contemporaneamente su mezza classifica pop senza che quasi nessuno lo riconoscesse come lo stesso campione.",
        "avvertenza": "Il filtro SSM2045 scalda qualsiasi campione digitale. Anche un vetro rotto, se glielo chiedete gentilmente, suonerà quasi analogico.",
        "da_ascoltare": {"brano": "Sledgehammer", "artista": "Peter Gabriel", "anno": "1986",
                          "cosa": "Il flauto shakuhachi sintetico che apre il brano è un campione della libreria sonora dell'Emulator II."},
        "foto": {
            "file": "assets/foto/emulator/principale.jpg",
            "autore": "John R. Southern",
            "licenza": "CC BY-SA 2.0",
            "fonte": "Wikimedia Commons (originariamente Flickr)",
        },
        "fonti": [
            {"titolo": "«E-mu Emulator» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/E-mu_Emulator", "data": "2026-09-04"},
            {"titolo": "«E-mu Emulator II» — Vintage Synth Explorer",
             "url": "https://www.vintagesynth.com/e-mu/emulator-ii", "data": "2026-09-04"},
            {"titolo": "«Peter Gabriel's 'Sledgehammer' sample of E-mu Systems's 'Shakuhachi'» — WhoSampled",
             "url": "https://www.whosampled.com/sample/327101/Peter-Gabriel-Sledgehammer-E-mu-Systems-Shakuhachi/", "data": "2026-09-04"},
            {"titolo": "«Sledgehammer (Peter Gabriel song)» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Sledgehammer_(Peter_Gabriel_song)", "data": "2026-09-04"},
            {"titolo": "«E-mu Systems» — Wikipedia (EN), storia aziendale e fondatori",
             "url": "https://en.wikipedia.org/wiki/E-mu_Systems", "data": "2026-09-04"},
        ],
        "hashtags": ["#emu", "#emulator", "#campionatore", "#sampler", "#musicaelettronica"],
        "verificata": True,
    },
    # ---------------------------------------------------------------- 24
    {
        "slug": "crumar",
        "numero": 24,
        "serie": "I SINTETIZZATORI",
        "strumento": "Crumar Performer",
        "anno": "1979",
        "luogo": "Castelfidardo (AN), Italia",
        "costruttore": "Crumar (Mario Crucianelli)",
        "specifiche": [
            ("ANNO", "1979"),
            ("COSTRUTTORE", "Crumar (Castelfidardo)"),
            ("SINTESI", "Divisione di frequenza (TOS)"),
            ("VOCI", "49 tasti, polifonia totale"),
        ],
        "gancio": "Niente oscillatori: solo un cristallo di quarzo e 49 tasti, per un'orchestra tascabile made in Italy",
        "sottotitolo": "Il sintetizzatore di archi e ottoni che Nick Rhodes portò nei primi dischi dei Duran Duran.",
        "la_macchina": "Lanciato nel 1979 dall'italiana Crumar, il Performer è una macchina polifonica ad archi e ottoni che non usa oscillatori individuali: un unico generatore digitale produce le note più acute, poi una catena di divisori le abbassa di ottava in ottava, così tutti i 49 tasti suonano insieme senza bisogno di intonare nulla. Due sezioni indipendenti — Strings (con chorus a BBD) e Brass (filtro e inviluppo propri) — si mescolano su 15 cursori, senza memorie. Economico e trasportabile, divenne uno degli strumenti simbolo dell'industria tastieristica marchigiana a fine anni '70.",
        "inventore_nome": "Crumar (Mario Crucianelli)",
        "inventore": "Crumar nacque nel 1971 a Castelfidardo (Marche) da Mario Crucianelli, che aveva appena lasciato l'azienda di famiglia Elka dopo una spaccatura interna. L'azienda arrivò a contare 300 dipendenti tra i due laboratori di Castelfidardo, cuore storico della liuteria italiana per strumenti a tastiera. Prima del Performer, Crumar produceva pianoforti elettronici e string machine come Compac-piano e Compac-string; dopo, arrivarono il sintetizzatore DS-2 e, nel 1983, lo Spirit disegnato con Bob Moog.",
        "come_funziona": "Il cuore del Performer è un generatore digitale (top octave synthesizer) che produce le dodici note dell'ottava più acuta come onde quadre; una catena di circuiti divisori le dimezza in cascata per ricavare le ottave inferiori. Ogni tasto pigiato attinge semplicemente a una frequenza già pronta: ecco perché lo strumento è sempre completamente polifonico, senza i limiti di voce tipici dei synth a oscillatori veri. La sezione Strings aggiunge un effetto ensemble a BBD, la Brass un filtro passa-basso con inviluppo attacco/decadimento.",
        "richiami": [
            ("FIG. 1", "Generatore top-octave + divisori"),
            ("FIG. 2", "15 cursori, zero memorie"),
            ("FIG. 3", "Sezioni Strings e Brass separate"),
        ],
        "chi_lusata": [
            {"artista": "Nick Rhodes (Duran Duran)", "nota": "protagonista degli archi nei primi due album, «Duran Duran» (1981) e «Rio» (1982), insieme a Jupiter-4 e Prophet-5", "ig": None},
        ],
        "menzioni_extra": [
            {"ig": "crumar_instruments",
             "riga": "Il marchio Crumar è ancora attivo, oggi a Roncade (TV): lo trovate come @crumar_instruments."},
        ],
        "aneddoto": "Nick Rhodes dei Duran Duran lo mise al centro del suono d'archi dei primi due album della band, «Duran Duran» (1981) e «Rio» (1982), affiancandolo a un Roland Jupiter-4 e a un Prophet-5. Nonostante questo, il Performer resta uno dei synth italiani più trascurati dai collezionisti, complice un suono spesso liquidato come «plasticoso» — eppure proprio quella plastica, unita al prezzo contenuto, lo rese uno degli strumenti più esportati della new wave dei primi anni '80.",
        "avvertenza": "Questa macchina non ricorda nulla: il suono di oggi va riscritto a mano sui 15 cursori, ogni volta che la accendete.",
        "foto": {
            "file": "assets/foto/crumar/principale.jpg",
            "autore": "PerfectCircuit",
            "licenza": "CC0 1.0",
            "fonte": "Wikimedia Commons (originariamente su Pixabay)",
        },
        "fonti": [
            {"titolo": "«Crumar» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Crumar", "data": "2026-09-04"},
            {"titolo": "«Crumar Performer» — Vintage Synth Explorer",
             "url": "https://www.vintagesynth.com/crumar/performer", "data": "2026-09-04"},
            {"titolo": "«Crumar Performer 70's String & Brass Synthesizer» — MATRIXSYNTH",
             "url": "https://www.matrixsynth.com/2010/01/crumar-performer-70s-string-brass.html", "data": "2026-09-04"},
            {"titolo": "«Crumar Performer» — Polynominal",
             "url": "https://www.polynominal.com/m/crumar-performer.htm", "data": "2026-09-04"},
        ],
        "hashtags": ["#crumar", "#sintetizzatore", "#stringmachine", "#madeinitaly", "#synth"],
        "verificata": True,
    },
    # ---------------------------------------------------------------- 25
    {
        "slug": "juno106",
        "numero": 25,
        "serie": "I SINTETIZZATORI",
        "strumento": "Roland Juno-106",
        "anno": "1984",
        "luogo": "Hamamatsu, Giappone",
        "costruttore": "Roland Corporation",
        "specifiche": [
            ("ANNO", "1984"),
            ("COSTRUTTORE", "Roland Corporation"),
            ("SINTESI", "DCO sottrattiva"),
            ("VOCI", "6 voci"),
        ],
        "gancio": "Nato per essere il Juno economico, è diventato il polifonico analogico più clonato della storia",
        "sottotitolo": "Il synth con cui Roland rese l'analogico stabile, accessibile e, per un difetto di fabbrica, leggendario.",
        "la_macchina": "Il Juno-106 è un sintetizzatore polifonico a 6 voci uscito nel febbraio 1984, evoluzione del Juno-60 con l'aggiunta del MIDI e memoria raddoppiata a 128 patch. Ogni voce ha un solo oscillatore digitalmente controllato (DCO) più un filtro passa-basso risonante a 24 dB/ottava, e l'intero synth passa attraverso un chorus stereo che ne gonfia il suono sottile in una texture larga e brillante: è quel chorus, più di ogni altra cosa, ad aver definito il «suono Juno» del synth-pop.",
        "inventore_nome": "Roland Corporation (progetto di squadra)",
        "inventore": "Roland, fondata a Osaka nel 1972 da Ikutaro Kakehashi e oggi con sede a Hamamatsu, lanciò il primo Juno (Juno-6) nel 1982; il Juno-106 arrivò nel 1984 come terzo capitolo della serie. Nessun singolo progettista è accreditato pubblicamente per il Juno-106, a differenza di altre macchine Roland dell'epoca: fu un progetto di squadra interno, pensato per abbattere i costi del Juno-60 mantenendone il suono, grazie proprio ai DCO al posto dei più costosi oscillatori a voltaggio controllato (VCO).",
        "come_funziona": "Il DCO non è digitale nel suono, solo nell'accordatura: un segnale di clock digitale, generato da un microcontrollore, comanda un transistor che scarica un condensatore a intervalli regolari, producendo un'onda a dente di sega analogica. Un convertitore digitale-analogico compensa il volume alle frequenze più alte. Il risultato: l'oscillatore resta sempre accordato, cosa che i VCO analogici dell'epoca non garantivano, pur mantenendo il timbro pieno dell'analogico puro.",
        "richiami": [
            ("FIG. 1", "DCO: oscillatore a clock digitale"),
            ("FIG. 2", "Chorus stereo a BBD, due profondità"),
            ("FIG. 3", "Chip voce 80017A, uno per voce"),
        ],
        "chi_lusata": [
            {"artista": "Chvrches", "nota": "gran parte del basso di «The Bones of What You Believe» (2013) è un Juno-106", "ig": None},
            {"artista": "William Orbit", "nota": "tra i primi a usarlo pesantemente in studio già a fine anni '80", "ig": None},
            {"artista": "Vince Clarke", "nota": "synth fisso del suo studio, insieme a Xpander, MKS-80 e Prophet VS", "ig": None},
        ],
        "menzioni_extra": [
            {"ig": "rolandglobal",
             "riga": "Il produttore originale, Roland Corporation, è ancora @rolandglobal."},
        ],
        "aneddoto": "Ogni voce del Juno-106 dipende da un chip custom Roland, il 80017A (VCF+VCA in un solo componente): non è più prodotto da decenni e ha un tasso di guasto talmente alto da essere quasi proverbiale tra i tecnici, tanto che oggi esistono cloni moderni pensati apposta per rimpiazzarlo. È probabilmente il motivo per cui, oggi, quasi ogni Juno-106 in circolazione ha già perso e recuperato almeno una voce.",
        "avvertenza": "Ogni voce vive in un chip 80017A introvabile dagli anni '80. Quando muore una voce, è per sempre, finché non trovate un clone.",
        "foto": {
            "file": "assets/foto/juno106/principale.jpg",
            "autore": "Iainf",
            "licenza": "Pubblico dominio",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "«Roland Juno-106» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Roland_Juno-106", "data": "2026-09-04"},
            {"titolo": "«The Design of the Roland Juno oscillators» — blog di Thea Flowers (Stargirl)",
             "url": "https://blog.thea.codes/the-design-of-the-juno-dco/", "data": "2026-09-04"},
            {"titolo": "«Roland 80017A» — Polynominal",
             "url": "https://www.polynominal.com/roland-80017A/", "data": "2026-09-04"},
            {"titolo": "«The Story Behind Every Song On Chvrches' Debut Album» — Stereogum",
             "url": "https://stereogum.com/2236734/chvrches-debut-album-the-bones-of-what-you-believe-turns-10/interviews/footnotes-interview", "data": "2026-09-04"},
        ],
        "hashtags": ["#juno106", "#roland", "#sintetizzatore", "#synth", "#musicaelettronica"],
        "verificata": True,
    },
    # ---------------------------------------------------------------- 26
    {
        "slug": "synket",
        "numero": 26,
        "serie": "LE ORIGINI",
        "strumento": "Synket (Synthesizer Ketoff)",
        "anno": "1963",
        "luogo": "Roma, Italia",
        "costruttore": "Paolo Ketoff, per l'Accademia Americana di Roma",
        "specifiche": [
            ("ANNO", "1963"),
            ("COSTRUTTORE", "Paolo Ketoff (Roma)"),
            ("SINTESI", "Sottrattiva, 3 moduli indipendenti"),
            ("VOCI", "3 (una tastiera per modulo)"),
        ],
        "gancio": "Prima ancora del Moog da palco, a Roma un tecnico del suono ne aveva già costruito uno portatile",
        "sottotitolo": "Tre tastierine, tre generatori, un'idea nata per l'Accademia Americana: tra i primi sintetizzatori pensati per il palco.",
        "la_macchina": "Costruito da Paolo Ketoff a partire dal 1963 su commissione dell'Accademia Americana di Roma, il Synket è tra i primissimi sintetizzatori pensati per il concerto dal vivo, anni prima del Minimoog. È fatto di tre «sound-combiner» indipendenti — ciascuno con oscillatore a onda quadra, divisori di frequenza, filtri e modulatori — mescolati in un'unica uscita, pilotati da tre tastierine di due ottave, una per modulo. Ketoff ne costruì a mano solo una decina di esemplari in dodici anni, ognuno leggermente diverso dagli altri: oggi sono sparsi tra i musei di Roma, Parigi, Monaco, Baltimora e Milano.",
        "inventore_nome": "Paolo Ketoff",
        "inventore": "Paolo Ketoff (Roma, 1921-1996), discendente di esuli russi, si diplomò in tecnica del suono al Centro Sperimentale di Cinematografia nel 1940 e diresse gli studi di registrazione della RCA Italiana dal 1953 al 1968, lavorando tra l'altro alla colonna sonora candidata all'Oscar «55 giorni a Pechino» e a «L'Avventura» di Antonioni. Nel 1963 l'Accademia Americana di Roma gli chiese uno strumento elettronico che il compositore residente John Eaton potesse portare in scena come uno strumento tradizionale: nacque così il Synket, «Synthesizer-Ketoff».",
        "come_funziona": "Ogni sound-combiner genera un'onda quadra la cui frequenza può essere divisa per 2, 3, 4, 5 o 8 tramite pulsanti, per ottenere armonici diversi; il segnale passa poi in tre filtri (40 Hz-20 kHz) modulati da tre oscillatori a bassa frequenza. Le tastierine sono sensibili al tocco e permettono di piegare l'intonazione muovendo il dito lateralmente sul tasto, come su un clavicordo; ogni singolo tasto può essere accordato a parte, così da poter suonare scale microtonali. L'elettronica ibrida, a stato solido e valvole, lavora con segnali fino a 30V picco-picco.",
        "richiami": [
            ("FIG. 1", "3 sound-combiner indipendenti"),
            ("FIG. 2", "Tastiere a piegatura laterale"),
            ("FIG. 3", "Tasti accordabili singolarmente"),
        ],
        "chi_lusata": [
            {"artista": "John Eaton", "nota": "oltre 1000 concerti col Synket tra il 1966 e il 1974; compose «Concert Piece for Synket and Orchestra», 1968", "ig": None},
            {"artista": "John Cage", "nota": "Ketoff realizzò dal vivo le parti elettroniche dei suoi «Song Books» a Parigi, ottobre 1970", "ig": None},
            {"artista": "Domenico Guaccero e il gruppo Nuova Consonanza", "nota": "tra i compositori italiani d'avanguardia che utilizzarono gli strumenti di Ketoff a Roma", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": "Nell'aprile 1965, all'Accademia Americana di Roma, John Eaton eseguì al Synket i suoi «Songs for R.P.B.»: è generalmente considerata la prima esecuzione dal vivo mai data con un sintetizzatore elettronico, anni prima che i grandi synth modulari lasciassero gli studi di registrazione per il palco. Eaton diventò poi il concertista di riferimento dello strumento, portandolo in oltre mille concerti tra il 1966 e il 1974. Nel 1970 fu lo stesso Ketoff a realizzare dal vivo, a Parigi, le parti elettroniche dei «Song Books» di John Cage.",
        "avvertenza": "Ogni tasto va accordato singolarmente prima dell'uso: scambiare due tastierine sposta anche le note.",
        "da_ascoltare": {"brano": "Songs for R.P.B.", "artista": "John Eaton (voce e Synket, con soprano)",
                          "anno": "1965",
                          "cosa": "Prima esecuzione dal vivo mai documentata con un sintetizzatore elettronico, Accademia Americana di Roma, aprile 1965."},
        "foto": {
            "file": "assets/foto/synket/principale.jpg",
            "autore": "Dida Foto",
            "licenza": "CC BY-SA 4.0",
            "fonte": "Wikimedia Commons (foto storica del 1966, via 120years.net)",
        },
        "fonti": [
            {"titolo": "«Paolo Ketoff» — Wikipedia (IT)",
             "url": "https://it.wikipedia.org/wiki/Paolo_Ketoff", "data": "2026-09-04"},
            {"titolo": "«Studio Paolo Ketoff» — Accademia Nazionale di Santa Cecilia",
             "url": "https://santacecilia.it/studiopaoloketoff/", "data": "2026-09-04"},
            {"titolo": "«Il primo sintetizzatore portatile della storia» — Istituto Corelli",
             "url": "https://www.istitutocorelli.com/il-primo-sintetizzatore-portatile-le-origini-della-musica-elettronica-a-roma/", "data": "2026-09-04"},
            {"titolo": "«The 'Syn-ket' (or 'Synthesiser-Ketoff'). Paolo Ketoff & John Eaton, Italy, 1963» — 120 Years of Electronic Music",
             "url": "https://120years.net/the-syn-ket-or-synthesiser-ketoff-paolo-ketoff-john-eaton-italy-1963/", "data": "2026-09-04"},
        ],
        "hashtags": ["#synket", "#paoloketoff", "#sintetizzatore", "#storiadellamusica", "#musicaelettronica"],
        "verificata": True,
    },
    # ---------------------------------------------------------------- 27
    {
        "slug": "synclavier",
        "numero": 27,
        "serie": "GLI STUDI",
        "strumento": "New England Digital Synclavier",
        "anno": "1977",
        "luogo": "Norwich, Vermont",
        "costruttore": "New England Digital Corporation",
        "specifiche": [
            ("ANNO", "1977"),
            ("COSTRUTTORE", "New England Digital"),
            ("SINTESI", "FM (su licenza Yamaha) + campionamento"),
            ("PREZZO", "25.000-200.000 $"),
        ],
        "gancio": "Costava quanto una casa, suonava come un'orchestra intera e Michael Jackson ne aveva uno a casa",
        "sottotitolo": "Il primo sintetizzatore digitale in tempo reale: nato in un college del Vermont, finito nei salotti delle popstar più pagate del mondo.",
        "la_macchina": "Il Synclavier è il primo strumento digitale in tempo reale mai messo in vendita: non un computer da programmare offline come i suoi predecessori accademici, ma una macchina che rispondeva subito ai tasti, con sintesi FM, poi campionamento a 16 bit e infine un vero registratore digitale multitraccia. Costava da 25.000 a oltre 200.000 dollari a seconda della configurazione: fu per anni lo strumento-status symbol degli studi di fascia altissima e delle popstar con budget da colonna sonora, prima che i sampler economici lo rendessero superfluo.",
        "inventore_nome": "Sydney Alonso e Cameron Jones",
        "inventore": "Il Synclavier nacque al Dartmouth College, in New Hampshire, dalla collaborazione tra il professore di elettronica musicale Jon Appleton e due programmatori, Sydney Alonso e Cameron Jones, che nel 1972 lavoravano al computer centrale del college per farlo suonare e allenare l'orecchio degli studenti. Alonso e Jones fondarono la New England Digital Corporation nel 1976 a Norwich, Vermont, e nel 1977-78 misero in vendita la prima Synclavier: circa 20 unità, vendute soprattutto a università. L'azienda chiuse nel 1993 dopo circa 1.600 sistemi prodotti.",
        "come_funziona": "Il primo Synclavier genera il suono con sintesi FM, la stessa tecnologia resa poi celebre dal Yamaha DX7, prodotta su licenza dello stesso brevetto giapponese. Con il Synclavier II, dal 1980, si aggiunge il campionamento: fino a 16 bit e 100 kHz di frequenza, con dischi rigidi al posto del nastro per registrare e montare l'audio come dati digitali — anni prima che «registrazione su disco rigido» fosse un'espressione comune. La polifonia parte da 16 voci ed è arrivata, nelle configurazioni più costose, fino a 96.",
        "richiami": [
            ("FIG. 1", "Sintesi FM su licenza Yamaha"),
            ("FIG. 2", "Campionamento 16 bit, fino a 100 kHz"),
            ("FIG. 3", "Tastiera VPK velocity + pressione"),
        ],
        "chi_lusata": [
            {"artista": "Michael Jackson", "nota": "il «gong» che apre «Beat It» (1983) riproduce nota per nota un demo di fabbrica del Synclavier II del 1981", "ig": "michaeljackson"},
            {"artista": "Frank Zappa", "nota": "«Jazz from Hell» (1986), quasi interamente composto ed eseguito sul Synclavier: Grammy 1988 al Miglior Rock Instrumental", "ig": "zappa"},
            {"artista": "Sting", "nota": "«The Dream of the Blue Turtles» (1985): il Synclavier II lo accompagnò in studio e in tour per gran parte degli anni '80", "ig": "theofficialsting"},
        ],
        "menzioni_extra": [],
        "aneddoto": "L'apertura sintetica di «Beat It» — il celebre «gong» che introduce il pezzo — non è un suono originale: è la riproduzione nota per nota di un demo del Synclavier II inciso nel 1981 da Denny Jaeger su un disco promozionale distribuito da New England Digital. Michael Jackson lo aveva sentito e lo voleva identico; il tastierista Tom Bähler comprò un Synclavier, lo portò agli Westlake Studios e ricreò il suono partendo dal patch di fabbrica preimpostato, praticamente identico all'originale del demo.",
        "avvertenza": "La sintesi FM è su licenza di un brevetto giapponese. Se ricorda un DX7 non è un caso: condividono il brevetto, non il conto in banca.",
        "da_ascoltare": {"brano": "Beat It", "artista": "Michael Jackson", "anno": "1983",
                          "cosa": "L'intro sintetica è la riproduzione nota per nota di un demo di fabbrica del Synclavier II inciso nel 1981."},
        "foto": {
            "file": "assets/foto/synclavier/principale.jpg",
            "autore": "John R. Southern",
            "licenza": "CC BY-SA 2.0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "«Synclavier» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Synclavier", "data": "2026-09-04"},
            {"titolo": "«Blast from the past: New England Digital Synclavier» — MusicRadar",
             "url": "https://www.musicradar.com/news/blast-from-the-past-new-england-digital-synclavier", "data": "2026-09-04"},
            {"titolo": "«1978 New England Digital Synclavier» — Mix Magazine",
             "url": "https://www.mixonline.com/technology/1978-new-england-digital-synclavier-383609", "data": "2026-09-04"},
            {"titolo": "«Did Michael Jackson's 'Beat It' Copy A Synth Demo Record?» — Synthtopia",
             "url": "https://www.synthtopia.com/content/2023/07/22/did-michael-jacksons-beat-it-copy-a-synth-demo-record/", "data": "2026-09-04"},
            {"titolo": "«Beat It» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Beat_It", "data": "2026-09-04"},
        ],
        "hashtags": ["#synclavier", "#newenglanddigital", "#sintesifm", "#musicaelettronica", "#synth"],
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
    a = scheda.get("da_ascoltare")
    if a:
        righe.append(f"DA ASCOLTARE — {a['artista']}, «{a['brano']}» ({a['anno']}): {a['cosa']}")
        righe.append("")
    # LEZIONE IMPARATA (28/08/2026). La chiusura era «Dinamo dice: …», una
    # battuta. Riletta tutta insieme, la serie mostrava il problema: erano
    # osservazioni generiche che si potevano scambiare fra una scheda e
    # l'altra senza che nulla cambiasse — e una battuta intercambiabile non
    # è una battuta, è riempitivo. Le uniche due che funzionavano non
    # facevano dello spirito: raccontavano un fatto assurdo con la faccia
    # seria. Da qui Dinamo cambia mestiere: non è la spalla comica, è chi
    # compila il catalogo, e chiude con un'avvertenza da manuale d'uso.
    # REGOLA: l'avvertenza deve poter stare SOLO su questa scheda. Se la
    # puoi spostare su un'altra macchina, è sbagliata e va riscritta.
    # Le schede 1-4 erano già pubblicate quando è cambiata la regola e
    # restano com'erano: si riscrive il futuro, non i post usciti.
    if scheda.get("avvertenza"):
        righe.append(f"AVVERTENZE: {scheda['avvertenza']}")
    else:
        righe.append(f"Dinamo dice: «{scheda['battuta_dinamo']}»")
    righe.append("")
    righe.append(cta(scheda))
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
        a = scheda.get("da_ascoltare")
        coda = (f" Da ascoltare: {a['artista']}, «{a['brano']}» ({a['anno']}), {a['cosa']}"
                if a else "")
        return f"{nome} ({anno}) — chi ha usato questa macchina: {artisti}.{coda}"[:900]
    chiusura = scheda.get("avvertenza") or scheda.get("battuta_dinamo", "")
    return f"{nome} ({anno}) — la storia. {scheda['aneddoto'][:600]} {chiusura}"


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
    if not scheda.get("avvertenza") and not scheda.get("battuta_dinamo"):
        errori.append("manca la riga di chiusura (avvertenza)")
    if len(scheda.get("battuta_dinamo", "")) > MAX_BATTUTA:
        errori.append(f"battuta {len(scheda['battuta_dinamo'])} caratteri (max {MAX_BATTUTA})")
    if len(scheda.get("avvertenza", "")) > MAX_AVVERTENZA:
        errori.append(f"avvertenza {len(scheda['avvertenza'])} caratteri (max {MAX_AVVERTENZA})")
    a = scheda.get("da_ascoltare")
    if a:
        mancanti = [k for k in ("brano", "artista", "anno", "cosa") if not a.get(k)]
        if mancanti:
            errori.append(f"da_ascoltare incompleto, mancano: {mancanti}")
        elif len(a["cosa"]) > MAX_ASCOLTO:
            errori.append(f"da_ascoltare {len(a['cosa'])} caratteri (max {MAX_ASCOLTO})")
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
