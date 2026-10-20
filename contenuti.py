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

# Il reel del formato 2 (07/10/2026, vedi genera_reel.py): 5 battute da
# 2,6 secondi, una frase per battuta su un pannello che non deve coprire
# la macchina. In 2,6 secondi si leggono una dozzina di parole: i limiti
# stanno lì. La prima battuta è il gancio e si legge mentre il pollice
# decide se scorrere: è la più corta.
REEL_BATTUTE = 5
# Interruttore di passaggio (07/10/2026): le battute delle 62 schede sono
# in verifica. Finché non sono inserite tutte, una scheda senza battute
# non blocca i controlli (bloccherebbe il post del giorno); il suo reel
# semplicemente non si costruisce, e lo dice nel log. Si mette a True nel
# commit che inserisce le battute, e da lì non si spegne più.
REEL_OBBLIGATORIE = True
MAX_REEL_GANCIO = 60
MAX_REEL_BATTUTA = 75
MAX_REEL_KICK = 28
MAX_REEL_CTA = 50

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
        "reel_battute": [
            ("ELETTROFONI · N. 001", "Bob Moog prestò un prototipo a Sun Ra. Mai restituito."),
            ("AUTUNNO 1969", "Bill Hemsath monta il primo prototipo in pausa pranzo, con scarti."),
            ("1970 · SUN RA", "Sun Ra lo suona su «My Brother the Wind», prima che sia in vendita."),
            ("BOB MOOG", "All'inizio era scettico. Il Minimoog salverà la sua azienda."),
            ("FINO AL 1981", "Circa 12.000 esemplari. E oggi il Model D è ancora a listino."),
        ],
        "reel_cta": "Mandalo a chi non restituisce mai niente",
        # Registrazione della macchina vera (17/10/2026, regola del proprietario:
        # il suono vero in ogni uscita). Licenza verificata sulla pagina;
        # estratto 0:02-0:33 dell'assolo; dopo 0:45 la pagina annuncia una citazione dei Led Zeppelin, quindi ci si ferma prima.
        "reel_audio": {
            "file": "assets/audio/minimoog/registrazione.mp3", "inizio": 0,
            "autore": "Analogist", "licenza": "CC0 1.0",
            "fonte": "freesound.org/s/449816",
            "url": "https://freesound.org/s/449816/",
            "cosa": "un Minimoog Model D del 1977, non la riedizione: un assolo improvvisato con l'eco",
        },
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
        "reel_battute": [
            ("ELETTROFONI · N. 002", "La TR-808 morì quando finirono i transistor difettosi."),
            ("1980 · ROLAND", "Kikumoto la progetta con circuiti, senza campioni. Listino 1.195 $."),
            ("TRANSISTOR 2SC828", "Rullante, clap, piatti: fruscio da transistor scartati, presi apposta."),
            ("1983 · 12.000 UNITÀ", "Fabbriche senza più difetti, Roland senza ricambi: produzione chiusa."),
            ("METÀ ANNI '80", "Finisce al pegno a meno di 100 $. In cameretta nascono house e techno."),
        ],
        "reel_cta": "Mandalo a chi fa i beat in cameretta",
        "reel_audio": {
            "file": "assets/audio/tr808/registrazione.ogg", "inizio": 33,
            "autore": "Theofanis Siassios", "licenza": "CC BY-SA 3.0",
            "fonte": "Wikimedia Commons",
            "url": "https://commons.wikimedia.org/wiki/File:808patterns_01.ogg",
            "cosa": "una TR-808 vera che suona i suoi pattern",
        },
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
        "reel_battute": [
            ("ELETTROFONI · N. 003", "L'inventore del theremin costruì anche una cimice."),
            ("PIETROGRADO, 1920", "Lev Termen si accorge che la sua mano, senza toccare, cambia il suono."),
            ("1922 · CREMLINO", "Secondo il suo racconto, Lenin ci suonò un'aria di Glinka."),
            ("1938", "Torna in URSS e lo arrestano. Kolyma, poi un laboratorio-prigione."),
            ("«THE THING» · MOSCA 1945", "Nel Gran Sigillo regalato all'ambasciatore USA. Funziona 7 anni."),
        ],
        "reel_cta": "Mandalo a chi ama le storie di spie",
        "reel_audio": {
            "file": "assets/audio/theremin/registrazione.ogg", "inizio": 0,
            "autore": "Fabio Pesce, caricata da Effebit", "licenza": "pubblico dominio",
            "fonte": "Wikimedia Commons",
            "url": "https://commons.wikimedia.org/wiki/File:Epro_theremin_middle_bach.ogg",
            "cosa": "un theremin Moog Etherwave Pro, non uno di Termen, su una melodia di Bach",
        },
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
        "reel_battute": [
            ("ELETTROFONI · N. 004", "Collaudava Mellotron. Poi fondò i Moody Blues."),
            ("BIRMINGHAM, 1963", "Sotto ogni tasto, un nastro registrato. Dopo circa 8 secondi finisce."),
            ("MIKE PINDER · 18 MESI", "Passa 18 mesi a collaudarli nella fabbrica dei fratelli Bradley."),
            ("UN MELLOTRON USATO", "Poi ne compra uno usato. Nessuno conosce la macchina meglio di lui."),
            ("MOODY BLUES · 1967", "Ci costruisce «Nights in White Satin»."),
        ],
        "reel_cta": "Mandalo a chi ama «Nights in White Satin»",
        # Registrazione della macchina vera (17/10/2026, regola del proprietario:
        # il suono vero in ogni uscita). Licenza verificata sulla pagina;
        # l'unica registrazione libera dimostrabile: «played on a Mellotron M400». Estratto 0:02-0:17.
        "reel_audio": {
            "file": "assets/audio/mellotron/registrazione.mp3", "inizio": 0,
            "autore": "Analogist", "licenza": "CC0 1.0",
            "fonte": "freesound.org/s/449908",
            "url": "https://freesound.org/s/449908/",
            "cosa": "un Mellotron M400 che suona un nastro di effetti: i bip spaziali, non gli archi",
        },
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
        "reel_battute": [
            ("ELETTROFONI · N. 005", "Un solo preset suonava nel 40% delle hit n.1 del 1986"),
            ("1983 · 1.995 DOLLARI", "Yamaha lancia il DX7. Costa la metà di un Jupiter-8"),
            ("BRIAN ENO", "«Ce l'hanno tutti. Nessuno lo sa programmare»"),
            ("PRESET N. 11", "È E.PIANO 1, il piano elettrico di fabbrica. Nelle n.1 R&B, il 61%"),
            ("«TAKE ON ME» · 1985", "E il basso degli a-ha? Preset BASS 1, uscito così dalla fabbrica"),
        ],
        "reel_cta": "Mandalo a chi canta «Take On Me» in macchina",
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
        "reel_battute": [
            ("ELETTROFONI · N. 006", "Herbie Hancock campionò le voci di bambini e le suonò"),
            ("SYDNEY · 1979", "Il Fairlight CMI: un computer australiano con la penna ottica"),
            ("8 BIT · 73 TASTI", "Registri un suono vero, un cane o un vaso rotto, e lo suoni sui tasti"),
            ("1983 · SESAME STREET", "Le voci dei bambini diventano note, davanti a loro"),
            ("UNA DI QUELLE VOCI", "Era Tatyana Ali, futura star di «Willy, il principe di Bel-Air»"),
        ],
        "reel_cta": "Mandalo a chi sa a memoria la sigla di Willy",
        # Registrazione della macchina vera (17/10/2026, regola del proprietario:
        # il suono vero in ogni uscita). Licenza verificata sulla pagina;
        # la pagina: «Recorded with a Fairlight IIX ... essentially an 8-Bit Fairlight Sample». Riff originale.
        "reel_audio": {
            "file": "assets/audio/fairlight/registrazione.mp3", "inizio": 0,
            "autore": "amackenzie (chitarra: Ajax)", "licenza": "CC BY 3.0",
            "fonte": "freesound.org/s/150428",
            "url": "https://freesound.org/s/150428/",
            "cosa": "un Fairlight IIx che fa il suo mestiere: una chitarra acustica campionata a 8 bit e risuonata",
        },
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
        "reel_battute": [
            ("ELETTROFONI · N. 007", "Nessuno sapeva programmarla. Così nacque l'acid house"),
            ("1981 · 395 $", "Roland vende la TB-303 come basso per chi prova senza bassista"),
            ("1984 · FUORI PRODUZIONE", "Non somiglia a nessun basso. Finisce nei banchi dei pegni di Chicago"),
            ("40 O 200 DOLLARI", "Spanky dei Phuture la compra usata. Sul prezzo non concordano"),
            ("«ACID TRACKS» · 1987", "DJ Pierre gira le manopole a pattern acceso. Spanky: «continua così»"),
        ],
        "reel_cta": "Mandalo a chi non ha mai letto un manuale",
        "reel_audio": {
            "file": "assets/audio/tb303/registrazione.ogg", "inizio": 8,
            "autore": "I speak so quietly", "licenza": "CC BY-SA 4.0",
            "fonte": "Wikimedia Commons",
            "url": "https://commons.wikimedia.org/wiki/File:The_Sound_of_Roland_TB-303_for_Wikipedia.ogg",
            "cosa": "una TB-303 vera",
        },
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
        "reel_battute": [
            ("ELETTROFONI · N. 008", "Inventò l'organo Hammond e non sapeva suonare una nota"),
            ("CHICAGO · 1935", "Laurens Hammond faceva orologi elettrici. L'organo ne usa il motore"),
            ("W.L. LAHEY · CONTABILE", "I suoni li giudicava il contabile della ditta, organista diplomato"),
            ("1940 · DON LESLIE", "Ascolta al telefono l'altoparlante rotante di Leslie. Dice no"),
            ("NON SERVÌ A NIENTE", "Vieta ai negozi di venderlo. I musicisti li vorranno insieme lo stesso"),
        ],
        "reel_cta": "Mandalo a chi dice «io non so suonare»",
        # Registrazione della macchina vera (17/10/2026, regola del proprietario:
        # il suono vero in ogni uscita). Licenza verificata sulla pagina;
        # è la stessa registrazione della scheda del Leslie (lì conta la cassa, qui l'organo). Pagina: «Hammond Tonewheel H-series Organ with Leslie cabinet».
        "reel_audio": {
            "file": "assets/audio/hammond/registrazione.mp3", "inizio": 0,
            "autore": "MrAuralization", "licenza": "CC BY 4.0",
            "fonte": "freesound.org/s/158628",
            "url": "https://freesound.org/s/158628/",
            "cosa": "un organo Hammond serie H a ruote foniche, col Leslie: un giro gospel",
        },
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
        "hashtags": ["#ondesmartenot", "#mauricemartenot", "#musicaelettronica", "#radiohead", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 009", "Quel suono in «Ghostbusters» non è un theremin"),
            ("GRANDE GUERRA", "Il radiotelegrafista Martenot ama i battimenti delle valvole radio"),
            ("PARIGI · 20 APRILE 1928", "Ci lavora 10 anni. Poi li porta all'Opéra, e il solista è lui"),
            ("TASTIERA + ANELLO", "Le Ondes Martenot: un anello al dito e glissandi che sembrano una voce"),
            ("1949 → 1984", "Messiaen la vuole in «Turangalîla». Elmer Bernstein, in «Ghostbusters»"),
        ],
        "reel_cta": "Mandalo a chi giura che è un theremin",
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
        "hashtags": ["#arp2600", "#arpinstruments", "#sintetizzatore", "#starwars", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 010", "Metà della voce di R2-D2 è un essere umano"),
            ("1977 · BEN BURTT", "Ben Burtt deve dare una voce a un robot che non parla"),
            ("LISTINO 2.600 $", "Prende un ARP 2600, una valigia con gli altoparlanti dentro"),
            ("METÀ CIRCUITO", "Al synth mescola la propria voce. Per metà elettronico, per metà umano"),
            ("IL PIANTO DI R2-D2", "Ci mette 6 mesi. Ne esce un pianto acuto che riconoscono tutti"),
        ],
        "reel_cta": "Mandalo a chi sa fare la voce di R2-D2",
        # Registrazione della macchina vera (16/10/2026): licenza libera,
        # verificata sulla pagina Freesound (descrizione + licenza).
        "reel_audio": {
            "file": "assets/audio/arp2600/registrazione.mp3", "inizio": 0,
            "autore": "jonopodmore", "licenza": "CC BY 4.0",
            "fonte": "freesound.org/s/70145",
            "url": "https://freesound.org/s/70145/",
            "cosa": "un ARP 2600 vero: i 3 oscillatori su una scala esatonale, il filtro mosso a mano",
        },
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
        "hashtags": ["#vcs3", "#ems", "#sintetizzatore", "#battiato", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 011", "Battiato va fino a Londra per un synth nato in un capanno"),
            ("PUTNEY, LONDRA", "Peter Zinovieff, figlio di aristocratici russi, ha un capanno in giardino"),
            ("4.000 STERLINE", "La tiara diventa un computer. Il primo in una casa privata, dice lui"),
            ("1969 · EMS", "In quel capanno sul Tamigi nasce il VCS3. Scatola di legno, 330 sterline"),
            ("1972 · FRANCO BATTIATO", "Franco Battiato ci incide «Fetus» e «Pollution». Tra i primi in Italia"),
        ],
        "reel_cta": "Mandalo a chi ha tutti i dischi di Battiato",
        # Registrazione della macchina vera (16/10/2026): licenza libera,
        # verificata sulla pagina Freesound. Il file è un estratto di 60 s
        # (da 2:00) dei 23 minuti originali, per non appesantire il repo.
        "reel_audio": {
            "file": "assets/audio/vcs3/registrazione.mp3", "inizio": 5,
            "autore": "missionariojose", "licenza": "CC BY 4.0",
            "fonte": "freesound.org/s/205611",
            "url": "https://freesound.org/s/205611/",
            "cosa": "un VCS3 vero, quello dell'Università di Bangor, su una delle patch del suo manuale",
        },
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
        "hashtags": ["#farfisacompact", "#farfisa", "#organo", "#pinkfloyd", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 012", "«When a Man Loves a Woman» ha un organo di Ancona"),
            ("PERCY SLEDGE · 1966", "Numero uno nel 1966. L'intro la credono tutti un Hammond"),
            ("SPOONER OLDHAM ALL'ORGANO", "È un Farfisa rosso. Del booster dirà: «suonava come mille calabroni»"),
            ("CAMERANO, ANCONA", "FAbbriche Riunite FISArmoniche: 3 fabbriche fuse insieme nel 1946"),
            ("OGGI", "Il marchio Farfisa sopravvive. Sui citofoni"),
        ],
        "reel_cta": "Mandalo a chi ha un citofono Farfisa",
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
        "hashtags": ["#trautonium", "#trautwein", "#musicaelettronica", "#hitchcock", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 013", "Gli uccelli di Hitchcock non sono uccelli"),
            ("TRAUTWEIN, BERLINO 1930", "Il Trautonium non ha tasti. Si preme un filo teso su una barra"),
            ("OSKAR SALA", "Allievo di Hindemith, studia fisica per capirlo. Ci passerà 70 anni"),
            ("ALFRED HITCHCOCK", "Da giovane lo sente alla radio tedesca. Se lo ricorda per 30 anni"),
            ("«GLI UCCELLI», 1963", "Ogni stridio è Oskar Sala al Mixtur-Trautonium, con Remi Gassmann"),
        ],
        "reel_cta": "Mandalo a chi non dorme dopo «Gli uccelli»",
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
        "hashtags": ["#studiodifonologia", "#rai", "#musicaelettronica", "#johncage", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 014", "John Cage da Mike Bongiorno, come esperto di funghi"),
            ("MILANO, 1955", "Lo Studio di Fonologia: lo vogliono Berio e Maderna, la RAI paga"),
            ("NOVEMBRE 1958", "Berio invita John Cage, che ci monta «Fontana Mix»"),
            ("1959", "Intanto va a «Lascia o raddoppia?»: 5 puntate fra gennaio e febbraio"),
            ("IN PRIMA SERATA", "Fra una domanda e l'altra suona i suoi pezzi. Vince 5 milioni di lire"),
        ],
        "reel_cta": "Mandalo a chi va per funghi",
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
        "hashtags": ["#stylophone", "#dubreq", "#sintetizzatore", "#davidbowie", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 015", "C'è un giocattolo per bambini in «Space Oddity» di Bowie"),
            ("BRIAN JARVIS, 1967", "Ripara il pianoforte giocattolo della nipote e gli viene un'idea"),
            ("DUBREQ, LONDRA, 1968", "Lo Stylophone: tasti di rame stampato, e si suona con un pennino"),
            ("DAVID BOWIE", "Ci compone la melodia di «Space Oddity». E lo suona anche sul disco"),
            ("11 LUGLIO 1969", "Esce 5 giorni prima che parta l'Apollo 11. Primo successo di Bowie"),
        ],
        "reel_cta": "Mandalo a chi sa «Space Oddity» a memoria",
        "reel_audio": {
            "file": "assets/audio/stylophone/registrazione.ogg", "inizio": 11,
            "autore": "sisterray (Freesound)", "licenza": "CC0",
            "fonte": "Wikimedia Commons",
            "url": "https://commons.wikimedia.org/wiki/File:Notes_on_a_stylophone.ogg",
            "cosa": "uno Stylophone vero",
        },
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
        "hashtags": ["#spaceecho", "#roland", "#effettiaudio", "#kingtubby", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 016", "Il dub di King Tubby nasce spingendo questa scatola"),
            ("IKUTARO KAKEHASHI", "Le eco a nastro muoiono presto: il nastro, tirato, si consuma"),
            ("OSAKA, 1974", "Nel Roland Space Echo il nastro gira sciolto, senza bobine. E dura"),
            ("OLTRE METÀ CORSA", "Alzate il ritorno e l'eco si rimangia se stessa, fino a fischiare"),
            ("KING TUBBY · LEE PERRY", "Nel mix alzano il ritorno finché ulula, poi lo riabbassano"),
        ],
        "reel_cta": "Mandalo a chi mette l'eco su tutto",
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
        "hashtags": ["#korgms20", "#korg", "#sintetizzatore", "#daftpunk", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 017", "Fatto per le scuole. Ci è nato «Da Funk» dei Daft Punk"),
            ("TOKYO · 1978", "Fumio Mieda vuole i cavetti dei modulari su un synth da studente"),
            ("INGRESSO ESP", "Canti nel microfono e il Korg MS-20 suona le tue note. Anche stonate"),
            ("NEGOZI DELL'USATO", "Passa di moda e finisce nell'usato. Lì lo compra chi inventa la techno"),
            ("DAFT PUNK · 1995", "Il lead sporco e saturo di «Da Funk»? È un Korg MS-20"),
        ],
        "reel_cta": "Mandalo a chi ha consumato «Da Funk»",
        # Registrazione della macchina vera (17/10/2026, regola del proprietario:
        # il suono vero in ogni uscita). Licenza verificata sulla pagina;
        # caricata nel 2008, prima delle riedizioni (mini 2013, FS 2014). Estratto 0:30-1:15. Non è la scala scartata il 07/10.
        "reel_audio": {
            "file": "assets/audio/ms20/registrazione.mp3", "inizio": 0,
            "autore": "dajs", "licenza": "CC0 1.0",
            "fonte": "freesound.org/s/51733",
            "url": "https://freesound.org/s/51733/",
            "cosa": "un Korg MS-20 originale: il rumore bianco nell'ESP che fa partire note a caso, con phaser e riverbero",
        },
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
        "hashtags": ["#linnlm1", "#rogerlinn", "#drummachine", "#prince", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 018", "«When Doves Cry» di Prince non ha un piatto. Perché?"),
            ("LOS ANGELES · 1980", "Roger Linn campiona i colpi dell'amico batterista Art Wood, uno a uno"),
            ("5.000 DOLLARI", "La Linn LM-1 costa come un'auto. E la memoria, nel 1980, una fortuna"),
            ("8 BIT · 28 KHZ", "Cassa e rullante ci stanno. Un crash ha la coda lunga, occupa troppo"),
            ("PRINCE · 1984", "Prince la accorda più bassa. E nel disco il crash non arriva mai"),
        ],
        "reel_cta": "Mandalo al tuo amico batterista",
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
        "hashtags": ["#musiceasel", "#buchla", "#sintetizzatore", "#alessandrocortini", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 019", "Cortini cerca un Easel per anni. Trova il primo prototipo"),
            ("BERKELEY · 1973", "Don Buchla chiude uno studio intero in una valigetta: il Music Easel"),
            ("NIENTE TASTI", "«Una tastiera è dittatoriale», dice Buchla. Qui ci sono piastre sensibili"),
            ("IL PRIMO PROTOTIPO", "Alessandro Cortini lo trova anni dopo. «Ho pianto», racconta"),
            ("«FORSE» · 2013", "In un mese ci suona «Forse Vol. 1 & 2», dal vivo, senza sovraincisioni"),
        ],
        "reel_cta": "Mandalo a chi ha pianto per uno strumento",
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
        "hashtags": ["#synthex", "#elka", "#sintetizzatore", "#steviewonder", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 020", "Fatto a Castelfidardo. L'ultimo è per Stevie Wonder"),
            ("UN PROGETTO IN PROPRIO", "Mario Maggi lo progetta in proprio. Galanti/GEM e Crumar dicono di no"),
            ("ELKA · CASTELFIDARDO", "Arriva alla Elka grazie a un amico che lì deve riparare un organo"),
            ("DOPO NOTTI INSONNI", "Lo chiama Synthex: corto, con la X in fondo. Pensa ai fumetti di Tex"),
            ("«SKELETONS» · 1987", "L'ultimo Synthex, su misura per Stevie Wonder: il basso di «Skeletons»"),
        ],
        "reel_cta": "Mandalo a chi è di Castelfidardo",
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
        "hashtags": ["#tr909", "#roland", "#drummachine", "#daftpunk", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 021", "La 909 dei Daft Punk suona i piatti jazz di un tecnico"),
            ("1983 · 1.195 DOLLARI", "Roland TR-909: cassa e rullante sono sintesi. I piatti no"),
            ("ATSUSHI HOSHIAI", "Porta in ufficio i suoi piatti, un Paiste sopra e uno Zildjian sotto"),
            ("DI NOTTE, PER SETTIMANE", "Sposta i microfoni fino al punto giusto. Poi li campiona a 6 bit"),
            ("FLOP: 10.000 PEZZI", "Roland la ritira dopo un anno. Da usata, farà techno e house"),
        ],
        "reel_cta": "Mandalo al tuo amico batterista jazz",
        # Registrazione della macchina vera (17/10/2026, regola del proprietario:
        # il suono vero in ogni uscita). Licenza verificata sulla pagina;
        # NON è «909 house pattern.ogg», scartata il 07/10 perché fatta in FL Studio. Pagina: «fait à la TR-909». Estratto 0:06-0:46.
        "reel_audio": {
            "file": "assets/audio/tr909/registrazione.mp3", "inizio": 0,
            "autore": "Sylvain87", "licenza": "CC BY 1.0",
            "fonte": "Wikimedia Commons",
            "url": "https://commons.wikimedia.org/wiki/File:TR-909.ogg",
            "cosa": "una Roland TR-909 vera: un pattern house con qualche variazione suonata dal vivo",
        },
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
        "hashtags": ["#optigan", "#mattel", "#organo", "#davidlynch", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 022", "Il suono di un giocattolo Mattel è in «Twin Peaks»"),
            ("27 GENNAIO 1971", "Mattel presenta l'Optigan, un organo da salotto per famiglie"),
            ("57 PISTE OTTICHE", "Suona registrazioni vere su un disco, lette con la luce come al cinema"),
            ("1980 · WESSEX STUDIOS", "Steve Hackett lo registra in un bagno, col disco «Big Band Beat»"),
            ("DAVID LYNCH", "Lynch campiona lo stesso disco. Nel 2017 è in «Twin Peaks: The Return»"),
        ],
        "reel_cta": "Mandalo a chi ha visto tutto «Twin Peaks»",
        # Registrazione della macchina vera (16/10/2026): licenza libera,
        # verificata sulla pagina Freesound (descrizione + licenza).
        "reel_audio": {
            "file": "assets/audio/optigan/registrazione.mp3", "inizio": 0,
            "autore": "Make Noise", "licenza": "CC0 1.0",
            "fonte": "freesound.org/s/522914",
            "url": "https://freesound.org/s/522914/",
            "cosa": "pattern di batteria letti dai dischi ottici di un Optigan vero",
        },
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
        "gancio": "Registri un violino una volta sola e lo suoni su 61 tasti. Nel 1984 pareva un trucco da prestigiatore",
        "sottotitolo": "Il campionatore a 8 bit della E-mu: quello che ha messo un'orchestra su un dischetto da 5 pollici e un quarto.",
        "la_macchina": "È una tastiera grigia da 61 tasti con due lettori di floppy sul fianco sinistro, e dentro non c'è nessun suono: li carichi tu, dai dischetti. E-mu li vendeva a librerie (archi, ottoni, un flauto giapponese, perfino un vetro rotto) e puoi registrare anche i tuoi, a 8 bit. Il campione poi va su tutta la tastiera da solo, più acuto a destra e più grave a sinistra, e più ti allontani dalla nota originale più si sente che è una registrazione tirata. A me piace proprio quello: gli archi dell'Emulator non suonano veri, suonano da Emulator. Costava molto meno di un Fairlight, e uno studio serio se lo poteva permettere.",
        "inventore_nome": "Dave Rossum e Scott Wedge",
        "inventore": "Dave Rossum e Scott Wedge fondano la E-mu nel 1971 a Santa Cruz e per anni costruiscono sintetizzatori modulari su misura, pochi pezzi, per altri musicisti. Al NAMM del 1979 vedono il Fairlight CMI e la Linn LM-1 e fanno i conti: il Fairlight costa 30.000 dollari, la stessa cosa si può fare spendendo molto meno. Il primo Emulator esce nel 1981. Il II, nel 1984, aggiunge la cosa che secondo me lo salva dall'essere solo un Fairlight povero: i filtri analogici SSM2045, che addolciscono i campioni a 8 bit e li fanno suonare come se fossero passati da un synth.",
        "come_funziona": "Il suono entra da un ingresso, viene tagliato in 27.700 fettine al secondo e ognuna viene scritta con un numero a 8 bit, cioè uno fra 256 valori. Sono pochi, e si sente: da lì viene il fruscio granuloso dei campioni. Il dischetto da 5 pollici e un quarto li conserva. Quando premi un tasto la macchina rilegge la registrazione a una velocità diversa per ogni nota, poi la passa in un filtro analogico, il chip SSM2045, a 4 poli, che toglie le frequenze alte in modo morbido e, se alzi la risonanza, si mette a cantare. Otto voci, quindi otto note alla volta; otto parti diverse via MIDI; un sequencer a 8 tracce.",
        "richiami": [
            ("FIG. 1", "Campionamento 8 bit, 27,7 kHz"),
            ("FIG. 2", "Filtro risonante SSM2045, 24 dB/oct"),
            ("FIG. 3", "61 tasti velocity + floppy 5¼\""),
        ],
        "chi_lusata": [
            {"artista": "Pet Shop Boys", "nota": "«West End Girls» (1986): gli archi, la tromba e la cassa sono campioni Emulator, uno sopra l'altro", "ig": "petshopboys"},
            {"artista": "Peter Gabriel", "nota": "Il flauto che apre «Sledgehammer» (1986) è il dischetto shakuhachi della libreria E-mu", "ig": None},
            {"artista": "Sade", "nota": "«Love Is Stronger Than Pride»: stesso flauto, stesso dischetto", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": "Nella libreria dell'Emulator II c'è un dischetto con un flauto giapponese, uno shakuhachi, registrato senza pensare a niente di preciso. Nel 1986 quel campione apre «Sledgehammer» di Peter Gabriel. Poi lo ritrovi in «Love Is Stronger Than Pride» di Sade, e negli Enigma. È proprio la stessa registrazione, uscita dallo stesso floppy, e per anni nessuno ci ha fatto caso: sentivi un flauto e pensavi a un flautista. Io l'ho scoperto tardi, e da quel giorno lo sento dappertutto.",
        "avvertenza": "Il filtro SSM2045 scalda qualsiasi campione digitale. Anche un vetro rotto, se glielo chiedete gentilmente, suonerà quasi analogico.",
        "da_ascoltare": {"brano": "Sledgehammer", "artista": "Peter Gabriel", "anno": "1986",
                          "cosa": "Il flauto dell'intro. Ascoltatelo sapendo che è un dischetto di fabbrica: non torna più come prima."},
        "foto": {
            "file": "assets/foto/emulator/principale.jpg",
            "ritaglio": True,   # scontornata su bianco: si mostra intera
            "autore": "John R. Southern",
            "licenza": "CC BY-SA 2.0",
            "fonte": "Wikimedia Commons (originariamente Flickr)",
        },
        # Tre inquadrature diverse invece della stessa foto ripetuta su
        # copertina, slide 2 e slide 3 (richiesta del proprietario,
        # 13/09/2026). Ognuna serve alla sua slide: lo strumento intero
        # per «che cos'e'», i due lettori da 5 pollici e un quarto per
        # chi l'ha costruita, la scheda di memoria per «come funziona» —
        # che su un campionatore e' letteralmente il punto.
        "foto_extra": [
            {"file": "assets/foto/emulator/strumento.jpg", "ritaglio": True,
             "autore": "Mojosynths, ritocco di Pittigrilli",
             "licenza": "pubblico dominio",
             "fonte": "Wikimedia Commons",
             "didascalia": "Il pannello"},
            {"file": "assets/foto/emulator/dischi.jpg",
             "autore": "John R. Southern",
             "licenza": "CC BY-SA 2.0",
             "fonte": "Wikimedia Commons",
             "didascalia": "I due lettori da 5\u00bc pollici"},
            {"file": "assets/foto/emulator/memoria.jpg",
             "autore": "John R. Southern",
             "licenza": "CC BY-SA 2.0",
             "fonte": "Wikimedia Commons",
             "didascalia": "La scheda di memoria"},
        ],
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
        "hashtags": ["#emulator", "#emu", "#campionatore", "#petergabriel", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 023", "Il flauto di «Sledgehammer» è un dischetto di fabbrica"),
            ("1984 · SANTA CRUZ", "Dentro l'E-mu Emulator II non c'è un suono. Li carichi da floppy"),
            ("UN FLAUTO GIAPPONESE", "Fra archi e ottoni, nella libreria E-mu c'è anche uno shakuhachi"),
            ("1986 · PETER GABRIEL", "Apre «Sledgehammer». Senti un flauto e pensi a un flautista"),
            ("STESSO DISCHETTO", "Lo ritrovi in «Love Is Stronger Than Pride» di Sade. E negli Enigma"),
        ],
        "reel_cta": "Mandalo a chi canta «Sledgehammer» in auto",
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
        "gancio": "Costa poco, pesa poco, suona di plastica. E i Duran Duran ci hanno fatto i primi due dischi",
        "sottotitolo": "Il synth di archi e ottoni della Crumar, anno 1979: 49 tasti, 15 cursori e neanche una memoria.",
        "la_macchina": "Una tastiera di 49 tasti con due file di cursori sopra, da una parte gli ottoni, dall'altra gli archi. Dentro non ci sono oscillatori come in un synth normale. C'è un generatore digitale che fa le 12 note più acute e una catena di divisori che le porta giù di ottava in ottava, quindi puoi premere tutti i tasti che vuoi e suonano tutti. Gli archi passano da un chorus a BBD, gli ottoni da un filtro con il suo inviluppo, e i due si mescolano sui 15 cursori. Memorie: zero. Dicono tutti che suona di plastica. Sì. Ma è una plastica che nel 1979 costava molto meno degli altri e si portava in giro senza fatica.",
        "inventore_nome": "Crumar (Mario Crucianelli)",
        "inventore": "Mario Crucianelli viene dalla Elka, l'azienda di famiglia. Nel 1971 la lascia dopo una spaccatura in casa e fonda la Crumar a Castelfidardo, la città delle fisarmoniche. In pochi anni arriva a 300 dipendenti su due laboratori. Prima del Performer fa pianoforti elettronici e string machine, i Compac; dopo arrivano il DS-2 e, nel 1983, lo Spirit, disegnato insieme a Bob Moog. Il Performer sta in mezzo, e per me è quello che spiega meglio cosa sapeva fare quella fabbrica: prendere un'idea semplice e farla costare poco.",
        "come_funziona": "Un chip genera le 12 note dell'ottava più alta come onde quadre. Sotto ci sono i divisori: ogni stadio dimezza la frequenza, e dimezzare vuol dire scendere di un'ottava esatta. Così tutte le note di tutte le ottave esistono già, sempre, e il tasto non fa altro che aprire il rubinetto di quella giusta. Per questo non c'è un limite di polifonia, ed è anche per questo che tutto ha lo stesso carattere un po' fermo, da organo. Gli archi lo nascondono con il chorus a BBD, che sfasa il segnale e lo fa ondeggiare; gli ottoni con un filtro passa-basso e un inviluppo di attacco e decadimento.",
        "richiami": [
            ("FIG. 1", "Generatore top-octave + divisori"),
            ("FIG. 2", "15 cursori, zero memorie"),
            ("FIG. 3", "Sezioni Strings e Brass separate"),
        ],
        "chi_lusata": [
            {"artista": "Nick Rhodes (Duran Duran)", "nota": "Gli archi dei primi due album, «Duran Duran» (1981) e «Rio» (1982), accanto a Jupiter-4 e Prophet-5", "ig": None},
        ],
        "menzioni_extra": [
            {"ig": "crumar_instruments",
             "riga": "Il marchio Crumar è ancora attivo, oggi a Roncade (TV): lo trovate come @crumar_instruments."},
        ],
        "aneddoto": "Nick Rhodes lo mette nei primi due dischi dei Duran Duran, «Duran Duran» del 1981 e «Rio» del 1982, e lo tiene accanto a un Jupiter-4 e a un Prophet-5 che costavano molto di più. Gli archi che sentite lì sono in buona parte suoi. Eppure il Performer è rimasto uno dei synth italiani che i collezionisti guardano meno, con la fama del suono «plasticoso». A me quella plastica piace, ed è anche il motivo per cui la macchina ha viaggiato tanto: costava poco, e si è ritrovata su parecchi dischi new wave dei primi anni Ottanta.",
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
        "hashtags": ["#crumarperformer", "#crumar", "#sintetizzatore", "#duranduran", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 024", "Gli archi dei primi Duran Duran? Molti da Castelfidardo"),
            ("CASTELFIDARDO, 1971", "Mario Crucianelli lascia l'Elka di famiglia e fonda la Crumar"),
            ("1979 · 49 TASTI", "Esce il Crumar Performer: archi e ottoni, 15 cursori, zero memorie"),
            ("SUONA DI PLASTICA", "Lo dicono tutti. Però costa molto meno degli altri, e pesa poco"),
            ("NICK RHODES", "Lo usa su «Duran Duran» e «Rio», vicino a un Prophet-5 molto più caro"),
        ],
        "reel_cta": "Mandalo a chi aveva il poster dei Duran Duran",
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
        "gancio": "Nato come il Juno economico. Quarant'anni dopo lo clonano ancora",
        "sottotitolo": "Sei voci analogiche, un chorus che fa quasi tutto il lavoro e un chip che prima o poi muore.",
        "la_macchina": "Esce a febbraio del 1984 ed è il Juno-60 rifatto per costare meno: 6 voci, il MIDI, 128 memorie invece di 64. Ogni voce ha un oscillatore solo e un filtro passa-basso a 24 dB per ottava con la risonanza. Da solo suona sottile, quasi povero. Poi c'è il chorus stereo, con due profondità, e quando lo accendi il suono si allarga e diventa quella cosa lucida e piena che tutti chiamano «suono Juno». Lo dico sempre a chi ne compra uno: il Juno è il chorus. Il resto è un buon synth normale.",
        "inventore_nome": "Roland Corporation (progetto di squadra)",
        "inventore": "Non c'è un nome. Roland, fondata a Osaka nel 1972 da Ikutaro Kakehashi, non ha mai accreditato un progettista per il Juno-106, a differenza di altre sue macchine dell'epoca: fu un lavoro di squadra con un obiettivo preciso, tenere il suono del Juno-60 abbassando i costi. Il primo Juno, il 6, è del 1982; il 106 è il terzo della serie. La scelta che lo rese possibile fu il DCO, un oscillatore comandato da un clock digitale, molto più economico dei VCO analogici. Mi piace che sia una macchina senza padre. La spiega bene.",
        "come_funziona": "Il DCO non è un oscillatore digitale. È analogico: un transistor scarica un condensatore e la rampa che ne esce è una vera onda a dente di sega. Digitale è solo il comando, cioè il clock che decide quando scaricare, generato da un microcontrollore. Per questo l'accordatura non va mai via, cosa che nel 1984 con i VCO non era affatto scontata. Un convertitore digitale-analogico rialza il volume delle note più acute, che altrimenti uscirebbero deboli. Dopo l'oscillatore, filtro e amplificatore stanno in un chip solo, l'80017A, uno per voce.",
        "richiami": [
            ("FIG. 1", "DCO: oscillatore a clock digitale"),
            ("FIG. 2", "Chorus stereo a BBD, due profondità"),
            ("FIG. 3", "Chip voce 80017A, uno per voce"),
        ],
        "chi_lusata": [
            {"artista": "Chvrches", "nota": "Quasi tutto il basso di «The Bones of What You Believe» (2013)", "ig": None},
            {"artista": "William Orbit", "nota": "Ce l'aveva in studio già alla fine degli anni Ottanta, e si sente", "ig": None},
            {"artista": "Vince Clarke", "nota": "In studio fisso, accanto a Xpander, MKS-80 e Prophet VS", "ig": None},
        ],
        "menzioni_extra": [
            {"ig": "rolandglobal",
             "riga": "Il produttore originale, Roland Corporation, è ancora @rolandglobal."},
        ],
        "aneddoto": "Quel chip, l'80017A, non lo fanno più da decenni e ha un tasso di guasto che fra i tecnici è quasi una barzelletta. Una voce se ne va, poi un'altra. Oggi esistono cloni moderni fatti apposta per sostituirlo, e se ne trovate uno usato è quasi certo che abbia già perso e recuperato almeno una voce. Il mio consiglio, prima di comprarlo: tenete premute sei note e contatele.",
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
        "hashtags": ["#juno106", "#roland", "#sintetizzatore", "#vinceclarke", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 025", "Ha 6 voci. Prima di comprarlo, contatele."),
            ("FEBBRAIO 1984", "Roland Juno-106: il Juno-60 rifatto per costare meno."),
            ("CHIP 80017A", "Ogni voce vive in un chip suo. Non lo fanno più da decenni."),
            ("TASSO DI GUASTO", "Fra i tecnici è quasi una barzelletta. Muore una voce, poi un'altra."),
            ("SE NE TROVATE UNO USATO", "Quasi di sicuro ha già perso e ritrovato almeno una voce."),
        ],
        "reel_cta": "Mandalo a chi sta per comprare un Juno-106",
        # Registrazione della macchina vera (16/10/2026): licenza libera,
        # verificata sulla pagina Freesound (descrizione + licenza).
        "reel_audio": {
            "file": "assets/audio/juno106/registrazione.mp3", "inizio": 225,
            "autore": "missionariojose", "licenza": "CC BY 4.0",
            "fonte": "freesound.org/s/219360",
            "url": "https://freesound.org/s/219360/",
            "cosa": "uno Juno-106 vero in un'improvvisazione registrata diretta",
        },
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
        "gancio": "Roma, 1963: un tecnico del suono costruisce un synth da portare in scena. Il Moog da palco arriva dopo",
        "sottotitolo": "Tre tastierine, tre generatori, una decina di esemplari fatti a mano da Paolo Ketoff per l'Accademia Americana.",
        "la_macchina": "Tre moduli uguali, che Ketoff chiama sound-combiner, ognuno con un oscillatore a onda quadra, i suoi divisori, i filtri e i modulatori, e ognuno con la sua tastierina di due ottave. Tutto va in un'uscita sola. È uno strumento da concerto, fatto per stare su un palco, e siamo nel 1963, prima del Minimoog. Ketoff ne ha costruiti a mano una decina in dodici anni, uno diverso dall'altro. Oggi stanno nei musei, a Roma, Parigi, Monaco, Baltimora e Milano. La cosa che mi colpisce, guardandolo, è quanto è piccolo.",
        "inventore_nome": "Paolo Ketoff",
        "inventore": "Paolo Ketoff nasce a Roma nel 1921 da una famiglia di esuli russi. Si diploma in tecnica del suono al Centro Sperimentale nel 1940 e dal 1953 al 1968 dirige gli studi della RCA Italiana, dove passano anche «L'Avventura» di Antonioni e «55 giorni a Pechino», che prende una candidatura all'Oscar per la colonna sonora. Nel 1963 l'Accademia Americana gli chiede una cosa strana per l'epoca: uno strumento elettronico che il compositore residente, John Eaton, possa portare in scena come un pianoforte o un violino. Lui lo chiama Synket, Synthesizer-Ketoff. Muore nel 1996.",
        "come_funziona": "Ogni modulo parte da un'onda quadra. Con dei pulsanti la dividi per 2, 3, 4, 5 o 8 e ottieni altre altezze, in rapporto armonico con la prima. Poi tre filtri, da 40 Hz a 20 kHz, mossi da tre oscillatori lenti. Le tastierine sentono il tocco e, se sposti il dito di lato sul tasto, l'intonazione si piega, come su un clavicordo. Ogni tasto si accorda per conto suo, quindi puoi costruirti scale che sul pianoforte non esistono. Dentro c'è un misto di valvole e transistor, con segnali fino a 30 volt picco-picco. Roba robusta.",
        "richiami": [
            ("FIG. 1", "3 sound-combiner indipendenti"),
            ("FIG. 2", "Tastiere a piegatura laterale"),
            ("FIG. 3", "Tasti accordabili singolarmente"),
        ],
        "chi_lusata": [
            {"artista": "John Eaton", "nota": "Più di 1.000 concerti col Synket fra il 1966 e il 1974, e un «Concert Piece for Synket and Orchestra» nel 1968", "ig": None},
            {"artista": "John Cage", "nota": "Le parti elettroniche dei «Song Books», Parigi, ottobre 1970: le fa Ketoff dal vivo", "ig": None},
            {"artista": "Domenico Guaccero e il gruppo Nuova Consonanza", "nota": "Fra i romani d'avanguardia che usavano gli strumenti di Ketoff", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": "Aprile 1965, Accademia Americana di Roma. John Eaton suona al Synket i suoi «Songs for R.P.B.», e per quanto se ne sa è la prima volta che un sintetizzatore viene suonato dal vivo davanti a un pubblico. I grandi modulari, in quegli anni, stavano ancora chiusi negli studi. Eaton diventa l'uomo del Synket, oltre 1.000 concerti fra il 1966 e il 1974. E nel 1970, a Parigi, è Ketoff in persona a fare dal vivo le parti elettroniche dei «Song Books» di John Cage.",
        "avvertenza": "Ogni tasto va accordato singolarmente prima dell'uso: scambiare due tastierine sposta anche le note.",
        "da_ascoltare": {"brano": "Songs for R.P.B.", "artista": "John Eaton (voce e Synket, con soprano)",
                          "anno": "1965",
                          "cosa": "Aprile 1965, Roma: il primo concerto con un sintetizzatore di cui si abbia notizia. Una voce di soprano e il Synket, niente altro."},
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
        "hashtags": ["#synket", "#paoloketoff", "#sintetizzatore", "#johncage", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 026", "Il primo concerto con un synth? Forse è stato a Roma."),
            ("ROMA, 1963", "Paolo Ketoff, tecnico del suono, costruisce il Synket."),
            ("ACCADEMIA AMERICANA", "È per John Eaton, da portare in scena come un violino."),
            ("APRILE 1965", "Eaton lo suona dal vivo. I grandi modulari stanno chiusi negli studi."),
            ("1966-1974", "Poi Eaton, col Synket, fa più di 1.000 concerti."),
        ],
        "reel_cta": "Mandalo a chi porta i synth sul palco",
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
        "gancio": "Costava quanto una casa, e Michael Jackson ne aveva uno in casa",
        "sottotitolo": "Il primo strumento digitale che rispondeva subito ai tasti. Nato in un college del Vermont, finito in mano a chi poteva spendere 200.000 dollari.",
        "la_macchina": "Prima del Synclavier, per fare musica con un computer scrivevi le note e aspettavi che la macchina le calcolasse. Questo invece risponde subito, tasto premuto e suono fuori, ed è il primo del genere messo in vendita. Parte con la sintesi FM, poi aggiunge il campionamento a 16 bit e alla fine un registratore digitale multitraccia vero. Il prezzo andava da 25.000 a più di 200.000 dollari, e infatti lo trovavi negli studi più ricchi e a casa delle popstar. Quando i campionatori economici hanno cominciato a fare le stesse cose è sparito in fretta. A me resta simpatico proprio per quanto era esagerato.",
        "inventore_nome": "Sydney Alonso e Cameron Jones",
        "inventore": "Nel 1972, al Dartmouth College nel New Hampshire, il professore Jon Appleton e due programmatori, Sydney Alonso e Cameron Jones, lavorano al computer centrale del campus per farlo suonare e per allenare l'orecchio degli studenti. Alonso e Jones fondano la New England Digital nel 1976, a Norwich, nel Vermont, e fra il 1977 e il 1978 vendono il primo Synclavier: circa 20 unità, quasi tutte a università. L'azienda chiude nel 1993, dopo circa 1.600 sistemi. Non tantissimi, se pensate a quanto se ne è parlato.",
        "come_funziona": "Il primo Synclavier fa il suono con la sintesi FM, la stessa tecnica che qualche anno dopo il Yamaha DX7 porterà in tutte le case, prodotta su licenza dello stesso brevetto. Dal 1980, con il Synclavier II, arriva il campionamento: fino a 16 bit e 100 kHz, con i dischi rigidi al posto del nastro, così registri e tagli l'audio come dati, anni prima che la frase «registrare su hard disk» volesse dire qualcosa per qualcuno. La polifonia parte da 16 voci e nelle configurazioni più care arriva a 96.",
        "richiami": [
            ("FIG. 1", "Sintesi FM su licenza Yamaha"),
            ("FIG. 2", "Campionamento 16 bit, fino a 100 kHz"),
            ("FIG. 3", "Tastiera VPK velocity + pressione"),
        ],
        "chi_lusata": [
            {"artista": "Michael Jackson", "nota": "Il «gong» di «Beat It» (1983) è un demo di fabbrica del Synclavier II del 1981, rifatto uguale", "ig": "michaeljackson"},
            {"artista": "Frank Zappa", "nota": "«Jazz from Hell» (1986), quasi tutto scritto e suonato sul Synclavier: Grammy nel 1988", "ig": "zappa"},
            {"artista": "Sting", "nota": "«The Dream of the Blue Turtles» (1985), e poi in tour per buona parte degli anni Ottanta", "ig": "theofficialsting"},
        ],
        "menzioni_extra": [],
        "aneddoto": "Il «gong» che apre «Beat It», nel 1983, non è un suono fatto per quel disco. È un demo del Synclavier II che Denny Jaeger aveva inciso nel 1981 per un disco promozionale della New England Digital. Michael Jackson lo sente e lo vuole così, identico. Il tastierista Tom Bähler compra un Synclavier, lo porta agli Westlake Studios e lo rifà partendo dal suono di fabbrica, che era già quasi quello. Quindi quel disco si apre con un preset. Non lo dico per sminuirlo, lo dico perché è andata così.",
        "avvertenza": "La sintesi FM è su licenza di un brevetto giapponese. Se ricorda un DX7 non è un caso: condividono il brevetto, non il conto in banca.",
        "da_ascoltare": {"brano": "Beat It", "artista": "Michael Jackson", "anno": "1983",
                          "cosa": "L'intro. È un demo di fabbrica del 1981 rifatto nota per nota. Riascoltatelo sapendolo."},
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
        "hashtags": ["#synclavier", "#newenglanddigital", "#sintetizzatore", "#michaeljackson", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 027", "Il gong di «Beat It» nasce da un preset di fabbrica."),
            ("1981 · DISCO PROMOZIONALE", "È un demo che Denny Jaeger incide per il Synclavier II."),
            ("MICHAEL JACKSON", "Jackson lo sente e lo vuole così, identico."),
            ("TOM BÄHLER", "Il tastierista compra un Synclavier e lo porta in studio."),
            ("WESTLAKE STUDIOS", "Lo rifà partendo dal suono di fabbrica, che è già quasi quello."),
        ],
        "reel_cta": "Mandalo a chi dice che i preset sono da pigri",
        "verificata": True,
    },
    # ---------------------------------------------------------------- 28
    {
        "slug": "simmonssds5",
        "numero": 28,
        "serie": "LE DRUM MACHINE",
        "strumento": "Simmons SDS-V",
        "anno": "1981",
        "luogo": "Hatfield",
        "costruttore": "Simmons",
        "specifiche": [
            ("ANNO", "1981"),
            ("ORIGINE", "Inghilterra"),
            ("PELLI", "Esagonali, in policarbonato"),
            ("SUONO", "Sintesi analogica"),
        ],
        "gancio": "Le pelli sono ricavate dagli scudi antisommossa. Non è una metafora",
        "sottotitolo": "Il primo kit elettronico che un batterista poteva suonare al posto della batteria, non accanto.",
        "la_macchina": "Sei pastiglie esagonali collegate a un cervello a moduli: uno per la cassa, uno per il rullante, uno per ogni tom. Ogni modulo è un piccolo sintetizzatore con le sue manopole (rumore, tono, tempo di decadimento, click d'attacco) e non c'è nessun campione dentro: il suono si costruisce girando i comandi. Esce nella prima metà del 1981 e in un paio d'anni quel tom che scende lo senti in radio di continuo.",
        "inventore_nome": "Dave Simmons",
        "inventore": "Simmons fonda la sua azienda nel 1978 a St Albans e porta la prima versione alla fiera musicale di Londra nel 1981. Non aveva solo pastiglie esagonali: al banchetto c'erano anche un kit a forma di cuore e uno a forma di pipistrello. L'esagono vinse perché era l'unica forma che si poteva affiancare senza lasciare buchi, e perché sembrava una cosa del futuro invece di una batteria mancata.",
        "come_funziona": "Sotto la superficie dura c'è un sensore che misura quanto forte la colpisci, e basta: non registra dove, non registra come. Quel singolo numero fa partire il modulo, che genera il suono da zero \u2014 un impulso di rumore per il rullante, un'oscillazione che scende di tono per il tom. È per questo che il tom della Simmons fa quel «pioum» che scivola verso il basso: non è un tom registrato, è un'onda a cui qualcuno ha detto di cadere.",
        "richiami": [
            ("FIG. 1", "Pastiglia esagonale, sensore unico"),
            ("FIG. 2", "Un modulo per ogni pezzo"),
            ("FIG. 3", "Tom: oscillatore che scende"),
        ],
        "chi_lusata": [
            {"artista": "Bill Bruford", "nota": "Dai King Crimson in poi: la batteria smette di imitare il legno", "ig": None},
            {"artista": "Phil Collins", "nota": "Il tom elettronico diventa il suono degli anni Ottanta", "ig": None},
            {"artista": "Talk Talk", "nota": "Lee Harris la usa quando suonava ancora nuova, non nostalgica", "ig": None},
            {"artista": "The Cars", "nota": "David Robinson fra i primi a metterla su disco in America", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": "Le pastiglie erano fatte dello stesso policarbonato durissimo degli scudi che la polizia inglese usava in quegli anni. Robustissime: reggevano qualunque bacchettata. Il problema è che restituivano tutto il colpo al braccio di chi le suonava, e i batteristi hanno cominciato a lamentarsi di polsi e gomiti. Se ne trovate una, provatela con bacchette leggere e non fate una serata intera la prima volta.",
        "avvertenza": "La superficie non cede di un millimetro. Tutto quello che dai torna indietro, e a fine serata lo senti nei polsi.",
        "foto": {
            "file": "assets/foto/simmonssds5/principale.jpg",
            "autore": "Wolfgang Stief",
            "licenza": "CC BY 2.0",
            "fonte": "Wikimedia Commons \u2014 Deutsches Museum",
        },
        "fonti": [
            {"titolo": "«Simmons SDSV» \u2014 Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Simmons_SDSV", "data": "2026-09-09"},
            {"titolo": "«SDS-V Drum Synthesizer, 1981» \u2014 We Are the Mutants",
             "url": "https://wearethemutants.com/2017/04/12/sds-v-drum-synthesizer-1981/", "data": "2026-09-09"},
        ],
        "hashtags": ["#simmonssdsv", "#simmons", "#batteriaelettronica", "#philcollins", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 028", "Pelli dello stesso materiale degli scudi antisommossa."),
            ("INGHILTERRA, 1981", "Simmons SDS-V: 6 pastiglie esagonali al posto della batteria."),
            ("POLICARBONATO", "Reggono qualunque bacchettata. Non cedono di un millimetro."),
            ("IL PROBLEMA", "Il colpo torna tutto nel braccio. I batteristi si lamentano dei polsi."),
            ("IN UN PAIO D'ANNI", "Quel tom che scende lo senti in radio di continuo."),
        ],
        "reel_cta": "Mandalo a un batterista che picchia forte",
        "verificata": True,
    },
    # ---------------------------------------------------------------- 29
    {
        "slug": "solina",
        "numero": 29,
        "serie": "GLI ORGANI",
        "strumento": "Solina String Ensemble",
        "anno": "1974",
        "luogo": "Bodegraven",
        "costruttore": "Eminent",
        "specifiche": [
            ("ANNO", "1974"),
            ("ORIGINE", "Paesi Bassi"),
            ("VOCI", "Sei, a interruttore"),
            ("CHORUS", "Triplo, a secchielli"),
        ],
        "gancio": "Spegni il chorus e resta un organo mediocre. Quell'effetto \u00e8 met\u00e0 dello strumento",
        "sottotitolo": "Non imita gli archi: fabbrica un suono che gli assomiglia e che nessuna orchestra ha mai fatto.",
        "la_macchina": "Dodici oscillatori, uno per ogni nota della scala, e una catena di divisori che li abbassa di ottava in ottava: così tutti i tasti suonano insieme, senza limiti di polifonia. Sei interruttori accendono le voci (violino, viola, tromba, corno, violoncello, contrabbasso) e si possono tenere premuti tutti insieme. Nasce nel 1974 dalla sezione archi di un organo da salotto, l'Eminent 310 Unique.",
        "inventore_nome": "Eminent BV",
        "inventore": "Eminent costruiva organi elettronici in Olanda, a Bodegraven. Nel 310 Unique del 1972 c'era una sezione «archi» che piaceva pi\u00f9 di tutto il resto dell'organo: la staccarono, le misero una tastiera intorno e la vendettero da sola. \u00c8 uno dei rari casi in cui uno strumento nasce non da un'invenzione ma da un pezzo di un'altra macchina che funzionava troppo bene per restare l\u00ec dentro.",
        "come_funziona": "Il trucco non sta negli oscillatori, che da soli darebbero un suono fermo e sottile. Sta dopo: tre linee di ritardo a «secchielli» \u2014 catene di condensatori che passano il segnale di mano in mano \u2014 pilotate da due oscillatori lenti che ne cambiano di continuo la velocit\u00e0. Il risultato \u00e8 la stessa nota sfasata tre volte, che batte contro se stessa: l'orecchio la sente come tanti strumenti leggermente scordati, cio\u00e8 come una sezione d'archi.",
        "richiami": [
            ("FIG. 1", "Dodici oscillatori, divisori a valle"),
            ("FIG. 2", "Sei voci a interruttore"),
            ("FIG. 3", "Tre ritardi + due oscillatori lenti"),
        ],
        "chi_lusata": [
            {"artista": "Pink Floyd", "nota": "Richard Wright: il tappeto sotto met\u00e0 di quello che suonano dal 1975", "ig": "pinkfloyd"},
            {"artista": "Jean-Michel Jarre", "nota": "Il velo di archi che tiene insieme le sue lunghe distese", "ig": "jeanmicheljarre"},
            {"artista": "Herbie Hancock", "nota": "Lo porta dentro il jazz elettrico quando nessuno se lo aspettava", "ig": "herbiehancock"},
            {"artista": "Elton John", "nota": "Archi finti su dischi che potevano permettersi quelli veri", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": "In America non la conoscevano come Solina. La distribuiva la ARP, quella degli Odyssey e dei 2600, e ci metteva sopra il proprio marchio: ARP String Ensemble. Dentro era la stessa macchina fatta a Bodegraven, in Olanda. Così un sacco di dischi degli anni Settanta che sembrano avere gli archi veri hanno dentro questa scatola olandese, con uno dei due nomi sopra. Io le riconosco dal chorus: una volta che lo hai sentito, non lo confondi più.",
        "avvertenza": "Il chorus non si spegne mai. Senza, restano dodici oscillatori fermi: l'effetto non abbellisce il suono, lo costruisce.",
        "foto": {
            "file": "assets/foto/solina/principale.jpg",
            "autore": "Pingel",
            "licenza": "CC BY-SA 3.0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "\u00abARP String Ensemble\u00bb \u2014 Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/ARP_String_Ensemble", "data": "2026-09-10"},
            {"titolo": "\u00abSolina String Ensemble Series 2 e Series 42\u00bb \u2014 EBOARDMUSEUM, Google Arts & Culture",
             "url": "https://artsandculture.google.com/story/solina-string-ensemble-series-2-and-series-42/ZAVBDLMPNTX_zQ", "data": "2026-09-10"},
        ],
        "hashtags": ["#solina", "#eminent", "#stringmachine", "#pinkfloyd", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 029", "Archi nei Pink Floyd? Un pezzo di organo da salotto"),
            ("BODEGRAVEN, OLANDA", "Eminent fa organi. Nel 310 Unique del 1972 c'è una sezione archi."),
            ("1974", "Piace più del resto dell'organo. La staccano e nasce la Solina."),
            ("IL TRUCCO È IL CHORUS", "La stessa nota, sfasata 3 volte. L'orecchio sente una sezione d'archi."),
            ("PINK FLOYD, DAL 1975", "Richard Wright la usa come tappeto sotto la band."),
        ],
        "reel_cta": "Mandalo a chi giura che erano archi veri",
        "reel_audio": {
            "file": "assets/audio/solina/registrazione.ogg", "inizio": 69,
            "autore": "MFbay", "licenza": "pubblico dominio",
            "fonte": "Wikimedia Commons",
            "url": "https://commons.wikimedia.org/wiki/File:ARP-Solina_Violin_modulated_Akkord.ogg",
            "cosa": "una ARP Solina, sezione violini con la modulazione",
        },
        "verificata": True,
    },
    # ---------------------------------------------------------------- 30
    {
        "slug": "ppgwave",
        "numero": 30,
        "serie": "I SINTETIZZATORI",
        "strumento": "PPG Wave 2.2",
        "anno": "1982",
        "luogo": "Amburgo",
        "costruttore": "Palm Products GmbH",
        "specifiche": [
            ("ANNO", "1982"),
            ("ORIGINE", "Germania"),
            ("OSCILLATORI", "Digitali, 8 bit"),
            ("FILTRI", "Analogici, 24 dB"),
        ],
        "gancio": "Oscillatori digitali dentro, filtri analogici fuori: nessuno l'aveva ancora fatto",
        "sottotitolo": "Trenta tabelle da sessantaquattro onde l'una, e una manopola che ci cammina dentro.",
        "la_macchina": "Otto voci, sedici oscillatori digitali a 8 bit, e in memoria trenta «tavole d'onda»: ognuna \u00e8 una fila di 64 forme d'onda diverse, messe in ordine come i fotogrammi di un film. Il suono non sta in una forma sola, sta nel percorso che si fa attraverso la fila. Poi tutto esce da filtri passa-basso analogici da 24 dB per ottava, gli stessi che avrebbe un sintetizzatore tradizionale.",
        "inventore_nome": "Wolfgang Palm",
        "inventore": "Palm fonda la PPG ad Amburgo nel 1975 e la chiude nel 1987, indebitato per una macchina che non fece in tempo a vendere. In mezzo ci sono dodici anni in cui inventa la sintesi a tavole d'onda, che oggi trovate dentro un sacco di synth digitali, quasi sempre senza il suo nome accanto.",
        "come_funziona": "Prendi 64 onde leggermente diverse e mettile in fila. Se ne suoni una sola hai un timbro fermo; se una manopola o un inviluppo cammina lungo la fila, il timbro cambia mentre la nota suona, e cambia in modi che nessun filtro pu\u00f2 imitare \u2014 perch\u00e9 non sta togliendo armoniche, sta sostituendo l'onda. A 8 bit i numeri sono pochi e si sente: ogni onda porta con s\u00e9 una grana metallica.",
        "richiami": [
            ("FIG. 1", "30 tavole, 64 onde ciascuna"),
            ("FIG. 2", "Scansione: si cammina nella fila"),
            ("FIG. 3", "Filtri analogici in uscita"),
        ],
        "chi_lusata": [
            {"artista": "David Bowie", "nota": "Fra i primi a portarlo su un disco grande", "ig": "davidbowie"},
            {"artista": "Depeche Mode", "nota": "Il timbro che si muove mentre la nota resta ferma", "ig": None},
            {"artista": "Thomas Dolby", "nota": "Fra i primi a usarlo, nei primi anni Ottanta", "ig": None},
            {"artista": "Tangerine Dream", "nota": "Tavole d'onda al posto delle sequenze analogiche", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": "Gli 8 bit non erano una scelta estetica: erano quello che si poteva permettere nel 1982. Quella povert\u00e0 di numeri lascia un residuo ruvido su ogni suono, e per anni i costruttori hanno inseguito pi\u00f9 bit per toglierlo. Oggi chi cerca «il suono PPG» cerca esattamente quel residuo, e i sintetizzatori moderni lo rimettono dentro apposta.",
        "avvertenza": "La grana metallica non si toglie: sono gli 8 bit degli oscillatori. Non \u00e8 un difetto da correggere, \u00e8 la voce.",
        "foto": {
            "file": "assets/foto/ppgwave/principale.jpg",
            "autore": "John R. Southern",
            "licenza": "CC BY-SA 2.0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "\u00abPPG Wave\u00bb \u2014 Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/PPG_Wave", "data": "2026-09-10"},
            {"titolo": "\u00abPPG Wave 2\u00bb \u2014 Vintage Synth Explorer",
             "url": "https://www.vintagesynth.com/ppg/wave-2", "data": "2026-09-10"},
            {"titolo": "\u00abPalm Products GmbH\u00bb \u2014 Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Palm_Products_GmbH", "data": "2026-09-10"},
        ],
        "hashtags": ["#ppgwave", "#ppg", "#sintetizzatore", "#davidbowie", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 030", "La sua idea sta in tanti synth. Il suo nome quasi mai"),
            ("AMBURGO, 1975", "Wolfgang Palm fonda la PPG. Lì inventa la sintesi a tavole d'onda."),
            ("1982", "Nel PPG Wave 64 onde stanno in fila, come i fotogrammi di un film."),
            ("8 BIT", "Nel 1982 di più non si può avere. Ne esce una grana ruvida."),
            ("1987", "Palm chiude la PPG in debito, per una macchina che non vende in tempo."),
        ],
        "reel_cta": "Mandalo a chi suona con le tavole d'onda",
        "verificata": True,
    },
    # ---------------------------------------------------------------- 31
    {
        "slug": "mpc60",
        "numero": 31,
        "serie": "I CAMPIONATORI",
        "strumento": "Akai MPC60",
        "anno": "1988",
        "luogo": "Los Angeles e Tokyo",
        "costruttore": "Akai",
        "specifiche": [
            ("ANNO", "1988"),
            ("DESIGN", "Roger Linn"),
            ("CAMPIONAMENTO", "12 bit, 40 kHz"),
            ("MEMORIA", "13-26 secondi"),
        ],
        "gancio": "Non inventò il campionamento: gli diede sedici pad da colpire con le dita",
        "sottotitolo": "Roger Linn disegna l'interfaccia, Akai costruisce l'elettronica: nasce la macchina che insegna all'hip hop a suonare con le mani.",
        "la_macchina": "Otto anni dopo la sua prima drum machine, Roger Linn torna con una macchina che campiona: 12 bit, 40 kHz, i suoni su sedici pad quadrati sensibili alla pressione (un dito, sedici livelli di forza) e un sequencer che tiene 60.000 note. Linn disegna l'interfaccia in California, Akai costruisce l'elettronica a Tokyo. Esce a dicembre del 1988 a 5.000 dollari.",
        "inventore_nome": "Roger Linn (con Akai)",
        "inventore": (
            "Linn aveva già inventato la LM-1 e la LinnDrum, le prime drum "
            "machine con suoni campionati invece che sintetizzati. Per la "
            "MPC60 lascia il lavoro elettronico ad Akai, a Tokyo, e si "
            "concentra su quello che sa fare meglio: il modo in cui la si "
            "suona. È lui a disegnare i sedici pad quadrati sensibili al "
            "tocco, pensati per essere colpiti con le dita come una piccola "
            "batteria, non programmati un passo alla volta con un cursore."
        ),
        "come_funziona": (
            "Ogni pad richiama un campione diverso, e la pressione del dito "
            "ne decide il volume: sedici livelli dinamici, non acceso o "
            "spento. Il sequencer aggiunge uno swing regolabile — a metà "
            "corsa i colpi cadono dritti, oltre iniziano a slittare verso il "
            "tempo di una terzina — la stessa formula che Linn aveva già "
            "messo nella sua prima drum machine, e che qui i produttori "
            "usano per far suonare umano un ritmo scritto al computer."
        ),
        "richiami": [
            ("FIG. 1", "16 pad a pressione"),
            ("FIG. 2", "Campioni 12 bit"),
            ("FIG. 3", "Sequencer 60.000 note"),
        ],
        "chi_lusata": [
            {"artista": "DJ Premier", "nota": "La svolta nel suono di Gang Starr, da «Daily Operation» (1992) in poi", "ig": None},
            {"artista": "DJ Shadow", "nota": "«Endtroducing.....» (1996), un intero album da una sola MPC60", "ig": None},
        ],
        "menzioni_extra": [
            {"ig": "akai_pro",
             "riga": "La sigla MPC è oggi di @akai_pro."},
            {"ig": "roger.linn",
             "riga": "Il suo disegnatore, Roger Linn, è ancora in attività: lo trovi come @roger.linn."},
        ],
        "aneddoto": "Nel 1996 DJ Shadow pubblica «Endtroducing.....»: quasi tutto il disco esce da un'unica MPC60 comprata usata su consiglio di un altro DJ, senza tastiera né sintetizzatore. Solo dischi trovati nei mercatini, spezzettati e rimessi in fila sedici pad alla volta. Provate a immaginare il lavoro: 13 secondi di memoria per volta, sedici pad e un album intero.",
        "avvertenza": "Il sequencer regge 60.000 note. I campioni no: appena 13 secondi di serie, 26 con l'espansione. Una sinfonia in coda, un rullante in memoria.",
        "da_ascoltare": {"brano": 'Endtroducing.....', "artista": 'DJ Shadow',
                          "anno": '1996',
                          "cosa": 'Ogni suono del disco arriva da un vinile diverso, tutti richiamati con gli stessi sedici pad.'},
        "foto": {
            "file": "assets/foto/mpc60/principale.jpg",
            "autore": "Matt Friedman",
            "licenza": "CC BY 3.0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "«Akai MPC» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Akai_MPC", "data": "2026-09-11"},
            {"titolo": "«It's the heart of my studio»: the story of the Akai MPC — MusicRadar",
             "url": "https://www.musicradar.com/music-tech/its-the-heart-of-my-studio-the-story-of-the-akai-mpc-from-the-mpc60-to-the-mpc-live-iii",
             "data": "2026-09-11"},
            {"titolo": "«Akai MPC60 Revisited» — Sound On Sound",
             "url": "https://www.soundonsound.com/music-business/akai-mpc60-revisited", "data": "2026-09-11"},
            {"titolo": "«Akai MPC60» — Vintage Synth Explorer",
             "url": "https://www.vintagesynth.com/akai/mpc60", "data": "2026-09-11"},
        ],
        "hashtags": ["#mpc60", "#akai", "#campionatore", "#djshadow", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 031", "DJ Shadow: un album con 13 secondi di memoria per volta"),
            ("1988 · 5.000 DOLLARI", "Roger Linn disegna i comandi, Akai fa l'elettronica a Tokyo."),
            ("16 PAD", "La MPC60 si suona con le dita. I pad sentono quanto forte premi."),
            ("DJ SHADOW", "Ne compra una usata, su consiglio di un altro DJ."),
            ("«ENDTRODUCING.....», 1996", "Niente tastiere, niente synth. Dischi dei mercatini, tagliati sui pad."),
        ],
        "reel_cta": "Mandalo a chi compra dischi ai mercatini",
        "verificata": True,
    },
    # ---------------------------------------------------------------- 32
    {
        "slug": "prophet5",
        "numero": 32,
        "serie": "I SINTETIZZATORI",
        "strumento": "Sequential Circuits Prophet-5",
        "anno": "1978",
        "luogo": "San Jose, California",
        "costruttore": "Sequential Circuits",
        "specifiche": [
            ("ANNO", "1978"),
            ("COSTRUTTORE", "Sequential Circuits"),
            ("VOCI", "5, polifonico"),
            ("MEMORIA", "40 patch"),
        ],
        "gancio": "Il primo synth che si ricordava i suoni: bastava un numero, non venti manopole",
        "sottotitolo": "Cinque voci analogiche pilotate da un piccolo cervello digitale: nasce la memoria patch, e da qui nascerà anche il MIDI.",
        "la_macchina": "Fino al 1977 un sintetizzatore polifonico si programmava girando decine di manopole, ogni volta da capo: nessuna macchina ricordava un suono. Il Prophet-5 ne memorizza quaranta, e li richiami premendo un numero. Dentro, cinque voci analogiche identiche; sopra, un microprocessore che non genera il suono ma registra la posizione di ogni manopola. Debutta al NAMM di gennaio 1978. Per chi suonava dal vivo cambiava tutto, e si capisce ancora oggi quando ne accendi uno e il suono che avevi ieri è ancora lì.",
        "inventore_nome": "Dave Smith e John Bowen",
        "inventore": "Dave Smith fonda la Sequential Circuits a San Jose, in California, e disegna il Prophet-5 con John Bowen, che firma anche la sezione Poly-Mod. Sarà lo stesso Smith, pochi anni dopo, a mettere a punto con Ikutaro Kakehashi di Roland il protocollo MIDI: il primo collegamento della storia unisce un Prophet-600, erede diretto di questa macchina, a uno Jupiter-6 Roland.",
        "come_funziona": (
            "Il microprocessore non tocca l'audio: legge la posizione di "
            "ogni manopola e la scrive in memoria, poi la richiama esatta "
            "quando premi un numero. Il suono resta interamente analogico. "
            "Nei primi esemplari, però, gli oscillatori SSM slittano di "
            "accordatura con il calore della stanza: bisogna riaccordare la "
            "macchina più volte in un concerto. Solo dalla terza revisione, "
            "con un chip diverso al posto degli SSM, il Prophet-5 impara a "
            "restare accordato da solo."
        ),
        "richiami": [
            ("FIG. 1", "5 voci analogiche"),
            ("FIG. 2", "Microprocessore di memoria"),
            ("FIG. 3", "40 patch richiamabili"),
        ],
        "chi_lusata": [
            {"artista": "Talking Heads", "nota": "Il basso e il lead di «Burning Down the House» (1983)", "ig": None},
            {"artista": "The Cars", "nota": "Il riff che apre «Let's Go» (1979), sincronia fra due oscillatori", "ig": None},
            {"artista": "Radiohead", "nota": "L'accordo che apre «Everything in Its Right Place» (2000)", "ig": None},
        ],
        "menzioni_extra": [
            {"ig": "sequential_llc",
             "riga": "L'azienda esiste ancora, oggi si chiama Sequential: la trovi come @sequential_llc."},
        ],
        "aneddoto": "Gennaio 1978, NAMM. Il Prophet-5 costa quasi 4.000 dollari e in poche settimane arrivano 400 ordini, che per un'azienda piccola come la Sequential sono un bel guaio oltre che una festa. Le prime due revisioni escono con i chip SSM che dicevamo, e chi suona dal vivo impara a riaccordare fra un pezzo e l'altro. La terza cambia chip e il problema sparisce. In tutto ne hanno fatti circa 8.000, fino a metà anni Ottanta. Se ne cercate uno, chiedete quale revisione. Non è pignoleria.",
        "avvertenza": "Le prime due revisioni si scordano con il calore: chip instabili. Solo la terza, con un chip diverso, resta accordata da sola.",
        "da_ascoltare": {"brano": "Let's Go", "artista": "The Cars",
                          "anno": "1979",
                          "cosa": "Quel riff metallico che apre il pezzo è hard sync fra i due oscillatori: la firma tecnica del Prophet-5."},
        "foto": {
            "file": "assets/foto/prophet5/principale.jpg",
            "autore": "Michele Brina",
            "licenza": "CC BY-SA 4.0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "«Dave Smith and Sequential Circuits» — MIDI.org",
             "url": "https://midi.org/dave-smith-and-sequential-circuits", "data": "2026-09-11"},
            {"titolo": "«Prophet-5» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Prophet-5", "data": "2026-09-11"},
            {"titolo": "«1978: Sequential Circuits Prophet-5» — Mix Online",
             "url": "https://www.mixonline.com/technology/1978-sequential-circuits-prophet-5-first-programmable-polyphonic-synth-383725",
             "data": "2026-09-11"},
            {"titolo": "«Sequential Circuits Prophet 5» — Vintage Synth Explorer",
             "url": "https://www.vintagesynth.com/sequential-circuits/prophet-5", "data": "2026-09-11"},
        ],
        "hashtags": ["#prophet5", "#sequentialcircuits", "#sintetizzatore", "#radiohead", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 032", "Nel 1977 nessun synth polifonico ha la memoria"),
            ("SAN JOSE, CALIFORNIA", "Dave Smith e John Bowen disegnano il Prophet-5 alla Sequential."),
            ("NAMM, GENNAIO 1978", "Tiene 40 suoni in memoria. Li richiami premendo un numero."),
            ("QUASI 4.000 DOLLARI", "400 ordini in poche settimane. Per un'azienda piccola, un bel guaio."),
            ("POCHI ANNI DOPO", "Primo collegamento MIDI: un Prophet-600, suo erede, e uno Jupiter-6."),
        ],
        "reel_cta": "Mandalo a chi non salva mai i suoi preset",
        "verificata": True,
    },
    # ---------------------------------------------------------------- 33
    {
        "slug": "dmx",
        "numero": 33,
        "serie": "LE DRUM MACHINE",
        "strumento": "Oberheim DMX",
        "anno": "1980",
        "luogo": "Los Angeles",
        "costruttore": "Oberheim Electronics",
        "specifiche": [
            ("ANNO", "1980"),
            ("COSTRUTTORE", "Oberheim"),
            ("CAMPIONI", "8 bit, reali"),
            ("VOCI", "Regolabili singolarmente"),
        ],
        "gancio": "Non finge una batteria: la registra, e te la lascia accordare come un nastro",
        "sottotitolo": "Suoni veri di batteria dentro una macchina del 1980, con la stessa manopola che un tempo accelerava un registratore a bobine.",
        "la_macchina": "Fino a quel momento le drum machine imitavano il suono di una batteria con circuiti che oscillano. La DMX lo registra: dentro ci sono ventiquattro campioni digitali a 8 bit di rullante, cassa, piatti e percussioni vere, richiamabili con volume e accordatura regolabili voce per voce. Esce nel 1980 a quasi 2.900 dollari, disegnata da Marcus Ryle per l'azienda di Tom Oberheim, e in pochi anni la trovi sotto la new wave e sotto i primi dischi hip hop.",
        "inventore_nome": "Marcus Ryle (Oberheim)",
        "inventore": "Tom Oberheim fonda la sua azienda a Los Angeles nel 1969, costruendo prima moduli per altri synth e poi sintetizzatori propri. Alla DMX lavora un giovane ingegnere, Marcus Ryle, che la presenta insieme a Oberheim stesso al NAMM dei primi anni '80. È fra le prime drum machine a mettere dentro suoni registrati invece di oscillatori.",
        "come_funziona": (
            "Ogni voce ha una sua schedina con il campione già inciso: non "
            "un oscillatore che disegna un'onda, ma una piccola memoria che "
            "la rilegge. Per accordarla non si tocca il timbro: si cambia "
            "la velocità con cui il campione viene riletto, esattamente "
            "come si accelera o rallenta un nastro. Alzarla lo rende più "
            "corto e più acuto, abbassarla lo allunga e lo scurisce — la "
            "stessa nota, letta a un'altra velocità."
        ),
        "richiami": [
            ("FIG. 1", "24 campioni digitali"),
            ("FIG. 2", "8 bit per voce"),
            ("FIG. 3", "Accordatura a velocità variabile"),
        ],
        "chi_lusata": [
            {"artista": "New Order", "nota": "Il ritmo di «Blue Monday» (1983), tutto programmato a mano", "ig": None},
            {"artista": "Run-D.M.C.", "nota": "L'unico accompagnamento di «Sucker M.C.'s» (1983)", "ig": None},
            {"artista": "Herbie Hancock", "nota": "Il backbeat di «Rockit» (1983), sotto il riff campionato dal Fairlight", "ig": "herbiehancock"},
        ],
        "menzioni_extra": [
            {"ig": "oberheim_electronics",
             "riga": "L'azienda di Tom Oberheim è tornata: oggi è @oberheim_electronics."},
        ],
        "aneddoto": "Nel 1983 i New Order affidano alla DMX il ritmo di «Blue Monday»: sedicesimi di cassa incalzanti e rullate di tom programmate un colpo alla volta, senza un batterista in studio. Lo stesso anno la usano i Run-D.M.C. in «Sucker M.C.'s», dove oltre alla voce e ai dischi scratchati non c'è nient'altro.",
        "avvertenza": "Non ha un filtro per accordare i suoni: cambia la velocità con cui rilegge il campione, come un nastro. Più veloce è più acuto.",
        "da_ascoltare": {"brano": "Blue Monday", "artista": "New Order",
                          "anno": "1983",
                          "cosa": "Quel rullo di cassa incalzante nell'intro è la DMX programmata colpo per colpo, non un giro suonato."},
        "foto": {
            "file": "assets/foto/dmx/principale.jpg",
            "autore": "Matt Mechtley (ritagliata da Shoulder-synth)",
            "licenza": "CC BY-SA 2.0",
            "fonte": "Wikimedia Commons — Deutsches Museum",
        },
        "fonti": [
            {"titolo": "«Oberheim DMX» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Oberheim_DMX", "data": "2026-09-11"},
            {"titolo": "«Oberheim DMX» — Vintage Synth Explorer",
             "url": "https://www.vintagesynth.com/oberheim/dmx.php", "data": "2026-09-11"},
            {"titolo": "«The Happy Drum Machine Accident That Produced New Order's Best Known Hit» — Reverb",
             "url": "https://reverb.com/news/the-happy-drum-machine-accident-that-produced-new-orders-best-known-hit",
             "data": "2026-09-11"},
            {"titolo": "«Sucker M.C.'s» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Sucker_M.C.%27s", "data": "2026-09-11"},
        ],
        "hashtags": ["#oberheimdmx", "#oberheim", "#drummachine", "#neworder", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 033", "«Blue Monday»: in studio non c'è nessun batterista"),
            ("NEW ORDER · 1983", "Cassa a sedicesimi e rullate di tom, programmate un colpo alla volta."),
            ("OBERHEIM DMX", "Il ritmo è di una Oberheim DMX, uscita nel 1980 a quasi 2.900 dollari."),
            ("24 CAMPIONI · 8 BIT", "Le altre drum machine la batteria la imitano. Questa la registra."),
            ("RUN-D.M.C. · 1983", "Lo stesso anno, in «Sucker M.C.'s» ci sono voce, scratch e lei. Basta."),
        ],
        "reel_cta": "Mandalo a chi balla ancora «Blue Monday»",
        "verificata": True,
    },
    # ---------------------------------------------------------------- 34
    {
        "slug": "h910",
        "numero": 34,
        "serie": "GLI EFFETTI",
        "strumento": "Eventide H910 Harmonizer",
        "anno": "1975",
        "luogo": "New York",
        "costruttore": "Eventide",
        "specifiche": [
            ("ANNO", "1975"),
            ("COSTRUTTORE", "Eventide"),
            ("PRINCIPIO", "Pitch-shift digitale"),
            ("ESCURSIONE", "±1 ottava"),
        ],
        "gancio": "Il primo effetto digitale in commercio: storpiava il tempo, non solo il suono",
        "sottotitolo": "Cambia l'intonazione senza toccare la velocità: una magia che nel 1975 nessun altro sapeva fare.",
        "la_macchina": "Nel 1975 processare il suono in digitale è quasi impensabile per il mercato: i convertitori costano una fortuna e li usano solo i laboratori. L'H910 li mette in un rack da studio. Alza o abbassa l'intonazione di un suono fino a un'ottava intera senza cambiarne la velocità, la prima volta che succede fuori da un laboratorio, con un ritardo rigenerativo che può anche accumularsi su se stesso fino a esplodere. Costa 1.600 dollari. Nel 1975 era un prezzo da studio, non da musicista.",
        "inventore_nome": "Richard Factor e Tony Agnello (Eventide)",
        "inventore": "Eventide nasce nel 1971 a Manhattan, fondata da Richard Factor insieme a Stephen Katz e Orville Greene. È Factor ad assegnare il progetto dell'H910 all'ingegnere Tony Agnello, che lo costruisce nel 1974 e lo presenta a un'associazione di ingegneri del suono l'anno dopo. Non è un'azienda di strumenti musicali: fa apparecchiature per la radiotelevisione. L'H910 nasce quasi per caso.",
        "come_funziona": (
            "Dentro, due letture della stessa linea di ritardo digitale, "
            "incrociate per cambiare l'intonazione senza toccare la "
            "durata. Nel punto dove le due letture si scambiano resta un "
            "piccolo vuoto di fase, udibile come un'imperfezione: da questa "
            "macchina nasce la parola inglese «glitch», usata ancora oggi "
            "per lo stesso difetto. Alzando il ritorno il segnale rientra "
            "pitchato su se stesso: ogni giro sale o scende di quota, "
            "finché non parte in oscillazione controllata."
        ),
        "richiami": [
            ("FIG. 1", "Pitch-shift ±1 ottava"),
            ("FIG. 2", "Ritardo rigenerativo"),
            ("FIG. 3", "Conversione analogico-digitale"),
        ],
        "chi_lusata": [
            {"artista": "David Bowie", "nota": "La batteria rigenerata di «Low» (1977), prod. Tony Visconti", "ig": "davidbowie"},
            {"artista": "AC/DC", "nota": "Sotto il rullante di «Back in Black» (1980), scordato di proposito", "ig": None},
            {"artista": "Frank Zappa", "nota": "Nel suo rig per chitarra, da metà anni '70", "ig": None},
        ],
        "menzioni_extra": [
            {"ig": "eventideaudio",
             "riga": "L'azienda esiste ancora e fa ancora effetti da studio: @eventideaudio."},
        ],
        "aneddoto": "Nel 1977, in studio per «Low» di David Bowie, il produttore Tony Visconti convince tutti a provare l'H910 sulla batteria di Dennis Davis, rimandando l'uscita di nuovo dentro la macchina: il rullante metallico e discendente di «Breaking Glass» esce da lì. Tre anni dopo Tony Platt lo usa scordato di proposito sotto il rullante vero di «Back in Black» degli AC/DC. Due dischi che non c'entrano niente l'uno con l'altro, e in mezzo la stessa scatola.",
        "avvertenza": "Ogni cambio di intonazione lascia un vuoto di fase nel punto di incrocio: da questo difetto nasce la parola «glitch».",
        "da_ascoltare": {"brano": "Breaking Glass", "artista": "David Bowie",
                          "anno": "1977",
                          "cosa": "Quel rullante metallico che scende di tono è l'H910 che rimanda il suono dentro se stesso, pitchato a ogni giro."},
        "foto": {
            "file": "assets/foto/h910/principale.jpg",
            "autore": "Nalzatron",
            "licenza": "CC BY-SA 3.0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "«Eventide, Inc.» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Eventide,_Inc", "data": "2026-09-11"},
            {"titolo": "«1975: Eventide H910 Harmonizer» — Mix Online",
             "url": "https://www.mixonline.com/technology/1975-eventide-h910-harmonizer-377972", "data": "2026-09-11"},
            {"titolo": "«H910 Harmonizer» — Eventide Audio",
             "url": "https://www.eventideaudio.com/rackmount/h910-harmonizer/", "data": "2026-09-11"},
            {"titolo": "Intervista a Tony Platt su «Back in Black» — SoloDallas",
             "url": "https://solodallas.com/blogs/blog/recording-back-in-black-the-album-interviews-with-tony-platt",
             "data": "2026-09-11"},
        ],
        "hashtags": ["#h910", "#eventide", "#effettiaudio", "#davidbowie", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 034", "La parola «glitch» è nata dentro questa scatola"),
            ("EVENTIDE · MANHATTAN", "Eventide non fa strumenti: fa apparecchi per la radio e la TV."),
            ("1975 · 1.600 DOLLARI", "L'H910 sposta la nota fino a un'ottava senza toccare la velocità."),
            ("IL DIFETTO", "Due letture dello stesso ritardo. Dove si scambiano, un vuoto: il glitch."),
            ("DAVID BOWIE · 1977", "Il rullante che scende di tono in «Breaking Glass» viene da lì."),
        ],
        "reel_cta": "Mandalo a chi ha consumato «Low» di Bowie",
        "verificata": True,
    },
    # ---------------------------------------------------------------- 35
    {
        "slug": "ondioline",
        "numero": 35,
        "serie": "GLI ANTENATI",
        "strumento": "Ondioline",
        "anno": "1947",
        "luogo": "Parigi",
        "costruttore": "Georges Jenny",
        "specifiche": [
            ("ANNO", "1947"),
            ("ORIGINE", "Francia"),
            ("TASTIERA", "Sospesa su molle"),
            ("VOLUME", "Leva al ginocchio"),
        ],
        "gancio": "La tastiera \u00e8 appoggiata su molle: si spinge di lato, come una corda di violino",
        "sottotitolo": "L'alternativa povera alle Ondes Martenot, costruita a mano da un uomo solo per vent'anni.",
        "la_macchina": "Una tastiera corta montata sopra un mobile con l'altoparlante dentro. Il timbro nasce da un circuito a multivibratore e passa per un banco di cursori \u2014 da dieci a diciassette secondo il modello \u2014 che tolgono e aggiungono armoniche: da l\u00ec escono legni, ottoni, archi, e cose che non assomigliano a niente. Il volume non sta su una manopola ma su una leva che si spinge col ginocchio, cos\u00ec le mani restano libere.",
        "inventore_nome": "Georges Jenny",
        "inventore": "Jenny comincia a costruirne il primo esemplare alla fine degli anni Trenta, mentre \u00e8 ricoverato in un sanatorio del sud della Francia per tubercolosi. Voleva una macchina che facesse quello che facevano le Ondes Martenot ma che una famiglia potesse permettersi. Ne costru\u00ec circa milleduecento fra la met\u00e0 degli anni Quaranta e la fine dei Sessanta, quasi tutti con le proprie mani.",
        "come_funziona": "I tasti non sono avvitati al telaio: poggiano su molle disegnate apposta. Premuto un tasto, lo si pu\u00f2 spingere a destra e a sinistra, e l'intonazione si piega di conseguenza \u2014 lo stesso gesto che fa un violinista sulla corda, su una tastiera. Il vibrato quindi non arriva da un oscillatore che lo produce sempre uguale: lo fa la mano, nota per nota, e non ce ne sono due identici.",
        "richiami": [
            ("FIG. 1", "Tasti su molle, spinta laterale"),
            ("FIG. 2", "Multivibratore + cursori armonici"),
            ("FIG. 3", "Leva del volume al ginocchio"),
        ],
        "chi_lusata": [
            {"artista": "Jean-Jacques Perrey", "nota": "Vent'anni a costruirci sopra una tecnica che non aveva nessun altro", "ig": None},
            {"artista": "Georges Jenny", "nota": "Il costruttore la presentava lui stesso alla radio francese", "ig": None},
            {"artista": "Gotye", "nota": "Settant'anni dopo ne restaura gli esemplari e ci porta in tour un'orchestra", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": "Nel 1949 uno studente di medicina sent\u00ec alla radio francese un signore che presentava una macchina sconosciuta. Si chiamava Jean-Jacques Perrey, and\u00f2 a cercarlo, e Jenny gli mise in mano uno strumento e un lavoro: fu il primo venditore dell'Ondioline. Non ne vendette moltissimi, ma ci pass\u00f2 vent'anni sopra e ne divenne l'unico vero virtuoso: quasi tutto quello che oggi sappiamo di come suona lo si deve a lui.",
        "avvertenza": "Il vibrato non c'\u00e8 finch\u00e9 non lo fai tu. Se tieni il dito fermo, la nota resta dritta come un tubo.",
        "foto": {
            "file": "assets/foto/ondioline/principale.jpg",
            "autore": "ForgottenFuturesBB",
            "licenza": "CC BY-SA 4.0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "\u00abOndioline\u00bb \u2014 Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Ondioline", "data": "2026-09-11"},
            {"titolo": "\u00abWally De Backer on the Lasting Influence of Jean-Jacques Perrey and the Ondioline\u00bb \u2014 Red Bull Music Academy Daily",
             "url": "https://daily.redbullmusicacademy.com/2017/07/gotye-ondioline-interview/", "data": "2026-09-11"},
        ],
        "hashtags": ["#ondioline", "#georgesjenny", "#musicaelettronica", "#gotye", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 035", "Jenny la comincia in sanatorio, malato di tubercolosi"),
            ("GEORGES JENNY · ANNI '30", "Jenny vuole ciò che fanno le Ondes Martenot, a un prezzo da famiglia."),
            ("ONDIOLINE · 1947", "Esce l'Ondioline. Tasti su molle, da spingere di lato come una corda."),
            ("RADIO FRANCESE · 1949", "Uno studente di medicina sente Jenny alla radio. E va a cercarlo."),
            ("JEAN-JACQUES PERREY", "È Jean-Jacques Perrey. Ci passerà sopra 20 anni, unico vero virtuoso."),
        ],
        "reel_cta": "Mandalo a un violinista che odia le tastiere",
        "verificata": True,
    },
    # ---------------------------------------------------------------- 36
    {
        "slug": "rhodes",
        "numero": 36,
        "serie": "GLI ELETTROMECCANICI",
        "strumento": "Fender Rhodes",
        "anno": "1965",
        "luogo": "Fullerton, California",
        "costruttore": "Fender / CBS",
        "specifiche": [
            ("ANNO", "1965"),
            ("PRINCIPIO", "Barre percosse + pickup"),
            ("TASTI", "73 o 88"),
            ("VERSIONI", "Suitcase e Stage"),
        ],
        "gancio": "Sotto ogni tasto un diapason zoppo. Il pianoforte che Harold Rhodes ha cominciato in un ospedale militare",
        "sottotitolo": "Una barra d'acciaio percossa davanti a un pickup: il pianoforte elettrico che non prova nemmeno a sembrare un pianoforte.",
        "la_macchina": "Sembra un pianoforte da studio col coperchio di plastica, ma dentro non ci sono corde. Ogni tasto fa battere un martelletto su una barretta d'acciaio accordata, che vibra davanti a un pickup magnetico, come la corda di una chitarra elettrica. Il suono esce da un amplificatore e non da una cassa, e quindi lo tratti come una chitarra: tremolo, phaser, wah. Dal 1965 la CBS lo vende in due forme, la Suitcase con amplificatore e altoparlanti nel mobile sotto, e la Stage, senza, che pesa la metà. 73 o 88 tasti. Il timbro a campana lo riconoscete anche se non sapete come si chiama: è quello.",
        "inventore_nome": "Harold Rhodes",
        "inventore": "Harold Rhodes insegnava pianoforte a Los Angeles, e insegnare è la cosa che ha fatto per tutta la vita, anche quando costruiva strumenti. Dopo la guerra fa il suo primo pianoforte elettrico, il Pre-Piano (sull'anno le fonti non sono d'accordo: 1946 per alcune, 1948 per altre). Nel 1959 si mette in società con Leo Fender e insieme fanno il Piano Bass, 32 tasti, solo le note basse. Quando la CBS compra la Fender, nel 1965, esce il primo Fender Rhodes, con 73 tasti. Il marchio passa alla Roland nel 1987. Rhodes muore nel 2000.",
        "come_funziona": "Ogni nota \u00e8 un diapason asimmetrico, brevettato da Rhodes: una barretta sottile, il tine, e sopra una barra d'acciaio pi\u00f9 grossa, la tone bar. Il martelletto colpisce solo la barretta; la barra grossa entra in risonanza e allunga la vibrazione, che da sola si spegnerebbe in un attimo. Davanti alla punta della barretta sta un pickup elettromagnetico, lo stesso principio della chitarra elettrica: il metallo che vibra nel campo della bobina genera la corrente che va all'amplificatore. Niente corde e niente cassa armonica: staccato l'amplificatore, un Rhodes si sente appena.",
        "richiami": [
            ("FIG. 1", "Tine + tone bar: diapason asimmetrico"),
            ("FIG. 2", "Pickup magnetico, come una chitarra"),
            ("FIG. 3", "Suitcase con ampli, Stage senza"),
        ],
        "chi_lusata": [
            {"artista": "Herbie Hancock", "nota": "Con Miles Davis in «Stuff» (1968), sull'album Miles in the Sky", "ig": "herbiehancock"},
            {"artista": "Ray Manzarek (The Doors)", "nota": "I Doors non avevano un bassista: le linee di basso le fa lui, con la sinistra, sul Piano Bass a 32 tasti", "ig": "thedoors"},
            {"artista": "Stevie Wonder", "nota": "L'intro di \u00abYou Are the Sunshine of My Life\u00bb (1972) \u00e8 un Rhodes che sale per toni interi", "ig": None},
        ],
        "menzioni_extra": [],
        "da_ascoltare": {"brano": "Stuff", "artista": "Miles Davis", "anno": "1968",
                         "cosa": "Apre Miles in the Sky. Il Rhodes è di Herbie Hancock: sentite come sta sotto la tromba senza coprirla mai."},
        "aneddoto": "1942. Harold Rhodes è nell'aviazione militare americana e ha un compito strano: far suonare i soldati feriti, a letto, come terapia. Non esiste un pianoforte che stia su un letto, quindi ne costruisce uno, due ottave e mezzo, da tenere sulle ginocchia, con le barre ricavate dai tubi di alluminio di scarto dei bombardieri B-17. Lo chiamano Xylette. Quanti ne abbiano fatti non lo so dire: una fonte scrive più di 125.000, un'altra scrive «migliaia». Quello che è sicuro è che la barra di metallo percossa è la stessa idea che vent'anni dopo sta dentro il Rhodes.",
        "avvertenza": "Sotto ogni tasto c'\u00e8 un diapason zoppo: la gamba sottile fa la nota, quella grossa la fa durare. Non toglietene una per alleggerire.",
        "foto": {
            "file": "assets/foto/rhodes/principale.jpg",
            "posizione": "center 58%",
            "autore": "CasinoKat",
            "licenza": "CC BY-SA 3.0",
            "fonte": "Wikimedia Commons",
        },
        # Ordine = tavola: 2 la macchina intera, 3 un altro esemplare,
        # 4 il meccanismo (barre, diapason e pickup) sotto «come funziona».
        "foto_extra": [
            {"file": "assets/foto/rhodes/suitcase.jpg", "posizione": "center 22%",
             "autore": "Cliff", "licenza": "CC BY 2.0", "fonte": "Wikimedia Commons",
             "didascalia": "Suitcase 88: l'amplificatore \u00e8 il mobile sotto"},
            {"file": "assets/foto/rhodes/mark1.jpg",
             "autore": "Daniel Spils", "licenza": "CC BY 2.0", "fonte": "Wikimedia Commons",
             "didascalia": "Mark I Suitcase 73 del 1977"},
            {"file": "assets/foto/rhodes/interno.jpg",
             "autore": "CasinoKat", "licenza": "CC BY-SA 3.0", "fonte": "Wikimedia Commons",
             "didascalia": "Tone bar, tine e pickup, nota per nota"},
        ],
        "fonti": [
            {"titolo": "\u00abRhodes piano\u00bb \u2014 Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Rhodes_piano", "data": "2026-09-13"},
            {"titolo": "\u00abThe History of Rhodes\u00bb \u2014 Rhodes Music (sito ufficiale)",
             "url": "https://rhodesmusic.com/the-history-of-rhodes/", "data": "2026-09-13"},
            {"titolo": "\u00abThe Piano That Changed the History of Music\u00bb \u2014 fenderrhodes.com",
             "url": "http://www.fenderrhodes.com/history/narrative.html", "data": "2026-09-13"},
            {"titolo": "\u00abMiles in the Sky\u00bb \u2014 Wikipedia (EN), crediti di \u00abStuff\u00bb",
             "url": "https://en.wikipedia.org/wiki/Miles_in_the_Sky", "data": "2026-09-13"},
            {"titolo": "\u00abMiles Davis, Miles in the Sky\u00bb \u2014 Jarrett House North",
             "url": "https://jarretthousenorth.com/2022/07/30/miles-davis-miles-in-the-sky/", "data": "2026-09-13"},
            {"titolo": "\u00abRay Manzarek \u2014 Fender Rhodes Piano Bass\u00bb \u2014 How To Play Bass",
             "url": "https://how-to-play-bass.com/ray-manzarek-keyboard-bass-fender-rhodes-piano-bass", "data": "2026-09-13"},
            {"titolo": "\u00abYou Are the Sunshine of My Life\u00bb \u2014 Piano With Jonny",
             "url": "https://pianowithjonny.com/piano-lessons/play-you-are-the-sunshine-of-my-life/", "data": "2026-09-13"},
        ],
        "hashtags": ["#fenderrhodes", "#fender", "#pianoelettrico", "#herbiehancock", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 036", "Un pianoforte per soldati feriti, coi tubi dei B-17"),
            ("AVIAZIONE USA · 1942", "Harold Rhodes deve far suonare i feriti a letto, come terapia."),
            ("XYLETTE", "Lo chiamano Xylette: 2 ottave e mezzo, da tenere sulle ginocchia."),
            ("1965 · FENDER RHODES", "L'idea della barra percossa finisce dentro il Fender Rhodes."),
            ("MILES DAVIS · 1968", "In «Stuff» lo suona Herbie Hancock, sotto la tromba senza coprirla."),
        ],
        "reel_cta": "Mandalo a chi ha un Rhodes in cantina",
        "reel_audio": {
            "file": "assets/audio/rhodes/registrazione.ogg", "inizio": 0,
            "autore": "Fetz", "licenza": "pubblico dominio",
            "fonte": "Wikimedia Commons",
            "url": "https://commons.wikimedia.org/wiki/File:Rhodes_Mark_I_Tubeamp.ogg",
            "cosa": "un Rhodes Mark I in un amplificatore a valvole",
        },
        "verificata": True,
    },
    # SCARTI del rifornimento del 22/09/2026 (verifica su 2 fonti non
    # superata, o fonti in contraddizione senza modo di scioglierla):
    # - Duran Duran, «Rio» (1982): usa un Jupiter-4, non l'8 (confuso a
    #   lungo con «Hungry Like the Wolf», che invece è confermato Jupiter-8
    #   dallo stesso Nick Rhodes). Tenuto solo il brano giusto.
    # - TR-606: nessuna fonte assegna il progetto a un solo ingegnere
    #   (Tadao Kikumoto è documentato per TB-303/TR-808/TR-909, MAI per il
    #   606): niente nome inventato, si cita solo il team Roland.
    # - SP-1200: scartato un numero di «esemplari sopravvissuti» che
    #   gira online senza fonte primaria; scartato un brano specifico
    #   (non abbastanza documentato) per «da_ascoltare».
    # - Speak & Spell: scartato il sample dei Kraftwerk (una fonte lo dà
    #   per certo, un'altra — la voce Wikipedia stessa — non lo conferma
    #   affatto: contraddizione non risolta) e il sample di 808 State
    #   «Ancodia» (una sola fonte, WhoSampled, nessun riscontro indipendente).
    # - Vox Continental: scartato John Lennon / «Think for Yourself» (una
    #   sola fonte, un wiki di fan).
    # - Yamaha CS-80: scartato ogni peso in kg specifico — le fonti online
    #   danno numeri diversi e nessuna è una scheda tecnica Yamaha.
    # ---------------------------------------------------------------- 37
    {
        "slug": "voxcontinental",
        "numero": 37,
        "serie": "GLI ORGANI",
        "strumento": "Vox Continental",
        "anno": "1962",
        "luogo": "Dartford, Kent",
        "costruttore": "Jennings Musical Instruments (JMI)",
        "specifiche": [
            ("ANNO", "1962"),
            ("COSTRUTTORE", "Jennings Musical Instruments"),
            ("TASTI", "49, invertiti"),
            ("DRAWBAR", "6"),
        ],
        "gancio": "Tasti bianchi e neri invertiti, come un clavicembalo: l'organo pensato per stare in una valigia",
        "sottotitolo": "Sei drawbar e un case arancione: l'organo per il furgone della band, non per lo studio di registrazione.",
        "la_macchina": "Vale la pena guardarlo prima di sentirlo: tasti bianchi e neri invertiti, come un clavicembalo, e sei drawbar a slitta al posto delle solite levette. Dentro non ci sono valvole né le ruote foniche dell'Hammond: gli oscillatori sono a transistor, e il Continental pesa una frazione di un organo a valvole, sta nel bagagliaio di un furgone. Non prova a imitare la chiesa: il timbro è nasale, tagliente, fatto apposta per bucare chitarra e basso su un palco senza microfono dedicato all'organo. Il case arancione, o rosso a seconda del mercato, si vede da fondo sala.",
        "inventore_nome": "Les Hills e il reparto tecnico JMI",
        "inventore": "Il case squadrato e i tasti invertiti sono un brevetto del dicembre 1955, firmato dal designer Les Hills per la Jennings Musical Instruments di Tom Jennings — lo stesso Jennings che nel 1957 fonda il marchio Vox per vendere amplificatori alle band inglesi. I circuiti a transistor, al posto delle valvole, li sviluppa il reparto tecnico dell'azienda, con Albert Hogben fra gli ingegneri. Il Continental arriva sul mercato nell'agosto 1962, a 225 ghinee: la prima menzione a stampa che si trova è sulla Music Trade Press di giugno di quell'anno.",
        "come_funziona": "Ogni drawbar aggiunge o toglie un'armonica, come su un Hammond: sei in tutto, quattro per l'altezza del suono e due per scegliere fra il timbro reed e quello flute. La differenza è dentro: niente ruote foniche, l'onda la fanno oscillatori a transistor, uno per nota nella prima ottava e poi divisi verso l'alto per le altre. È il motivo per cui il Continental si solleva con una mano sola e un Hammond no. Il rovescio della medaglia: i primi transistor al germanio sono instabili, e l'organo va accordato più spesso di quanto vorreste.",
        "richiami": [
            ("FIG. 1", "Tasti bianchi/neri invertiti"),
            ("FIG. 2", "6 drawbar: 4 altezza + 2 timbro"),
            ("FIG. 3", "Oscillatori a transistor"),
        ],
        "chi_lusata": [
            {"artista": "Alan Price (The Animals)", "nota": "L'intro di «The House of the Rising Sun» (1964), drawbar aperti a salire, manda una generazione di tastieristi nei negozi Vox", "ig": None},
            {"artista": "Ray Manzarek (The Doors)", "nota": "Il suo Continental di inizio anni Sessanta è oggi nella collezione della Rock & Roll Hall of Fame", "ig": "thedoors"},
            {"artista": "Doug Ingle (Iron Butterfly)", "nota": "Scrive e suona «In-A-Gadda-Da-Vida» (1968) su questo organo, diciassette minuti su un lato intero del disco", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": "Una sera di fine anni Sessanta Doug Ingle si siede al suo Continental dopo aver bevuto un gallone di vino Red Mountain, quasi quattro litri, e scrive una canzone che intitola «In the Garden of Eden». Quando la canta al batterista Ron Bushy perché se la segni, la voce gli esce così impastata che Bushy scrive quello che sente: «In-A-Gadda-Da-Vida». Il titolo sbagliato resta. Il pezzo, inciso nel 1968 sull'organo di quella sera, occupa da solo il secondo lato del disco.",
        "avvertenza": "I miei oscillatori sono a transistor al germanio: si scaldano e calano d'intonazione. Ridatemi un quarto d'ora, prima di accusarmi di stonare.",
        "da_ascoltare": {"brano": "The House of the Rising Sun", "artista": "The Animals", "anno": "1964",
                         "cosa": "L'intro di Alan Price sale per gradi, drawbar aperti: è il suono che nel '64 manda tutti i tastieristi nei negozi Vox."},
        "foto": {
            "file": "assets/foto/voxcontinental/principale.jpg",
            "autore": "Docrobbie",
            "licenza": "CC BY-SA 4.0",
            "fonte": "Wikimedia Commons",
        },
        "foto_extra": [
            {"file": "assets/foto/voxcontinental/drawbars.jpg",
             "autore": "Docrobbie", "licenza": "CC BY-SA 4.0", "fonte": "Wikimedia Commons",
             "didascalia": "I sei drawbar: quattro per l'altezza, due per il timbro"},
        ],
        "fonti": [
            {"titolo": "«Vox Continental» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Vox_Continental", "data": "2026-09-22"},
            {"titolo": "«The Vox Continental portable transistor organ, 1962-1964» — voxac30.org.uk",
             "url": "https://www.voxac30.org.uk/vox_continental.html", "data": "2026-09-22"},
            {"titolo": "«Doug Ingle» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Doug_Ingle", "data": "2026-09-22"},
            {"titolo": "«Vox Continental Combo Organ» — Reverb",
             "url": "https://reverb.com/p/vox-continental", "data": "2026-09-22"},
        ],
        "hashtags": ["#voxcontinental", "#vox", "#organo", "#thedoors", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 037", "«In-A-Gadda-Da-Vida»: vino e un titolo capito male"),
            ("FINE ANNI '60", "Doug Ingle degli Iron Butterfly si siede al suo Vox Continental."),
            ("UN GALLONE DI VINO", "Ha bevuto. Scrive una canzone e la chiama «In the Garden of Eden»."),
            ("RON BUSHY, BATTERIA", "La canta al batterista perché se la segni. Ma la voce è impastata."),
            ("1968 · 17 MINUTI", "Bushy scrive quello che sente: «In-A-Gadda-Da-Vida». E resta così."),
        ],
        "reel_cta": "Mandalo a chi storpia i titoli delle canzoni",
        "reel_audio": {
            "file": "assets/audio/voxcontinental/registrazione.ogg", "inizio": 23,
            "autore": "Ritchie333", "licenza": "CC BY-SA 4.0",
            "fonte": "Wikimedia Commons",
            "url": "https://commons.wikimedia.org/wiki/File:Vox_Continental.ogg",
            "cosa": "un Vox Continental vero",
        },
        "verificata": True,
    },
    # ---------------------------------------------------------------- 38
    {
        "slug": "tr606",
        "numero": 38,
        "serie": "LE DRUM MACHINE",
        "strumento": "Roland TR-606 Drumatix",
        "anno": "1981",
        "luogo": "Hamamatsu, Giappone",
        "costruttore": "Roland Corporation",
        "specifiche": [
            ("ANNO", "1981"),
            ("COSTRUTTORE", "Roland Corporation"),
            ("SUONI", "7, analogici"),
            ("MEMORIA", "32 pattern"),
        ],
        "gancio": "Doveva solo accompagnare un basso finto. Il mercato non lo voleva: il dancefloor sì",
        "sottotitolo": "Sette suoni analogici pensati per chitarristi senza batterista: la Drumatix che il mercato ha rifiutato e il dancefloor ha riscoperto.",
        "la_macchina": "È la metà «silver» di una coppia: esce insieme al TB-303, pensato come un metronomo con più voci per chi suona la chitarra da solo, senza batterista. Sette suoni — cassa, rullante, due tom, charleston aperto e chiuso, piatto — tutti generati da circuiti analogici, non registrati. Ha 32 pattern in memoria e una presa DIN sync per agganciarsi al 303. Programmarlo è scomodo e i suoni sono dichiaratamente finti: nel 1981 questo basta a farlo sembrare un giocattolo mal riuscito, e infatti il mercato lo snobba.",
        "inventore_nome": "Il reparto R&S di Roland",
        "inventore": "Il TR-606 non ha un solo padre dichiarato nelle fonti: nasce nei laboratori Roland di Hamamatsu, sotto la direzione del fondatore Ikutaro Kakehashi, come metà economica di un progetto pensato per i musicisti senza banda. L'idea è pratica quasi fino alla mestizia: un chitarrista compra il TB-303 per la linea di basso e il TR-606 per la batteria, li collega con un cavo DIN sync e si allena da solo. Il mercato del 1981 non la capisce: le due macchine restano sugli scaffali, poi nei negozi dell'usato, finché non le comprano musicisti che le usano per tutt'altro.",
        "come_funziona": "Ogni suono nasce da un piccolo circuito analogico dedicato — un oscillatore e un inviluppo per la cassa, rumore bianco filtrato per charleston e piatto — non da un campione registrato. Si programma passo-passo, sedici passi per pattern, premendo i pulsanti mentre una fila di LED scorre: lo stesso principio del TB-303 e dell'808 dello stesso giro d'anni. La presa DIN sync manda e riceve l'impulso di tempo: collegato al 303, il 606 diventa il metronomo che tiene insieme tutto.",
        "richiami": [
            ("FIG. 1", "Cassa, rullante, tom: analogici"),
            ("FIG. 2", "16 passi a LED"),
            ("FIG. 3", "DIN sync verso il TB-303"),
        ],
        "chi_lusata": [
            {"artista": "Sisters of Mercy", "nota": "Lo mettono al centro del suono goth-rock di «First and Last and Always» (1985)", "ig": None},
            {"artista": "Massive Attack", "nota": "Fra le macchine ritmiche dei primi dischi trip hop di Bristol", "ig": None},
            {"artista": "Nine Inch Nails", "nota": "Trent Reznor lo usa fra i drum synth analogici delle prime registrazioni industrial", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": "Roland lo produce dal 1981 al 1984, poi lo toglie di produzione: troppo scomodo da programmare, suoni troppo finti per un mercato che ancora sperava nei musicisti veri. Le scorte finiscono nei banchi dell'usato insieme al TB-303, svendute. Lì le trovano musicisti che non cercavano una batteria vera, e negli anni successivi il 606 finisce su dischi goth, industrial, electro e techno — generi che nel 1981 non esistevano ancora con quel nome.",
        "avvertenza": "Non ho un microfono dentro: ogni tamburo che sentite è un circuito che finge. Se cercate un rullante vero, cercate altrove.",
        "foto": {
            "file": "assets/foto/tr606/principale.jpg",
            "autore": "Midas Wouters",
            "licenza": "CC BY-SA 3.0",
            "fonte": "Wikimedia Commons",
        },
        "foto_extra": [
            {"file": "assets/foto/tr606/dettaglio.jpg",
             "autore": "Dadadata", "licenza": "CC BY-SA 4.0", "fonte": "Wikimedia Commons",
             "didascalia": "Il pannello passo-passo, sedici LED"},
        ],
        "fonti": [
            {"titolo": "«Roland TR-606» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Roland_TR-606", "data": "2026-09-22"},
            {"titolo": "«Drumatix: The Perpetual Appeal of the TR-606» — Roland Articles (sito ufficiale)",
             "url": "https://articles.roland.com/drumatix-the-perpetual-appeal-of-the-tr-606/", "data": "2026-09-22"},
            {"titolo": "«The Roland TR-606» — Perfect Circuit",
             "url": "https://www.perfectcircuit.com/signal/roland-tr606", "data": "2026-09-22"},
        ],
        "hashtags": ["#tr606", "#roland", "#drummachine", "#nineinchnails", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 038", "Fatto per chi suona da solo, finito nei Sisters of Mercy"),
            ("HAMAMATSU, 1981", "Roland lancia il TR-606 insieme al TB-303, con un cavo per collegarli."),
            ("7 SUONI ANALOGICI", "Un chitarrista senza band: il 303 fa il basso, il 606 la batteria."),
            ("1984", "Troppo scomodo, suoni troppo finti. Fuori produzione e svenduto."),
            ("SISTERS OF MERCY, 1985", "Lo mettono al centro del loro goth in «First and Last and Always»."),
        ],
        "reel_cta": "Mandalo al chitarrista che suona da solo",
        "verificata": True,
    },
    # ---------------------------------------------------------------- 39
    {
        "slug": "sp1200",
        "numero": 39,
        "serie": "I CAMPIONATORI",
        "strumento": "E-mu SP-1200",
        "anno": "1987",
        "luogo": "Santa Cruz, California",
        "costruttore": "E-mu Systems",
        "specifiche": [
            ("ANNO", "1987"),
            ("COSTRUTTORE", "E-mu Systems"),
            ("CAMPIONAMENTO", "12 bit, 26,04 kHz"),
            ("MEMORIA", "10 secondi"),
        ],
        "gancio": "Dieci secondi di memoria in tutto, divisi in quattro pezzi: e con quei dieci secondi si costruisce un genere",
        "sottotitolo": "Campionatore e batteria in una scatola grigia, 12 bit e un filtro analogico: il suono sporco che l'hip hop delle origini non ha mai voluto pulire.",
        "la_macchina": "È un campionatore e una drum machine nella stessa scatola: si registra un pezzo di un disco — un rullante, un fiato, un urlo — e lo si suona dai pad o dalla tastiera, con tanto di sequencer per incastrare i giri. La memoria totale è dieci secondi, divisi in quattro banchi da due secondi e mezzo l'uno: con quei dieci secondi Marley Marl, il Bomb Squad e Pete Rock costruiscono buona parte del suono dell'hip hop newyorchese di fine anni Ottanta. Otto voci di polifonia, cento pattern, cento canzoni in memoria.",
        "inventore_nome": "Dave Rossum",
        "inventore": "Dave Rossum fonda E-mu Systems nel 1971 a Santa Cruz, prima per costruire moduli analogici, poi campionatori: l'Emulator nel 1981, il Drumulator nel 1983, e nel 1987, con il contributo di Marco Alpert, l'SP-1200. Lo pensa come erede dell'SP-12, per unire la programmabilità del Drumulator alla capacità di campionare dell'Emulator II. Non lo progetta per l'hip hop: lo progetta per chi in studio non può permettersi un Emulator intero. Sarà l'hip hop a deciderne il destino.",
        "come_funziona": "Campiona a 26,04 kHz e 12 bit — molto meno di un CD — e proprio lì sta il carattere: la bassa risoluzione e i chip di filtro analogico SSM2044 tolgono le frequenze alte e ci mettono dentro una grana che un campionatore più fedele non avrebbe. Ogni suono singolo dura al massimo due secondi e mezzo. Cambiare l'intonazione di un campione, sul 1200, vuol dire farlo suonare più lento o più veloce: non c'è correzione, e infatti si sente.",
        "richiami": [
            ("FIG. 1", "12 bit, 26,04 kHz"),
            ("FIG. 2", "4 banchi da 2,5 secondi"),
            ("FIG. 3", "Filtro analogico SSM2044"),
        ],
        "chi_lusata": [
            {"artista": "The Bomb Squad", "nota": "Costruiscono con questo campionatore i collage di rumore di «It Takes a Nation of Millions to Hold Us Back» (Public Enemy, 1988)", "ig": None},
            {"artista": "Pete Rock", "nota": "Fra i produttori che lo adottano come campionatore principale negli anni Novanta", "ig": None},
            {"artista": "DJ Premier", "nota": "Lo stesso, sui primi dischi con Guru nei Gang Starr", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": "E-mu smette di costruirlo nel 1997: i chip SSM2044 del filtro non si trovano più sul mercato, e senza quelli il suono dell'SP-1200 non è più lo stesso. Il prezzo dell'usato, da allora, sale invece di scendere: più di trent'anni dopo, un campionatore del 1987 vale più di uno nuovo con specifiche tecniche molto più alte, perché quello che i produttori cercano non è la fedeltà, è la grana.",
        "avvertenza": "Campiono a 12 bit: non è un difetto da correggere, è la mia voce. Se volete un suono pulito, non chiamate me.",
        "foto": {
            "file": "assets/foto/sp1200/principale.jpg",
            "autore": "2xUeL",
            "licenza": "Pubblico dominio",
            "fonte": "Wikimedia Commons",
        },
        "foto_extra": [
            {"file": "assets/foto/sp1200/retro.jpg",
             "autore": "2xUeL", "licenza": "Pubblico dominio", "fonte": "Wikimedia Commons",
             "didascalia": "Il pannello posteriore: ingressi, uscite, MIDI"},
        ],
        "fonti": [
            {"titolo": "«E-mu SP-1200» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/E-mu_SP-1200", "data": "2026-09-22"},
            {"titolo": "«The Legendary E-mu SP-1200 Sampling Percussion» — Vintage Digital Australia",
             "url": "https://www.vintagedigital.com.au/e-mu-sp-1200/", "data": "2026-09-22"},
            {"titolo": "«E-mu SP-1200» — Vintage Synth Explorer",
             "url": "https://www.vintagesynth.com/e-mu/sp-1200", "data": "2026-09-22"},
            {"titolo": "«E-mu Systems Pioneered Sampling in Hip-Hop with the SP 1200» — The Music Origins Project",
             "url": "https://musicorigins.org/item/hip-hop-and-the-e-mu-sp1200/", "data": "2026-09-22"},
        ],
        "hashtags": ["#sp1200", "#emu", "#campionatore", "#publicenemy", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 039", "10 secondi di memoria: ci nasce il suono dei Public Enemy"),
            ("SANTA CRUZ, 1987", "Dave Rossum di E-mu fa l'SP-1200 per chi non può pagarsi un Emulator."),
            ("4 BANCHI DA 2,5 SECONDI", "12 bit e 26,04 kHz, molto meno di un CD. È lì il carattere."),
            ("PUBLIC ENEMY, 1988", "Il Bomb Squad ci monta i collage di «It Takes a Nation of Millions»"),
            ("1997", "Chip del filtro esauriti, E-mu smette. Da lì l'usato sale di prezzo."),
        ],
        "reel_cta": "Mandalo a chi campiona ancora dai dischi",
        "verificata": True,
    },
    # ---------------------------------------------------------------- 40
    {
        "slug": "univibe",
        "numero": 40,
        "serie": "GLI EFFETTI",
        "strumento": "Univox Uni-Vibe",
        "anno": "1968",
        "luogo": "Tokyo, Giappone",
        "costruttore": "Shin-ei (distribuito da Univox)",
        "specifiche": [
            ("ANNO", "1968"),
            ("COSTRUTTORE", "Shin-ei / Univox"),
            ("PRINCIPIO", "Ottico, senza op-amp"),
            ("CONTROLLO", "Pedale di velocità"),
        ],
        "gancio": "Doveva imitare un altoparlante che gira. O forse una radio che capta Mosca, di notte",
        "sottotitolo": "Una lampadina, quattro fotoresistenze e un pedale: l'effetto che oscilla come un altoparlante rotante senza avere nulla che ruoti.",
        "la_macchina": "Dentro la scatola non c'è niente che gira: c'è una lampadina che pulsa e quattro fotoresistenze che ne seguono la luce, cambiando la fase del segnale che passa. Il risultato suona come un altoparlante Leslie, quello con la cassa rotante degli organi Hammond, ma il Uni-Vibe non ha parti meccaniche — solo un circuito ottico, senza un solo amplificatore operazionale, come si dice fra chi lo ripara. Un pedale separato, collegato con un cavo a parte, regola la velocità dell'oscillazione, dal tremolo lento al vibrato che sembra impazzito.",
        "inventore_nome": "Fumio Mieda",
        "inventore": "Fumio Mieda lo progetta a metà degli anni Sessanta per la giapponese Honey, che lo chiama Vibra-Chorus; quando Honey chiude, nel 1968, il circuito passa alla Shin-ei, che aggiunge il pedale di velocità esterno e lo vende negli Stati Uniti tramite Univox, col nome Uni-Vibe. Sul motivo per cui suona così, le fonti non concordano: la versione più diffusa dice che Mieda voleva imitare il Leslie; lui stesso, in un'intervista, ha raccontato di essersi ispirato al suono di una radio che riceve Radio Mosca di notte, modulato dall'atmosfera. Può darsi che siano vere entrambe.",
        "come_funziona": "La lampadina al centro del circuito si accende e si spegne a un ritmo regolabile; quattro fotoresistenze, disposte intorno, cambiano resistenza seguendo quella luce, e spostano di conseguenza la fase del segnale audio che ci passa attraverso. È un phaser, tecnicamente, ma il suono è più denso e più lento di un phaser a transistor, proprio perché la luce non reagisce mai di scatto come un circuito elettronico puro. Il pedale esterno regola solo la velocità: l'intensità dell'effetto resta fissa.",
        "richiami": [
            ("FIG. 1", "Lampadina + 4 fotoresistenze"),
            ("FIG. 2", "Circuito ottico, senza op-amp"),
            ("FIG. 3", "Pedale di velocità esterno"),
        ],
        "chi_lusata": [
            {"artista": "Jimi Hendrix", "nota": "Lo usa dal vivo a Woodstock, agosto 1969, e in studio su «Machine Gun» (Band of Gypsys, 1970)", "ig": None},
            {"artista": "David Gilmour (Pink Floyd)", "nota": "La chitarra ondulata di «Breathe», in apertura di «The Dark Side of the Moon» (1973)", "ig": None},
            {"artista": "Robin Trower", "nota": "Il suono che definisce il brano-titolo di «Bridge of Sighs» (1974)", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": "Hendrix lo acquista nella seconda metà del 1969, meno di un anno prima di morire: significa che compare solo negli ultimi concerti e nelle ultime session, non nei dischi degli anni precedenti. A Woodstock, il 18 agosto 1969, lo tiene acceso per buona parte del set. Il pedale che aveva davvero ai suoi piedi, oggi, è esposto all'EMP Museum di Seattle — la foto di questa scheda è quel pedale, non una ristampa.",
        "avvertenza": "Non ho niente che giri, dentro: solo una lampadina e quattro occhi che ne seguono la luce. Se sento caldo, sto solo lavorando.",
        "da_ascoltare": {"brano": "Bridge of Sighs", "artista": "Robin Trower", "anno": "1974",
                         "cosa": "Il pezzo che dà il titolo all'album: ascoltate come l'oscillazione dell'Uni-Vibe si muove insieme alla nota, non sopra."},
        "foto": {
            "file": "assets/foto/univibe/principale.jpg",
            "autore": "~Jen~",
            "licenza": "CC BY 2.0",
            "fonte": "Wikimedia Commons",
            "didascalia": "Il pedale di Hendrix, oggi all'EMP Museum di Seattle",
        },
        "fonti": [
            {"titolo": "«Uni-Vibe» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Uni-Vibe", "data": "2026-09-22"},
            {"titolo": "«The Univox Uni-Vibe was the Final Stompbox to Land in Jimi Hendrix's Effects Chain» — GuitarPlayer",
             "url": "https://www.guitarplayer.com/gear/the-univox-uni-vibe-was-the-final-stompbox-to-land-in-jimi-hendrixs-effects-chain", "data": "2026-09-22"},
            {"titolo": "«Jimi Hendrix's Shin-ei/Univox Uni-Vibe» — Ground Guitar",
             "url": "https://www.groundguitar.com/jimi-hendrix-gear/jimi-hendrixs-shin-ei-univox-uni-vibe/", "data": "2026-09-22"},
            {"titolo": "«The Secrets Behind Robin Trower's Guitar Tone on Bridge of Sighs» — Guitar World",
             "url": "https://www.guitarworld.com/features/the-secrets-behind-robin-trowers-guitar-tone-on-bridge-of-sighs", "data": "2026-09-22"},
            {"titolo": "«Bridge of Sighs (Robin Trower album)» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Bridge_of_Sighs_(Robin_Trower_album)", "data": "2026-09-22"},
        ],
        "hashtags": ["#univibe", "#univox", "#effettichitarra", "#jimihendrix", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 040", "Questo pedale finisce ai piedi di Jimi Hendrix"),
            ("FUMIO MIEDA, METÀ ANNI '60", "Si dice che imitasse un Leslie. Mieda parla di Radio Mosca, di notte."),
            ("UNI-VIBE, 1968", "Dentro non gira niente: una lampadina e 4 fotoresistenze."),
            ("SECONDA METÀ DEL 1969", "Hendrix compra l'Uni-Vibe meno di un anno prima di morire."),
            ("WOODSTOCK, 18/08/1969", "Lo tiene acceso per buona parte del set. Oggi è in un museo a Seattle."),
        ],
        "reel_cta": "Mandalo al chitarrista fissato con Hendrix",
        "reel_audio": {
            "file": "assets/audio/univibe/registrazione.ogg", "inizio": 7,
            "autore": "Fret Junkies, estratto di Skimel", "licenza": "CC BY 3.0",
            "fonte": "Wikimedia Commons",
            "url": "https://commons.wikimedia.org/wiki/File:Univibe_medium_speed,_chorus_setting_(classic_sound).ogg",
            "cosa": "una chitarra in un Uni-Vibe, velocità media, posizione chorus",
        },
        "verificata": True,
    },
    # ---------------------------------------------------------------- 41
    {
        "slug": "jupiter8",
        "numero": 41,
        "serie": "I SINTETIZZATORI",
        "strumento": "Roland Jupiter-8",
        "anno": "1981",
        "luogo": "Hamamatsu, Giappone",
        "costruttore": "Roland Corporation",
        "specifiche": [
            ("ANNO", "1981"),
            ("COSTRUTTORE", "Roland Corporation"),
            ("VOCI", "8"),
            ("OSCILLATORI", "2 per voce"),
        ],
        "gancio": "Prima di lui la polifonia si pagava in stabilità: questo synth Roland non stona mai",
        "sottotitolo": "Otto voci, 64 patch in memoria, un circuito che non perde l'accordatura: il sintetizzatore con cui Roland si mette a fianco dei giganti americani.",
        "la_macchina": "Otto voci polifoniche, due oscillatori per ciascuna con sync e cross-modulation, un filtro passa-basso risonante a 12 o 24 dB per ottava più uno passa-alto: sulla carta assomiglia a molti synth dell'epoca. La differenza si sente all'accensione. Un circuito di compensazione della temperatura tiene gli oscillatori accordati anche dopo ore sotto le luci di scena, cosa che ai concorrenti analogici capita raramente. In memoria stanno 64 patch, la tastiera si divide in due suoni diversi, e le uscite XLR bilanciate sono pensate per lo studio oltre che per il palco.",
        "inventore_nome": "Il reparto R&S di Roland",
        "inventore": "Nessuna fonte assegna il Jupiter-8 a un solo progettista: nasce nei laboratori Roland di Hamamatsu nel 1980, sotto la guida del fondatore Ikutaro Kakehashi, come sintetizzatore di punta dell'azienda per la prima metà degli anni Ottanta. Esce a inizio 1981, prezzo 5.295 dollari, e resta in produzione fino al 1985: ne escono circa 3.300 esemplari. È il primo synth Roland pensato per competere apertamente con i polifonici americani, Sequential e Oberheim, sul loro stesso terreno: l'affidabilità sul palco.",
        "come_funziona": "Ogni voce ha due VCO con sync e modulazione incrociata, quindi timbri più complessi di un solo oscillatore per voce. Il filtro passa-basso, il cuore del suono Roland di quegli anni, si può mettere a 12 o 24 dB per ottava di pendenza; un secondo filtro, passa-alto e non risonante, toglie il grasso in eccesso alle basse frequenze. Un microprocessore Zilog Z80 gestisce la memoria delle 64 patch e la scansione di tastiera e pannelli: è uno dei primi synth Roland in cui il controllo digitale non tocca il suono, che resta interamente analogico.",
        "richiami": [
            ("FIG. 1", "2 VCO per voce, sync + cross-mod"),
            ("FIG. 2", "Filtro 12/24 dB per ottava"),
            ("FIG. 3", "64 patch, CPU Zilog Z80"),
        ],
        "chi_lusata": [
            {"artista": "Duran Duran (Nick Rhodes)", "nota": "L'arpeggio di «Hungry Like the Wolf» (1982) è un Jupiter-8: lo ha confermato lui stesso, dopo anni in cui i fan lo scambiavano per un Jupiter-4", "ig": None},
            {"artista": "Queen (Fred Mandel)", "nota": "Il turnista Fred Mandel lo suona su «Radio Ga Ga», «Hammer to Fall» e l'assolo di «I Want to Break Free» (The Works, 1984)", "ig": None},
            {"artista": "Michael Jackson", "nota": "È fra i synth usati nelle session di «Thriller» (1982)", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": "Per anni, fra chi suona synth, gira una discussione su quale Jupiter abbiano usato i Duran Duran in «Hungry Like the Wolf»: l'arpeggio suona come un Jupiter-8, ma «Rio», lo stesso anno, usa di sicuro un Jupiter-4, e i due synth in un mix si confondono facilmente. Nick Rhodes ha chiuso la discussione di persona, anni dopo: è un Jupiter-8, programmato con l'arpeggiatore interno e mandato a un sequencer esterno insieme a un TR-808 per il ritmo. Dal vivo, comunque, i Duran Duran portavano entrambi i synth sullo stesso palco.",
        "avvertenza": "Ho un circuito che mi tiene accordato anche sotto le luci calde del palco. Gli altri synth di quest'epoca no: se stonano, non è colpa mia.",
        "da_ascoltare": {"brano": "I Want to Break Free", "artista": "Queen", "anno": "1984",
                         "cosa": "L'assolo di sintetizzatore, registrato da Fred Mandel in una sola ripresa: solo l'ultima nota, con un portamento discendente, è un secondo overdub."},
        "foto": {
            "file": "assets/foto/jupiter8/principale.jpg",
            "autore": "Ed Uthman (rielaborazione: Clusternote)",
            "licenza": "CC BY-SA 2.0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "«Roland Jupiter-8» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Roland_Jupiter-8", "data": "2026-09-22"},
            {"titolo": "«JUPITER: King of the Polysynths» — Roland Articles (sito ufficiale)",
             "url": "https://articles.roland.com/jupiter-king-of-the-polysynths/", "data": "2026-09-22"},
            {"titolo": "«How Duran Duran's 'Hungry Like the Wolf' Began Its Long Ascent» — Ultimate Classic Rock",
             "url": "https://ultimateclassicrock.com/duran-duran-hungry-like-the-wolf/", "data": "2026-09-22"},
            {"titolo": "«Hungry Like The Wolf» — Songfacts",
             "url": "https://www.songfacts.com/facts/duran-duran/hungry-like-the-wolf", "data": "2026-09-22"},
            {"titolo": "«I Want to Break Free» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/I_Want_to_Break_Free", "data": "2026-09-22"},
        ],
        "hashtags": ["#jupiter8", "#roland", "#sintetizzatore", "#queen", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 041", "Per anni i fan dei Duran Duran hanno sbagliato synth"),
            ("1982 · DURAN DURAN", "L'arpeggio di «Hungry Like the Wolf». Per molti è un Jupiter-4."),
            ("STESSO ANNO · «RIO»", "«Rio» usa di sicuro un Jupiter-4, e in un mix i due si confondono."),
            ("NICK RHODES", "Anni dopo lo dice Nick Rhodes in persona. È un Jupiter-8."),
            ("DAL VIVO", "E sul palco i Duran Duran se li portano tutti e due."),
        ],
        "reel_cta": "Mandalo a chi giurava che era un Jupiter-4",
        "verificata": True,
    },
    # ---------------------------------------------------------------- 42
    {
        "slug": "speakspell",
        "numero": 42,
        "serie": "I GIOCATTOLI",
        "strumento": "Speak & Spell",
        "anno": "1978",
        "luogo": "Dallas, Texas",
        "costruttore": "Texas Instruments",
        "specifiche": [
            ("ANNO", "1978"),
            ("COSTRUTTORE", "Texas Instruments"),
            ("CHIP", "TMS5100 (LPC)"),
            ("PAROLE", "oltre 200"),
        ],
        "gancio": "Un giocattolo per bambini di 7 anni nasconde il primo sintetizzatore vocale su un solo chip",
        "sottotitolo": "Oltre 200 parole in un dizionario elettronico da studio: il chip che insegna a un giocattolo a parlare.",
        "la_macchina": "È un dizionario elettronico per bambini dai 7 anni in su: tastiera a membrana, display a fluorescenza sottovuoto, una fessura per cartucce ROM con altre liste di parole. Si preme una parola, la voce sintetica la pronuncia, il bambino prova a scriverla lettera per lettera. Dentro non c'è nessuna voce campionata: il chip ricrea il parlato da zero, comprimendolo in poche centinaia di byte per parola con un modello matematico chiamato linear predictive coding. È il primo giocattolo con un sintetizzatore vocale su un solo chip, e quella voce leggermente metallica si riconosce ancora oggi.",
        "inventore_nome": "Paul Breedlove, Gene Frantz, Larry Brantingham, Richard Wiggins",
        "inventore": "Il progetto parte nel 1976 dentro Texas Instruments, con un budget iniziale di 25.000 dollari: doveva dimostrare che la sintesi vocale si poteva mettere su un chip solo, il TMS5100, invece che su un'intera scheda da laboratorio. Il team, guidato da Paul Breedlove con Gene Frantz, Larry Brantingham e Richard Wiggins, lo trasforma in un prodotto per bambini: un dizionario che parla, non solo che legge. Debutta al Consumer Electronics Show del giugno 1978. In Italia lo vendono con un altro nome, Grillo Parlante — lo stesso soprannome del personaggio di Pinocchio.",
        "come_funziona": "Il TMS5100 non riproduce un audio campionato: ricrea la voce con un modello matematico del tratto vocale umano, il linear predictive coding, che descrive ogni suono con pochi coefficienti invece che con migliaia di campioni. Il risultato occupa pochissima memoria — l'intero vocabolario di partenza sta in pochi kilobyte — ma ha quella grana leggermente metallica che oggi si chiama, con affetto, il suono della sintesi vocale anni Settanta. Le cartucce ROM aggiungono vocabolari nuovi senza cambiare l'elettronica dentro.",
        "richiami": [
            ("FIG. 1", "TMS5100, sintesi a chip singolo"),
            ("FIG. 2", "Linear predictive coding"),
            ("FIG. 3", "Fessura per cartucce ROM"),
        ],
        "chi_lusata": [
            {"artista": "Depeche Mode", "nota": "Intitolano il loro album d'esordio proprio «Speak & Spell» (1981), omaggio dichiarato al giocattolo", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": "Nel 1982 Steven Spielberg mette uno Speak & Spell modificato nelle mani di Elliott, il protagonista di «E.T. l'extra-terrestre»: è il congegno con cui il bambino aiuta l'alieno a costruire il comunicatore per «telefonare casa». Il giocattolo non canta né suona: nel film fa da prop tecnico, eppure quell'immagine — un dizionario elettronico smontato su un tavolo pieno di fili — resta più impressa di molte delle 200 parole che sa davvero pronunciare.",
        "avvertenza": "Non ho registrato nessuna voce: la ricostruisco da un modello matematico. Se sembro un robot, è perché in un certo senso lo sono.",
        "foto": {
            "file": "assets/foto/speakspell/principale.jpg",
            "autore": "Tilemahos Efthimiadis",
            "licenza": "CC BY-SA 2.0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "«Speak & Spell (toy)» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Speak_%26_Spell_(toy)", "data": "2026-09-22"},
            {"titolo": "«Milestones: Speak & Spell, the First Use of a Digital Signal Processing IC for Speech Generation, 1978» — Engineering and Technology History Wiki (IEEE)",
             "url": "https://ethw.org/Milestones:Speak_&_Spell,_the_First_Use_of_a_Digital_Signal_Processing_IC_for_Speech_Generation,_1978", "data": "2026-09-22"},
            {"titolo": "«Speak & Spell History: Texas Instruments' Greatest Product» — Tedium",
             "url": "https://tedium.co/2018/06/19/speak-and-spell-history/", "data": "2026-09-22"},
            {"titolo": "«Speak & Spell (album)» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Speak_%26_Spell_(album)", "data": "2026-09-22"},
        ],
        "hashtags": ["#speakandspell", "#texasinstruments", "#sintesivocale", "#depechemode", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 042", "E.T. vuole telefonare casa. Gli serve questo giocattolo"),
            ("TEXAS INSTRUMENTS · 1976", "Deve provare che una voce sintetica sta su un chip solo, il TMS5100."),
            ("GIUGNO 1978", "Debutta come Speak & Spell, un dizionario che parla. Dai 7 anni in su."),
            ("IN ITALIA", "Da noi si chiama Grillo Parlante. Come quello di Pinocchio."),
            ("1982 · SPIELBERG", "Lo dà a Elliott, modificato, per costruire il comunicatore di «E.T.»."),
        ],
        "reel_cta": "Mandalo a chi aveva il Grillo Parlante",
        # Registrazione della macchina vera (16/10/2026): licenza libera,
        # verificata sulla pagina Freesound (descrizione + licenza).
        "reel_audio": {
            "file": "assets/audio/speakspell/registrazione.mp3", "inizio": 0,
            "autore": "deaf02", "licenza": "CC0 1.0",
            "fonte": "freesound.org/s/563030",
            "url": "https://freesound.org/s/563030/",
            "cosa": "uno Speak & Spell vero che recita l'alfabeto",
        },
        "verificata": True,
    },
    # ---------------------------------------------------------------- 43
    {
        "slug": "vp330",
        "numero": 43,
        "serie": "GLI EFFETTI",
        "strumento": "Roland VP-330 Vocoder Plus",
        "anno": "1979",
        "luogo": "Hamamatsu, Giappone",
        "costruttore": "Roland Corporation",
        "specifiche": [
            ("ANNO", "1979"),
            ("COSTRUTTORE", "Roland Corporation"),
            ("VOCODER", "10 bande"),
            ("TASTI", "49"),
        ],
        "gancio": "Un vocoder a dieci bande dentro una tastiera d'archi: la voce robotica degli anni Ottanta nasce qui",
        "sottotitolo": "Vocoder a dieci bande più synth d'archi e coro sintetico, in una tastiera sola: la voce robotica dei primi anni Ottanta ha questo nome.",
        "la_macchina": "È l'ultimo di una linea di synth d'archi Roland iniziata nel 1975: sopra i tasti aggiunge un vocoder a dieci bande — sette per una voce umana sintetica, dieci per processare quella vera attraverso il microfono incorporato — più due registri di coro sintetico e la sezione archi ereditata dai modelli precedenti. Si suona come una tastiera normale, ma quello che esce, se si parla nel microfono mentre si tengono gli accordi, è la propria voce trasformata in accordo: il suono che negli anni Ottanta si sente da Stevie Wonder a Laurie Anderson.",
        "inventore_nome": "Il reparto R&S di Roland",
        "inventore": "Il VP-330 chiude una linea di sintetizzatori d'archi che Roland apre nel 1975 con l'RS-101: ogni modello aggiunge qualcosa, e nel 1979 il VP-330 ci mette sopra un vocoder completo, da cui il nome «Vocoder Plus». Costa 2.695 dollari, una cifra alta per l'epoca, e resta in listino solo un anno, fino al 1980, prima di essere sostituito. Nonostante la vita commerciale breve — ne restano pochi, e valgono più oggi che nel 1979 — diventa lo strumento con cui più produttori associano il suono vocoder dei primi anni Ottanta.",
        "come_funziona": "Il microfono incorporato cattura la voce e la scompone in dieci bande di frequenza; ogni banda controlla, in tempo reale, l'ampiezza della banda corrispondente di un suono sintetico generato dai synth d'archi interni. Il risultato è la voce che «parla» attraverso un accordo, invece che attraverso le corde vocali. Volendo, si può ignorare il microfono e usare solo la sezione «Human Voice», sette bande fisse che imitano un coro senza bisogno di parlare.",
        "richiami": [
            ("FIG. 1", "Vocoder 10 bande + microfono"),
            ("FIG. 2", "Human Voice, 7 bande fisse"),
            ("FIG. 3", "Sezione archi ereditata dagli RS"),
        ],
        "chi_lusata": [
            {"artista": "Stevie Wonder", "nota": "Canta l'intera ultima strofa di «I Just Called to Say I Love You» (1984) attraverso il vocoder del VP-330", "ig": None},
            {"artista": "Laurie Anderson", "nota": "La voce filtrata di «O Superman» (1981) passa dal vocoder del VP-330, con gli archi sintetici che entrano a metà pezzo", "ig": None},
            {"artista": "Vangelis", "nota": "Lo usa per il coro sintetico di «Chariots of Fire» e per «Tears in Rain» nella colonna sonora di Blade Runner", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": "Nel 2020 il produttore Koz mette le mani su un VP-330 appena comprato: prima ancora di sapere cosa farci, la sezione Human Voice con l'ensemble acceso e il portamento premuto diventa l'apertura di «Levitating» di Dua Lipa. Quarant'anni dopo il debutto, lo stesso circuito che faceva cantare Stevie Wonder apre una hit pop del 2020.",
        "avvertenza": "La mia voce non è la mia: è la vostra, passata per dieci filtri e un accordo. Parlate chiaro, o canterò quello che dite male.",
        "da_ascoltare": {"brano": "O Superman", "artista": "Laurie Anderson", "anno": "1981",
                         "cosa": "Otto minuti su un accordo che oscilla fra La bemolle e Do minore: il vocoder VP-330 entra sulla voce fin dal primo verso."},
        "foto": {
            "file": "assets/foto/vp330/principale.jpg",
            "autore": "ghostdad",
            "licenza": "CC BY-SA 2.0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "«Roland VP-330» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Roland_VP-330", "data": "2026-09-22"},
            {"titolo": "«5 songs that use Roland's classic VP-330 Vocoder Plus» — MusicRadar",
             "url": "https://www.musicradar.com/news/5-songs-vp-330", "data": "2026-09-22"},
            {"titolo": "«Roland VP-330 - figurehead of the Vocoder Hype» — GreatSynthesizers",
             "url": "https://greatsynthesizers.com/en/review/roland-vp-330-figurehead-of-the-vocoder-hype/", "data": "2026-09-22"},
        ],
        "hashtags": ["#vp330", "#roland", "#vocoder", "#dualipa", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 043", "«Levitating» di Dua Lipa si apre con un synth del 1979"),
            ("ROLAND · 1979", "Il Roland VP-330 costa 2.695 dollari e resta in listino un anno solo."),
            ("1984 · STEVIE WONDER", "L'ultima strofa di «I Just Called to Say I Love You» passa da qui."),
            ("2020 · IL PRODUTTORE KOZ", "Koz se ne compra uno. Non sa ancora cosa farci."),
            ("SEZIONE HUMAN VOICE", "Ensemble acceso, portamento premuto. Ed è l'intro di «Levitating»."),
        ],
        "reel_cta": "Mandalo a chi ha «Levitating» in playlist",
        # Registrazione della macchina vera (17/10/2026, regola del proprietario:
        # il suono vero in ogni uscita). Licenza verificata sulla pagina;
        # la pagina registra il coro nota per nota; qui due note (una quinta sopra) unite in dissolvenza.
        "reel_audio": {
            "file": "assets/audio/vp330/registrazione.mp3", "inizio": 0,
            "autore": "Elektrik_Musik", "licenza": "CC0 1.0",
            "fonte": "freesound.org/s/170493",
            "url": "https://freesound.org/s/170493/",
            "cosa": "un Roland VP-330 vero: il coro femminile, due note tenute",
        },
        "verificata": True,
    },
    # ---------------------------------------------------------------- 44
    {
        "slug": "cs80",
        "numero": 44,
        "serie": "I SINTETIZZATORI",
        "strumento": "Yamaha CS-80",
        "anno": "1976",
        "luogo": "Hamamatsu, Giappone",
        "costruttore": "Yamaha",
        "specifiche": [
            ("ANNO", "1976"),
            ("COSTRUTTORE", "Yamaha"),
            ("VOCI", "8"),
            ("TASTIERA", "Aftertouch + ribbon"),
        ],
        "gancio": "Un nastro sotto i tasti piega le note come una chitarra: Vangelis lo chiamava «il migliore mai fatto»",
        "sottotitolo": "Otto voci, aftertouch nota per nota, un ribbon controller sotto la tastiera: il sintetizzatore che si suona come si suona un violino.",
        "la_macchina": "Otto voci polifoniche, due oscillatori ciascuna, due filtri passa-alto e due passa-basso per voce: sulla carta un synth analogico come tanti del 1976. La differenza sta nel tocco. La tastiera legge la velocity e l'aftertouch nota per nota, non su tutta la tastiera insieme come quasi tutti i concorrenti, e sotto i tasti corre un ribbon controller, una striscia sensibile al tocco con cui si piegano le note in continuo. È pesante e ingombrante, e al debutto il mercato lo trova più caro e più difficile da programmare del Prophet-5 di Sequential, uscito poco dopo.",
        "inventore_nome": "Yamaha",
        "inventore": "Non emerge un nome singolo dietro il CS-80: nasce nei laboratori Yamaha di Hamamatsu come punta di una linea, la serie CS, iniziata l'anno prima con modelli più semplici. Esce nel 1976 a 6.900 dollari, un prezzo da studio professionale più che da musicista di banda. Il pubblico iniziale è tiepido: pesante, costoso, con un sistema di patch scomodo da richiamare dal vivo. Lo salva la scena, non il negozio: bastano pochi musicisti a scoprire cosa si può fare con l'aftertouch polifonico e il ribbon, e il CS-80 diventa lo strumento che si cerca apposta, non quello che capita.",
        "come_funziona": "Ogni voce ha due oscillatori, due filtri e un proprio inviluppo per il filtro e uno per l'ampiezza: per questo due voci diverse possono sovrapporsi come due strumenti reali, uno che entra dolce e uno che entra secco. La tastiera è sensibile al tocco nota per nota — l'aftertouch, la pressione dopo che il tasto è già premuto, agisce diversamente su ogni dito — mentre il ribbon controller sotto i tasti, una striscia orizzontale, piega l'intonazione in modo continuo al tocco del pollice, senza gradini.",
        "richiami": [
            ("FIG. 1", "8 voci, 2 oscillatori ciascuna"),
            ("FIG. 2", "Aftertouch polifonico"),
            ("FIG. 3", "Ribbon controller sotto i tasti"),
        ],
        "chi_lusata": [
            {"artista": "Vangelis", "nota": "Lo usa dal 1977 (Spiral) fino a Blade Runner e Chariots of Fire, e lo definisce «il miglior sintetizzatore analogico mai costruito»", "ig": None},
            {"artista": "Toto (David Paich)", "nota": "Il fiato che apre «Africa» (1982) è un CS-80: Steve Porcaro lo mostra a Paich apposta per scrivere un pezzo pensato per quel suono", "ig": None},
            {"artista": "Michael Jackson", "nota": "Il motivo di accordi di «Billie Jean» (1982) è registrato in una sola ripresa su un CS-80", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": "Nel 2024 un CS-80 va all'asta su Reverb con una scheda che lo descrive appartenuto a Vangelis, prezzo richiesto oltre 400.000 sterline: la provenienza è dichiarata, non certificata, e il compositore ne possedeva più di uno, quindi nessuno può dire con certezza se sia proprio quello di «Blade Runner». Vero o no, il prezzo dice quanto vale oggi un sintetizzatore che nel 1976 il mercato considerava troppo ingombrante da comprare.",
        "avvertenza": "Il mio aftertouch legge ogni dito per conto suo, non tutta la tastiera insieme. Se un accordo suona storto, guardate quale dito premete più forte.",
        "da_ascoltare": {"brano": "Africa", "artista": "Toto", "anno": "1982",
                         "cosa": "Ascoltate il fiato che apre il pezzo, prima ancora della voce: è il CS-80, non un ottone vero."},
        "foto": {
            "file": "assets/foto/cs80/principale.jpg",
            "autore": "Csaba Zvekan",
            "licenza": "CC BY 2.0",
            "fonte": "Wikimedia Commons",
        },
        "foto_extra": [
            {"file": "assets/foto/cs80/interno.jpg",
             "autore": "J R", "licenza": "CC BY-SA 2.0", "fonte": "Wikimedia Commons",
             "didascalia": "L'elettronica dentro un CS-80"},
        ],
        "fonti": [
            {"titolo": "«Yamaha CS-80» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Yamaha_CS-80", "data": "2026-09-22"},
            {"titolo": "«Exploring The Yamaha CS-80» — Reverb Machine",
             "url": "https://reverbmachine.com/blog/exploring-the-yamaha-cs-80/", "data": "2026-09-22"},
            {"titolo": "«The Synth Sounds of Toto's 'Africa'» — Reverb News",
             "url": "https://reverb.com/news/the-synth-sounds-of-totos-africa", "data": "2026-09-22"},
            {"titolo": "«$500k Yamaha CS-80 claimed to have belonged to Vangelis goes up for sale on Reverb» — MusicRadar",
             "url": "https://www.musicradar.com/music-tech/analogue-synths/this-is-the-real-deal-gbp400k-yamaha-cs-80-claimed-to-have-belonged-to-vangelis-goes-up-for-sale-on-reverb", "data": "2026-09-22"},
        ],
        "hashtags": ["#cs80", "#yamaha", "#sintetizzatore", "#michaeljackson", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 044", "Il fiato che apre «Africa» dei Toto non è un ottone"),
            ("YAMAHA · 1976", "È uno Yamaha CS-80. Costa 6.900 dollari e il pubblico è tiepido."),
            ("TOTO · STEVE PORCARO", "Porcaro lo fa sentire a David Paich perché ci scriva un pezzo."),
            ("1982 · MICHAEL JACKSON", "C'è un CS-80 anche negli accordi di «Billie Jean». Una sola ripresa."),
            ("2024 · REVERB", "Uno va in vendita a oltre 400.000 sterline. Forse di Vangelis."),
        ],
        "reel_cta": "Mandalo a chi canta «Africa» al karaoke",
        "verificata": True,
    },
    # ---------------------------------------------------------------- 45
    {
        "slug": "telharmonium",
        "numero": 45,
        "serie": "LE ORIGINI",
        "strumento": "Telharmonium",
        "anno": "1906",
        "luogo": "Holyoke, Massachusetts",
        "costruttore": "Thaddeus Cahill",
        "specifiche": [
            ("ANNO", "1906"),
            ("PESO", "200 tonnellate"),
            ("ALTERNATORI", "145"),
            ("USCITA", "Cavi del telefono"),
        ],
        "gancio": "200 tonnellate di generatori in cantina, e la musica arriva a casa dal telefono. Siamo nel 1906",
        "sottotitolo": "Thaddeus Cahill costru\u00ec un sintetizzatore grande come una fabbrica e ci vendette la musica in abbonamento.",
        "la_macchina": "Un telaio d'acciaio lungo 18 metri, otto alberi che girano, 145 "
            "alternatori che generano corrente alle frequenze delle note. Sopra "
            "ci stanno due consolle con le tastiere e quasi 2.000 interruttori. "
            "Altoparlanti non ce ne sono: il segnale entra nei cavi del telefono "
            "e riemerge dall'altra parte dentro un corno di ottone, in un albergo "
            "o in un ristorante che paga l'abbonamento. Per portarlo da Holyoke a "
            "New York servirono 30 vagoni.",
        "inventore_nome": "Thaddeus Cahill",
        "inventore": "Cahill nasce in Iowa nel 1867 e deposita il brevetto nel 1897, "
            "quando il telefono ha vent'anni e la radio non c'è ancora. L'idea "
            "non era solo costruire lo strumento: era vendere la musica come si "
            "vende la corrente, a contatore, dentro i fili che c'erano già. Ne "
            "costruì tre. Il primo pesava 7 tonnellate ed era un prototipo per "
            "trovare i soldi; il secondo è quello che andò a New York. La società "
            "fallì nel 1914 e Cahill morì vent'anni dopo, a 66 anni.",
        "come_funziona": "Ogni nota ha il suo alternatore: un rotore che gira dentro un campo "
            "magnetico e produce corrente alternata alla frequenza giusta. Un la "
            "a 440 hertz è un alternatore che fa 440 oscillazioni al secondo, e "
            "basta. Per cambiare timbro si sommano più alternatori accordati "
            "sugli armonici, dosandoli con dei trasformatori. È sintesi additiva, "
            "la stessa che trent'anni dopo Hammond mette nelle ruote foniche "
            "dell'organo. La corrente che esce è già segnale audio e va dritta "
            "nel doppino.",
        "richiami": [
            ("FIG. 1", "145 alternatori, uno per nota"),
            ("FIG. 2", "Armonici sommati: sintesi additiva"),
            ("FIG. 3", "Uscita diretta sul doppino"),
        ],
        "chi_lusata": [
            {"artista": "Mark Twain", "nota": "Lo ascolt\u00f2 nel dicembre 1906 e disse che avrebbe dovuto rimandare la propria morte", "ig": None},
            {"artista": "Gli abbonati di New York", "nota": "Alberghi e ristoranti, con la musica che usciva da un corno di ottone appeso al soffitto", "ig": None},
            {"artista": "Chi telefonava, senza volerlo", "nota": "Il segnale passava nelle linee vicine: la gente si trovava la musica dentro le proprie chiamate", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": "Dicembre 1906, Broadway all'altezza della 39esima strada. Mark Twain entra nella sala del Telharmonium, si siede vicino alla consolle e si fa suonare la marcia nuziale del Lohengrin. Poi dice una frase che il New York Times stampa il 23: il guaio di queste cose nuove e bellissime \u00e8 che si mettono di traverso ai tuoi programmi, e adesso non pu\u00f2 pi\u00f9 andarsene dal mondo finch\u00e9 non l'ha sentita ancora e ancora. Di quel suono non resta niente. Non esiste una sola registrazione del Telharmonium.",
        "avvertenza": "Il suono esce dal doppino del telefono, non da un altoparlante. Se la linea \u00e8 quella sbagliata, il concerto lo sentono altri.",
        "foto": {
            "file": "assets/foto/telharmonium/principale.jpg",
            "posizione": "center 45%",
            "autore": "autore sconosciuto (1906)",
            "licenza": "pubblico dominio",
            "fonte": "Wikimedia Commons",
        },
        # Ordine = tavola: 2 la consolle, 3 il miscelatore di timbri,
        # 4 la sala degli alternatori sotto \u00abcome funziona\u00bb.
        "foto_extra": [
            {"file": "assets/foto/telharmonium/consolle.png",
             "autore": "Lazarnick", "licenza": "pubblico dominio", "fonte": "Wikimedia Commons",
             "didascalia": "La consolle dei tasti"},
            # Ritaglio alto: la banda e' larga e bassa, e centrata pescava
            # le gambe dell'operaio e mezzo miscelatore. A 15% entrano la
            # faccia e la cima della macchina, che e' il confronto di misura.
            {"file": "assets/foto/telharmonium/miscelatore.png",
             "posizione": "center 15%",
             "autore": "Lazarnick", "licenza": "pubblico dominio", "fonte": "Wikimedia Commons",
             "didascalia": "Il miscelatore dei timbri, e l'uomo che lo teneva acceso"},
            {"file": "assets/foto/telharmonium/alternatori.png",
             "autore": "Lazarnick", "licenza": "pubblico dominio", "fonte": "Wikimedia Commons",
             "didascalia": "La sala degli alternatori"},
        ],
        "fonti": [
            {"titolo": "\u00abTelharmonium\u00bb \u2014 Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Telharmonium", "data": "2026-09-23"},
            {"titolo": "\u00abThaddeus Cahill\u00bb \u2014 Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Thaddeus_Cahill", "data": "2026-09-23"},
            {"titolo": "\u00abThe Telharmonium\u00bb \u2014 120 Years of Electronic Music",
             "url": "https://120years.net/the-telharmonium-thaddeus-cahill-usa-1897/", "data": "2026-09-23"},
            {"titolo": "\u00abTwain and the Telephone\u00bb \u2014 The New York Times, 23/12/1906 (archivio twainquotes.com)",
             "url": "http://www.twainquotes.com/19061223.html", "data": "2026-09-23"},
        ],
        "hashtags": ["#telharmonium", "#thaddeuscahill", "#musicaelettronica", "#marktwain", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 045", "Per questa musica Mark Twain vuole rimandare la morte."),
            ("NEW YORK, DICEMBRE 1906", "Esce dal Telharmonium di Thaddeus Cahill. Pesa 200 tonnellate."),
            ("NIENTE ALTOPARLANTI", "Alberghi e ristoranti abbonati la ricevono dai cavi del telefono."),
            ("LINEE VICINE", "Il segnale sconfina, e c'è chi la sente dentro le telefonate."),
            ("1914", "Nel 1914 la società fallisce. Non ne esiste una sola registrazione."),
        ],
        "reel_cta": "Mandalo a chi ascolta musica in abbonamento",
        "verificata": True,
    },
    # ---------------------------------------------------------------- 46
    {
        "slug": "novachord",
        "numero": 46,
        "serie": "GLI ANTENATI",
        "strumento": "Hammond Novachord",
        "anno": "1939",
        "luogo": "Chicago",
        "costruttore": "Hammond Organ Company",
        "specifiche": [
            ("ANNO", "1939"),
            ("VALVOLE", "163"),
            ("POLIFONIA", "72 note"),
            ("ESEMPLARI", "1.069"),
        ],
        "gancio": "Nel 1939 la Hammond mette in vendita un sintetizzatore polifonico da salotto. Non lo compra quasi nessuno",
        "sottotitolo": "Un mobile di noce pieno di valvole, e una tastiera che suona tutte "
            "le note insieme: il primo sintetizzatore polifonico di serie.",
        "la_macchina": "Sembra un pianoforte da salotto: mobile di noce, gambe tornite, una "
            "fila di manopole nere sopra la tastiera. Dentro ci sono le valvole, "
            "e qui le fonti litigano. 163 per alcune, 169 per altre, e non ho "
            "trovato nessuno che dica di averle contate. I tasti sono 72 e "
            "suonano tutti insieme, senza nessun limite di polifonia. Pesa 230 "
            "chili.",
        "inventore_nome": "Laurens Hammond, John Hanert e C. N. Williams",
        "inventore": "La Hammond aveva già l'organo a ruote foniche, uscito nel 1935, e "
            "cercava qualcosa da vendere alle famiglie. Laurens Hammond lo "
            "progetta con John Hanert e C. N. Williams, e il Novachord si sente "
            "per la prima volta alla Fiera Mondiale di New York del 1939: Ferde "
            "Grofè ci mette in piedi un'orchestra di quattro Novachord e un "
            "organo Hammond, che suona tutti i giorni allo stand della Ford.",
        "come_funziona": "Dodici oscillatori a valvole fanno le dodici note dell'ottava più "
            "acuta. Sotto ci sono i divisori: ogni stadio dimezza la frequenza, e "
            "dimezzare vuol dire scendere di un'ottava esatta. Cosi' tutte le "
            "note sono sempre pronte senza pagare un oscillatore per tasto. È lo "
            "stesso trucco che 35 anni dopo useranno le string machine come il "
            "Crumar Performer. Il resto è già un sintetizzatore, con i filtri in "
            "parallelo e un inviluppo che si sceglie con un commutatore a sette "
            "posizioni.",
        "richiami": [
            ("FIG. 1", "12 oscillatori + divisori"),
            ("FIG. 2", "163 valvole (o 169)"),
            ("FIG. 3", "7 inviluppi a commutatore"),
        ],
        "chi_lusata": [
            {"artista": "Max Steiner", "nota": "Il Novachord \u00e8 dentro la colonna sonora di \u00abVia col vento\u00bb (1939)", "ig": None},
            {"artista": "Ferde Grof\u00e9", "nota": "Alla Fiera Mondiale del 1939 dirige un'orchestra di quattro Novachord", "ig": None},
            {"artista": "Il cinema di paura americano", "nota": "\u00abRebecca\u00bb, \u00abIl mistero del falco\u00bb e poi \u00abAi confini della realt\u00e0\u00bb", "ig": None},
        ],
        "menzioni_extra": [
            # Verificato il 23/09/2026: hammondorganco.com linka
            # @officialhammondorgan nel piede di pagina, e il profilo si
            # presenta come Hammond Organ USA.
            {"ig": "officialhammondorgan",
             "riga": "La Hammond esiste ancora e fa ancora organi: è @officialhammondorgan."},
        ],
        "aneddoto": "La Hammond lo pensa per il salotto di casa, come il suo organo. Ma "
            "un mobile pieno di valvole accese non resta accordato da solo, e chi "
            "lo comprava doveva farlo rimettere a posto. Nel 1942 la produzione "
            "si ferma per un motivo che con la musica non c'entra niente: le "
            "valvole servono alla guerra. Dopo la guerra nessuno la riapre. In "
            "tre anni ne erano uscite 1.069, o 1.096 — anche su questo le fonti "
            "non vanno d'accordo. Oggi se ne conoscono meno di 200.",
        "avvertenza": "Le valvole scaldano e l'accordatura se ne va. Accendetelo mezz'ora prima, e mettete in conto di ritoccarla a met\u00e0 serata.",
        "foto": {
            "file": "assets/foto/novachord/principale.jpg",
            "autore": "Hollow Sun",
            "licenza": "CC BY 3.0",
            "fonte": "Wikimedia Commons",
        },
        "foto_extra": [
            {"file": "assets/foto/novachord/oscillatori.jpg",
             "autore": "Hollow Sun", "licenza": "CC BY 3.0", "fonte": "Wikimedia Commons",
             "didascalia": "I dodici oscillatori master"},
            {"file": "assets/foto/novachord/valvole.jpg",
             "autore": "Hollow Sun", "licenza": "CC BY 3.0", "fonte": "Wikimedia Commons",
             "didascalia": "Dentro il Novachord"},
            {"file": "assets/foto/novachord/divisori.jpg",
             "autore": "Hollow Sun", "licenza": "CC BY 3.0", "fonte": "Wikimedia Commons",
             "didascalia": "La fila dei divisori, valvola per valvola"},
        ],
        "fonti": [
            {"titolo": "\u00abNovachord\u00bb \u2014 Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Novachord", "data": "2026-09-23"},
            {"titolo": "\u00abThe Novachord\u00bb \u2014 120 Years of Electronic Music",
             "url": "https://120years.net/the-novachordl-hammond-c-n-williamsusa1939/", "data": "2026-09-23"},
            {"titolo": "\u00abNovachord: Hammond\u2019s Polyphonic Synthesizer\u00bb \u2014 GreatSynthesizers",
             "url": "https://greatsynthesizers.com/en/general/novachord-hammonds-polyphonic-synthesizer-from-1938/", "data": "2026-09-23"},
            {"titolo": "\u00abNovachord\u00bb \u2014 Soniccouture (scheda storica e colonne sonore)",
             "url": "https://www.soniccouture.com/en/products/24-vintage/g21-novachord/", "data": "2026-09-23"},
        ],
        "hashtags": ["#novachord", "#hammond", "#1939", "#sintetizzatore", "#valvole"],
        "reel_battute": [
            ("ELETTROFONI · N. 046", "Dentro «Via col vento» c'è un sintetizzatore del 1939."),
            ("CHICAGO, 1939", "È l'Hammond Novachord: 72 tasti, e suonano tutti insieme."),
            ("MOBILE DI NOCE", "La Hammond lo pensa per il salotto di casa. Pesa 230 chili."),
            ("1942", "Nel 1942 la produzione si ferma: le valvole servono alla guerra."),
            ("IN 3 ANNI", "Ne erano usciti 1.069, o 1.096. Oggi se ne conoscono meno di 200."),
        ],
        "reel_cta": "Mandalo a chi sa a memoria «Via col vento»",
        "verificata": True,
    },
    # ---------------------------------------------------------------- 47
    {
        "slug": "clavinet",
        "numero": 47,
        "serie": "GLI ELETTROMECCANICI",
        "strumento": "Hohner Clavinet D6",
        "anno": "1971",
        "luogo": "Trossingen, Germania",
        "costruttore": "Hohner",
        "specifiche": [
            ("MODELLO D6", "1971"),
            ("CORDE", "60, con martelletti"),
            ("TASTI", "60 (fa1-mi6)"),
            ("ESEMPLARI", "~38.000"),
        ],
        "gancio": "Sessanta corde pizzicate contro un'incudine. Da qui esce tutto il funky degli anni Settanta",
        "sottotitolo": "Ernst Zacharias voleva rifare un clavicordo. Gli \u00e8 venuta fuori la tastiera pi\u00f9 ritmica mai costruita.",
        "la_macchina": "Sotto i tasti c'è un'arpa di metallo con 60 corde d'acciaio in "
            "diagonale. Premi un tasto e un tampone di gomma schiaccia la corda "
            "contro un'incudine metallica: la corda si divide in due, la parte "
            "che vibra passa davanti a due pickup magnetici, l'altra resta muta. "
            "Finché tieni il tasto la corda suona; appena lo molli una treccia di "
            "filato la smorza di colpo. Non c'è nessuna cassa. Il suono esiste "
            "solo dopo l'amplificatore, e sei interruttori a bilanciere scelgono "
            "il timbro e i pickup.",
        "inventore_nome": "Ernst Zacharias",
        "inventore": "Zacharias nasce nel 1924 a Neum\u00fcnster, studia ingegneria elettrica ed entra alla Hohner nel 1954. Prima del Clavinet aveva gi\u00e0 fatto il Cembalet e il Pianet, due tastiere a lamelle. Il primo prototipo, il Claviphon, \u00e8 del 1961 e nasce per rifare un clavicordo in versione moderna. Il problema era che Zacharias suonava pi\u00f9 forte di quanto il meccanismo reggesse: mise l'incudine fissa sotto la corda, e da quel cambio venne fuori uno strumento che il clavicordo non lo imita affatto.",
        "come_funziona": "È una chitarra elettrica con la tastiera. La corda non viene "
            "pizzicata ma schiacciata contro l'incudine, quindi il punto in cui "
            "si accorcia è sempre lo stesso e l'attacco è secco uguale a ogni "
            "nota. I pickup sono due, come su una chitarra, e con gli "
            "interruttori si sceglie quale usare e con che fase. Invertendone uno "
            "certe frequenze si annullano e il suono si assottiglia. La dinamica "
            "c'è tutta, perché il volume dipende solo da quanto forte batti il "
            "tasto.",
        "richiami": [
            # «Martelletto» era il termine del Rhodes, non del Clavinet:
            # qui il tasto non batte, schiaccia. La legenda diceva una
            # cosa e il testo accanto ne diceva un'altra.
            ("FIG. 1", "60 corde, tampone e incudine"),
            ("FIG. 2", "Due pickup, fase invertibile"),
            ("FIG. 3", "Smorzatore di filato"),
        ],
        "chi_lusata": [
            {"artista": "Stevie Wonder", "nota": "\u00abSuperstition\u00bb (1972), otto piste di Clavinet sovrapposte", "ig": None},
            {"artista": "Herbie Hancock", "nota": "Tutto \u00abHead Hunters\u00bb (1973) sta in piedi su questo timbro", "ig": "herbiehancock"},
            {"artista": "Billy Preston", "nota": "\u00abOuta-Space\u00bb (1972), dove il Clavinet fa da solista", "ig": None},
            {"artista": "Bob Marley", "nota": "\u00abCould You Be Loved\u00bb (1980): lo stesso strumento, met\u00e0 velocit\u00e0", "ig": "bobmarley"},
        ],
        "menzioni_extra": [],
        "da_ascoltare": {"brano": "Superstition", "artista": "Stevie Wonder", "anno": "1972",
                         "cosa": "Togliete mentalmente batteria e fiati: quello che resta \u00e8 tutto Clavinet, registrato pi\u00f9 volte e impilato."},
        "aneddoto": "Il disco che ha reso famoso il Clavinet non \u00e8 suonato col Clavinet famoso. \u00abSuperstition\u00bb esce nel 1972, quando il D6 \u00e8 gi\u00e0 in commercio da un anno, ma Stevie Wonder lo registr\u00f2 su un modello C, pi\u00f9 vecchio. Il D6 \u00e8 diventato lo standard dopo, e oggi chi cerca \u00abquel suono\u00bb compra quello. In vent'anni la Hohner ne ha fatti circa 38.000, contro i 250.000 Rhodes dello stesso periodo. Alla chiusura, nel 1982, l'attrezzatura per costruirli \u00e8 stata distrutta.",
        "avvertenza": "La corda suona finch\u00e9 tenete gi\u00f9 il tasto e tace appena lo mollate. Il ritmo non lo fa il pezzo: lo fanno le vostre dita che si staccano.",
        "foto": {
            "file": "assets/foto/clavinet/targa.jpg",
            "posizione": "center 25%",
            "autore": "Marc Wathieu",
            "licenza": "CC BY 2.0",
            "fonte": "Wikimedia Commons",
        },
        # LEZIONE IMPARATA (23/09/2026): la prima foto della 2 era il
        # Clavinet aperto sopra un Rhodes. Vera, e la didascalia lo diceva,
        # ma nella banda la scritta piu' leggibile era «Rhodes»: su una
        # scheda che parla di un'altra macchina l'occhio legge il marchio
        # sbagliato. Buttata. E la foto del museo prometteva «i martelletti
        # e la targa»: nella foto intera ci sono tutti e due, ai due
        # estremi, e la banda ne mostrava solo i fili in mezzo. La
        # didascalia si scrive su quello che entra nel RITAGLIO, non su
        # quello che c'e' nel file.
        "foto_extra": [
            {"file": "assets/foto/clavinet/pannello.jpg",
             "posizione": "center 36%",
             "autore": "Henry Zbyszynski", "licenza": "CC BY 2.0", "fonte": "Wikimedia Commons",
             "didascalia": "I bilancieri del timbro, qui su un E7"},
            {"file": "assets/foto/clavinet/museo.jpg",
             "posizione": "center bottom",
             "autore": "guiltyx", "licenza": "CC BY 2.0", "fonte": "Wikimedia Commons",
             "didascalia": "Le leve dei tasti, viste da dentro il mobile"},
        ],
        "fonti": [
            {"titolo": "\u00abClavinet\u00bb \u2014 Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Clavinet", "data": "2026-09-23"},
            {"titolo": "\u00abErnst Zacharias & The Hohner Clavinet\u00bb \u2014 Sound On Sound",
             "url": "https://www.soundonsound.com/people/ernst-zacharias-hohner-clavinet", "data": "2026-09-23"},
            {"titolo": "\u00abThe Clavinet Chronicles\u00bb \u2014 Reverb News (sul modello usato in \u00abSuperstition\u00bb)",
             "url": "https://reverb.com/news/history-of-the-clavinet", "data": "2026-09-23"},
        ],
        "hashtags": ["#clavinet", "#hohner", "#funk", "#steviewonder", "#anni70"],
        "reel_battute": [
            ("ELETTROFONI · N. 047", "«Superstition» non è suonata sul Clavinet che cercate."),
            ("1961 · ERNST ZACHARIAS", "Alla Hohner, Ernst Zacharias vuole rifare un clavicordo moderno."),
            ("L'INCUDINE", "Zacharias suona troppo forte per la meccanica, e ci mette un'incudine."),
            ("TROSSINGEN, 1971", "Esce il Clavinet D6. Oggi chi cerca quel suono compra quello."),
            ("1972", "Ma Stevie Wonder incide «Superstition» su un modello C, più vecchio."),
        ],
        "reel_cta": "Mandalo a chi ha comprato un Clavinet D6",
        "verificata": True,
    },
    # ---------------------------------------------------------------- 48
    {
        "slug": "arpodyssey",
        "numero": 48,
        "serie": "I SINTETIZZATORI",
        "strumento": "ARP Odyssey",
        "anno": "1972",
        "luogo": "Lexington, Massachusetts",
        "costruttore": "ARP Instruments",
        "specifiche": [
            ("ANNO", "1972"),
            ("COSTRUTTORE", "ARP Instruments"),
            ("VOCI", "2 (duofonico)"),
            ("CHIUSO", "1981"),
        ],
        "gancio": "Non è monofonico come un Minimoog né polifonico come un Prophet: suona due note, né una né tante",
        "sottotitolo": "Il synth con cui ARP arrivò a superare Moog nelle vendite, e tre pastiglie a pressione al posto della rotella del pitch.",
        "la_macchina": "Il Minimoog suona una nota alla volta, il Prophet-5 ne suona cinque insieme: l'Odyssey sta in mezzo, duofonico, due note e basta. Sopra la tastiera non c'è la solita rotella ma tre pastiglie sensibili alla pressione del dito, una per piegare la nota in giù, una per il vibrato, una per piegarla in su. ARP lo produce dal 1972 al 1981, in tre versioni diverse di pannello e filtro. A me, del duofonico, piace proprio il limite — due note ti costringono a scegliere cosa suonare, non tutto insieme.",
        "inventore_nome": "David Friend e Alan R. Pearlman",
        "inventore": "Alan Robert Pearlman fonda ARP Instruments nel 1969 a Lexington, Massachusetts, con 100.000 dollari propri e altrettanti da investitori esterni. A progettare l'Odyssey nel 1972 è David Friend, ingegnere e cofondatore dell'azienda insieme a lui. ARP lo produce in tre versioni, fino al fallimento della società nel maggio 1981.",
        "come_funziona": "Due oscillatori per voce, sintesi sottrattiva, e un filtro che cambia con le versioni: 12 dB per ottava sul primo modello «black face», 24 dB in stile Moog sui modelli successivi, fino al filtro proprietario ARP da 24 dB sull'ultimo «arancione». Il duofonico funziona così — se premete due tasti, ogni oscillatore prende una nota diversa, ma se ne premete tre la terza nota viene ignorata. Bisogna suonarlo sapendo questo limite, non scoprirlo sul palco.",
        "richiami": [
            ("FIG. 1", "2 oscillatori, duofonico"),
            ("FIG. 2", "3 pastiglie a pressione"),
            ("FIG. 3", "Filtro 12 o 24 dB a seconda del modello"),
        ],
        "chi_lusata": [
            {"artista": "Herbie Hancock", "nota": "Suona l'Odyssey su «Head Hunters» (1973); sul basso esatto di «Chameleon» le fonti non concordano, Odyssey o Minimoog", "ig": "herbiehancock"},
            {"artista": "Kraftwerk", "nota": "Un Odyssey «white face» nella strumentazione di «Autobahn» (1974)", "ig": "kraftwerkofficial"},
        ],
        "menzioni_extra": [
            {"ig": "arpsynthesizer",
             "riga": "Il marchio, oggi di Korg, lo trovate ancora attivo da @arpsynthesizer."},
        ],
        "aneddoto": "A metà anni Settanta ARP supera Moog Music per quota di mercato: il 40% di un giro d'affari da 25 milioni di dollari, con un fatturato che nel 1977 tocca i 7 milioni. Poi il mercato cambia, arrivano synth più economici e più semplici da usare, e ARP non riesce a tenere il passo. Il 13 maggio 1981 l'azienda dichiara fallimento, otto anni dopo aver messo in vendita lo strumento che l'aveva fatta volare.",
        "avvertenza": "È duofonico, non monofonico: premete tre tasti e il terzo lo ignora. Non è un difetto del vostro esemplare, è come è fatto.",
        "da_ascoltare": {"brano": "Chameleon", "artista": "Herbie Hancock",
                          "anno": "1973",
                          "cosa": "Il basso che apre il pezzo, due oscillatori scordati apposta: il dubbio sul synth è nella scheda qui sopra."},
        "foto": {
            "file": "assets/foto/arpodyssey/principale.jpg",
            "autore": "Alison Cassidy",
            "licenza": "CC BY-SA 4.0",
            "fonte": "Wikimedia Commons",
        },
        "foto_extra": [
            {"file": "assets/foto/arpodyssey/due_versioni.jpg",
             "posizione": "center 30%",
             "autore": "Neil Voss", "licenza": "CC BY-SA 2.0", "fonte": "Wikimedia Commons",
             "didascalia": "Un altro esemplare, con un pannello diverso: ARP ne fece tre versioni"},
        ],
        "fonti": [
            {"titolo": "«ARP Odyssey» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/ARP_Odyssey", "data": "2026-09-18"},
            {"titolo": "«ARP Odyssey» — Vintage Synth Explorer",
             "url": "https://www.vintagesynth.com/arp/odyssey-1", "data": "2026-09-18"},
            {"titolo": "«ARP Instruments» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/ARP_Instruments", "data": "2026-09-18"},
            {"titolo": "«The Iconic Sounds Of Synthesis: Herbie Hancock's Chameleon Bassline» — Synthtopia",
             "url": "https://www.synthtopia.com/content/2015/04/21/the-iconic-sounds-of-synthesis-herbie-hancocks-chameleon-bassline/", "data": "2026-09-18"},
            {"titolo": "«Gear Rundown: Kraftwerk's Autobahn» — Mixdown Mag",
             "url": "https://mixdownmag.com.au/features/gear-rundown-kraftwerk-autobahn/", "data": "2026-09-18"},
            {"titolo": "«ARP (@arpsynthesizer)» — Instagram, account ufficiale ARP/Korg",
             "url": "https://www.instagram.com/arpsynthesizer/", "data": "2026-09-25"},
        ],
        "hashtags": ["#arpodyssey", "#sintetizzatore", "#musicaelettronica", "#anni70", "#synth"],
        "reel_battute": [
            ("ELETTROFONI · N. 048", "Con questo synth ARP vendette più di Moog. Non bastò."),
            ("LEXINGTON, 1969", "Alan R. Pearlman fonda ARP mettendoci 100.000 dollari suoi."),
            ("1972 · DAVID FRIEND", "David Friend progetta l'ARP Odyssey: suona 2 note, né una né tante."),
            ("1973-1974", "Herbie Hancock lo suona su «Head Hunters», i Kraftwerk su «Autobahn»."),
            ("13 MAGGIO 1981", "Poi arrivano synth più economici, e ARP dichiara fallimento."),
        ],
        "reel_cta": "Mandalo a chi giura solo sul Minimoog",
        # Registrazione della macchina vera (17/10/2026, regola del proprietario:
        # il suono vero in ogni uscita). Licenza verificata sulla pagina;
        # estratto 1:30-2:10 di un'improvvisazione di 11 minuti; la pagina: «using a 1972 ARP Odyssey synthesizer».
        "reel_audio": {
            "file": "assets/audio/arpodyssey/registrazione.mp3", "inizio": 0,
            "autore": "Jeff Archer", "licenza": "CC BY 3.0",
            "fonte": "archive.org",
            "url": "https://archive.org/details/ARPOdysseyImprovSundayNov.202016",
            "cosa": "un ARP Odyssey del 1972: un'improvvisazione dal vivo con un delay stereo",
        },
        "verificata": True,
    },
    # ---------------------------------------------------------------- 49
    {
        "slug": "phase90",
        "numero": 49,
        "serie": "GLI EFFETTI",
        "strumento": "MXR Phase 90",
        "anno": "1974",
        "luogo": "Rochester, New York",
        "costruttore": "MXR Innovations",
        "specifiche": [
            ("ANNO", "1974"),
            ("COSTRUTTORE", "MXR Innovations"),
            ("COMANDI", "1 manopola: Speed"),
            ("CIRCUITO", "4 stadi in cascata"),
        ],
        "gancio": "Una scatola arancione con una sola manopola: il primo pedale che la MXR abbia mai venduto",
        "sottotitolo": "Un phaser a quattro stadi in una scatola arancione: il primo pedale MXR, con una sola manopola per tutto il controllo.",
        "la_macchina": (
            "È un pedale phaser: sposta nel tempo una copia del segnale e "
            "la rimescola con l'originale, creando due tacche nello "
            "spettro che si spostano avanti e indietro, il suono che sale "
            "e scende come un respiro. C'è un solo comando, la manopola "
            "Speed, che decide quanto in fretta. La scatola è arancione, "
            "il logo nelle prime versioni è scritto a mano, lo chiamano "
            "'script logo', e nel 1977 diventa uno stampatello a blocchi. "
            "È il primo pedale che l'azienda vende, e per anni tiene in "
            "piedi il resto del catalogo."
        ),
        "inventore_nome": "Keith Barr",
        "inventore": (
            "Keith Barr è un tecnico quasi autodidatta di Rochester, New "
            "York. Le fonti non concordano sull'anno: la Columbian, nel "
            "necrologio del 2010, scrive che fonda MXR Innovations nel "
            "1973 insieme a Michael Laiacona e Terry Sherwood; Wikipedia "
            "mette il 1972, con Sherwood soltanto, e l'atto di "
            "incorporazione porta la data 1974, lo stesso anno in cui "
            "esce il Phase 90. Le prime schede dei pedali le incide lui "
            "stesso, con la scritta «hand built by guitarists». Barr "
            "muore nel 2010, a 60 anni."
        ),
        "come_funziona": (
            "Il segnale passa per quattro stadi che lo sfasano di 90 "
            "gradi ciascuno: in coppia creano due tacche nello spettro, "
            "punti dove certe frequenze quasi spariscono. Un piccolo "
            "oscillatore a bassa frequenza sposta quelle tacche avanti e "
            "indietro, usando un transistor a effetto di campo come "
            "resistenza variabile, non un potenziometro motorizzato ma "
            "un componente che cambia valore da solo con la tensione. "
            "Mescolato al segnale diretto, il risultato è quel suono che "
            "ondeggia. La manopola Speed regola solo la velocità: niente "
            "altro da girare."
        ),
        "richiami": [
            ("FIG. 1", "4 stadi di sfasamento"),
            ("FIG. 2", "Manopola Speed, unico comando"),
            ("FIG. 3", "Logo a mano, poi a blocchi dal 1977"),
        ],
        "chi_lusata": [
            {"artista": "Eddie Van Halen", "nota": "Lo sentì usare da Robin Trower a metà anni '70 e lo mise nell'assolo di «Eruption», 1978", "ig": "vanhalen"},
            {"artista": "David Gilmour (Pink Floyd)", "nota": "Lo usa dal vivo nel tour di Dark Side of the Moon, 1974-75, e nelle registrazioni di Wish You Were Here", "ig": "pinkfloyd"},
        ],
        "menzioni_extra": [],
        "da_ascoltare": {"brano": "Eruption", "artista": "Van Halen", "anno": "1978",
                         "cosa": "Un minuto e 42 di assolo da solo: ascoltate come il phaser resta acceso sotto il tapping senza mai coprirlo."},
        "aneddoto": (
            "Nel 1984 la MXR chiude, i debiti sono troppi. Tre anni dopo "
            "Jim Dunlop compra il marchio e rimette in produzione il "
            "Phase 90 quasi tale e quale, stessa scatola arancione, "
            "stessa manopola sola. La differenza vera è dentro, non "
            "fuori: le prime versioni, col logo scritto a mano, montano "
            "una resistenza da 24 kiloohm diversa da quella delle "
            "versioni a blocchi del '77, e il suono cambia, più morbido "
            "nel primo caso, più deciso nel secondo. A me piace di più il "
            "logo a mano, quello delle origini, la versione che tutti "
            "citano quando dicono «il vero Phase 90»."
        ),
        "avvertenza": "Il campo di oscillazione lo fissa un trimmer interno, non la manopola: se un esemplare suona storto, il problema è lì dentro, non sul pannello.",
        "foto": {
            "file": "assets/foto/phase90/principale.jpg",
            "autore": "Roadside Guitars",
            "licenza": "CC BY-SA 2.0",
            "fonte": "Wikimedia Commons",
        },
        "foto_extra": [
            {"file": "assets/foto/phase90/evh.jpg",
             "autore": "Art Bromage", "licenza": "CC BY-SA 2.0", "fonte": "Wikimedia Commons",
             "didascalia": "La riedizione a firma Eddie Van Halen"},
        ],
        "fonti": [
            {"titolo": "«MXR Phase 90» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/MXR_Phase_90", "data": "2026-09-15"},
            {"titolo": "«MXR» — Wikipedia (EN), fondazione dell'azienda",
             "url": "https://en.wikipedia.org/wiki/MXR", "data": "2026-09-15"},
            {"titolo": "«Audio inventor Keith Barr, 60, dies in Hockinson» — The Columbian",
             "url": "https://www.columbian.com/news/2010/sep/05/audio-inventor-keith-barr-60-dies-in-hockinson/", "data": "2026-09-15"},
            {"titolo": "«Robert Keeley Dark Side review» — Gilmourish.com, uso live di David Gilmour",
             "url": "https://www.gilmourish.com/?p=7285", "data": "2026-09-15"},
            {"titolo": "«MXR Phase 90 Analysis» — ElectroSmash, schema del circuito",
             "url": "https://electrosmash.mas-effects.com/mxr-phase90.html", "data": "2026-09-15"},
        ],
        "hashtags": ["#mxrphase90", "#pedaleeffetti", "#phaser", "#eddievanhalen", "#anni70"],
        "reel_battute": [
            ("ELETTROFONI · N. 049", "Una manopola sola. E Van Halen lo mise in «Eruption»."),
            ("ROCHESTER, 1974", "Il Phase 90 è il primo pedale che la MXR mette in vendita."),
            ("KEITH BARR", "Le prime schede le incide lui. C'è scritto «hand built by guitarists»."),
            ("METÀ ANNI '70", "Eddie Van Halen lo sente usare da Robin Trower."),
            ("1978", "In «Eruption» resta acceso sotto il tapping e non lo copre mai."),
        ],
        "reel_cta": "Mandalo a chi ha provato a rifare «Eruption»",
        "verificata": True,
    },
    # ---------------------------------------------------------------- 50
    {
        "slug": "crumards2",
        "numero": 50,
        "serie": "I SINTETIZZATORI",
        "strumento": "Crumar DS-2",
        "anno": "1978",
        "luogo": "Castelfidardo, Italia",
        "costruttore": "Crumar",
        "specifiche": [
            ("ANNO", "1978"),
            ("ORIGINE", "Castelfidardo"),
            ("OSCILLATORI", "2 DCO digitali"),
            ("COSTRUITI", "Circa 700"),
        ],
        "gancio": "Il primo sintetizzatore vero costruito nella capitale italiana della fisarmonica",
        "sottotitolo": "Un ibrido analogico-digitale del 1978, tra oscillatori a gradini e una sezione d'archi da 44 note.",
        "la_macchina": "Il DS-2 è un ibrido: sezione sintetizzatore monofonica con due DCO — oscillatori controllati digitalmente — accoppiata a una sezione poli/archi parafonica da 44 note, filtro passa-basso a 4 poli dal timbro alla Moog e due LFO, uno dei quali genera un'onda letteralmente 'a gradini'. Le due sezioni condividono la stessa modulazione. Ne furono costruiti circa 700 esemplari: oggi trovarne uno ancora funzionante è raro.",
        "inventore_nome": "Mario Crucianelli",
        "inventore": "Mario Crucianelli lascia la Elka di famiglia — fondata dal fratello Piero — dopo una diatriba familiare, e nel 1971 apre la Crumar a Castelfidardo insieme al socio F. Marchetti: il nome fonde i due cognomi. Castelfidardo è dal 1864 la capitale italiana della fisarmonica, da Paolo Soprani in poi. Nel 1978 la Crumar mette in produzione il DS-2, il suo primo sintetizzatore vero e proprio, dopo anni di organi e archi elettronici.",
        "come_funziona": "Le due DCO risolvono il problema classico degli oscillatori analogici — la deriva d'accordatura — ma generano un'onda digitale scalettata, non una curva continua: è quella scalettatura a dare al DS-2 il timbro ruvido e spigoloso. La sezione poli ottiene i denti di sega dividendo onde quadre e filtrandole in passa-alto. Risultato: un suono a metà tra il digitale e l'analogico, che non assomiglia bene a nessuno dei due.",
        "richiami": [
            ("FIG. 1", "2 DCO: oscillatori a gradini"),
            ("FIG. 2", "Poli/archi parafonico, 44 note"),
            ("FIG. 3", "Filtro 4 poli, timbro alla Moog"),
        ],
        "chi_lusata": [
            {"artista": "Sun Ra", "nota": "Lo suona dal vivo con l'Arkestra, uno dei tanti sintetizzatori italiani nella sua collezione", "ig": None},
            {"artista": "Legowelt (Danny Wolfers)", "nota": "Lo tiene in studio e lo mostra in un tour girato per Future Music Magazine", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": "Crumar chiude la produzione di strumenti nel 1986: la fisarmonica aveva reso Castelfidardo la capitale italiana della tastiera, ma il synth digitale giapponese la spiazza in meno di dieci anni. Il DS-2 resta una nota a margine, meno di 700 esemplari, finché nel 2026 Cherry Audio lo rimette in commercio come plugin — e perfino chi lo recensisce ammette di non averne mai suonato uno vero.",
        "avvertenza": "Le due DCO generano onde letteralmente a gradini, non curve: è la loro natura digitale, non un guasto di accordatura.",
        "foto": {
            "file": "assets/foto/crumards2/principale.jpg",
            "autore": "PerfectCircuit",
            "licenza": "CC0",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "Crumar DS-2 — Vintage Synth Explorer",
             "url": "https://www.vintagesynth.com/crumar/ds-2", "data": "2026-09-04"},
            {"titolo": "Say hello to the CRUMAR DS2 synthesizer, made in Italy — Legowelt.org",
             "url": "https://legowelt.org/463-2/", "data": "2026-09-04"},
            {"titolo": "Crumar — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Crumar", "data": "2026-09-04"},
            {"titolo": "Crucianelli / Elka — Crumar — Fetishguitars.com",
             "url": "https://www.fetishguitars.com/crucianelli/elka-crumar/", "data": "2026-09-04"},
            {"titolo": "Crumar DS-2 | Cherry Audio (pagina prodotto, ~700 esemplari costruiti)",
             "url": "https://cherryaudio.com/products/ds-2-synthesizer", "data": "2026-09-04"},
            {"titolo": "MATRIXSYNTH: Sun Ra Plays the Crumar DS-2 Synthesizer",
             "url": "https://www.matrixsynth.com/2023/03/sun-ra-plays-crumar-ds-2-synthesizer.html", "data": "2026-09-04"},
        ],
        "hashtags": ["#crumar", "#ds2", "#castelfidardo", "#sintetizzatore", "#musicaelettronica"],
        "reel_battute": [
            ("ELETTROFONI · N. 050", "Sun Ra suonava un synth della città delle fisarmoniche."),
            ("CASTELFIDARDO, 1971", "Mario Crucianelli litiga in famiglia, lascia la Elka e apre la Crumar."),
            ("1978", "Dopo anni di organi e archi, il primo synth vero: il Crumar DS-2."),
            ("2 OSCILLATORI DIGITALI", "Fanno onde a gradini, non curve. Per questo suona ruvido e spigoloso."),
            ("CIRCA 700 ESEMPLARI", "Ne escono circa 700. Sun Ra lo porta sul palco con l'Arkestra."),
        ],
        "reel_cta": "Mandalo a chi ha una fisarmonica in soffitta",
        "verificata": True,
    },
    # ---------------------------------------------------------------- 51
    {
        "slug": "buchla",
        "numero": 51,
        "serie": "I SINTETIZZATORI",
        "strumento": "Buchla 100 series (Music Box)",
        "anno": "1965",
        "luogo": "San Francisco, Stati Uniti",
        "costruttore": "Don Buchla",
        "specifiche": [
            ("ANNO", "1965"),
            ("ORIGINE", "San Francisco"),
            ("COMANDO", "Piastre capacitive"),
            ("MODULI", "Fino a 25"),
        ],
        "gancio": "Costruito per un centro di musica su nastro di San Francisco. Niente tastiera: solo piastre a contatto.",
        "sottotitolo": "Piastre capacitive, sequencer analogico e filtri voltage-controlled: nasce la sintesi «West Coast».",
        "la_macchina": "Il Buchla 100 series, o Music Box, è un sistema modulare senza tastiera: al posto dei tasti, piastre piatte a contatto capacitivo, ognuna accordabile a mano con un potenziometro — alcune ne portano due file, per due note diverse sotto lo stesso dito. Fino a 25 moduli in una cassa di legno: oscillatori e filtri voltage-controlled, un sequencer analogico, un generatore di rumore bianco. Fu installato nel 1965 al San Francisco Tape Music Center, il centro che Subotnick, Sender e Oliveros avevano fondato per lavorare sul nastro magnetico.",
        "inventore_nome": "Don Buchla",
        "inventore": "Don Buchla, fisico di formazione a Berkeley, comincia a montare i primi circuiti a controllo di tensione nel 1963. Nel 1965 consegna il sistema a Morton Subotnick e Ramon Sender, che lo avevano commissionato per il Tape Music Center: loro chiedono uno strumento per la sintesi dal vivo, lui rifiuta di copiare il pianoforte. Da qui nasce una scuola di progettazione — poi chiamata «West Coast» — diversa da quella di Robert Moog sulla costa opposta: niente tastiera, sequencer e casualità governata al posto delle note fisse.",
        "come_funziona": "Ogni piastra, toccata, manda una tensione di controllo: decide l'altezza, non fa suonare una nota fissata a priori come un tasto di pianoforte. La stessa tensione può arrivare da un sequencer analogico, o da un generatore di valori casuali. Quella tensione pilota oscillatori e filtri voltage-controlled, fino a 24 dB per ottava: il risultato è un suono che si programma per processi, non per note scritte una a una.",
        "richiami": [
            ("FIG. 1", "Piastre capacitive"),
            ("FIG. 2", "Sequencer analogico"),
            ("FIG. 3", "Filtri voltage-controlled"),
        ],
        "chi_lusata": [
            {"artista": "Morton Subotnick", "nota": "Compra il sistema nel 1966 e ci compone «Silver Apples of the Moon» (1967)", "ig": None},
            {"artista": "Pauline Oliveros", "nota": "Lo usa nel 1966 per «Beautiful Soop», da direttrice del centro a Mills College", "ig": None},
            {"artista": "Warner Jepson", "nota": "Nel 1969 ci registra «Buchla Christmas», canti natalizi per il MoMA di San Francisco", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": "Nel 1966 Subotnick compra il sistema e lo porta a New York, in uno studio di Bleecker Street: ci compone «Silver Apples of the Moon», primo disco elettronico commissionato da un'etichetta discografica, la Nonesuch. Lo stesso anno, a Oakland, Pauline Oliveros lo usa per «Beautiful Soop». Nel 1969 Warner Jepson lo trasforma in un disco di canti di Natale, «Buchla Christmas», registrato ai Mills College Electronic Music Studios per la festa di Natale del San Francisco Museum of Modern Art.",
        "avvertenza": "Ogni piastra si accorda a mano con un potenziometro: due file danno due note diverse sotto lo stesso dito.",
        "da_ascoltare": {
            "brano": "Silver Apples of the Moon",
            "artista": "Morton Subotnick",
            "anno": "1967",
            "cosa": "Primo disco elettronico commissionato da un'etichetta discografica, la Nonesuch: ogni suono nasce dal Buchla comprato da Subotnick per il suo studio newyorkese.",
        },
        "foto": {
            "file": "assets/foto/buchla/principale.jpg",
            "autore": "Ethan Hein",
            "licenza": "CC BY 2.0",
            "posizione": "85% 100%",
            "fonte": "Wikimedia Commons",
        },
        "fonti": [
            {"titolo": "«Don Buchla» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Don_Buchla", "data": "2026-09-04"},
            {"titolo": "«The San Francisco Tape Music Center Was an Early Home to the Avant-Garde» — Bandcamp Daily",
             "url": "https://daily.bandcamp.com/features/san-francisco-tape-music-center-history", "data": "2026-09-04"},
            {"titolo": "«Silver Apples of the Moon (Morton Subotnick album)» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Silver_Apples_of_the_Moon_(Morton_Subotnick_album)", "data": "2026-09-04"},
            {"titolo": "Note di copertina per «Alien Bog / Beautiful Soop» di Pauline Oliveros — DRAM (Discover Recordings, American Made)",
             "url": "https://www.dramonline.org/albums/pauline-oliveros-alien-bog-beautiful-soop/notes", "data": "2026-09-04"},
            {"titolo": "«Warner Jepson» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Warner_Jepson", "data": "2026-09-04"},
            {"titolo": "«Buchla 100 Series» — Vintage Synth Explorer",
             "url": "https://www.vintagesynth.com/buchla/100-series", "data": "2026-09-04"},
        ],
        "hashtags": ["#buchla", "#donbuchla", "#sintetizzatore", "#storiadellamusica", "#musicaelettronica"],
        "reel_battute": [
            ("ELETTROFONI · N. 051", "Don Buchla si rifiutò di copiare il pianoforte."),
            ("SAN FRANCISCO, 1965", "Lo consegna a Subotnick e Sender, che volevano la sintesi dal vivo."),
            ("NIENTE TASTI", "Al posto dei tasti, il Buchla ha piastre a contatto, accordate a mano."),
            ("NEW YORK, 1967", "Subotnick ci compone «Silver Apples of the Moon», per la Nonesuch."),
            ("1969", "E Warner Jepson ci registra dei canti di Natale: «Buchla Christmas»."),
        ],
        "reel_cta": "Mandalo a chi ha un modulare pieno di cavi",
        "verificata": True,
    },
    {
        "slug": "wurlitzer200a",
        "numero": 52,
        "serie": "GLI ELETTROMECCANICI",
        "strumento": "Wurlitzer 200A",
        "anno": "1968",
        "luogo": "DeKalb, Illinois",
        "costruttore": "Wurlitzer",
        "specifiche": [
            ("MODELLO 200", "1968"),
            ("MODELLO 200A", "1974"),
            ("TASTI", "64"),
            ("PESO", "25 kg senza gambe"),
        ],
        "gancio": "Una lamella d'acciaio da 6 millimetri, colpita da un martelletto. Se la picchi forte, abbaia",
        "sottotitolo": "Il piano elettrico che non ha corde e nemmeno i rebbi del Rhodes: dentro ha delle linguette, come un'armonica a bocca.",
        "la_macchina": (
            "Sembra una valigia nera su quattro gambe di metallo, con due manopole "
            "sole e gli altoparlanti nel coperchio. Dentro non ci sono corde: ogni "
            "tasto alza un martelletto che colpisce una lamella d'acciaio piatta, "
            "lunga qualche centimetro. I tasti sono 64 e pesa 25 chili senza le "
            "gambe, che è poi il motivo per cui esiste. Sul pannello c'è una "
            "manopola scritta «vibrato» che vibrato non fa: muove il volume, non "
            "l'altezza, quindi è un tremolo. L'etichetta è sbagliata da sempre e "
            "nessuno l'ha mai corretta."
        ),
        "inventore_nome": "Benjamin Miessner",
        "inventore": (
            "Miessner era un ingegnere radio, e nel 1932 presenta un pianoforte a "
            "coda con dentro un pickup elettrostatico: le corde ci sono ancora, "
            "l'amplificatore le raccoglie. Poi negli anni Cinquanta gli viene "
            "l'idea che cambia tutto. Via le corde, al loro posto delle lamelle "
            "d'acciaio: una lamella non tira come una corda, quindi non serve un "
            "telaio che regga le tonnellate, e lo strumento si può fare piccolo. "
            "La Wurlitzer costruisce il primo nel 1954 e va avanti fino al 1983."
        ),
        "come_funziona": (
            "La lamella sta a un capello di distanza da una placchetta di metallo, "
            "e fra le due c'è una tensione di 170 volt. Quando la lamella vibra, la "
            "distanza cambia, e cambiando cambia anche la carica: quella variazione "
            "è il segnale. Non è una bobina come sul Rhodes o sulla chitarra "
            "elettrica, è un condensatore che respira. Una cosa che a me nessuno "
            "aveva spiegato: il timbro sporco delle note basse non è un difetto "
            "dell'amplificatore, è la lamella che sotto un colpo forte si piega "
            "troppo e distorce da sola."
        ),
        "richiami": [
            ("FIG. 1", "64 lamelle d'acciaio, niente corde"),
            ("FIG. 2", "Pickup elettrostatico a 170 V"),
            ("FIG. 3", "Altoparlanti nel coperchio"),
        ],
        "chi_lusata": [
            {"artista": "Ray Charles", "nota": "«What'd I Say» (1959), su un modello 120 più vecchio", "ig": None},
            {"artista": "Joe Zawinul", "nota": "«Mercy, Mercy, Mercy» (1966), su un 140B", "ig": None},
            {"artista": "Supertramp", "nota": "«Dreamer» e «The Logical Song»: quasi tutto il loro suono", "ig": None},
            {"artista": "John Deacon", "nota": "«You're My Best Friend» dei Queen (1975), scritta su questo", "ig": None},
        ],
        "menzioni_extra": [],
        "da_ascoltare": {"brano": "You're My Best Friend", "artista": "Queen", "anno": "1975",
                         "cosa": "Le note basse dell'introduzione sono tutta lamella: ascoltate come si sporcano quando il tasto viene giù forte."},
        "aneddoto": (
            "John Deacon voleva scrivere qualcosa con un Wurlitzer, ma il "
            "pianista dei Queen era Freddie Mercury e Mercury non ne voleva "
            "sapere. Le sue parole: mi sono rifiutato di suonare quel coso, "
            "è metallico e orribile, perché usarlo quando hai un gran coda. "
            "Allora Deacon se lo porta a casa e impara a suonare da solo. "
            "Quello che gli esce mentre impara è «You're My Best Friend», che "
            "scrive per sua moglie Veronica. Dal vivo la suonavano con Mercury "
            "al pianoforte vero e Deacon al basso."
        ),
        "avvertenza": "Dentro ci sono 170 volt fra la lamella e la placchetta. Si accorda limando la lamella, e a strumento spento.",
        "foto": {
            "file": "assets/foto/wurlitzer200a/principale.jpg",
            "autore": "I99pema",
            "licenza": "CC BY-SA 4.0",
            "fonte": "Wikimedia Commons",
        },
        # Tre foto extra e non due: con due, la banda della tavola 4 ricade
        # su un ritaglio della copertina e quel ritaglio cadeva su un pezzo
        # di muro. Guardata la tavola, non il file.
        "foto_extra": [
            {"file": "assets/foto/wurlitzer200a/museo2.jpg",
             "posizione": "center 30%",
             "autore": "doryfour", "licenza": "CC BY-SA 2.0", "fonte": "Wikimedia Commons",
             "didascalia": "Due manopole sole, e gli altoparlanti dietro la griglia"},
            {"file": "assets/foto/wurlitzer200a/dettaglio.jpg",
             "autore": "I99pema", "licenza": "CC BY-SA 4.0", "fonte": "Wikimedia Commons",
             "didascalia": "Coperchio chiuso: è una valigia, e pesa 25 chili"},
            {"file": "assets/foto/wurlitzer200a/museo.jpg",
             "autore": "doryfour", "licenza": "CC BY-SA 2.0", "fonte": "Wikimedia Commons",
             "didascalia": "I 64 tasti, e il pedale che smorza"},
        ],
        "fonti": [
            {"titolo": "«Wurlitzer electronic piano» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Wurlitzer_electronic_piano", "data": "2026-09-29"},
            {"titolo": "«Benjamin Miessner» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Benjamin_Miessner", "data": "2026-09-29"},
            {"titolo": "«You're My Best Friend» — Wikipedia (EN), con le parole di Mercury e di Deacon",
             "url": "https://en.wikipedia.org/wiki/You%27re_My_Best_Friend", "data": "2026-09-29"},
            {"titolo": "«The Story Behind The Queen Song» — uDiscover Music",
             "url": "https://www.udiscovermusic.com/stories/queen-youre-my-best-friend-song/", "data": "2026-09-29"},
        ],
        "hashtags": ["#wurlitzer", "#pianoelettrico", "#queen", "#supertramp", "#anni70"],
        "reel_battute": [
            ("ELETTROFONI · N. 052", "Freddie Mercury non lo voleva: «metallico e orribile»."),
            ("25 KG SENZA GAMBE", "Il Wurlitzer non ha corde: dentro, martelletti e lamelle d'acciaio."),
            ("QUEEN", "John Deacon invece se lo porta a casa e impara a suonarlo da solo."),
            ("1975", "Mentre impara gli esce «You're My Best Friend». È per sua moglie."),
            ("SUL PALCO", "Dal vivo la suonano con Mercury al pianoforte vero e Deacon al basso."),
        ],
        "reel_cta": "Mandalo al tuo migliore amico",
        "reel_audio": {
            "file": "assets/audio/wurlitzer200a/registrazione.mp3", "inizio": 31,
            "autore": "Ritchie333", "licenza": "CC BY-SA 4.0",
            "fonte": "Wikimedia Commons",
            "url": "https://commons.wikimedia.org/wiki/File:Wurlitzer_EP200.mp3",
            "cosa": "un piano elettrico Wurlitzer della serie 200",
        },
        "verificata": True,
    },
    {
        "slug": "rhythmace",
        "numero": 53,
        "serie": "LE DRUM MACHINE",
        "strumento": "Ace Tone Rhythm Ace",
        "anno": "1967",
        "luogo": "Osaka, Giappone",
        "costruttore": "Ace Electronic Industries",
        "specifiche": [
            ("PRIMO MODELLO", "FR-1, 1967"),
            ("RITMI", "16 preselezionati"),
            ("CIRCUITO", "Matrice a diodi"),
            ("SUONI A MANO", "4 pulsanti"),
        ],
        "gancio": "Sedici ritmi in una scatola, nel 1967. È la nonna di tutte le Roland, e quasi nessuno sa come si chiama",
        "sottotitolo": "Ikutaro Kakehashi la costruisce cinque anni prima di fondare la Roland, e la vende con tre marchi diversi.",
        "la_macchina": (
            "Una cassetta di legno e plastica con dieci tasti color panna, una fila "
            "di nomi di ballo stampati sopra e quattro manopole. Si sceglie il "
            "ritmo premendo un tasto, si preme START e quello va avanti da solo "
            "finché non lo fermi. I suoni non sono registrati: cassa, rullante, "
            "piatto e legnetti escono da circuiti che imitano il colpo, e ci sono "
            "quattro pulsanti per suonarli a mano. Premendo due tasti di ritmo "
            "insieme i pattern si sovrappongono, e le combinazioni diventano più "
            "di cento."
        ),
        "inventore_nome": "Ikutaro Kakehashi",
        "inventore": (
            "Kakehashi ripara radio a Osaka e nel 1960 fonda la Ace Electronic "
            "Industries. Nel 1964 porta al NAMM la R1, una scatola a transistor "
            "che i ritmi non li aveva: li dovevi fare tu, a mano, e in America non "
            "la volle nessuno. Allora ci mette dentro una matrice a diodi che "
            "tiene in memoria i pattern, e nel 1967 esce la FR-1. Il brevetto lo "
            "deposita con un nome che dice tutto: «Automatic Rhythm Performance "
            "Device». Cinque anni dopo Kakehashi fonda la Roland."
        ),
        "come_funziona": (
            "Una matrice a diodi è una griglia di fili: da una parte i passi del "
            "tempo, dall'altra gli strumenti, e un diodo saldato in un incrocio "
            "vuol dire «qui suona la cassa». Il pattern non è scritto da nessuna "
            "parte, è la saldatura. Per questo i 16 ritmi sono 16 e non se ne "
            "possono aggiungere: cambiarli vorrebbe dire rifare il circuito. La "
            "programmazione, quella vera, arriva dieci anni dopo con la CR-78. "
            "Qui si sceglie soltanto, e va benissimo così."
        ),
        "richiami": [
            ("FIG. 1", "16 ritmi in una matrice a diodi"),
            ("FIG. 2", "4 suoni: cassa, rullante, piatto, legnetti"),
            ("FIG. 3", "Tre marchi, una sola macchina"),
        ],
        "chi_lusata": [
            {"artista": "La Hammond Organ Company", "nota": "La comprava da Ace Tone e la montava dentro i propri organi", "ig": "officialhammondorgan"},
            {"artista": "Chi la comprò come Multivox", "nota": "Negli Stati Uniti usciva col marchio della Peter Sorkin Music Company", "ig": None},
            {"artista": "Chi la comprò come Bentley", "nota": "In Gran Bretagna era la Bentley Rhythm Ace, e da lì il nome del gruppo", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": (
            "La macchina della foto dice «Rhythm Ace» in grande e «Multivox» "
            "accanto, ed è la stessa che in Inghilterra si chiamava Bentley. "
            "Kakehashi costruiva, gli altri mettevano il nome. Trent'anni dopo due "
            "ragazzi di Birmingham ne trovano una in un negozio dell'usato, gli "
            "piace la scritta e ci battezzano il gruppo: Bentley Rhythm Ace. Il "
            "nome di una drum machine giapponese venduta col marchio di un "
            "negozio di pianoforti inglese."
        ),
        "avvertenza": "I ritmi sono saldati, non programmati. Se ne volete uno che non c'è, l'unico modo è premere due tasti insieme.",
        "foto": {
            "file": "assets/foto/rhythmace/principale.jpg",
            "autore": "Alison Cassidy",
            "licenza": "CC BY-SA 4.0",
            "fonte": "Wikimedia Commons",
        },
        "foto_extra": [],
        "fonti": [
            {"titolo": "«Drum machine» — Wikipedia (EN), sezione Ace Tone",
             "url": "https://en.wikipedia.org/wiki/Drum_machine", "data": "2026-09-29"},
            {"titolo": "«Ikutaro Kakehashi» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Ikutaro_Kakehashi", "data": "2026-09-29"},
            {"titolo": "«The Rhythm Ace: Pioneering the Beat Revolution» — KR Sound",
             "url": "https://kr-sound.com/the-ace-tone-rhythm-ace-pioneering-the-beat-revolution/", "data": "2026-09-29"},
        ],
        "hashtags": ["#rhythmace", "#acetone", "#drummachine", "#roland", "#anni60"],
        "reel_battute": [
            ("ELETTROFONI · N. 053", "5 anni prima della Roland, il suo fondatore fece questa"),
            ("OSAKA, 1960", "Ikutaro Kakehashi ripara radio e fonda la Ace Electronic Industries."),
            ("NAMM, 1964", "Porta in America una scatola ritmica senza ritmi. Nessuno la vuole."),
            ("1967", "Ci salda dentro 16 ritmi. In Inghilterra è la Bentley Rhythm Ace."),
            ("30 ANNI DOPO", "Due ragazzi di Birmingham ne trovano una. Ci battezzano il gruppo."),
        ],
        "reel_cta": "Mandalo a chi giura solo sulle Roland",
        "verificata": True,
    },
    {
        "slug": "oberheim4voice",
        "numero": 54,
        "serie": "I SINTETIZZATORI",
        "strumento": "Oberheim Four Voice",
        "anno": "1975",
        "luogo": "Santa Monica, California",
        "costruttore": "Oberheim Electronics",
        "specifiche": [
            ("MODULO SEM", "1974"),
            ("QUATTRO VOCI", "1975"),
            ("TASTI", "49"),
            ("PREZZO", "4.295 $"),
        ],
        "gancio": "Quattro sintetizzatori monofonici in fila, e per la prima volta si può comprare un accordo",
        "sottotitolo": "Il primo polifonico in vendita a chiunque: quattro moduli SEM, otto oscillatori e una tastiera che smista le note.",
        "la_macchina": (
            "Dentro non c'è un sintetizzatore polifonico. Ci sono quattro "
            "sintetizzatori monofonici completi, uno accanto all'altro, ognuno "
            "con i suoi due oscillatori, il suo filtro e i suoi due inviluppi. "
            "La tastiera ha 49 tasti e un circuito che decide a quale dei quattro "
            "mandare la nota appena premuta. Per avere lo stesso timbro su tutte "
            "le voci bisogna regolare quattro pannelli identici a mano, manopola "
            "per manopola, finché non sono uguali. Costava 4.295 dollari, che nel "
            "1975 era un'automobile. A me quella fila di pannelli gemelli fa "
            "ancora impressione. È forza bruta, e ha funzionato."
        ),
        "inventore_nome": "Tom Oberheim",
        "inventore": (
            "Nel 1961 legge su una rivista di elettronica un articolo di Harald "
            "Bode: come si costruisce un modulatore ad anello che lavori sulle "
            "frequenze che si sentono. Se lo costruisce e lo usa nel gruppo dove "
            "suona. Poi glielo chiedono altri, e lo costruisce per loro; uno "
            "finisce nella colonna sonora de «L'altra faccia del pianeta delle "
            "scimmie», un altro va al trombettista Don Ellis. Nel 1969 apre la "
            "ditta e per anni campa di pedali. Diventa anche il primo rivenditore "
            "ARP della costa ovest e vende 2600 a Frank Zappa e a Leon Russell. "
            "Il SEM lo presenta nel maggio del 1974."
        ),
        "come_funziona": (
            "Il pezzo che conta non lo ha progettato lui. La tastiera a scansione "
            "la prende in licenza dalla E-mu di Dave Rossum, che l'aveva brevettata "
            "nel 1973: un circuito digitale guarda i tasti uno dopo l'altro, "
            "centinaia di volte al secondo, e quando ne trova uno abbassato "
            "assegna la nota al primo SEM libero. Tutto il resto, oscillatori e "
            "filtri, resta analogico. Provate a immaginarlo come un centralino "
            "telefonico con quattro linee. Se premete cinque tasti, il quinto non "
            "ha dove andare e la nota più vecchia se ne va."
        ),
        "richiami": [
            ("FIG. 1", "4 moduli SEM, uno per voce"),
            ("FIG. 2", "Tastiera a scansione, 49 tasti"),
            ("FIG. 3", "Programmer: 16 patch per voce"),
        ],
        "chi_lusata": [
            {"artista": "Vangelis", "nota": "ne teneva uno al Nemo Studios negli anni di «Spiral» (1977)", "ig": None},
            {"artista": "Herbie Hancock", "nota": "su «Monster» (1980) lavora con l'otto voci, cioè lo stesso in doppia misura", "ig": None},
            {"artista": "808 State", "nota": "il quattro voci esposto all'Horniman Museum di Londra era loro", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": (
            "Il prototipo numero 1 esiste ancora. Guardatelo da vicino: sui "
            "pannelli dei SEM ci sono etichette rosse coi puntini in rilievo, "
            "braille, perché quello strumento era di Stevie Wonder e le manopole "
            "doveva poterle ritrovare da solo. Sul pannello nero sopra i tasti c'è "
            "la firma di Tom Oberheim, fatta a pennarello argentato. Di tutte le "
            "fotografie che ho guardato per questa scheda è quella che mi ha fatto "
            "fermare. Non sembra un pezzo da museo, sembra un attrezzo che ha "
            "lavorato, con la carta adesiva ingiallita agli angoli."
        ),
        "avvertenza": "Quattro voci sono quattro accordature. Si accorda SEM per SEM, con la macchina già calda, o l'accordo non è un accordo.",
        "foto": {
            "file": "assets/foto/oberheim4voice/principale.jpg",
            "autore": "Robert Brook",
            "licenza": "CC BY 2.0",
            "fonte": "Wikimedia Commons",
        },
        # Tre foto extra: con meno, la banda della tavola 4 ricadrebbe su un
        # ritaglio della copertina, che qui è scura e sotto vetro.
        "foto_extra": [
            {"file": "assets/foto/oberheim4voice/prototipo.jpg",
             "autore": "Alison Cassidy", "licenza": "CC BY-SA 4.0", "fonte": "Wikimedia Commons",
             "didascalia": "Il prototipo numero 1: le etichette rosse sui pannelli sono in braille"},
            {"file": "assets/foto/oberheim4voice/sem.jpg",
             "autore": "Kevin Spencer", "licenza": "CC BY 2.0", "fonte": "Wikimedia Commons",
             "didascalia": "I moduli SEM da vicino: uno per voce, ognuno un synth completo"},
            {"file": "assets/foto/oberheim4voice/tastiera.jpg",
             "autore": "Kevin Spencer", "licenza": "CC BY 2.0", "fonte": "Wikimedia Commons",
             "didascalia": "Un otto voci a due manuali: lo stesso sistema, raddoppiato"},
        ],
        "fonti": [
            {"titolo": "«Oberheim Polyphonic Synthesizer» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Oberheim_Polyphonic_Synthesizer", "data": "2026-10-01"},
            {"titolo": "«Product History» — tomoberheim.com (sito del progettista)",
             "url": "https://www.tomoberheim.com/historical-products", "data": "2026-10-01"},
            {"titolo": "«Tom Oberheim» — Wikipedia (EN), su Bode, Don Ellis e la rivendita ARP",
             "url": "https://en.wikipedia.org/wiki/Tom_Oberheim", "data": "2026-10-01"},
            {"titolo": "«E-mu Systems» — Wikipedia (EN): tastiera a scansione brevettata nel 1973 e data in licenza a Oberheim",
             "url": "https://en.wikipedia.org/wiki/E-mu_Systems", "data": "2026-10-01"},
            {"titolo": "«Vangelis: Recording At Nemo Studios» — Sound On Sound (elenca l'Oberheim 4-Voice)",
             "url": "https://www.soundonsound.com/people/vangelis-recording-nemo-studios", "data": "2026-10-01"},
            {"titolo": "«Herbie Hancock's Electronic Instrument Glossary» — herbiehancock.com",
             "url": "https://www.herbiehancock.com/2016/09/14/herbie-hancocks-electronic-instrument-glossary/", "data": "2026-10-01"},
            {"titolo": "«File:Oberheim 4-voice prototype.jpg» — Wikimedia Commons, con la targhetta del museo nell'inquadratura",
             "url": "https://commons.wikimedia.org/wiki/File:Oberheim_4-voice_prototype.jpg", "data": "2026-10-01"},
        ],
        "hashtags": ["#oberheim", "#sintetizzatore", "#polifonia", "#anni70", "#musicaelettronica"],
        "reel_battute": [
            ("ELETTROFONI · N. 054", "Il prototipo numero 1 ha le etichette in braille"),
            ("MAGGIO 1974", "Tom Oberheim presenta il SEM. Un synth completo, una nota per volta."),
            ("1975", "Ne mette 4 in fila, e per la prima volta un accordo si può comprare."),
            ("4.295 DOLLARI", "Si chiama Oberheim Four Voice e costa quanto un'automobile."),
            ("IL NUMERO 1", "Era di Stevie Wonder. Le manopole doveva ritrovarle da solo."),
        ],
        "reel_cta": "Mandalo a chi venderebbe l'auto per un synth",
        "verificata": True,
    },
    {
        "slug": "korgm1",
        "numero": 55,
        "serie": "I SINTETIZZATORI",
        "strumento": "Korg M1",
        "anno": "1988",
        "luogo": "Tokyo, Giappone",
        "costruttore": "Korg",
        "specifiche": [
            ("USCITA", "1988"),
            ("VOCI", "16"),
            ("MEMORIA PCM", "4 MB"),
            ("VENDUTI", "250.000"),
        ],
        "gancio": "Il sintetizzatore più venduto di sempre. E Korg non ha mai confermato quanti",
        "sottotitolo": "Niente oscillatori, ma 86 forme d'onda registrate in 4 MB di memoria, due unità di effetti e un sequencer a 8 piste.",
        "la_macchina": (
            "Una tastiera nera da 61 tasti che a vederla non dice niente, e per "
            "sette anni è stata in ogni sala prove d'Europa. Dentro ci sono 4 MB "
            "di memoria con 86 forme d'onda registrate da strumenti veri, più 44 "
            "suoni di batteria e percussione; sopra, un filtro e un inviluppo per "
            "modellarle, due unità di effetti e un sequencer a 8 piste con la "
            "pila tampone. Korg la chiama «music workstation», cioè scrivi il "
            "pezzo, lo suoni e lo registri senza uscire dalla scatola. In "
            "Inghilterra costava 1.499 sterline. Le voci sono 16 e vanno divise "
            "fra tutte le piste."
        ),
        "inventore_nome": "Tsutomu Kato e Tadashi Osanai",
        "inventore": (
            "Kato aveva un locale notturno a Tokyo. Osanai era un fisarmonicista "
            "laureato all'università di Tokyo e ci suonava tutte le sere, "
            "accompagnandosi con una scatola ritmica americana, la Wurlitzer "
            "Sideman, che non gli piaceva. Convinse Kato a mettere i soldi per "
            "farne una migliore e nel 1963 uscì la Donca-Matic, chiamata così dal "
            "verso che faceva. La ditta si chiamava Keio, dalle iniziali dei due "
            "e dalla linea del treno lì accanto. Korg arriva nel 1967, da Keio più "
            "organ, perché il prodotto nuovo era un organo."
        ),
        "come_funziona": (
            "Il suono parte da un campione breve, qualche decina di millisecondi "
            "di pianoforte vero o di un colpo di rullante, letto in ciclo e poi "
            "passato in un filtro e in un inviluppo come su un synth analogico. "
            "Korg la chiamava AI synthesis. La novità non era campionare, che "
            "Fairlight ed Emulator facevano da anni, ma mettere nella stessa ROM "
            "anche le percussioni e due riverberi decenti, così il pezzo intero "
            "stava in una macchina sola. I campioni sono corti e gli attacchi "
            "duri. È per quello che il pianoforte dell'M1 lo riconoscete in due "
            "note."
        ),
        "richiami": [
            ("FIG. 1", "4 MB di PCM, 86 forme d'onda"),
            ("FIG. 2", "Sequencer a 8 piste"),
            ("FIG. 3", "Feritoia PROG/SEQ DATA"),
        ],
        "chi_lusata": [
            {"artista": "Robin S.", "nota": "«Show Me Love» (1990): quell'organo è il preset Organ 2, di fabbrica", "ig": None},
            {"artista": "Madonna", "nota": "«Vogue» (1990), scritta con Shep Pettibone su suoni dell'M1", "ig": None},
            {"artista": "Snap!", "nota": "«Rhythm Is a Dancer» (1992)", "ig": None},
            {"artista": "Bon Iver", "nota": "«Beth/Rest» (2012): l'M1 scelto apposta perché suona di 1988", "ig": None},
        ],
        "menzioni_extra": [],
        "da_ascoltare": {"brano": "Show Me Love", "artista": "Robin S.", "anno": "1990",
                         "cosa": "Il giro d'organo non l'ha programmato nessuno: è un preset preso dalla memoria di fabbrica e suonato così com'era."},
        "aneddoto": (
            "Il numero che gira è 250.000 esemplari e lo trovate scritto "
            "dappertutto. Sound On Sound è andato a chiederlo a Korg, e Korg non "
            "l'ha confermato. Ha confermato un'altra cosa: che la macchina numero "
            "100.000 è uscita dalla linea a novembre del 1990, due anni dopo "
            "l'inizio. Fate il conto di quante ne uscivano al giorno. Il quarto "
            "di milione io me lo tengo fra virgolette, ma il ritmo dei primi due "
            "anni dice già abbastanza."
        ),
        "avvertenza": "Le voci sono 16 in tutto, divise fra le 8 piste. Con pianoforte e batteria insieme le note in più spariscono, e non è un guasto.",
        "foto": {
            "file": "assets/foto/korgm1/principale.jpg",
            "autore": "deepsonic",
            "licenza": "CC BY 2.0",
            "fonte": "Wikimedia Commons",
        },
        "foto_extra": [
            {"file": "assets/foto/korgm1/angolo.jpg",
             "autore": "deepsonic", "licenza": "CC BY 2.0", "fonte": "Wikimedia Commons",
             "didascalia": "Il cursore del volume, i tasti e il bordo a gradini del pannello"},
            {"file": "assets/foto/korgm1/cartuccia.jpg",
             "autore": "deepsonic", "licenza": "CC BY 2.0", "fonte": "Wikimedia Commons",
             "didascalia": "La feritoia PROG/SEQ DATA: i suoni e le sequenze uscivano su cartuccia"},
            {"file": "assets/foto/korgm1/manopole.jpg",
             "autore": "deepsonic", "licenza": "CC BY 2.0", "fonte": "Wikimedia Commons",
             "didascalia": "PROG e COMBI: un suono solo, oppure otto impilati"},
        ],
        "fonti": [
            {"titolo": "«Korg M1» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Korg_M1", "data": "2026-10-01"},
            {"titolo": "«Korg M1 (Retrozone)» — Sound On Sound: i 250.000 non confermati, il numero di serie 100.000 a novembre 1990",
             "url": "https://www.soundonsound.com/reviews/korg-m1-retrozone", "data": "2026-10-01"},
            {"titolo": "«Korg» — Wikipedia (EN): Kato, Osanai, la Wurlitzer Sideman e la Donca-Matic",
             "url": "https://en.wikipedia.org/wiki/Korg", "data": "2026-10-01"},
            {"titolo": "«The legendary Korg M1 Organ 2 preset» — Gijs Verheijke, su «Show Me Love»",
             "url": "https://gijs.substack.com/p/the-legendary-korg-m1-organ-2-preset", "data": "2026-10-01"},
            {"titolo": "«How to make a classic house organ sound like Robin S.' Show Me Love» — MusicRadar",
             "url": "https://www.musicradar.com/how-to/classic-house-organ-robin-s-show-me-love", "data": "2026-10-01"},
        ],
        "hashtags": ["#korgm1", "#korg", "#sintetizzatore", "#madonna", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 055", "L'organo di «Show Me Love» non l'ha programmato nessuno"),
            ("TOKYO, 1988", "Esce il Korg M1, con 86 forme d'onda registrate da strumenti veri."),
            ("ROBIN S., 1990", "Quell'organo è il preset Organ 2 di fabbrica, suonato così com'è."),
            ("MADONNA, 1990", "«Vogue» la scrive con Shep Pettibone, sui suoni dell'M1."),
            ("NOVEMBRE 1990", "Dalla linea esce l'M1 numero 100.000. Sono passati 2 anni."),
        ],
        "reel_cta": "Mandalo a chi ha ballato «Show Me Love»",
        "reel_audio": {
            "file": "assets/audio/korgm1/registrazione.flac", "inizio": 10,
            "autore": "Alex Almirall, ESMUC", "licenza": "CC BY-SA 4.0",
            "fonte": "Wikimedia Commons",
            "url": "https://commons.wikimedia.org/wiki/File:KorgM1_Sonology_Esmuc.flac",
            "cosa": "un Korg M1 vero",
        },
        "verificata": True,
    },
    {
        "slug": "sh101",
        "numero": 56,
        "serie": "I SINTETIZZATORI",
        "strumento": "Roland SH-101",
        "anno": "1982",
        "luogo": "Osaka, Giappone",
        "costruttore": "Roland",
        "specifiche": [
            ("USCITA", "nov. 1982"),
            ("FINE PRODUZIONE", "1986"),
            ("TASTI", "32"),
            ("PREZZO", "495 $"),
        ],
        "gancio": "Doveva essere la tastiera a tracolla dei ragazzi. È finita a fare i bassi della techno",
        "sottotitolo": "Un oscillatore solo, 32 tasti, un sequencer da 100 passi e le pile dentro: Roland la vendeva per il palco.",
        "la_macchina": (
            "Grigia, leggera, coi cursori arancioni. Un oscillatore, un "
            "sub-oscillatore che suona una e due ottave sotto, un generatore di "
            "rumore e un mixer per dosarli; poi filtro, inviluppo, un LFO. Basta. "
            "I tasti sono 32 e va a pile. Sotto ai cursori stanno il sequencer da "
            "100 passi e l'arpeggiatore, coi tastini LOAD e PLAY. La facevano "
            "grigia, rossa e blu, e c'erano una tracolla di pelle e una "
            "impugnatura da infilare nel fianco. Memorie non ce ne sono: il suono "
            "che avete sul pannello è l'unico che avete."
        ),
        "inventore_nome": "Roland, su un'idea sbagliata",
        "inventore": (
            "Non c'è un progettista accreditato, c'è una scommessa. Alla fine del "
            "1982 Roland è convinta che il futuro sia il musicista che salta sul "
            "palco con la tastiera appesa al collo, e le pubblicità dell'SH-101 "
            "mettono ragazzi che saltano sopra la scritta «freedom for "
            "expression». La scommessa la perde: chi aveva 500 dollari se li "
            "teneva per un DX7, e nel 1986 la produzione chiude. Sette anni dopo "
            "quelle stesse macchine stavano nei banchi dei pegni a 50 sterline e "
            "se le compravano i ragazzi di Detroit e di Manchester."
        ),
        "come_funziona": (
            "Il peso del suono non viene dal filtro, viene dal mixer. Le tre "
            "sorgenti partono tutte dallo stesso oscillatore: dente di sega, "
            "impulso e il sub, che prende la frequenza e la divide per due o per "
            "quattro. Alzate il cursore del sub e la nota scende di corpo senza "
            "perdere l'attacco. Il filtro è un passa-basso e, con la risonanza "
            "tutta su, si mette a oscillare da solo. Il sequencer si riempie "
            "premendo le note una alla volta, senza schermo e senza griglia, e "
            "quando parte scoprite che cosa avete scritto."
        ),
        "richiami": [
            ("FIG. 1", "1 oscillatore + sub a -1 e -2 ottave"),
            ("FIG. 2", "Sequencer da 100 passi"),
            ("FIG. 3", "Presa MODULATION GRIP"),
        ],
        "chi_lusata": [
            {"artista": "A Guy Called Gerald", "nota": "«Voodoo Ray» (1988): l'SH-101 c'è in più di una traccia", "ig": None},
            {"artista": "Juan Atkins", "nota": "a Detroit dal 1985, su «Off To Battle» e «Interference»", "ig": None},
            {"artista": "Nightmares On Wax", "nota": "«Dextrous» (1989), figlio dichiarato di «Voodoo Ray»", "ig": "nightmaresonwax"},
            {"artista": "The Prodigy", "nota": "fra le macchine arrivate al giro rave intorno al 1990", "ig": None},
        ],
        "menzioni_extra": [],
        "da_ascoltare": {"brano": "Voodoo Ray", "artista": "A Guy Called Gerald", "anno": "1988",
                         "cosa": "Ascoltate il basso: è una nota sola col sub tirato su, e tiene in piedi tutto il pezzo da sola."},
        "aneddoto": (
            "La pubblicità del 1982 la mostrava appesa al collo, con "
            "l'impugnatura in mano come il manico di una chitarra. Quella parte "
            "non ha mai attecchito. Quello che è rimasto è la presa in alto a "
            "sinistra del pannello, dove l'impugnatura si infilava, con sopra "
            "scritto MODULATION GRIP: su quasi tutte le macchine che trovate oggi "
            "è vuota, e la plastica lì attorno è più chiara perché nessuno ci ha "
            "mai messo le dita. L'accessorio che doveva salvare lo strumento è "
            "l'unica cosa che di quello strumento è sparita."
        ),
        "avvertenza": "Le memorie non esistono. Prima di spegnere, la fotografia del pannello: è l'unico modo di ritrovare il suono di stasera.",
        # La copertina e' la fotografia col rapporto piu' vicino al riquadro:
        # quella frontale, piu' larga, veniva tagliata ai lati e si perdeva
        # la sigla stampata sul pannello. Guardata la tavola, non il file.
        "foto": {
            "file": "assets/foto/sh101/principale.jpg",
            # La tavola 4 non ha una foto sua e ricade su questa con un
            # ingrandimento: centrata, il ritaglio cadeva sui tasti. Alzando
            # il punto di messa a fuoco prende la fila dei cursori, che e'
            # quello di cui parla il testo.
            "posizione": "center 32%",
            "autore": "eternal jamzzzz",
            "licenza": "CC BY 2.0",
            "fonte": "Wikimedia Commons",
        },
        "foto_extra": [
            {"file": "assets/foto/sh101/pannello.jpg",
             "autore": "909 bd (Wikipedia EN)", "licenza": "CC BY-SA 3.0", "fonte": "Wikimedia Commons",
             "didascalia": "In alto a sinistra la presa MODULATION GRIP, quasi sempre vuota"},
            {"file": "assets/foto/sh101/blu.jpg",
             "posizione": "center 45%",
             "autore": "byCharly", "licenza": "CC BY 2.0", "fonte": "Wikimedia Commons",
             "didascalia": "La versione blu, uno dei tre colori, suonata dal vivo"},
        ],
        "fonti": [
            {"titolo": "«Roland SH-101» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Roland_SH-101", "data": "2026-10-01"},
            {"titolo": "«Instrumental Instruments: Roland SH-101» — Red Bull Music Academy Daily",
             "url": "https://daily.redbullmusicacademy.com/2017/09/roland-sh101-instrumental-instruments/", "data": "2026-10-01"},
            {"titolo": "«Roland SH101 (Retrozone)» — Sound On Sound",
             "url": "https://www.soundonsound.com/reviews/roland-sh101-retrozone", "data": "2026-10-01"},
        ],
        "hashtags": ["#sh101", "#roland", "#sintetizzatore", "#theprodigy", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 056", "Nata per il palco, finita nel basso di «Voodoo Ray»"),
            ("NOVEMBRE 1982", "Roland SH-101: 32 tasti, le pile, la tracolla di pelle."),
            ("1986", "Chi ha 500 dollari se li tiene per un DX7. La produzione chiude."),
            ("50 STERLINE", "Al banco dei pegni la prendono i ragazzi di Detroit e di Manchester."),
            ("A GUY CALLED GERALD, 1988", "«Voodoo Ray»: il basso è una nota sola, col sub tirato su."),
        ],
        "reel_cta": "Mandalo a chi suona la tastiera a tracolla",
        # Registrazione della macchina vera (16/10/2026): licenza libera,
        # verificata sulla pagina Freesound (descrizione + licenza).
        "reel_audio": {
            "file": "assets/audio/sh101/registrazione.mp3", "inizio": 0,
            "autore": "druidbloke", "licenza": "CC0 1.0",
            "fonte": "freesound.org/s/167115",
            "url": "https://freesound.org/s/167115/",
            "cosa": "un SH-101 vero che suona una linea di basso acid",
        },
        "verificata": True,
    },
    {
        "slug": "vl1",
        "numero": 57,
        "serie": "I GIOCATTOLI",
        "strumento": "Casio VL-Tone VL-1",
        "anno": "1980 circa",
        "luogo": "Tokyo, Giappone",
        "costruttore": "Casio",
        "specifiche": [
            ("USCITA", "1979-82?"),
            ("TASTI", "29"),
            ("SUONI", "5 + ADSR"),
            ("PREZZO", "69,95 $"),
        ],
        "gancio": "Una calcolatrice che suona. E con cinque suoni di plastica ci hanno fatto «Da Da Da»",
        "sottotitolo": "29 tasti, un display a cristalli liquidi e una calcolatrice vera dentro: Casio la vendeva come giocattolo.",
        "la_macchina": (
            "Sta in una mano. A sinistra la griglia dell'altoparlante, al centro "
            "il display e la scritta ELECTRONIC MUSICAL INSTRUMENT VL-1, poi due "
            "ottave e mezzo di tastini. Sotto i tasti bianchi, stampati, ci sono "
            "i numeri e i segni: premete CAL e diventa una calcolatrice, premete "
            "MUSIC e torna uno strumento. I suoni sono cinque e i nomi stanno "
            "sopra i due cursori, piano, violino, flauto, chitarra, fantasy. Sono "
            "imitazioni pessime e lo sanno anche loro. Il sesto si chiama ADSR e "
            "ve lo scrivete da soli."
        ),
        "inventore_nome": "I fratelli Kashio",
        "inventore": (
            "La Casio nasce nel 1946 a Tokyo e per trent'anni fa una cosa sola, "
            "calcolatrici. Nel 1957 Toshio Kashio mette a punto la 14-A, la prima "
            "calcolatrice compatta interamente elettrica, e la ditta cresce su "
            "quella. Negli anni Settanta i chip da calcolatrice costano ormai "
            "pochissimo e qualcuno in azienda fa la domanda giusta: se questo coso "
            "sa contare, può anche contare le vibrazioni di una nota. Il VL-1 è "
            "la risposta. Non esce dal reparto strumenti musicali, perché il "
            "reparto strumenti musicali non c'era ancora."
        ),
        "come_funziona": (
            "Si vede che il cuore è un chip da calcolatrice da come si programma "
            "il sesto suono. Premete ADSR e dovete digitare otto cifre in fila: la "
            "prima sceglie la forma d'onda, le altre l'attacco, il decadimento, il "
            "livello e la durata del sostegno, il rilascio, il vibrato, il "
            "tremolo. Un inviluppo che si scrive come un numero di telefono. Il "
            "risultato quasi sempre suona peggio dei cinque preimpostati, però è "
            "un ADSR vero, su una macchina da 69,95 dollari che la gente comprava "
            "per i bambini."
        ),
        "richiami": [
            ("FIG. 1", "Display a 8 caratteri"),
            ("FIG. 2", "ADSR in 8 cifre"),
            ("FIG. 3", "10 ritmi preimpostati"),
        ],
        "chi_lusata": [
            {"artista": "Trio", "nota": "«Da Da Da» (1982): ritmo Rock-1 e voce Piano, come escono dalla scatola", "ig": None},
            {"artista": "The Human League", "nota": "fra i primi a prenderla sul serio in studio", "ig": None},
            {"artista": "Stevie Wonder", "nota": "citato fra chi l'ha usata dalla scheda del museo che la espone", "ig": None},
        ],
        "menzioni_extra": [],
        "da_ascoltare": {"brano": "Da Da Da", "artista": "Trio", "anno": "1982",
                         "cosa": "La batteria è il ritmo Rock-1 della macchinetta, lasciato girare dall'inizio alla fine; il motivetto è la voce Piano."},
        "aneddoto": (
            "Non si riesce a stabilire di che anno sia. Wikipedia dice 1981. "
            "Vintage Synth Explorer dice giugno 1979. La didascalia su Commons "
            "dice 1980. La targhetta del museo che la espone, sotto la vetrina, "
            "dice «um 1982», cioè circa 1982. Quattro fonti, quattro anni. Succede "
            "agli oggetti usciti come giocattoli: arrivano nei negozi senza "
            "comunicati stampa e senza recensioni, e quando qualcuno si accorge "
            "che contano sono passati dieci anni e la data se l'è persa per strada."
        ),
        "avvertenza": "Cinque suoni di fabbrica, il sesto in otto cifre. Sbagliatene una e non c'è un tasto per tornare indietro: si ribatte tutto.",
        "foto": {
            "file": "assets/foto/vl1/principale.jpg",
            "autore": "Dontpanic",
            "licenza": "CC BY-SA 3.0",
            "fonte": "Wikimedia Commons",
            "ritaglio": True,
        },
        "foto_extra": [
            {"file": "assets/foto/vl1/museo.jpg",
             "posizione": "center 62%",
             "autore": "Reinraum", "licenza": "pubblico dominio", "fonte": "Wikimedia Commons",
             "didascalia": "In vetrina col manuale: «ELECTRONIC MUSICAL INSTRUMENT & CALCULATOR»"},
        ],
        "fonti": [
            {"titolo": "«Casio VL-1» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Casio_VL-1", "data": "2026-10-01"},
            {"titolo": "«Casio VL-Tone VL-1» — Vintage Synth Explorer (data: giugno 1979)",
             "url": "https://www.vintagesynth.com/casio/vl-tone-vl-1", "data": "2026-10-01"},
            {"titolo": "«Casio» — Wikipedia (EN): i fratelli Kashio e la calcolatrice 14-A del 1957",
             "url": "https://en.wikipedia.org/wiki/Casio", "data": "2026-10-01"},
            {"titolo": "«File:Casio VL-1 Inv Nr 81934.jpg» — Wikimedia Commons, con la targhetta «um 1982»",
             "url": "https://commons.wikimedia.org/wiki/File:Casio_VL-1_Inv_Nr_81934.jpg", "data": "2026-10-01"},
        ],
        "hashtags": ["#casiovl1", "#casio", "#sintetizzatore", "#steviewonder", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 057", "Una calcolatrice da 69,95 dollari ha fatto «Da Da Da»"),
            ("TOKYO · DAL 1946", "Casio per 30 anni fa calcolatrici e basta. Poi prova a farle suonare."),
            ("29 TASTI · 5 SUONI", "Il VL-1: premi CAL e fa i conti, premi MUSIC e suona."),
            ("1979? 1980? 1981? 1982?", "È un giocattolo e la data si è persa: 4 fonti, 4 anni diversi."),
            ("TRIO · 1982", "«Da Da Da»: ritmo Rock-1 e voce Piano, come escono dalla scatola."),
        ],
        "reel_cta": "Mandalo a chi canta ancora «Da Da Da»",
        "reel_audio": {
            "file": "assets/audio/vl1/registrazione.ogg", "inizio": 1,
            "autore": "Havelbaude", "licenza": "CC BY-SA 4.0",
            "fonte": "Wikimedia Commons",
            "url": "https://commons.wikimedia.org/wiki/File:Casio_vl1_rock1.ogg",
            "cosa": "un Casio VL-1 col suo ritmo «rock 1»",
        },
        "verificata": True,
    },
    {
        "slug": "polymoog",
        "numero": 58,
        "serie": "I SINTETIZZATORI",
        "strumento": "Moog Polymoog",
        "anno": "1975",
        "luogo": "Williamsville, New York",
        "costruttore": "Moog Music",
        "specifiche": [
            ("SYNTHESIZER", "1975"),
            ("KEYBOARD", "1978"),
            ("TASTI", "71"),
            ("FINE", "1980"),
        ],
        "gancio": "Una scheda elettronica per ogni tasto, 71 in tutto, dentro un mobile solo",
        "sottotitolo": "Moog arriva alla polifonia per la strada degli organi da casa, dividendo un oscillatore unico, e poi ci mette una scheda per nota.",
        "la_macchina": (
            "71 tasti pesati e sensibili al tocco, un pannello di cursori e, "
            "sotto il coperchio, file di schede verdi: una per ogni nota. Il "
            "primo modello esce nel 1975 a 5.295 dollari con otto suoni di "
            "fabbrica, dagli archi agli ottoni, e i cursori sopra per "
            "spostarli. Nel 1978 arriva la versione Keyboard, 3.995 dollari e 14 "
            "preset. La fama che si porta dietro non è per il suono ma per "
            "l'affidabilità, e il motivo si capisce contando: 71 schede sono 71 "
            "cose che si possono guastare."
        ),
        "inventore_nome": "Moog Music",
        "inventore": (
            "Nel 1975 il problema ce l'hanno tutti ed è uno solo, suonare un "
            "accordo. Un oscillatore per voce costa, e cinque voci costano cinque "
            "volte; nessuno ancora sa farne dieci a un prezzo di mercato. Moog "
            "prende la strada che gli organi da salotto battevano da vent'anni, "
            "cioè un oscillatore solo, altissimo, e una catena di divisori che da "
            "lì ricava tutte le note della tastiera. Il pezzo che ci aggiunge sta "
            "a valle. Non è un organo e non è un Minimoog moltiplicato per "
            "cinque, è una terza cosa, e in catalogo non ce n'erano altre."
        ),
        "come_funziona": (
            "Il generatore in cima fa le note più acute, i divisori le portano "
            "giù di ottava in ottava. Fin qui è un organo. La differenza sono le "
            "schede, una per tasto, ognuna col suo filtro, il suo inviluppo e il "
            "suo controllo di ampiezza: ogni nota ha la sua catena e nessuna "
            "ruba la voce a un'altra, come invece succede sui polifonici a voci "
            "contate. Quello che perdete è la programmazione. I preset li potete "
            "spostare con i cursori, ma un suono da zero su questa macchina non "
            "lo costruite."
        ),
        "richiami": [
            ("FIG. 1", "71 schede, una per tasto"),
            ("FIG. 2", "8 preset, 14 sulla Keyboard"),
            ("FIG. 3", "Tastiera sensibile al tocco"),
        ],
        "chi_lusata": [
            {"artista": "Gary Numan", "nota": "«Cars» (1979) e tutto «The Pleasure Principle», col preset Vox Humana", "ig": None},
            {"artista": "Prince", "nota": "fra chi ne ha avuto uno negli anni in cui erano nuovi", "ig": None},
        ],
        "menzioni_extra": [],
        "da_ascoltare": {"brano": "Cars", "artista": "Gary Numan", "anno": "1979",
                         "cosa": "Il tappeto che regge tutto il pezzo è un preset di fabbrica chiamato Vox Humana, premuto e basta."},
        "aneddoto": (
            "La versione Keyboard del 1978 aveva 14 preset coi nomi stampati "
            "sopra, e uno si chiamava Vox Humana. Gary Numan ci ha costruito "
            "sopra un disco intero nel 1979, dopo aver tolto la chitarra "
            "elettrica da tutto quello che faceva. Non ha programmato niente, ha "
            "premuto un pulsante. È una cosa che fa arrabbiare chi passa le sere "
            "a costruirsi i suoni da zero, e secondo me è esattamente il motivo "
            "per cui quel disco regge ancora: un timbro solo, riconoscibile, "
            "usato senza vergogna per quaranta minuti."
        ),
        "avvertenza": "Le schede sono 71, una per nota. Quando un tasto tace non è la tastiera: è la sua scheda, e va sfilata e rimessa.",
        # LEZIONE RIPETUTA (05/10/2026): la prima copertina era la fotografia di
        # una vetrina — strumento dietro una grata e, davanti, la scatola di un
        # controller MIDI moderno, che era la scritta piu' leggibile di tutta la
        # tavola. Si guarda la tavola generata, non il file.
        "foto": {
            "file": "assets/foto/polymoog/fronte.jpg",
            "autore": "Chris Sobczak",
            "licenza": "CC BY 2.0",
            "fonte": "Wikimedia Commons",
        },
        "foto_extra": [
            {"file": "assets/foto/polymoog/280a.jpg",
             "autore": "Automaton399", "licenza": "CC0", "fonte": "Wikimedia Commons",
             "didascalia": "La versione Keyboard del 1978, quella coi 14 preset"},
            {"file": "assets/foto/polymoog/schede.jpg",
             "autore": "Automaton399", "licenza": "CC0", "fonte": "Wikimedia Commons",
             "didascalia": "Dentro: le schede che fanno le voci, una per nota"},
        ],
        "fonti": [
            {"titolo": "«Polymoog» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Polymoog", "data": "2026-10-05"},
            {"titolo": "«The Pleasure Principle» — Wikipedia (EN): «Numan made liberal use of the Polymoog keyboard, particularly its distinctive Vox Humana preset»",
             "url": "https://en.wikipedia.org/wiki/The_Pleasure_Principle_(Gary_Numan_album)", "data": "2026-10-05"},
        ],
        "hashtags": ["#polymoog", "#moog", "#sintetizzatore", "#prince", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 058", "Il tappeto di «Cars» di Gary Numan? Un preset e basta"),
            ("1975 · 5.295 DOLLARI", "Suonare un accordo è il problema di tutti. Moog risponde col Polymoog."),
            ("71 TASTI, 71 SCHEDE", "Una scheda per ogni tasto: 71 cose che si possono guastare."),
            ("1978 · 14 PRESET", "La versione Keyboard ha 14 preset coi nomi stampati. Uno è Vox Humana."),
            ("GARY NUMAN · 1979", "Via la chitarra. Numan ci costruisce sopra «The Pleasure Principle»."),
        ],
        "reel_cta": "Mandalo a chi si costruisce i suoni da zero",
        "reel_audio": {
            "file": "assets/audio/polymoog/registrazione.ogg", "inizio": 1,
            "autore": "Raymangold22", "licenza": "CC0",
            "fonte": "Wikimedia Commons",
            "url": "https://commons.wikimedia.org/wiki/File:Vox_Humana_Polymoog.ogg",
            "cosa": "un Polymoog sul preset Vox Humana",
        },
        "verificata": True,
    },
    {
        "slug": "leslie",
        "numero": 59,
        "serie": "GLI EFFETTI",
        "strumento": "Leslie",
        "anno": "1941",
        "luogo": "Pasadena, California",
        "costruttore": "Electro Music",
        "specifiche": [
            ("PRIMO MODELLO", "1941"),
            ("ROTORI", "2"),
            ("GIRI LENTI", "40-50 al min."),
            ("GIRI VELOCI", "340-400 al min."),
        ],
        "gancio": "Hammond lo ascoltò al telefono e disse di no. Don Leslie se lo costruì in garage e lo vendette lo stesso",
        "sottotitolo": "Un armadio di legno con dentro una tromba e un tamburo che girano, per rendere meno piatto l'organo.",
        "la_macchina": (
            "Un armadio di legno con le persiane davanti. Dentro, in basso, c'è l'altoparlante dei bassi "
            "con un tamburo che gli gira intorno; in alto un driver per gli "
            "acuti con una tromba che gira anch'essa. Due velocità, che "
            "chiamano CHORALE e TREMOLO. Il modello più diffuso è il 122, "
            "poi c'è il 147, che funziona con più organi, e il 145, "
            "che è lo stesso in un mobile da 33 pollici."
        ),
        "inventore_nome": "Don Leslie",
        "inventore": (
            "Donald Leslie era un tecnico radio di Los Angeles, nato nel 1911 a "
            "Danville, Illinois. Nel 1937 compra un organo Hammond e in una "
            "stanza piccola lo trova spento, acuto e fermo. Costruisce un prototipo, e "
            "nel 1940 lo fa sentire a Hammond in un negozio di Los Angeles, "
            "con Laurens Hammond che ascolta per telefono da Chicago. Hammond "
            "ne vendeva già uno suo e non apprezzò l'effetto. Nel 1941 Leslie "
            "fonda la Electro Music a Pasadena e chiama l'aggeggio Vibratone "
            "30A. Lo costruisce in garage."
        ),
        "come_funziona": (
            "L'altoparlante sta fermo e gira la tromba che gli sta davanti: "
            "il suono parte ora in una direzione e ora in un'altra, e chi "
            "ascolta sente il timbro ondeggiare e l'intonazione, per effetto "
            "Doppler, oscillare un poco. A velocità lenta la tromba fa circa "
            "50 giri al minuto e il tamburo 40, a velocità alta 400 e 340. "
            "Quella lenta si chiama CHORALE, quella veloce TREMOLO."
        ),
        "richiami": [
            ("FIG. 1", "Cassa con le persiane"),
            ("FIG. 2", "Tromba e tamburo che girano"),
            ("FIG. 3", "Due velocità: CHORALE e TREMOLO"),
        ],
        "chi_lusata": [
            {"artista": "Jimmy Smith", "nota": "organista jazz, uno dei nomi che le fonti fanno per primi", "ig": None},
            {"artista": "Beatles", "nota": "su «Tomorrow Never Knows», 1966, dove ci passa la voce di Lennon", "ig": None},
            {"artista": "Richard Wright", "nota": "dei Pink Floyd, tastierista", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": (
            "Hammond cambia l'interfaccia degli altoparlanti sui suoi organi "
            "per renderli a prova di Leslie. Leslie ci mette poco ad "
            "aggirare il problema. Eppure, dice Wikipedia, degli organi "
            "Hammond lui non aveva stima: li avrebbe chiamati «quei "
            "maledetti aggeggi». Nel 1965 vende la ditta alla CBS. Hammond "
            "compra il nome Leslie nel 1980, o negli anni intorno: le fonti "
            "non coincidono. Mi piace la storia di un uomo che ha fatto "
            "la fortuna di un organo che non sopportava."
        ),
        "avvertenza": "Tromba e tamburo girano a velocità diverse, 400 e 340 giri al minuto sul veloce. Controllate che si muovano tutti e due, prima di pagarlo.",
        "foto": {
            "file": "assets/foto/leslie/rockfield.jpg",
            "autore": "Steve Knight",
            "licenza": "CC BY 2.0",
            "fonte": "Wikimedia Commons",
            "ritaglio": True,
        },
        "foto_extra": [
            {"file": "assets/foto/leslie/acrilico.jpg",
             "autore": "Hustvedt", "licenza": "CC BY-SA 3.0", "fonte": "Wikimedia Commons",
             "didascalia": "Un mobile trasparente: in primo piano l'altoparlante dei bassi, intorno i meccanismi"},
        ],
        "fonti": [
            {"titolo": "«Leslie speaker» — Wikipedia (EN): modelli, velocità, Hammond, CBS, chi lo ha usato",
             "url": "https://en.wikipedia.org/wiki/Leslie_speaker", "data": "2026-10-13"},
            {"titolo": "«Donald Leslie» — Wikipedia (EN): 1911, la dimostrazione del 1940, Electro Music, 48 brevetti",
             "url": "https://en.wikipedia.org/wiki/Donald_Leslie", "data": "2026-10-13"},
            {"titolo": "«Don Leslie» — Procol Harum, necrologio del 2004: Hammond, Electro Music, CBS 1965, 48 brevetti, Hammond e il 1980",
             "url": "https://procolharum.com/99/leslie_obit.htm", "data": "2026-10-13"},
        ],
        "hashtags": ["#lesliespeaker", "#leslie", "#organo", "#beatles", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 059", "Hammond sente il Leslie al telefono e dice di no"),
            ("DON LESLIE", "Nel 1940 Don Leslie fa sentire il prototipo. A Hammond non piace."),
            ("1941", "Leslie fonda la Electro Music a Pasadena e lo costruisce in garage."),
            ("TROMBA E TAMBURO", "Dentro girano una tromba e un tamburo, fino a 400 giri al minuto."),
            ("1966", "I Beatles ci passano la voce di Lennon in «Tomorrow Never Knows»."),
        ],
        "reel_cta": "Mandalo a chi suona l'organo",
        # Registrazione della macchina vera (16/10/2026): licenza libera,
        # verificata sulla pagina Freesound (descrizione + licenza).
        "reel_audio": {
            "file": "assets/audio/leslie/registrazione.mp3", "inizio": 2,
            "autore": "MrAuralization", "licenza": "CC BY 4.0",
            "fonte": "freesound.org/s/158628",
            "url": "https://freesound.org/s/158628/",
            "cosa": "un organo Hammond serie H che suona attraverso un cabinet Leslie vero",
        },
        "verificata": True,
    },
    {
        "slug": "cz101",
        "numero": 60,
        "serie": "I SINTETIZZATORI",
        "strumento": "Casio CZ-101",
        "anno": "1984",
        "luogo": "Tokyo, Giappone",
        "costruttore": "Casio",
        "specifiche": [
            ("USCITA", "nov. 1984"),
            ("PREZZO", "495 $"),
            ("VOCI", "8"),
            ("PRODOTTI", "68.500"),
        ],
        "gancio": "Digitale, programmabile e a 495 dollari, mentre il DX7 ne costava quattro volte tanti",
        "sottotitolo": "Tasti piccoli, sei pile torcia e una sintesi inventata in casa che Casio chiamava distorsione di fase.",
        "la_macchina": (
            "49 tasti piccoli, quattro ottave, e un pannello grigio pieno di "
            "tastini color sabbia. Ha i perni per la tracolla e va a sei pile "
            "torcia, quindi lo suonate dove vi pare. Le voci sono 8 con un "
            "oscillatore ciascuna, 4 se ne usate due per voce. Sul pannello "
            "leggete DCO, DCW e DCA scritti due volte, e sono le tre sezioni di "
            "ogni linea: oscillatore, forma d'onda, ampiezza. Di filtro non c'è "
            "traccia, e non è una dimenticanza."
        ),
        "inventore_nome": "Casio, un'altra volta",
        "inventore": (
            "Quattro anni dopo il VL-Tone la ditta delle calcolatrici si "
            "ripresenta, e stavolta vuole lo scaffale accanto allo Yamaha DX7. "
            "Il DX7 era digitale, costava quasi duemila dollari e lo sapevano "
            "programmare in pochi; la sintesi FM che gli stava dentro era un "
            "brevetto di Stanford, con la licenza da pagare. Casio si scrive un "
            "metodo proprio, la distorsione di fase, che arriva a un suono "
            "parente senza essere FM, e tiene il prezzo a un quarto. Non è "
            "un'operazione da ingegneri romantici, è una mossa commerciale. Ha "
            "funzionato."
        ),
        "come_funziona": (
            "Si parte da una sinusoide, la forma d'onda più povera che ci sia. "
            "Invece di cambiarne l'ampiezza si cambia la velocità con cui la si "
            "percorre, rallentando in un punto del ciclo e correndo nell'altro. "
            "Quello che esce ha gli spigoli dove prima era tondo, e gli spigoli "
            "sono armoniche. Variando quanto si distorce la fase il timbro si "
            "apre e si chiude, che è il mestiere del filtro su un analogico. Per "
            "questo qui il filtro non c'è e la sezione che fa quel lavoro si "
            "chiama DCW, cioè forma d'onda controllata digitalmente."
        ),
        "richiami": [
            ("FIG. 1", "DCO, DCW, DCA per linea"),
            ("FIG. 2", "8 voci, 4 con due oscillatori"),
            ("FIG. 3", "6 pile torcia"),
        ],
        "chi_lusata": [
            {"artista": "Vince Clarke", "nota": "degli Erasure: a un certo punto ne teneva quattro", "ig": None},
            {"artista": "Eurythmics", "nota": "fra i primi a prenderlo sul serio in studio", "ig": None},
            {"artista": "Salt-N-Pepa", "nota": "fra chi se lo è portato dentro un altro genere", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": (
            "Nel novembre del 1984 il CZ-101 arriva nei negozi a 495 dollari. Il "
            "DX7 ne costava quasi quattro volte e si programmava con un display a "
            "una riga e una tabella di parametri che nemmeno i commessi sapevano "
            "spiegare. Il Casio invece lo programmavano i ragazzi, perché costava "
            "poco e perché andava a pile: te lo portavi in camera. Fino al 1988 "
            "ne hanno fatti 68.500. A me la nomea di sintetizzatore dei poveri è "
            "sempre sembrata ingiusta, e negli anni Novanta quel suono di organo "
            "è tornato dentro migliaia di dischi da ballo senza che nessuno "
            "chiedesse quanto fosse costata la macchina."
        ),
        "avvertenza": "Altoparlante non ce n'è. L'unica uscita è la presa delle cuffie, quindi senza cuffie o amplificatore non lo sentite suonare.",
        "foto": {
            "file": "assets/foto/cz101/principale.jpg",
            "autore": "Neil Vance",
            "licenza": "CC BY-SA 4.0",
            "fonte": "Wikimedia Commons",
            "ritaglio": True,
        },
        "foto_extra": [
            {"file": "assets/foto/cz101/retro.jpg",
             "autore": "Clusternote", "licenza": "CC BY-SA 3.0", "fonte": "Wikimedia Commons",
             "didascalia": "Lo stesso strumento visto dall'altro verso",
            # Sulla tavola regge grazie alla didascalia; nel reel, che non
            # ne ha, il marchio capovolto sembra un errore di montaggio.
            "nel_reel": False},
            {"file": "assets/foto/cz101/angolo.jpg",
             "autore": "Clusternote", "licenza": "CC BY-SA 3.0", "fonte": "Wikimedia Commons",
             "didascalia": "Di sbieco: i tasti piccoli si vedono solo da qui"},
        ],
        "fonti": [
            {"titolo": "«Casio CZ synthesizers» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Casio_CZ_synthesizers", "data": "2026-10-05"},
            {"titolo": "«Phase distortion synthesis» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Phase_distortion_synthesis", "data": "2026-10-05"},
            {"titolo": "«Casio CZ-101: The Classic Synth That Went Head to Head With the DX7» — gearnews",
             "url": "https://www.gearnews.com/casio-cz-101/", "data": "2026-10-05"},
        ],
        "hashtags": ["#cz101", "#casio", "#sintetizzatore", "#eurythmics", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 060", "Quelli delle calcolatrici contro il DX7 di Yamaha"),
            ("NOVEMBRE 1984", "Il Casio CZ-101 costa 495 dollari. Il DX7 quasi 2.000."),
            ("BREVETTO DI STANFORD", "La FM è un brevetto di Stanford. Casio inventa la distorsione di fase."),
            ("68.500 ESEMPLARI", "Va a 6 pile torcia, e i ragazzi se lo portano in camera."),
            ("VINCE CLARKE · ERASURE", "Synth dei poveri, dicono. Vince Clarke degli Erasure ne tiene 4."),
        ],
        "reel_cta": "Mandalo a chi lo chiama synth dei poveri",
        # Registrazione della macchina vera (17/10/2026, regola del proprietario:
        # il suono vero in ogni uscita). Licenza verificata sulla pagina;
        # è un suono di rumori, non un preset: «A Casio CZ-101, abused to produce interesting sounding sounds and noises».
        "reel_audio": {
            "file": "assets/audio/cz101/registrazione.mp3", "inizio": 0,
            "autore": "altemark", "licenza": "CC BY 4.0",
            "fonte": "freesound.org/s/43342",
            "url": "https://freesound.org/s/43342/",
            "cosa": "un Casio CZ-101 vero, spinto a fare rumori: un drone digitale modulato",
        },
        "verificata": True,
    },
    {
        "slug": "poly800",
        "numero": 61,
        "serie": "I SINTETIZZATORI",
        "strumento": "Korg Poly-800",
        "anno": "1983",
        "luogo": "Giappone",
        "costruttore": "Korg",
        "specifiche": [
            ("LANCIO", "1983"),
            ("PREZZO", "795 $"),
            ("VOCI", "8 (o 4)"),
            ("TASTI", "49"),
        ],
        "gancio": "Costava 795 dollari e andava a pile. Atkins, May e Saunderson, i tre del techno di Detroit, ne avevano uno",
        "sottotitolo": "Otto voci programmabili sotto gli 800 dollari, e un solo filtro per tutte.",
        "la_macchina": (
            "49 tasti senza dinamica, 64 programmi in memoria e un sequencer da 256 passi. "
            "Va a pile e ha i ganci per la tracolla, quindi si può suonare "
            "in piedi come una tastiera da collo. Ha un joystick per modulare. "
            "Le voci sono 8, ma ogni voce ha due oscillatori: se li accendete "
            "tutti e due, il suono si fa più pieno e le voci scendono a 4. "
            "I programmi si salvano su cassetta."
        ),
        "inventore_nome": "Korg",
        "inventore": (
            "Lo presenta Korg nel 1983. Il nome di chi l'ha disegnato non l'ho "
            "trovato in nessuna fonte, e non ne invento uno. Nel 1984 esce l'EX-800, la stessa "
            "elettronica senza tastiera, da montare in un rack. Nel 1986 il "
            "Poly-800 II: al posto del chorus un delay digitale, e finalmente "
            "i messaggi SysEx per scambiare i suoni col computer."
        ),
        "come_funziona": (
            "Gli oscillatori sono digitali (DCO) e fanno dente di sega e "
            "onda quadra, con del rumore bianco da mescolare. Ogni oscillatore ha "
            "un inviluppo a 6 stadi: Attack, Decay, Break Point, Slope, Sustain, "
            "Release. Il filtro passa-basso risonante però è uno solo, "
            "condiviso da tutte le voci. Per questo lo chiamano paraphonic e non "
            "polifonico fino in fondo."
        ),
        "richiami": [
            ("FIG. 1", "Tastiera da 49 tasti e joystick"),
            ("FIG. 2", "Pannello con i 64 programmi"),
            ("FIG. 3", "Ganci per la tracolla"),
        ],
        "chi_lusata": [
            {"artista": "Juan Atkins", "nota": "uno dei tre di Belleville, Detroit: ne aveva uno in studio", "ig": None},
            {"artista": "Derrick May", "nota": "ce l'ha nelle liste degli strumenti prima del 1990", "ig": None},
            {"artista": "Kevin Saunderson", "nota": "ce l'aveva intorno al 1988, quando nasce Inner City", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": (
            "Il prezzo dipende da chi lo racconta. 795 dollari per Wikipedia, "
            "«meno di 800» nella pubblicità Korg su Musician nel 1984, 575 "
            "sterline per l'Inghilterra. Anche gli anni non tornano: 1983-1987 "
            "da una parte, 1984-1986 dall'altra. Sul filtro unico invece "
            "tutti sono d'accordo: The Mix lo chiama un difetto grosso, "
            "da string machine. Nel 1994 la stessa rivista lo dava usato "
            "a 100-130 sterline, con il voto più alto al rapporto qualità-prezzo."
        ),
        "avvertenza": "Con i due oscillatori accesi le voci scendono da 8 a 4. Contate quanti tasti suonate insieme, prima di dire che è un otto voci.",
        "foto": {
            "file": "assets/foto/poly800/ii.jpg",
            "autore": "rico blanco",
            "licenza": "CC BY-SA 2.0",
            "fonte": "Wikimedia Commons (un Poly-800 II, la versione del 1986)",
            "ritaglio": True,
        },
        "foto_extra": [
            {"file": "assets/foto/poly800/controls.jpg",
             "autore": "rico blanco", "licenza": "CC BY-SA 2.0", "fonte": "Wikimedia Commons",
             "didascalia": "Il pannello: joystick, tasti dei programmi e sequencer (un Poly-800 II)"},
        ],
        "fonti": [
            {"titolo": "«Korg Poly-800» — Wikipedia (EN): 1983, 795 $, 8 voci, DCO, filtro unico, 64 programmi, EX-800 e Poly-800 II",
             "url": "https://en.wikipedia.org/wiki/Korg_Poly-800", "data": "2026-10-16"},
            {"titolo": "«Total Recall: Korg Poly-800» — The Mix, settembre 1994: 575 sterline, filtro unico, 4 voci in doppio, elenco di chi l'ha usato",
             "url": "https://www.muzines.co.uk/articles/total-recall/8184", "data": "2026-10-16"},
            {"titolo": "«Korg Poly-800 Polyphonic Synthesizer» — SMEM (museo): i tre di Belleville, tecnologia e prezzo",
             "url": "https://www.smemmusic.ch/fr/node/1219", "data": "2026-10-16"},
        ],
        "hashtags": ["#poly800", "#korg", "#sintetizzatore", "#derrickmay", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 061", "Va a pile, e ce l'hanno i tre della techno di Detroit"),
            ("KORG · 1983", "8 voci programmabili, 49 tasti e i ganci per la tracolla."),
            ("IL TRUCCO", "Ogni voce ha due oscillatori: accesi tutti e due, le voci scendono a 4."),
            ("IL DIFETTO", "Un filtro solo, condiviso da tutte le voci."),
            ("DETROIT", "Juan Atkins, Derrick May e Kevin Saunderson: uno a testa, in studio."),
        ],
        "reel_cta": "Mandalo a chi suona in piedi",
        # Registrazione della macchina vera (17/10/2026, regola del proprietario:
        # il suono vero in ogni uscita). Licenza verificata sulla pagina;
        # estratto 0:01-0:35; la pagina: «the synth is unmodified and the audio has not been altered».
        "reel_audio": {
            "file": "assets/audio/poly800/registrazione.mp3", "inizio": 0,
            "autore": "Ryan Scott (ry ry of tokyo)", "licenza": "pubblico dominio",
            "fonte": "archive.org",
            "url": "https://archive.org/details/KorgPoly800WallBreakerBassDemoByRyRyOfTokyo",
            "cosa": "un Korg Poly-800 MKI non modificato: un basso con un suono programmato dall'autore",
        },
        "verificata": True,
    },
    {
        "slug": "omnichord",
        "numero": 62,
        "serie": "I GIOCATTOLI",
        "strumento": "Suzuki Omnichord",
        "anno": "1981",
        "luogo": "Giappone",
        "costruttore": "Suzuki",
        "specifiche": [
            ("PRIMO MODELLO", "OM-27, 1981"),
            ("ACCORDI", "27"),
            ("SUONI", "1: arpa"),
            ("FINE", "1996"),
        ],
        "gancio": "Si suona con un dito e le note sono sempre intonate. Eno e Lanois ci hanno fatto «Deep Blue Day»",
        "sottotitolo": "Un'autoarpa elettronica per chi non ha mai suonato.",
        "la_macchina": (
            "Un corpo marrone lucido a forma di paletta. A "
            "sinistra i tasti per gli accordi, al centro una piastra a "
            "strisce da accarezzare con le dita, a destra l'altoparlante. "
            "Si sceglie l'accordo, si striscia il dito e le note escono "
            "arpeggiate. In più c'è un ritmo preimpostato e un basso "
            "automatico. L'OM-27 ha 27 accordi e un solo suono, l'arpa."
        ),
        "inventore_nome": "Suzuki",
        "inventore": (
            "La Suzuki è un'azienda giapponese di famiglia che faceva armoniche "
            "dal 1953. Nel 1981 presenta l'Omnichord insieme al Portachord, "
            "e lo pensa per chi non ha mai suonato e si spaventa davanti a una "
            "tastiera. Nessuna delle fonti che ho trovato dice chi l'ha "
            "disegnato, quindi non lo dico. Nel 1984 escono OM-36 e OM-84, con "
            "più accordi. L'ultimo, l'OM-300, esce intorno al 1996."
        ),
        "come_funziona": (
            "La piastra è elettronica, non ci sono corde: tocchi una striscia e "
            "senti una nota dell'accordo scelto, sempre intonata. Non puoi "
            "sbagliare nota, puoi sbagliare accordo. I primi modelli sono "
            "analogici, dicono le fonti, fino al 1989."
        ),
        "richiami": [
            ("FIG. 1", "Tasti degli accordi: maggiore, minore e settima"),
            ("FIG. 2", "Piastra da strisciare"),
            ("FIG. 3", "Rhythm e altoparlante"),
        ],
        "chi_lusata": [
            {"artista": "Eurythmics", "nota": "il suono d'arpa in «Love Is a Stranger» (1982, ma una fonte dice 1983)", "ig": None},
            {"artista": "Brian Eno e Daniel Lanois", "nota": "«Deep Blue Day» dall'album «Apollo» (1983)", "ig": None},
            {"artista": "Daniel Lanois", "nota": "anche su «Trip Through Your Wires» degli U2 (1987)", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": (
            "Dave Stewart, che ne prese uno in Giappone, lo descrive come un "
            "incrocio fra un giocattolo e uno strumento. Sulla data di «Love Is a Stranger» le "
            "fonti non si mettono d'accordo, 1982 per Wikipedia e 1983 per "
            "un'altra. Nel 1985 Tiny Tim ha scritto sulla copertina di un "
            "suo singolo che era il primo disco suonato tutto con "
            "l'Omnichord. A me piace che, per chi non sa suonare, la prima "
            "regola sia: non puoi sbagliare nota."
        ),
        "avvertenza": "L'OM-27 ha 27 accordi e un solo suono, l'arpa. Se la vostra versione ne ha 36 o 84, non è un OM-27.",
        "foto": {
            "file": "assets/foto/omnichord/om27.jpg",
            "autore": "tico_24",
            "licenza": "CC BY 2.0",
            "fonte": "Wikimedia Commons",
            "ritaglio": True,
        },
        "foto_extra": [
            {"file": "assets/foto/omnichord/interno.jpg",
             "autore": "dana_dane", "licenza": "CC BY-SA 2.0", "fonte": "Wikimedia Commons",
             "didascalia": "Aperto: la scheda, l'altoparlante e la piastra staccata"},
        ],
        "fonti": [
            {"titolo": "«Omnichord» — Wikipedia (EN): Suzuki 1981, OM-27, modelli, Eurythmics, Eno e Lanois, Tiny Tim",
             "url": "https://en.wikipedia.org/wiki/Omnichord", "data": "2026-10-16"},
            {"titolo": "«Suzuki Omnichord history» — Perfect Circuit: 1981, OM-27 con 27 accordi e un solo suono, Eurythmics, Lanois",
             "url": "https://www.perfectcircuit.com/signal/suzuki-omnichord-history", "data": "2026-10-16"},
        ],
        "hashtags": ["#omnichord", "#suzuki", "#strumentielettronici", "#brianeno", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 062", "Basta un dito, e Brian Eno ci fa «Deep Blue Day»"),
            ("SUZUKI · 1981", "Un'autoarpa elettronica per chi non ha mai suonato."),
            ("COME SI SUONA", "Scegli un accordo e striscia il dito sulla piastra."),
            ("IL LIMITE", "L'OM-27 ha 27 accordi e un solo suono: l'arpa."),
            ("1983", "Eno e Lanois lo usano in «Deep Blue Day», dall'album «Apollo»."),
        ],
        "reel_cta": "Mandalo a chi non sa suonare",
        # Registrazione della macchina vera (17/10/2026, regola del proprietario:
        # il suono vero in ogni uscita). Licenza verificata sulla pagina;
        # estratto 0:00-0:16; è un OM-36, non il primo modello, e la didascalia lo dice.
        "reel_audio": {
            "file": "assets/audio/omnichord/registrazione.mp3", "inizio": 0,
            "autore": "InDimension", "licenza": "CC BY-SA 4.0",
            "fonte": "Wikimedia Commons",
            "url": "https://commons.wikimedia.org/wiki/File:Omnichord_Strummed_Sonic_Strings.ogg",
            "cosa": "un Omnichord OM-36, modello successivo all'OM-27 del 1981: le Sonic Strings strisciate sulla piastra",
        },
        "verificata": True,
    },
    # SCARTATI perché a fonte singola (o controversi):
    # - Murzin rifiuta il grado di generale nel 1967 (solo Snob).
    # - Premio Stalin per i congegni di puntamento (solo TechInsider; non trovato
    #   negli elenchi).
    # - costruito nell'appartamento in coabitazione (kommunalka) (solo Snob).
    # - Boris Jankovskij che gli dice che allo Stato non conviene (solo Snob; per
    #   120years Jankovskij e Garbuzov gli danno invece spazio al Conservatorio).
    # - il prototipo troppo grande per casa, quindi al museo di Skrjabin (solo Snob).
    # - Stanislav Krejči che salva l'ANS dalla rottamazione convincendo
    #   l'università (solo Wikipedia e i suoi cloni, es. Monoskop).
    # - Krejči compone disegnando a mano libera (solo il testo di Krejči).
    # - titoli dei pezzi di Schnittke («Potok»), Gubajdulina («Vivente - non
    #   vivente») e Denisov («Il canto degli uccelli») e gli anni 1968-1970
    #   (solo Krejči).
    # - Artem'ev: «impressione sconvolgente» al primo incontro con l'ANS (solo Snob).
    # - suoni di delfini sintetizzati per la Marina, studi sulla voce nei canali
    #   spaziali (solo TechInsider).
    # - dimensioni 180x160x120 cm e anno 1963 del secondo esemplare (solo
    #   TechInsider; altre fonti non danno l'anno).
    # - esposto a Londra e Parigi nel 1958 (solo 120years; TechInsider dice
    #   genericamente «esposizioni internazionali»).
    # - non si può portare al piano di sopra per il peso (solo Electronic Sound).
    # - il prototipo distrutto «poco dopo Solaris» (solo Under the Radar).
    # - la melodia di Bach rifatta sull'ANS (solo The Quietus; EEFB parla di
    #   Bach «alterato» senza dire con cosa).
    # - ESCLUSO apposta: «Stalker». Lo citano RBMA e Snob, ma EEFB scrive che per
    #   «Stalker» (1979) Artem'ev passa al Synthi 100: le fonti non concordano e
    #   la scheda tace.
    # - Alva Noto, «For 2» (2010), brano registrato dal vivo sull'ANS (solo Wikipedia).
    # - registrazione del 2009: il disegno è di Svetlana Bogatyr' (solo
    #   Synthtopia, in traduzione automatica) — per questo «cosa» dice
    #   «scarabocchi», come la pagina Commons.
    {
        "slug": "ans",
        "numero": 63,
        "serie": "LE ORIGINI",
        "strumento": "Sintetizzatore ANS",
        "anno": "1958",
        "luogo": "Mosca, URSS",
        "costruttore": "Evgenij Murzin",
        "specifiche": [
            ("PROTOTIPO", "1958"),
            ("TONI PURI", "720"),
            ("PASSO", "1/6 di semitono"),
            ("SPARTITO", "Vetro e mastice"),
        ],
        "gancio": "Si suona grattando il nero da una lastra di vetro. Ne esiste uno solo, a Mosca",
        "sottotitolo": "Le tre lettere sono le iniziali di Aleksandr Nikolaevič Skrjabin, il compositore che sognava una musica fatta anche di luce.",
        "la_macchina": (
            "Non ha una tastiera da suonare. Davanti c'è un telaio con una lastra "
            "di vetro coperta di mastice nero, e la musica si scrive grattandolo "
            "via. Dove togliete il nero passa la luce, e dove passa la luce c'è un "
            "suono. In verticale si legge l'altezza, in orizzontale il tempo, più "
            "o meno come su un pentagramma. Il mastice non asciuga mai, così uno "
            "sbaglio si cancella spalmandoci sopra altro nero. A me sembra l'unico "
            "strumento del catalogo che si suona più con gli occhi che con le "
            "mani, e non sono sicuro che sia un difetto."
        ),
        "inventore_nome": "Evgenij Murzin",
        "inventore": (
            "Murzin nasce a Samara nel 1914 e di mestiere fa l'ingegnere militare. "
            "Durante la guerra progetta apparecchi per il tiro contraereo, dopo "
            "sistemi di difesa aerea. La musica è la sua passione privata, e "
            "Skrjabin la sua fissa. L'idea gli viene dal cinema sonoro, che scrive "
            "il suono sulla pellicola come una striscia di luce e lo rilegge con "
            "una fotocellula. Sull'anno le fonti non concordano, chi dice 1937, "
            "chi 1938, chi 1939. Poi la guerra lo ferma. Ci lavora quasi vent'anni "
            "nel tempo libero, senza aspettare un rublo dallo Stato, e il "
            "prototipo è pronto nel 1958. Muore nel 1970."
        ),
        "come_funziona": (
            "Il suono parte da 5 dischi di vetro che girano. Su ognuno Murzin ha "
            "stampato 144 piste, con un procedimento inventato da lui, e ogni "
            "pista attraversata dalla luce dà un tono puro: 720 in tutto, a un "
            "sesto di semitono l'uno dall'altro, su 10 ottave. Quella luce arriva "
            "dietro la lastra. Dove il mastice è grattato passa, e 20 fotocellule "
            "la trasformano in corrente, ciascuna col suo filtro e il suo volume. "
            "La lastra scorre a motore o a mano, anche fino a fermarsi, e la "
            "velocità cambia la durata senza toccare l'intonazione. Provate a "
            "immaginare un graffio verticale. Accende tutte le note insieme, ed "
            "esce un fruscio."
        ),
        "richiami": [
            ("FIG. 1", "Lastra di vetro e mastice nero"),
            ("FIG. 2", "5 dischi, 720 toni puri"),
            ("FIG. 3", "20 fotocellule, 20 filtri"),
        ],
        "chi_lusata": [
            {"artista": "Eduard Artem'ev", "nota": "«Solaris» (1972) e «Lo specchio» (1975) di Andrej Tarkovskij", "ig": None},
            {"artista": "Stanislav Krejči", "nota": "nel laboratorio di Murzin dal 1961; il suo disco «ANS» esce con la Melodija nel 1970", "ig": None},
            {"artista": "Alfred Schnittke, Sofija Gubajdulina, Edison Denisov", "nota": "i loro pezzi per ANS stanno nella raccolta Melodija «Muzykal'noe prinošenie» (1990)", "ig": None},
            {"artista": "Coil", "nota": "«ANS», un cofanetto di drone registrati tutti sulla macchina di Mosca", "ig": None},
            {"artista": "Il cinema sovietico", "nota": "anche la commedia di Leonid Gajdaj «Il braccio di diamante» (1969)", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": (
            "Intorno al 1960 il prototipo trasloca in un posto che sembra scelto "
            "apposta, la casa-museo di Skrjabin a Mosca. Lì, intorno all'ANS, "
            "nasce il primo studio di musica elettronica dell'Unione Sovietica. "
            "Nel 1961 arriva Stanislav Krejči, compositore e tecnico del suono. "
            "Passano di lì Schnittke, la Gubajdulina, Denisov e un giovane Eduard "
            "Artem'ev. Più avanti lo studio finisce sotto la Melodija, la casa "
            "discografica di Stato, e in serie l'ANS non ci andrà mai. Quello che "
            "sta oggi al Museo Glinka è il secondo esemplare, costruito dopo. Il "
            "prototipo del 1958 non c'è più."
        ),
        "avvertenza": "Il mastice sulla lastra non asciuga mai. Tenete lontane le maniche: ogni graffio lascia passare la luce, e qui la luce è una nota.",
        "da_ascoltare": {"brano": "Solaris (colonna sonora)", "artista": "Eduard Artem'ev", "anno": "1972",
                         "cosa": "L'organo di Bach lo riconoscete. Ascoltate il resto, i suoni che non sapreste dire da che strumento escano: lì dentro c'è l'ANS."},
        "foto": {
            "file": "assets/foto/ans/principale.jpg",
            "autore": "Charles Hutchins (Celesteh)",
            "licenza": "CC BY 2.0",
            "fonte": "Wikimedia Commons",
            "didascalia": "L'ANS com'è oggi, al Museo Glinka di Mosca",
        },
        "foto_extra": [
            {"file": "assets/foto/ans/lastra.jpg",
             "autore": "Stardancer", "licenza": "CC BY-SA 3.0",
             "fonte": "Wikimedia Commons", "posizione": "center",
             "didascalia": "La lastra nel suo telaio, col mastice nero già graffiato (Theremin Center, 2006)"},
        ],
        "fonti": [
            {"titolo": "«ANS synthesizer» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/ANS_synthesizer", "data": "2026-10-20"},
            {"titolo": "S. Krejči, «The ANS Synthesizer» — Theremin Center, 1997",
             "url": "http://www.theremin.ru/archive/ans.htm", "data": "2026-10-20"},
            {"titolo": "«The ANS Synthesiser» — 120 Years of Electronic Music",
             "url": "https://120years.net/the-ans-synthesisereugeniy-murzinsoviet-union1958-2/", "data": "2026-10-20"},
            {"titolo": "«Synth-Aesthesia: Soviet Synths And The ANS» — RBMA Daily, 2012",
             "url": "https://daily.redbullmusicacademy.com/2012/08/history-soviet-synth-ans", "data": "2026-10-20"},
            {"titolo": "«Космическая музыка» — Snob",
             "url": "https://snob.ru/history/kosmicheskaya-muzyka-kto-pridumal-sintezator/", "data": "2026-10-20"},
            {"titolo": "«Синтезатор АНС» — TechInsider, 2013",
             "url": "https://www.techinsider.ru/design/14888-pervyy-v-mire-mnogogolosnyy-muzykalnyy-sintezator-ans/", "data": "2026-10-20"},
            {"titolo": "«Musical Offering» — Electronic Sound",
             "url": "https://www.electronicsound.co.uk/?p=17204", "data": "2026-10-20"},
            {"titolo": "«Eduard Artemyev's Compositional Strategies» — EEFB",
             "url": "https://eefb.org/retrospectives/eduard-artemyevs-compositional-strategies/", "data": "2026-10-20"},
        ],
        "hashtags": ["#anssynthesizer", "#murzin", "#sintetizzatore", "#tarkovsky", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 063", "I suoni strani di «Solaris» nascono grattando un vetro nero."),
            ("720 NOTE, NESSUN TASTO", "L'ANS si suona su un vetro col mastice nero. Dove gratti passa la luce."),
            ("MOSCA · FINE ANNI '30", "Evgenij Murzin, ingegnere militare, prende l'idea dal sonoro del cinema."),
            ("1958 · A.N.S.", "Murzin finisce l'ANS dopo vent'anni e gli dà le iniziali di Skrjabin."),
            ("TARKOVSKIJ · 1972", "Eduard Artem'ev ci scrive «Solaris». Oggi l'ANS è uno solo, a Mosca."),
        ],
        "reel_cta": "Mandalo a chi ha visto «Solaris» fino in fondo",
        # Registrazione della macchina vera (regola del 17/10/2026). Licenza
        # ricontrollata sulla pagina il 20/10/2026. Tratto da confermare
        # all'ascolto (vedi commento in testa): provvisorio 0:00-0:45.
        "reel_audio": {
            "file": "assets/audio/ans/registrazione.mp3", "inizio": 0,
            "autore": "octopusvision (Maxim Tarashchenko)", "licenza": "CC BY-SA 3.0",
            "fonte": "Wikimedia Commons",
            "url": "https://commons.wikimedia.org/wiki/File:The_ANS_Synthesizer_playing_doodles_(live).ogg",
            "cosa": "l'ANS vero, in una dimostrazione dal vivo a Mosca il 21 ottobre 2009: la macchina legge scarabocchi graffiati sul mastice di una lastra",
        },
        "verificata": True,
    },
    # ---------------------------------------------------------------- 64
    # Rifornimento del 20/10/2026. Audio: «inizio» è 0 perché il file è già
    # l'estratto tagliato (tratto scelto sullo spettrogramma, vedi sotto).
    # Scheda: Roland JD-800 (1991). Scritta il 2026-10-20.
    #
    # FOTO (tutte di Pete Brown, Flickr album «Roland JD-800 Restoration»,
    # CC BY 2.0, importate su Commons; guardate una per una, 960 px):
    # - principale: pannello restaurato con i cursori, il display («I-27:Killer
    #   Pad», «TVA:Level») e la tastiera; a sinistra il logo e' tagliato, ma
    #   nessun altro marchio e' leggibile e la macchina e' riconoscibile.
    #   Pagina: https://commons.wikimedia.org/wiki/File:Roland_JD-800_Restoration_-_Restoration_Complete!_(2015-06-26_22.52.59_by_Pete_Brown).jpg
    #   Thumbnail 1280: https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Roland_JD-800_Restoration_-_Restoration_Complete%21_%282015-06-26_22.52.59_by_Pete_Brown%29.jpg/1280px-Roland_JD-800_Restoration_-_Restoration_Complete%21_%282015-06-26_22.52.59_by_Pete_Brown%29.jpg
    # - pesi.jpg (slide 2): sotto la tastiera, i pesi neri dei tasti; il titolo
    #   su Commons dice «New keyboard weights. No red glue.». VERTICALE: il
    #   thumbnail di Wikimedia esce gia' ruotato (l'originale e' 5376x3024 con
    #   tag EXIF di rotazione), quindi scaricare il thumbnail, non l'originale.
    #   Da sola non si capisce: nel_reel False.
    #   Pagina: https://commons.wikimedia.org/wiki/File:Roland_JD-800_Restoration_-_New_keyboard_weights._No_red_glue._(2015-06-26_22.25.00_by_Pete_Brown).jpg
    #   Thumbnail 1280: https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Roland_JD-800_Restoration_-_New_keyboard_weights._No_red_glue._%282015-06-26_22.25.00_by_Pete_Brown%29.jpg/1280px-Roland_JD-800_Restoration_-_New_keyboard_weights._No_red_glue._%282015-06-26_22.25.00_by_Pete_Brown%29.jpg
    # - display.jpg (slide 3): primo piano del display, «SINGLE 015 CH:01 /
    #   I-27:Killer Pad» a sinistra, «TVA:Level 50 50» con TONE A, TONE B a destra.
    #   Pagina: https://commons.wikimedia.org/wiki/File:Roland_JD-800_Restoration_-_I-27_Killer_Pad_(2015-06-26_22.52.34_by_Pete_Brown).jpg
    #   Thumbnail 1280: https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Roland_JD-800_Restoration_-_I-27_Killer_Pad_%282015-06-26_22.52.34_by_Pete_Brown%29.jpg/1280px-Roland_JD-800_Restoration_-_I-27_Killer_Pad_%282015-06-26_22.52.34_by_Pete_Brown%29.jpg
    # - cursori.jpg (slide 4): le schede dei cursori smontate, file di
    #   potenziometri neri a slitta, «Roland» stampato sui circuiti.
    #   Pagina: https://commons.wikimedia.org/wiki/File:Roland_JD-800_Restoration_-_Cleaned_up_and_reinstalled_(2015-06-26_22.01.09_by_Pete_Brown).jpg
    #   Thumbnail 1280: https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Roland_JD-800_Restoration_-_Cleaned_up_and_reinstalled_%282015-06-26_22.01.09_by_Pete_Brown%29.jpg/1280px-Roland_JD-800_Restoration_-_Cleaned_up_and_reinstalled_%282015-06-26_22.01.09_by_Pete_Brown%29.jpg
    # Scartate: «Roland JD-800.jpg» (intera, ma 490x202 e di provenienza
    # incerta), «Jazzkatte.jpg» (tre tastiere e due gatti, il JD-800 non si
    # distingue), «About to clean the panel» (pannello senza cappucci e con
    # l'asciugamano dentro le feritoie), la foto del concerto di byCharly
    # (la macchina in primo piano e' il Korg Mono/Poly).
    #
    # AUDIO. Delle due registrazioni proposte nessuna dimostra la macchina
    # vera, quindi in reel_audio c'e' una terza:
    # - freesound.org/s/534782 (XHALE303, CC0, 17,5 s, «Tools: JD800»),
    #   caricata l'11/09/2020. Prima delle emulazioni ufficiali Roland
    #   (espansione per ZENOLOGY a inizio 2021, plug-in il 26/10/2021), ma
    #   l'autore lavora con librerie Kontakt (ProjectSAM, Heavyocity Damage
    #   nelle altre descrizioni): «JD800» puo' essere la tastiera o una
    #   libreria di campioni. Non dimostrabile. Suona bene: pad pieno da 0 a
    #   ~14 s, poi sfuma. Anteprima: https://cdn.freesound.org/previews/534/534782_9015615-hq.mp3
    # - freesound.org/s/802134 (Krivo_ok, CC BY 4.0, 18,6 s, «Simple chords
    #   with Rolands JD800»), caricata il 27/04/2025, quando esistono sia il
    #   plug-in Roland sia il JD-08: non dimostrabile.
    #   Anteprima: https://cdn.freesound.org/previews/802/802134_7570820-hq.mp3
    # - SCELTA: freesound.org/s/58 (fectoper, CC BY 4.0, 59,8 s), caricata
    #   l'11/03/2005, «A kind of abstract ambient patch programmed with a a
    #   Roland JD-800 synth». Nel 2005 di JD-800 software non ce n'erano:
    #   e' la tastiera vera. Difetti: mono, 22,05 kHz, livello basso per
    #   quasi tutto il file. RMS misurato secondo per secondo sull'anteprima:
    #   0-6 s quasi silenzio, 7-38 s tappeto a -30/-37 dBFS, 39-48 s il
    #   tratto pieno a -20/-24 dBFS, poi sfuma fino al silenzio a 58 s.
    #   inizio 39: parte pieno dal fotogramma 0, ma dopo 10 s cala e verso i
    #   17-19 s del reel e' quasi muto.
    #   Anteprima: https://cdn.freesound.org/previews/0/58_45-hq.mp3
    #   (la -lq e' https://cdn.freesound.org/previews/0/58_45-lq.mp3)
    #   Se si preferisce la 534782 (CC0), «cosa» va riscritto dicendo che
    #   l'autore scrive «JD800» senza dire se e' la tastiera.
    # FATTI E FONTI (due indipendenti per ognuno):
    # - 1991; 108 forme d'onda; 24 voci, 6 con 4 strati; 4 strati per suono;
    #   64 suoni; 1.699 sterline: SOS apr. 1991 (Colbeck), Music Technology
    #   giu. 1991 (Trask), Wikipedia, SOS 2005 (Reid). 44,1 kHz: Colbeck,
    #   Roland «Story of the JD-800», Wikipedia.
    # - prima del JD-800 rotella e display di due righe anche in Roland: Reid
    #   (SOS 2005: «one data wheel and a two-line LCD»); routine post-DX7 a
    #   pagine: Colbeck e Trask.
    # - 69 parametri per strato con un comando dedicato: Trask («69
    #   synthesis parameters per Tone have dedicated knobs, sliders or
    #   switches») e Roland («69 sliders and buttons»).
    # - cursori che fanno saltare il valore: Trask (il D70 invece aspetta di
    #   passare sul valore) e Wikipedia.
    # - filtro LPF/HPF/BPF risonante, 3 inviluppi, effetti: Reid, Wikipedia,
    #   Trask, Polynominal.
    # - Persing: forme d'onda e suoni di fabbrica (Wikipedia, Spectrasonics
    #   https://www.spectrasonics.net/company/other/ep-roland.php, Roland,
    #   Synthanatomy); R&D-LA a Culver City, breve vita, primo prodotto metà
    #   Giappone e metà LA (Wikipedia, Roland); capo sound designer 1984-2004
    #   e D-50 (Wikipedia «Eric Persing», Roland); Spectrasonics e Omnisphere
    #   (Wikipedia, Spectrasonics). Crystal Rhodes e' suo: Spectrasonics
    #   https://www.spectrasonics.net/products/keyscape/models/jd800-crystal-ep/
    #   e Roland (articolo su Prince), Guitarcloud.
    # - fine produzione: Wikipedia 1996, Vintage Synth Explorer 1993
    #   (https://www.vintagesynth.com/roland/jd-800). Detto come dubbio.
    # - colla rossa: Polynominal («red resin under the keys drips over
    #   mainboard … dead contacts»), Vintage Synth Explorer («red goo of
    #   death»), titolo della foto su Commons («No red glue»), matrixsynth
    #   (https://www.matrixsynth.com/2019/08/roland-jd-800-synthesizer-pristine.html).
    # - Prince, «Love Symbol» e «Damn U» con Crystal Rhodes: Roland (citazione
    #   di Barbarella) e Guitarcloud (che cita Barbarella con i numeri dei preset).
    # - Jarre, «Chronologie»: Wikipedia (dal libretto, Dreyfus FDM 36152-2) e
    #   matrixsynth (Arte 1993, Jarre mostra il JD800 in tour):
    #   https://www.matrixsynth.com/2012/02/jean-michel-jarre-megamix-arte.html
    # - Howlett: Future Music 1993 (lo aveva, non gli piaceva, scambiato con
    #   un Jupiter-8 ora rotto; buono per i bassi con l'enhancer; usato nella
    #   versione su album di «Fire») e SOS 1996 (provato in negozio dopo aver
    #   venduto gli analogici, «within a week I wasn't happy», un anno dopo il
    #   JD-990). «Fire» anche nella pagina strumenti di theprodigy.info
    #   (https://theprodigy.info/equipment/roland-jd-800.html).
    # - JD-990 da rack nel 1993: Wikipedia, Roland, SOS 2021 (Wherry).
    # - software Roland 2021 con i 64 suoni originali: comunicato Roland
    #   (https://www.roland.com/us/company/press_releases/2021/Roland-Announces-JD-800-Software-Synthesizer/)
    #   e Synthanatomy (https://synthanatomy.com/2021/10/roland-releases-jd-800-synthesizer-plugin-onto-roland-cloud.html).
    #
    # SCARTATI PERCHÉ A FONTE SINGOLA (o solo Roland, cioe' il costruttore
    # che parla di se' in due articoli):
    # - Kazuhisa Takahashi capo progetto, la frustrazione per i display, lo
    #   sviluppo dall'autunno 1989 (solo Roland «Story of the JD-800»);
    # - il colore pensato nero e l'aria da «bombardiere stealth»; i
    #   processori separati contro il ritardo del D-50; «Ac. Piano 1» unico
    #   campione acustico voluto dal commerciale; 128 passi dei cursori (solo
    #   Roland);
    # - Persing che programma il JD-800 accanto a Marcus Miller per «The King
    #   Is Gone» (solo Roland); Tony Banks e «I Can't Dance» (solo Roland);
    #   il basso di «Voodoo People» (Roland; e Howlett nel 1996 dice di averlo
    #   dato via presto: contraddetto, tolto);
    # - Prince che sega due JD-800 per farne uno ibrido (Keyboard 1999 via
    #   Guitarcloud, poi ripreso da Roland che cita Guitarcloud: non indipendenti);
    # - Mouse on Mars, A Guy Called Gerald «Anything», Sasha, Air Liquide
    #   (solo Roland, Equipboard copia lo stesso testo); Kevin Moore e
    #   «Images and Words» (solo ipotesi in un'intervista);
    # - prezzo USA 2.895 dollari (solo Wikipedia); 61 cursori (solo
    #   Polynominal: il numero non torna con le altre fonti, quindi niente
    #   conteggio dei cursori, solo i 69 parametri);
    # - Persing chiamato da Tom Beckman al NAMM 1984; Spectrasonics fondata
    #   nel 1994 con la moglie (solo Wikipedia);
    # - Crystal Rhodes «in quasi tutti i dischi pop dell'epoca» (Spectrasonics,
    #   cioè Persing su se stesso: superlativo vago, comunque fuori).
    {
        "slug": "jd800",
        "numero": 64,
        "serie": "I SINTETIZZATORI",
        "strumento": "Roland JD-800",
        "anno": "1991",
        "luogo": "Giappone e Los Angeles",
        "costruttore": "Roland",
        "specifiche": [
            ("USCITA", "1991"),
            ("VOCI", "24"),
            ("FORME D'ONDA", "108"),
            ("PREZZO UK", "1.699 £"),
        ],
        "gancio": "Otto anni di menu dopo il DX7, Roland rimette i cursori su un synth digitale",
        "sottotitolo": "108 forme d'onda campionate a 44,1 kHz, 24 voci, 4 strati per suono e un pannello che sembra il banco di un mixer.",
        "la_macchina": (
            "Sul pannello, le file di cursori grigi muovono tutte il suono: "
            "inviluppi, filtro, i due LFO, il volume di ognuno dei 4 strati. Nel "
            "1991 un synth digitale si programmava con una rotella e un display di "
            "due righe, pagina dopo pagina, e la stessa Roland li faceva così da "
            "anni. Il JD-800 dà un comando suo a 69 parametri. Secondo me è la "
            "macchina più bella da toccare di tutto il catalogo. Se ne trovate uno "
            "usato, chiedete della colla rossa. I pesi sotto i tasti erano "
            "incollati con una resina che col tempo cola sui contatti, e i tasti "
            "smettono di suonare."
        ),
        "inventore_nome": "Eric Persing",
        "inventore": (
            "Il JD-800 è il primo prodotto Roland progettato metà in Giappone e "
            "metà a Los Angeles, in un ufficio piccolo di Culver City che è durato "
            "pochi anni. Lì Eric Persing fa tutte le 108 forme d'onda e i 64 suoni "
            "di fabbrica. In Roland è il capo dei sound designer dal 1984 al 2004, "
            "e prima aveva fatto i suoni del D-50. Uno dei suoi preset è un piano "
            "elettrico che si chiama Crystal Rhodes. Tenetelo a mente per la slide "
            "5. Più tardi Persing ha fondato Spectrasonics, quella di Omnisphere. "
            "Su quando il JD-800 sia uscito di produzione le fonti non concordano, "
            "c'è chi scrive 1993 e chi 1996."
        ),
        "come_funziona": (
            "Il suono parte da una delle 108 forme d'onda in memoria, registrate a "
            "44,1 kHz. Ci sono onde classiche da synth, pezzi di strumenti messi in "
            "ciclo, attacchi brevi. Poi passa in un filtro passa-basso, passa-alto "
            "o passa-banda con la risonanza, e in tre inviluppi, per l'altezza, il "
            "filtro e il volume. Questo è uno strato. Un suono ne mette insieme "
            "fino a 4, e qui c'è un conto da fare: le voci sono 24 con uno strato "
            "solo, 6 con quattro. In fondo c'è una catena di effetti con "
            "distorsione, phaser, chorus, delay e riverbero. Di analogico non c'è "
            "niente, anche se il pannello ve lo fa credere."
        ),
        "richiami": [
            ("FIG. 1", "108 forme d'onda a 44,1 kHz"),
            ("FIG. 2", "Filtro LPF, HPF, BPF con risonanza"),
            ("FIG. 3", "4 strati: 24 voci, 6 a strati pieni"),
        ],
        "chi_lusata": [
            {"artista": "Prince", "nota": "«Love Symbol» (1992): secondo il tastierista Tommy Barbarella c'è dappertutto", "ig": None},
            {"artista": "Jean-Michel Jarre", "nota": "«Chronologie» (1993): il JD 800 è nella lista delle macchine sul libretto", "ig": "jeanmicheljarre"},
            {"artista": "The Prodigy", "nota": "«Experience» (1992), nella versione di «Fire» che sta sull'album", "ig": None},
        ],
        # @rolandglobal e @jeanmicheljarre sono gia' usati e verificati in
        # contenuti.py (schede 808, 909, Space Echo; Oxygène, Synthex).
        "menzioni_extra": [
            {"ig": "rolandglobal",
             "riga": "Nel 2021 @rolandglobal l'ha rifatto in software, con i 64 suoni originali."},
        ],
        "aneddoto": (
            "Liam Howlett dei Prodigy vende i suoi synth analogici. In un negozio "
            "prova un JD-800, gli sembra che abbia la sensazione dell'analogico e "
            "lo compra. A casa, racconta, entro una settimana sa che non gli "
            "piace. Fa in tempo a usarlo nella versione di «Fire» che sta "
            "sull'album, e a Future Music dice che per i bassi è buono, per via "
            "dell'enhancer. Poi lo scambia con un Jupiter-8, che quando rilascia "
            "l'intervista si è già rotto. Un anno dopo aver dato via il JD-800 si "
            "compra il JD-990, la versione da rack, senza cursori."
        ),
        "avvertenza": "Richiamato un suono, i cursori restano dove li avevate lasciati. Toccatene uno e il valore salta lì di colpo, anche con la nota tenuta.",
        "da_ascoltare": {"brano": "Damn U", "artista": "Prince", "anno": "1992",
                         "cosa": "Dentro c'è il preset Crystal Rhodes. Lo racconta Tommy Barbarella, che suonava le tastiere con Prince nei New Power Generation."},
        "foto": {
            "file": "assets/foto/jd800/principale.jpg",
            "autore": "Pete Brown",
            "licenza": "CC BY 2.0",
            "fonte": "Wikimedia Commons",
            "didascalia": "Un JD-800 appena restaurato. Sul display, il suono I-27",
        },
        "foto_extra": [
            {"file": "assets/foto/jd800/pesi.jpg",
             "autore": "Pete Brown", "licenza": "CC BY 2.0", "fonte": "Wikimedia Commons",
             "posizione": "center", "nel_reel": False,
             "didascalia": "Sotto la tastiera: i pesi dei tasti rimessi senza la colla rossa"},
            {"file": "assets/foto/jd800/display.jpg",
             "autore": "Pete Brown", "licenza": "CC BY 2.0", "fonte": "Wikimedia Commons",
             "posizione": "center",
             "didascalia": "Il display: a sinistra il nome del suono, a destra il parametro toccato"},
            {"file": "assets/foto/jd800/cursori.jpg",
             "autore": "Pete Brown", "licenza": "CC BY 2.0", "fonte": "Wikimedia Commons",
             "posizione": "center",
             "didascalia": "Le schede dei cursori, smontate durante un restauro"},
        ],
        "fonti": [
            {"titolo": "«Knobular Synthesis» — Sound On Sound, aprile 1991",
             "url": "https://www.muzines.co.uk/articles/knobular-synthesis/7410", "data": "2026-10-20"},
            {"titolo": "«Roland JD800» — Music Technology, giugno 1991",
             "url": "https://www.muzines.co.uk/articles/roland-jd800/821", "data": "2026-10-20"},
            {"titolo": "«The History of Roland, Part 3» — Sound On Sound, 2005",
             "url": "https://www.soundonsound.com/music-business/history-roland-part-3", "data": "2026-10-20"},
            {"titolo": "«Roland JD-800» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Roland_JD-800", "data": "2026-10-20"},
            {"titolo": "«Eric Persing and the JD-800» — Roland, 2021",
             "url": "https://articles.roland.com/digital-dreams-eric-persing-and-the-jd-800/", "data": "2026-10-20"},
            {"titolo": "«Prince e il JD-800» — Roland, 2021",
             "url": "https://articles.roland.com/?p=40800", "data": "2026-10-20"},
            {"titolo": "«Roland JD-800» — Guitarcloud (Prince)",
             "url": "https://guitarcloud.org/equipment/roland-jd-800/", "data": "2026-10-20"},
            {"titolo": "Liam Howlett — Future Music, febbraio 1993",
             "url": "https://theprodigy.info/articles/prodigious-talent.html", "data": "2026-10-20"},
            {"titolo": "Liam Howlett — Sound On Sound, 1996",
             "url": "https://theprodigy.info/articles/sound_on_sound_1996.html", "data": "2026-10-20"},
            {"titolo": "«Roland JD-800» — Polynominal (la resina rossa)",
             "url": "https://www.polynominal.com/m/roland-jd-800.htm", "data": "2026-10-20"},
        ],
        "hashtags": ["#jd800", "#roland", "#sintetizzatore", "#prince", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 064", "Il Roland JD-800 riporta i cursori sui synth digitali"),
            ("ANNI '80", "Dal DX7 in poi un synth digitale si programma a menu, una pagina per volta."),
            ("ROLAND · 1991", "Sul pannello del JD-800, 69 parametri hanno un comando ciascuno."),
            ("LOS ANGELES", "Eric Persing ci programma i 64 suoni di fabbrica. Uno è Crystal Rhodes."),
            ("PRINCE · 1992", "Prince mette Crystal Rhodes in «Damn U», dal disco «Love Symbol»."),
        ],
        "reel_cta": "Mandalo a chi passa le ore dentro i menu",
        # Registrazione: freesound.org/s/58, licenza ricontrollata sulla pagina
        # (Attribution 4.0). Caricata l'11/03/2005, prima di qualunque JD-800
        # software: e' la tastiera vera. Tratto pieno 0:39-0:49, poi sfuma.
        # Anteprima: https://cdn.freesound.org/previews/0/58_45-hq.mp3
        "reel_audio": {
            "file": "assets/audio/jd800/registrazione.mp3", "inizio": 0,
            "autore": "fectoper", "licenza": "CC BY 4.0",
            "fonte": "freesound.org/s/58",
            "url": "https://freesound.org/s/58/",
            "cosa": "un JD-800 vero, nel 2005: un pad ambient programmato da chi l'ha registrato, in mono e a bassa risoluzione",
        },
        "verificata": True,
    },
    # ---------------------------------------------------------------- 65
    # Rifornimento del 20/10/2026. Audio: «inizio» è 0 perché il file è già
    # l'estratto tagliato (tratto scelto sullo spettrogramma, vedi sotto).
    # Scheda «polivoks» — scritta il 2026-10-20.
    #
    # FOTO (tutte viste: thumbnail scaricati e guardati)
    # principale: https://commons.wikimedia.org/wiki/File:Polivoks_new.jpg
    #   OriginalJambo, CC BY-SA 4.0, 3999x2000, 2023
    #   thumb 1280: https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Polivoks_new.jpg/1280px-Polivoks_new.jpg
    #   Foto 2:1, macchina intera di fronte su un tavolo di legno: "ritaglio": True
    #   perché in copertina si veda tutta, tastiera compresa.
    # extra 1: https://commons.wikimedia.org/wiki/File:Polivoks_(closeup).jpg
    #   Rob Sinclair, CC BY-SA 2.0, 3622x2415, bianco e nero
    #   thumb 1280: https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Polivoks_%28closeup%29.jpg/1280px-Polivoks_%28closeup%29.jpg
    #   Si vedono ПОЛИВОКС col logo, ГЕНЕРАТОР I e II, МИКШЕР, e a destra
    #   ФИЛЬТР con ЧАСТОТА СРЕЗА e РЕЗОНАНС. Il cirillico è ovunque, quindi la
    #   didascalia regge con qualunque ritaglio.
    # extra 2: https://commons.wikimedia.org/wiki/File:%D0%91%D1%80%D0%B5%D0%BD%D0%B4%D1%8B_%D1%81%D0%BE%D0%B2%D0%B5%D1%82%D1%81%D0%BA%D0%BE%D0%B3%D0%BE_%D0%A3%D1%80%D0%B0%D0%BB%D0%B0_38.jpg
    #   Леонид Макаров (Leonid Makarov), CC0, 4000x2256, 13/02/2021; categoria
    #   «Brands of the Soviet Urals - The Museum of History and Archeology of the Urals»
    #   thumb 1280: https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/%D0%91%D1%80%D0%B5%D0%BD%D0%B4%D1%8B_%D1%81%D0%BE%D0%B2%D0%B5%D1%82%D1%81%D0%BA%D0%BE%D0%B3%D0%BE_%D0%A3%D1%80%D0%B0%D0%BB%D0%B0_38.jpg/1280px-%D0%91%D1%80%D0%B5%D0%BD%D0%B4%D1%8B_%D1%81%D0%BE%D0%B2%D0%B5%D1%82%D1%81%D0%BA%D0%BE%D0%B3%D0%BE_%D0%A3%D1%80%D0%B0%D0%BB%D0%B0_38.jpg
    #   Polivoks in vetrina con un pedale davanti, riflessi del vetro sopra la
    #   macchina: "nel_reel": False (nel reel i riflessi sembrerebbero un difetto).
    #
    # AUDIO
    # pagina: https://freesound.org/s/148940/  (odo-ada, CC0 — ricontrollato sulla
    #   pagina il 2026-10-20; «Vladimir Kuzmin, engineer of the popular "polivoks"
    #   synthesizer gives a demonstration of his invention. recorded may 2002 in
    #   yekaterinburg on minidisc with Soundman binaural microphones»; 3:55)
    # file: https://cdn.freesound.org/previews/148/148940_37247-hq.mp3
    #   (l'anteprima -lq.mp3 è confermata dal lettore incorporato di Freesound;
    #   la -hq segue lo stesso schema. Dal container cdn.freesound.org dà 403:
    #   va scaricato dal runner.)
    # TRATTO: 211-235 s (fino alla fine del file). Non ho potuto ascoltarlo: il
    #   tratto è ricavato dallo spettrogramma e dalla forma d'onda di Freesound
    #   (780 px = 235,5 s), misurando quanto restano ferme le armoniche colonna
    #   per colonna. Fra 213 e 229 s ci sono note tenute forti, righe orizzontali
    #   pulite, l'ampiezza più alta del file: è la macchina. Seconda scelta
    #   99-115 s (stessa firma, ampiezza più bassa). Nel resto le note sono brevi
    #   e in mezzo c'è il parlato irregolare. DA RIASCOLTARE prima di montare:
    #   è una registrazione d'ambiente e una voce sotto le note non si vede.
    #
    # DA ASCOLTARE omesso apposta: le attribuzioni a un brano preciso sono tutte a
    #   fonte singola («Black Cherry» e «Train» di Goldfrapp: solo Sound On Sound
    #   2003; «Ulysses» di Franz Ferdinand: solo Wikipedia, che cita un critico
    #   non raggiungibile; «Hellwalker» di Mick Gordon: solo una tesina). Gli
    #   ALBUM invece hanno 3-5 fonti e stanno in chi_lusata.
    #
    # Timbro: lo slug va aggiunto a suoni.VOCE_SCHEDA (valida_scheda lo pretende).
    # FONTI PER FATTO (chi regge cosa)
    # - filtro 12 dB, 2 op-amp + 6 resistenze, niente condensatori discreti
    #   (capacità interna degli op-amp): SOS 2010, Cherry Audio (Mark Barton);
    #   12 dB e passa-basso/passa-banda anche MusicTech «USSR vs ADSR».
    # - voleva il suono del Minimoog / la «dolcezza» del Moog: Synthtopia 2009, Cherry Audio.
    # - quasi un anno sul filtro: SOS 2010, Synthtopia 2009.
    # - suono ruvido/sporco: SOS 2010 («harsh, abrasive, distorted», specie con
    #   la risonanza alta), Cherry Audio («rough-sounding»).
    # - inviluppi in loop AD: SOS 2010, Synthtopia 2009, MusicTech.
    # - pannello a gradini = moduli sotto: SOS 2010 (schede su backplane, comandi
    #   distanziati per i moduli), RBMA 2016 («3D control panel shows the module structure»).
    # - duofonico, 2 oscillatori: SOS 2010, Gearnews, Synthtopia 2009, Wikipedia.
    # - 920 rubli: SOS 2010, RBMA 2016, Moscow Times 2009, Synthtopia 2009.
    # - troppo caro per i singoli, comprato da enti culturali: SOS 2010, RBMA 2016.
    # - numeri: Kuzmin ~25.000 (RBMA), 20-30.000 (SOS); >100.000 (Moscow Times,
    #   Synthtopia 2009). Scritto come disaccordo.
    # - Vladivostok 1953: RBMA 2016, Fontanka 2026.
    # - bassista nella band universitaria: SOS 2010, RBMA 2016. Laurea 1976: idem.
    # - Vector fabbrica nata in guerra, a Ekaterinburg: SOS 2010 (radici nella
    #   seconda guerra mondiale), RBMA 2016 («former war factory»).
    # - Feofilov nella squadra: SOS 2010 (Pheophilov), Fontanka 2026 (Fiofilov).
    # - Olimpiada e le radio militari: Moscow Times 2009, Fontanka 2026, Synthtopia 2009.
    # - Moog, Korg, Roland come modello: RBMA 2016, Fontanka 2026 (Synthtopia
    #   2009: «American and Japanese synths»).
    # - prototipo 1980, produzione 1982: Izvestia 2026, Synthtopia 2026; 1982-1990
    #   anche SOS, RBMA, Moscow Times. Kachkanar/Formanta: SOS 2010, MusicTech.
    # - morto il 12/06/2026: Synthtopia 2026 (annuncio Elta Music), Izvestia 2026,
    #   Fontanka 2026; 72 anni: Fontanka (TASS), coerente con la nascita 13/10/1953.
    # - nessuna vendita fuori dall'URSS fino al 1991: SOS 2010, RBMA 2016.
    # - anni '90 Germania/Polonia, techno dura e industriale: RBMA 2016 (Germania,
    #   Polonia, hard techno, industrial), SOS 2010 (hard techno, industrial).
    # - Kuzmin scopre la fama con internet a inizio anni 2000: RBMA 2016, SOS 2010 («until around 2002»).
    # - registrazione maggio 2002 a Ekaterinburg: pagina Freesound (è la
    #   registrazione stessa).
    # - Franz Ferdinand, «Tonight» (2009): SOS (pagina audio, «all over»),
    #   RBMA, Moscow Times, MusicTech. Goldfrapp, «Black Cherry»: SOS 2003, RBMA,
    #   MusicTech, Moscow Times. Mick Gordon, Doom 2016: Gearnews, Fontanka.
    # - Instagram: @franz_ferdinand dal link di franzferdinand.com
    #   (franzferdinand.ffm.to/ig → instagram.com/franz_ferdinand/);
    #   @goldfrappmusic dal link di goldfrapp.com. Da seguire prima dell'uscita.
    #
    # FATTI SCARTATI PERCHÉ A FONTE SINGOLA
    # - Kuzmin che prende in prestito per una notte i synth delle band in tour (solo SOS).
    # - Vladimir Lugovetz, inventore del FAEMI e suocero di Kuzmin (solo SOS).
    # - il logo che sembra lo yin e yang ma sono due punti di saldatura (solo SOS).
    # - il nome che vuol dire «molti timbri», non polifonia (solo SOS).
    # - tastiera a contatti reed con magneti; 48 tasti da fa a mi (SOS dice 48,
    #   MusicTech e SOS 2003 dicono 49: le fonti non concordano, tolto).
    # - mobile di metallo invece del truciolato rivestito (solo SOS).
    # - interruttore Gate On per suonare senza tasti (solo SOS).
    # - Kuzmin che si costruisce il basso perché non si trovavano chitarre (solo RBMA).
    # - padre militare; diploma di architettura di Olimpiada; colore cachi (solo RBMA;
    #   il cachi nelle foto non si vede).
    # - Kuzmin: «ogni Polivoks costruito dalla Vector funziona ancora» (solo RBMA;
    #   SOS racconta il contrario sull'affidabilità).
    # - «non si entra due volte nella stessa acqua» sul rifarlo (solo RBMA).
    # - lasciò la Vector nel 1991 con 8 ingegneri (solo RBMA).
    # - 920 rubli = 8 mesi di stipendio (solo Moscow Times).
    # - Troitsky: negli anni '80 sembrava roba da poco, tutti volevano un DX7 (solo Moscow Times).
    # - Kapranos: «il pannello di controllo di un carro armato sovietico» (solo
    #   Moscow Times); «costruito con pezzi di ricambio nella guerra fredda» (solo NME 2007).
    # - Will Gregory: trovato in Germania Est, manopole che «mandano tutto fuori
    #   di testa», basso «da sottomarino» in «Black Cherry», ringhio in «Train» (solo SOS 2003).
    # - «Ulysses» e «Lucid Dreams» (solo Wikipedia/Simon Maes); «Hellwalker» di
    #   Doom (solo una tesina della Bradford College).
    # - Rammstein (Moscow Times e Izvestia lo nominano senza un disco: vago, tolto).
    # - prezzo 600 rubli (un risultato di ricerca, contro 920 di quattro fonti).
    {
        "slug": "polivoks",
        "numero": 65,
        "serie": "I SINTETIZZATORI",
        "strumento": "Formanta Polivoks",
        "anno": "1982",
        "luogo": "URSS",
        "costruttore": "Formanta (gruppo Vector)",
        "specifiche": [
            ("USCITA", "1982"),
            ("PREZZO", "920 rubli"),
            ("VOCI", "2, duofonico"),
            ("FILTRO", "12 dB, 2 amplificatori"),
        ],
        "gancio": "Il filtro non ha condensatori: 2 amplificatori e 6 resistenze. Doveva suonare dolce come un Minimoog",
        "sottotitolo": "Un ingegnere degli Urali voleva dare all'URSS il suono dei synth americani e giapponesi. Gli è venuto un altro suono.",
        "la_macchina": (
            "Il pannello è a gradini, e non per bellezza: ogni riquadro in "
            "rilievo corrisponde a una scheda di circuito infilata lì sotto. Le "
            "scritte sono tutte in cirillico. Ci sono 2 oscillatori, un filtro, 2 "
            "inviluppi, e si suonano al massimo 2 note insieme. Costava 920 "
            "rubli, troppi per un musicista, e infatti li compravano soprattutto "
            "gli enti culturali. Quanti ne siano usciti non si sa. Kuzmin parlava "
            "di circa 25.000, la Moscow Times nel 2009 scriveva più di 100.000. "
            "Io mi fido di lui. Se ne trovate uno, l'interruttore rosso a destra "
            "con scritto СЕТЬ è l'accensione."
        ),
        "inventore_nome": "Vladimir Kuzmin",
        "inventore": (
            "Vladimir Kuzmin nasce a Vladivostok nel 1953. Nella band "
            "dell'università suona il basso, si laurea nel 1976 e va a lavorare "
            "alla Vector di Ekaterinburg, una fabbrica nata durante la guerra che "
            "ora fa strumenti elettronici. Lì guida una squadra piccola: Yuri "
            "Feofilov per l'elettronica e sua moglie Olimpiada per il mobile e il "
            "pannello, che lei disegna guardando le radio militari sovietiche. "
            "Kuzmin vuole che i musicisti abbiano i colori di Moog, Korg e Roland, "
            "che in URSS non si trovano quasi. Il prototipo è del 1980, la "
            "Formanta di Kachkanar lo produce dal 1982. Kuzmin è morto il 12 "
            "giugno 2026, a 72 anni."
        ),
        "come_funziona": (
            "Kuzmin voleva un filtro dolce come quello del Minimoog e ci ha "
            "lavorato quasi un anno. Alla fine ne fa uno tutto suo, con 2 "
            "amplificatori operazionali e 6 resistenze. Il lavoro che in ogni "
            "altro filtro fanno i condensatori qui lo fanno quelli minuscoli che "
            "stanno già dentro gli amplificatori. Taglia 12 dB per ottava, in "
            "passa-basso o in passa-banda. Di dolce non ha niente: con la "
            "risonanza alta è ruvido e sporco, e secondo me è proprio per questo "
            "che lo si cerca ancora. I 2 inviluppi possono ripetere in loop "
            "attacco e decadimento, e allora il suono pulsa come se dietro ci "
            "fosse un sequencer."
        ),
        "richiami": [
            ("FIG. 1", "Filtro: 2 amplificatori, 6 resistenze"),
            ("FIG. 2", "Passa-basso o passa-banda"),
            ("FIG. 3", "Inviluppi in ripetizione"),
        ],
        "chi_lusata": [
            {"artista": "Franz Ferdinand", "nota": "in tutto l'album «Tonight: Franz Ferdinand» (2009)", "ig": "franz_ferdinand"},
            {"artista": "Goldfrapp", "nota": "sull'album «Black Cherry» (2003)", "ig": "goldfrappmusic"},
            {"artista": "Mick Gordon", "nota": "nella colonna sonora del videogioco Doom (2016)", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": (
            "Fino al 1991 il Polivoks non esce dall'URSS, e la produzione si è "
            "già fermata nel 1990. Poi le frontiere si aprono e i Polivoks usati "
            "prendono la strada della Germania e della Polonia, dove negli anni "
            "'90 finiscono nella techno più dura e nella musica industriale. "
            "Kuzmin non ne sa niente. Lo scopre all'inizio degli anni 2000, "
            "quando comincia a usare internet, e trova all'estero gente che "
            "cerca la sua macchina. La registrazione del reel è di quel periodo: "
            "maggio 2002, Ekaterinburg, Kuzmin che suona il suo Polivoks davanti "
            "a un registratore a minidisc."
        ),
        "avvertenza": "Pannello in cirillico. РЕЗОНАНС è la risonanza: a fine corsa il filtro del Polivoks non fischia, graffia. Abbassare il volume prima.",
        "foto": {
            "file": "assets/foto/polivoks/principale.jpg",
            "autore": "OriginalJambo",
            "licenza": "CC BY-SA 4.0",
            "fonte": "Wikimedia Commons",
            "ritaglio": True,
            "didascalia": "In alto al centro c'è scritto ПОЛИВОКС: sul pannello è tutto in cirillico",
        },
        "foto_extra": [
            {"file": "assets/foto/polivoks/pannello.jpg",
             "autore": "Rob Sinclair", "licenza": "CC BY-SA 2.0", "fonte": "Wikimedia Commons",
             "didascalia": "I 2 generatori, il miscelatore e il filtro, con le manopole numerate da 0 a 6"},
            {"file": "assets/foto/polivoks/museo.jpg",
             "autore": "Leonid Makarov", "licenza": "CC0", "fonte": "Wikimedia Commons",
             "nel_reel": False,
             "didascalia": "In vetrina al Museo di storia e archeologia degli Urali, fra i marchi sovietici della regione"},
        ],
        "fonti": [
            {"titolo": "«Formanta Polivoks» — Sound On Sound, luglio 2010",
             "url": "https://www.soundonsound.com/reviews/formanta-polivoks-synthesizer", "data": "2026-10-20"},
            {"titolo": "Intervista a Vladimir Kuzmin — RBMA Daily, 2016",
             "url": "https://daily.redbullmusicacademy.com/2016/03/vladimir-kuzmin-interview", "data": "2026-10-20"},
            {"titolo": "«Instrument Sound That Went Round the World» — The Moscow Times, 2009",
             "url": "https://www.themoscowtimes.com/archive/instrument-sound-that-went-round-the-world", "data": "2026-10-20"},
            {"titolo": "«The Formanta Polivoks» — Synthtopia, 2009",
             "url": "https://www.synthtopia.com/content/2009/08/17/formanta-polivoks/", "data": "2026-10-20"},
            {"titolo": "Il filtro del Polivoks — Cherry Audio",
             "url": "https://cherryaudio.com/news/secrets-of-atomika", "data": "2026-10-20"},
            {"titolo": "Morto Vladimir Kuzmin — Synthtopia, 2026",
             "url": "https://synthtopia.com/content/2026/06/13/polivoks-synthesizer-designer-vladimir-kuzmin-has-died/", "data": "2026-10-20"},
            {"titolo": "Morto Vladimir Kuzmin — Fontanka, 2026",
             "url": "https://www.fontanka.ru/2026/06/16/76480447/", "data": "2026-10-20"},
            {"titolo": "Morto Vladimir Kuzmin — Izvestia, 2026",
             "url": "https://en.iz.ru/en/2116073/2026-06-16/vladimir-kuzmin-creator-polyvox-synthesizer-has-died", "data": "2026-10-20"},
            {"titolo": "«DOOM: Making the music of hell» — Gearnews, 2016",
             "url": "https://www.gearnews.com/?p=6113", "data": "2026-10-20"},
        ],
        "hashtags": ["#polivoks", "#formanta", "#sintetizzatore", "#franzferdinand", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 065", "Il filtro del Polivoks non ha nemmeno un condensatore"),
            ("VECTOR · EKATERINBURG", "Vladimir Kuzmin vuole dare all'URSS il suono di Moog, Korg e Roland."),
            ("UN ANNO SUL FILTRO", "Il filtro di Kuzmin ha 2 amplificatori e 6 resistenze, e graffia."),
            ("1991 · FRONTIERE APERTE", "Il Polivoks arriva in Germania e in Polonia, nella techno più dura."),
            ("INTERNET · INIZI 2000", "Su internet Kuzmin scopre che all'estero il Polivoks è famoso."),
        ],
        "reel_cta": "Mandalo a chi sa leggere il cirillico",
        "reel_audio": {
            # inizio = secondi nel file intero di Freesound (3:55). Vedi TRATTO sopra.
            "file": "assets/audio/polivoks/registrazione.mp3", "inizio": 0,
            "autore": "odo-ada", "licenza": "CC0 1.0",
            "fonte": "freesound.org/s/148940",
            "url": "https://freesound.org/s/148940/",
            "cosa": "Vladimir Kuzmin in persona che suona il suo Polivoks, Ekaterinburg, maggio 2002: registrazione d'ambiente su minidisc",
        },
        "verificata": True,
    },
    # ---------------------------------------------------------------- 66
    # Rifornimento del 20/10/2026. Audio: «inizio» è 0 perché il file è già
    # l'estratto tagliato (tratto scelto sullo spettrogramma, vedi sotto).
    # Scheda «d50» — Roland D-50 (1987). Fonti aperte il 20/10/2026.
    #
    # FOTO PRINCIPALE
    #   Pagina:    https://commons.wikimedia.org/wiki/File:Roland_D-50_Front.JPG
    #   Autore iixorbiusii, pubblico dominio (rilascio dell'autore), 1805x1200, 3/12/2010.
    #   Thumbnail: https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Roland_D-50_Front.JPG/1280px-Roland_D-50_Front.JPG
    #              (960: .../960px-Roland_D-50_Front.JPG)
    #   Vista dall'alto, macchina intera: joystick a sinistra del display, a destra
    #   lo schema serigrafato delle strutture, in alto a sinistra una scheda di
    #   memoria Roland infilata nella feritoia. Ritaglio consigliato: tutta.
    #
    # FOTO EXTRA (deepsonic, Flickr -> Commons, CC BY-SA 2.0; l'esemplare è un
    # D-50 con l'espansione Musitronics, «D-50 EX» nella descrizione Commons)
    #   joystick.jpg  https://commons.wikimedia.org/wiki/File:P1010903_(49964950062).jpg  (2048x1088)
    #     https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/P1010903_%2849964950062%29.jpg/1280px-P1010903_%2849964950062%29.jpg
    #     Joystick in primo piano a sinistra, accanto le scritte UPPER/LOWER e
    #     PARTIAL BALANCE, poi il display. Il display è retroilluminato verde
    #     (modifica dell'esemplare): la didascalia parla del joystick, non del display.
    #   retro.jpg     https://commons.wikimedia.org/wiki/File:P1010850_(49964949627).jpg  (2048x734)
    #     https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/P1010850_%2849964949627%29.jpg/1280px-P1010850_%2849964949627%29.jpg
    #     Il retro, con la scritta «Roland D-50» grande al centro e le prese a sinistra.
    #   Scartata: «Roland LA32 Chip.jpg» (categoria D-50, ma la descrizione dice che
    #   il chip viene da un D-110: non è questa macchina).
    #
    # REGISTRAZIONE (reel_audio)
    #   Scelta: Freesound 437313, agerven, CC0, 3:54, WAV 44.1k stereo.
    #   Pagina: https://freesound.org/s/437313/
    #   Anteprima: https://cdn.freesound.org/previews/437/437313_2554953-hq.mp3
    #              (lq: https://cdn.freesound.org/previews/437/437313_2554953-lq.mp3)
    #   È LA MACCHINA VERA: la descrizione dice «one track, D50 only, no effects or
    #   overdubs» e che i bordoni sono suonati «on the D50's own keyboard» (arpeggi
    #   da una Arturia Keystep). Un D-50 con la sua tastiera: non il plug-in Roland
    #   Cloud né la D-05, che una tastiera non ce l'hanno. Lo stesso pacchetto
    #   «agerven_D50_sounds» ha registrazioni D50 dal 2016, prima di plug-in e D-05.
    #   NON è Pizzagogo: è un suono programmato dall'autore («working on a new
    #   sound»), improvvisato. La didascalia lo dice.
    #   Tratto: non ho potuto ascoltarlo (container bloccato da Freesound). Dalla
    #   forma d'onda: silenzio/attacco nei primi ~5 s, tutto pieno dopo, il punto più
    #   denso fra 2:20 e 2:35. Proposta: da 140 a 165 s (inizio=140); alternativa
    #   8-33 s. Da ascoltare prima di montare.
    #
    #   Alternativa scartata per ora: Commons «D-50 Pizzagogo - Patch.wav»
    #   (W. B. Jaeger, CC0 1.0, 14,17 s, 3/10/2023, «factory patch 44 Pizzagogo»)
    #   https://commons.wikimedia.org/wiki/File:D-50_Pizzagogo_-_Patch.wav
    #   https://upload.wikimedia.org/wikipedia/commons/2/2f/D-50_Pizzagogo_-_Patch.wav
    #   Sarebbe perfetta per la storia, ma né la pagina né il profilo dell'autore
    #   dicono se è un D-50 vero o il plug-in Roland Cloud (che esiste dal 2017 e
    #   ha gli stessi preset). Regola di CLAUDE.md: «non dimostrabile» = fuori
    #   (come l'Hammond). Se il proprietario o l'autore confermano l'hardware,
    #   va questa, con cosa = «il preset Pizzagogo, il suono di Orinoco Flow».
    # ------------------------------------------------------------------ FATTI E FONTI
    # Ogni fatto qui sopra, con le due fonti indipendenti:
    # - 1987, 61 tasti, 16 voci: Wikipedia; Vintage Synth Explorer (vintagesynth.com/roland/d-50); Roland 30°.
    # - 1.445 sterline: SOS mag. 1987 (Russ); Music Technology mag. 1987 (Trask).
    # - 100 campioni, 47 attacchi, 29 in ciclo: Music Technology 1987; SOS 1997 (Ward). 47 anche Wikipedia.
    # - riverbero digitale con 32 programmi: SOS 1987; Music Technology 1987.
    # - tra i primi col riverbero/effetti dentro: Roland 30° («first performance synthesizer with
    #   integrated DSP effects»); Wikipedia («among the first»); VSE («for the first time digital reverb»).
    # - Russ «do not be fooled»: è la recensione stessa (SOS 1987), citata come tale.
    # - stufi della FM / più facile del DX7: SOS 1997; Vintage Synth Explorer.
    # - soffi e strappi d'arco negli attacchi: SOS 1987 («brassy chiffs, bow scrapes»); SOS 1997 («breathy chiffs»).
    # - toglie il primo posto al DX7 fino all'M1: SOS feb. 2018, recensione D-05 (Reid: «ended the
    #   dominance of the DX7»); Wikipedia (il più popolare fino all'M1, l'anno dopo); Roland Articles
    #   («topped synthesizer sales charts»).
    # - memoria cara, quindi solo attacchi: Roland Articles; Wikipedia.
    # - l'attacco fa riconoscere lo strumento: Roland 30° (Kikumoto); Wikipedia (History).
    # - onda quadra o dente di sega + filtro/inviluppo: Wikipedia; SOS 1997; Music Technology 1987.
    # - Upper/Lower, due parziali ciascuna: SOS 1997; Wikipedia; Roland 30°.
    # - joystick per il bilanciamento: Roland 30°; SOS 1997; Wikipedia.
    # - Pizzagogo costruito sul campione Pizz: Synthmania; de.wikipedia «LA-Synthese».
    # - Persing al NAMM 1984 e poi capo del sound design: SOS 2000; Designing Sound 2010
    #   (designingsound.org/2010/01/21/interview-with-eric-persing-founder-of-spectrasonics); Roland 30°.
    # - prima i suoni li facevano gli ingegneri, a macchina finita: Designing Sound 2010 (Persing);
    #   Roland 30° («Before D-50, it was normal to make sounds after hardware development»).
    # - preset di Persing e Scott: Roland 30°; Wikipedia; SOS 2000 («a majority of the patches»).
    # - Spectrasonics 1994 con la moglie, Omnisphere: SOS 2000; NAMM Oral History.
    # - Watermark registrato fra Dublino (Aigle) e Orinoco Studios: Wikipedia «Orinoco Flow»; Great Irish Songbook.
    # - manca un pezzo, scritto per ultimo/in fretta: SOS mar. 1989; Great Irish Songbook.
    # - pizzicato di un D-50: SOS 1989; Roland Articles; Synthmania. «Pizzagogo»: Roland Articles; Synthmania; Wikipedia.
    # - preset ritoccati e sovrapposti: SOS 1989 (e Wikipedia «customising a patch», che cita SOS):
    #   lo si dice come voce discordante, non come fatto.
    # - titolo dallo studio: Wikipedia; Great Irish Songbook; The Ringer 2018.
    # - testi di Roma Ryan: Wikipedia; Songfacts (citazione di Roma Ryan).
    # - ottobre 1988, primo posto UK per 3 settimane: Wikipedia; Great Irish Songbook
    #   (sul giorno non concordano: 3 ottobre contro 15, quindi solo «ottobre»).
    # - Man in the Mirror, introduzione col D-50: SOS 2017 (notizia D-05); Roland Articles.
    # - Jarre, «Revolutions» (1988): SOS 2017; Roland Articles.
    # - D-05 nel 2017: SOS 2017 e 2018; Wikipedia.
    #
    # HANDLE (link dal sito ufficiale, aperti il 20/10/2026):
    # - official_enya: enya.com -> instagram.com/official_enya
    # - jeanmicheljarre: jeanmicheljarre.com -> instagram.com/jeanmicheljarre
    # - rolandglobal: roland.com/global -> instagram.com/rolandglobal
    # - spectrasonics_official: spectrasonics.net -> instagram.com/spectrasonics_official
    # - Michael Jackson: None. michaeljackson.com rimanda a un link accorciato
    #   (MichaelJackson.lnk.to/_followAW/instagram) che da qui non ho potuto seguire.
    #   NB: la scheda Synclavier usa già "michaeljackson": se quella verifica vale, si può mettere.
    #
    # ------------------------------------------------------------------ SCARTATI (fonte singola)
    # - Kikumoto (TR-808) «capo tecnico» del D-50 e la frase sul 90% dell'identità di un
    #   suono nei primi 20-30 ms: solo la pagina Roland del 30°.
    # - Toshio Yamabata capo del progetto; Kazz Takahashi e il joystick: solo Roland.
    # - «Digital Native Dance» nato per sbaglio da fonemi messi in ciclo: solo Roland
    #   (il fatto che sia un ciclo di più campioni c'è anche in SOS 1997, non l'errore).
    # - Persing coinvolto nei suoni fin dall'inizio dello sviluppo, cosa insolita: solo Roland.
    # - Adrian Scott partito come dimostratore: solo Roland.
    # - Persing capo del sound design fino al 2005: solo Roland.
    # - il D-50 per «Watermark» era noleggiato, e il giro di accordi mai usato: solo SOS 1989.
    # - Enya suona tutte le tastiere, niente sequencer: solo SOS 1989.
    # - «Nicky, where's the single?» di Rob Dickins: la stessa intervista (Guardian 2008)
    #   ripresa da The Ringer e Songfacts; e Roma Ryan dice che il singolo si decise alla fine.
    # - The Ringer: «very little synthesizer», 30 archi veri e timpani: fonte singola.
    # - Pizzagogo = Pizz + Agogo (il secondo campione): solo le pagine di W. B. Jaeger su Commons/de.wiki.
    # - patch numero 44: solo Commons.
    # - prezzo USA: 1.895 / 1.995 / 2.095 dollari a seconda della fonte; tenuto solo il prezzo UK.
    # - aprile 1987 come mese d'uscita: solo Wikipedia.
    # - il joystick non manda dati MIDI; il joystick rumoroso (Russ 1987): fonte singola ciascuno.
    # - TEC Award 1988: Wikipedia con link morto.
    # - Clapton «Bad Love», Bangles «Hazy Shade of Winter», New Order «Vanishing Point»,
    #   George Michael «Faith» (scheda PN-D50), Gary Numan: solo Roland Articles per il brano.
    # - Fantasia nelle musiche di Star Trek: The Next Generation: Future Music 2020 per il
    #   preset, Roland solo per la serie.
    # - il D-50 ha influenzato l'M1: solo Wikipedia.
    # - pianoforte di fabbrica debole: c'è in due fonti (MT 1987, SOS 1997) ma è un giudizio, lasciato fuori per spazio.
    {
        "slug": "d50",
        "numero": 66,
        "serie": "I SINTETIZZATORI",
        "strumento": "Roland D-50",
        "anno": "1987",
        "luogo": "Osaka, Giappone",
        "costruttore": "Roland",
        "specifiche": [
            ("USCITA", "1987"),
            ("VOCI", "16"),
            ("CAMPIONI PCM", "100"),
            ("PREZZO UK", "1.445 £"),
        ],
        "gancio": "Il pizzicato di Enya in «Orinoco Flow» viene da un suono di fabbrica di questa tastiera",
        "sottotitolo": "Toglie il primo posto al DX7 di Yamaha e lo tiene finché, l'anno dopo, non arriva il Korg M1.",
        "la_macchina": (
            "Una tastiera nera da 61 tasti, con un joystick a sinistra del display, "
            "che in Inghilterra nel 1987 costa 1.445 sterline. Dentro ci sono 100 "
            "campioni corti e un riverbero digitale con 32 programmi: è uno dei primi "
            "synth ad averne uno suo. Martin Russ la prova per Sound On Sound a maggio "
            "del 1987 e avverte di non farsi ingannare, perché non è un sintetizzatore "
            "come gli altri. Chi aveva litigato per anni con la sintesi FM "
            "del DX7 qui ritrova filtri e inviluppi. Io un D-50 lo riconosco dalla "
            "testa delle note, dove quasi sempre c'è un soffio o uno strappo d'arco."
        ),
        "inventore_nome": "Eric Persing e Adrian Scott",
        "inventore": (
            "La macchina la progetta il reparto ricerca di Roland, ma a me interessa "
            "di più chi ci ha messo dentro i suoni. Eric Persing nel 1984 fa le "
            "dimostrazioni Roland al NAMM, la fiera americana degli strumenti, e da "
            "lì diventa il capo del sound design. Fino ad allora in Roland i suoni di "
            "fabbrica li facevano gli ingegneri, a macchina finita. Col D-50 li "
            "scrivono lui e Adrian Scott, e sono proprio quei suoni a finire nei "
            "dischi. Nel 1994 Persing fonda con la moglie Spectrasonics, la ditta di "
            "Omnisphere. Secondo me è la prima volta che chi ha fatto i preset conta "
            "quanto chi ha fatto la macchina."
        ),
        "come_funziona": (
            "Nel 1987 la memoria costa troppo per registrare uno strumento intero, e "
            "in Roland sono convinti che a farlo riconoscere sia l'inizio della nota. "
            "Così dei 100 campioni 47 sono soltanto attacchi, il colpo di martelletto "
            "o lo strappo dell'arco. Altri 29 sono forme d'onda in ciclo. Il resto "
            "della nota lo fa un oscillatore digitale, onda quadra o dente di sega, "
            "con filtro e inviluppo. Ogni suono ha due metà, Upper e Lower, fatte di "
            "due parziali ciascuna, e col joystick decidete quanto pesa l'una "
            "sull'altra. Pizzagogo parte dal campione del pizzicato d'archi."
        ),
        "richiami": [
            ("FIG. 1", "47 attacchi campionati"),
            ("FIG. 2", "Onda quadra o dente di sega"),
            ("FIG. 3", "Joystick: dosa le parziali"),
        ],
        "chi_lusata": [
            {"artista": "Enya", "nota": "«Orinoco Flow» (1988), sul preset Pizzagogo", "ig": "official_enya"},
            {"artista": "Michael Jackson", "nota": "l'introduzione di «Man in the Mirror» (1987)", "ig": None},
            {"artista": "Jean-Michel Jarre", "nota": "l'album «Revolutions» (1988)", "ig": "jeanmicheljarre"},
        ],
        "menzioni_extra": [
            {"ig": "rolandglobal",
             "riga": "Nel 2017 Roland l'ha rifatto in piccolo, il D-05: @rolandglobal."},
            {"ig": "spectrasonics_official",
             "riga": "La ditta che Eric Persing ha fondato nel 1994 è @spectrasonics_official."},
        ],
        "aneddoto": (
            "Nel 1988 «Watermark» è quasi finito. Enya, il produttore Nicky Ryan e "
            "Roma Ryan, che scrive i testi, lo hanno registrato fra Dublino e gli "
            "Orinoco Studios di Londra, e si accorgono che manca ancora un pezzo. Lo "
            "costruiscono in fretta sul pizzicato di un D-50. Il titolo lo prendono "
            "dallo studio. «Orinoco Flow» esce come singolo a ottobre e sta al primo "
            "posto in Inghilterra per 3 settimane. Sul suono le fonti non concordano: "
            "Roland dice Pizzagogo così com'è, Sound On Sound nel 1989 parla di preset "
            "ritoccati e sovrapposti. Ascoltatelo e decidete voi."
        ),
        "avvertenza": "Nei suoni che imitano uno strumento il campione è solo l'attacco. Se dopo un attimo sembra un'altra cosa è perché lo è: il resto è sintesi.",
        "da_ascoltare": {"brano": "Man in the Mirror", "artista": "Michael Jackson",
                         "anno": "1987",
                         "cosa": "Le note che aprono il pezzo, prima che entri la voce, vengono da un D-50 uscito quell'anno."},
        "foto": {
            "file": "assets/foto/d50/principale.jpg",
            "autore": "iixorbiusii",
            "licenza": "pubblico dominio",
            "fonte": "Wikimedia Commons",
            "ritaglio": True,
            "didascalia": "Il D-50 dall'alto: il joystick a sinistra del display, una scheda di memoria nella feritoia",
        },
        "foto_extra": [
            {"file": "assets/foto/d50/joystick.jpg",
             "autore": "deepsonic", "licenza": "CC BY-SA 2.0", "fonte": "Wikimedia Commons",
             "didascalia": "Il joystick e la scritta PARTIAL BALANCE: con un pollice si dosano le parziali"},
            {"file": "assets/foto/d50/retro.jpg",
             "autore": "deepsonic", "licenza": "CC BY-SA 2.0", "fonte": "Wikimedia Commons",
             "didascalia": "Il retro, con il nome scritto grande e le prese a sinistra"},
        ],
        "fonti": [
            {"titolo": "«Roland D-50» — Sound On Sound, maggio 1987 (Martin Russ)",
             "url": "https://www.muzines.co.uk/articles/roland-d-50/1218", "data": "2026-10-20"},
            {"titolo": "«Roland D50» — Music Technology, maggio 1987",
             "url": "https://www.muzines.co.uk/articles/roland-d50/2026", "data": "2026-10-20"},
            {"titolo": "«Roland D50» — Sound On Sound, luglio 1997",
             "url": "https://www.soundonsound.com/reviews/roland-d50", "data": "2026-10-20"},
            {"titolo": "D-50, 30° anniversario — Roland",
             "url": "https://www.roland.com/ca/promos/d-50_30th_anniversary/", "data": "2026-10-20"},
            {"titolo": "«Sounds of the D-50» — Roland Articles",
             "url": "https://articles.roland.com/listening-guide-sounds-of-the-d-50/", "data": "2026-10-20"},
            {"titolo": "«Enya: Watermark» — Sound On Sound, marzo 1989",
             "url": "https://www.muzines.co.uk/articles/enya-watermark/4506", "data": "2026-10-20"},
            {"titolo": "«Orinoco Flow» — Great Irish Songbook",
             "url": "https://great-irish-songbook.shorthandstories.com/orinoco-flow/index.html", "data": "2026-10-20"},
            {"titolo": "«Eric Persing» — Sound On Sound, 2000",
             "url": "https://www.soundonsound.com/people/eric-persing-creating-spectrasonics", "data": "2026-10-20"},
            {"titolo": "Roland D-50 — Synthmania",
             "url": "https://www.synthmania.com/d-50.htm", "data": "2026-10-20"},
            {"titolo": "Roland D-50 — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Roland_D-50", "data": "2026-10-20"},
        ],
        "hashtags": ["#rolandd50", "#roland", "#sintetizzatore", "#michaeljackson", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 066", "Il pizzicato di «Orinoco Flow» nasce da un suono di fabbrica"),
            ("ROLAND · 1987", "Il Roland D-50 tiene in memoria solo l'attacco degli strumenti veri."),
            ("I SUONI DI FABBRICA", "I suoni del D-50 li scrivono Eric Persing e Adrian Scott. Uno è Pizzagogo."),
            ("LONDRA · 1988", "A «Watermark» di Enya manca un pezzo. Nasce sul pizzicato di un D-50."),
            ("OTTOBRE 1988", "«Orinoco Flow» esce come singolo e va al primo posto in Inghilterra."),
        ],
        "reel_cta": "Mandalo a chi ha ancora «Watermark» in cassetta",
        "reel_audio": {
            "file": "assets/audio/d50/registrazione.mp3", "inizio": 0,
            "autore": "agerven", "licenza": "CC0",
            "fonte": "Freesound",
            "url": "https://freesound.org/s/437313/",
            "cosa": "un Roland D-50 vero, suonato dalla sua tastiera con un suono programmato da chi registra (non è Pizzagogo), senza effetti esterni",
        },
        "verificata": True,
    },
    # ---------------------------------------------------------------- 67
    # Rifornimento del 20/10/2026. Audio: «inizio» è 0 perché il file è già
    # l'estratto tagliato (tratto scelto sullo spettrogramma, vedi sotto).
    # Clavia Nord Lead — scheda scritta il 2026-10-20.
    #
    # FOTO (entrambe di John Athayde, CC BY 2.0, licenza letta sulla pagina
    # Commons con l'API extmetadata; tutte e due sono un Nord Lead 2 del 1997,
    # su Commons non c'è nessuna foto libera del primo Nord Lead a tastiera,
    # solo del Nord Rack e sfocata; il Nord Lead 2 ha la stessa scocca rossa
    # e lo stesso schema di pannello):
    #   principale: https://commons.wikimedia.org/wiki/File:Clavia_Nord_Lead_2_on_Yamaha_DX7,.jpg
    #     originale 1600x1200; thumbnail 1280:
    #     https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Clavia_Nord_Lead_2_on_Yamaha_DX7%2C.jpg/1280px-Clavia_Nord_Lead_2_on_Yamaha_DX7%2C.jpg
    #     Guardata (thumbnail 960): il Nord Lead 2 in diagonale riempie la foto,
    #     «nord lead 2» si legge sulla scocca; sotto si vedono i tasti del DX7 e
    #     in basso a sinistra, piccola, la scritta YAMAHA. Il rosso domina.
    #   extra: https://commons.wikimedia.org/wiki/File:Clavia_Nord_Lead_2_-_a_bit_excited_on_the_%22E%22_key.jpg
    #     originale 1200x1600 (verticale); thumbnail 960:
    #     https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Clavia_Nord_Lead_2_-_a_bit_excited_on_the_%22E%22_key.jpg/960px-Clavia_Nord_Lead_2_-_a_bit_excited_on_the_%22E%22_key.jpg
    #     Descrizione dell'autore: «Mishaps in the van. Time to buy a flight
    #     case.» Si vedono le manopole, la scritta «made in Sweden by Clavia» e
    #     un tasto bianco sollevato a metà della foto. Per la reel va bene
    #     (verticale); in una banda orizzontale il tasto rotto sta al centro.
    #
    # AUDIO: https://freesound.org/s/60282/ — «Nord LoveStory1.wav», KatHakaku,
    #   Creative Commons 0 (letta sulla pagina), 1:38.9, caricato il 12/09/2008.
    #   Descrizione dell'autore: «Same Sequence Different Nord Lead settings»;
    #   sta nel pack «Nord Lead 2 - Ambient and Such» (n. 3465): è un Nord
    #   Lead 2, non il primo modello, e la «cosa» lo dice. Il 1997 è l'anno del
    #   modello, NON dell'esemplare: la pagina non dice quando è stato comprato.
    #   Anteprima mp3 (dall'iframe di embed, nella pagina non compare):
    #     https://cdn.freesound.org/previews/60/60282_164285-hq.mp3
    #     (lq: https://cdn.freesound.org/previews/60/60282_164285-lq.mp3)
    #   Tratto migliore: NON ASCOLTATO. Dal container il CDN di Freesound
    #   risponde 403, quindi non ho potuto sentirlo né misurarlo. Va scelto con
    #   l'analisi RMS dopo il download dal runner (inizio provvisorio 0). È una
    #   sequenza ripetuta con impostazioni diverse: probabilmente qualunque
    #   tratto di 20-30 s fa sentire due o tre timbri.
    # VERIFICA, fatto per fatto (le due fonti indipendenti):
    # - Clavia fondata nel 1983 a Stoccolma da Nordelius e Carlsson, in uno
    #   scantinato; Digital Percussion Plate 1; ddrum l'anno dopo col rosso nel
    #   marchio; ddrum venduta nel 2005 al distributore USA (Armadillo):
    #   Music Inc. 2023 + Wikipedia «Clavia» (+ nordkeyboards.com/about-us/ per
    #   scantinato, 1983, DPP1, ddrum).
    # - Prima di Nord, Clavia nota per le ddrum: SOS maggio 1995 + Music Inc.
    # - Nord Lead 1995, primo synth di Clavia: SOS 1995 + nordkeyboards.com.
    # - 4 voci, 12 con l'espansione; Motorola 56002; 2 oscillatori (sega,
    #   triangolo, impulso con PWM), 2 LFO, 2 ADSR: SOS 1995 + SOS 1996 (Reid)
    #   + sequencer.de (voci e DSP).
    # - Una manopola per funzione, niente menu; pitch stick di legno + rotella
    #   di modulazione; rosso: SOS 1995 + Mixdown («wooden pitch bend toggle»,
    #   «real-time control over menu diving») + Wikipedia «Nord Lead».
    # - «Virtual analog» coniato da Clavia col Nord Lead e diventato il nome
    #   della categoria: Wikipedia «Nord Lead» + Mixdown + sequencer.de; SOS
    #   1995 lo chiama già «Virtual Analogue Synthesis instrument».
    # - Forma d'onda calcolata in tempo reale dal DSP: SOS 1995 + Wikipedia
    #   («DSPs programmed to emulate»).
    # - Somiglianza con il Prophet-5: SOS 1996 (Reid) + MusicRadar/Future Music
    #   (Nordelius: «something like a Minimoog or Prophet-5 architecture»).
    # - Il sogno di un Prophet-5 tutto digitale: MusicRadar/Future Music;
    #   Prophet-5 suo preferito: SOS 2015 («my personal favourite, the
    #   Prophet 5»). Due fonti per il legame Nordelius-Prophet-5; la parola
    #   «sogno» è solo di MusicRadar (vedi sotto: testo non aperto per intero).
    # - Nord Lead 2 nel 1997 con 16 voci: SOS settembre 1997 + Wikipedia.
    # - Howlett: «I love the Nord... set the new standard for analogue» e «the
    #   other three members all like it too - after all, it's nice and red»:
    #   theprodigy.info (The Mix, ottobre 1998) + VICE 2014 (Mixmag, settembre
    #   1998). Le due fonti NON concordano sulla rivista, e la scheda lo dice.
    # - Nord Lead nel rack di Howlett nel 1996: theprodigy.info (foto «from
    #   1996») + VICE («el setup de Howlett en 1996»).
    # - «Funky Shit» col preset Funky del Nord Lead: theprodigy.info + VICE;
    #   «Funky Shit» su «The Fat of the Land», 30/06/1997: Wikipedia
    #   discografia Prodigy + Under the Radar (tracklist ristampa).
    # - Jarre: «Nordlead» nelle note di copertina di «Oxygène 7–13» (1997):
    #   Wikipedia + strawberrybricks.com; nel tour del 1997 lo mostra: SOS
    #   settembre 1997 («made a special effort to show off his Nord») +
    #   recensione di un concerto a Stoccolma, maggio 1997, ludd.ltu.se
    #   (Nord Lead II promozionale).
    # - Handle: @nordkeyboards (link Instagram su nordkeyboards.com),
    #   @theprodigyofficial (theprodigy.com), @jeanmicheljarre
    #   (jeanmicheljarre.com). Il proprietario li segue prima dell'uscita.
    #
    # SCARTATI perché a fonte singola (o fonti non indipendenti):
    # - Peter Jubel ha scritto il software del Nord Lead: solo SOS 2003
    #   (intervista a Ernst Nathorst-Böös); Wikipedia e Mixdown la riprendono.
    # - Progettato, costruito e spedito «in meno di 10 mesi»: solo David
    #   Crombie, SOS 1995. Nordelius (MusicRadar) dice solo «un progetto
    #   veloce, avevo due programmatori».
    # - Nordelius veniva dall'elettronica per le telecomunicazioni svedesi: solo
    #   MusicRadar.
    # - Nordelius aveva un Prophet-5 costoso che non teneva l'accordatura; il
    #   sovracampionamento contro l'aliasing: solo MusicRadar.
    # - Prezzo: 1.500 sterline la tastiera, 1.300 il rack: solo SOS 1995.
    # - Il filtro non autooscilla: solo Sound On Sound (1995 e 1996, stessa
    #   testata e stesso autore, non indipendenti).
    # - Tastiera di 4 ottave, display a due cifre, 99 memorie: solo SOS 1995.
    # - Jarre suona «Oxygène IV» su un Nord Lead II promozionale a Stoccolma:
    #   solo una recensione su ludd.ltu.se.
    # - Prima del Nord, Howlett usava un Roland SH-101: solo theprodigy.info.
    # - La sirena di Prodigy fatta con un preset del Nord modificato: solo
    #   theprodigy.info.
    # - Anniversary Model del 2008: 299 esemplari (Sonicstate) o 300
    #   (Wikipedia); le fonti non concordano e non serve alla storia.
    # - Infected Mushroom e la psy-trance israeliana, The Crystal Method: solo
    #   VICE (più elenchi generici di vintagesynth.com sul Nord Rack).
    # - Prince e il Nord Lead 2 su «Newpower Soul»: solo guitarcloud.org, e
    #   con «most likely».
    # - «Café del Mar» (Energy 52): solo un video di Sonicstate che mostra la
    #   macchina in studio, senza dire cosa suona.
    {
        "slug": "nordlead",
        "numero": 67,
        "serie": "I SINTETIZZATORI",
        "strumento": "Clavia Nord Lead",
        "anno": "1995",
        "luogo": "Stoccolma, Svezia",
        "costruttore": "Clavia DMI",
        "specifiche": [
            ("USCITA", "1995"),
            ("VOCI", "4, espandibili a 12"),
            ("PROCESSORE", "Motorola 56002"),
            ("SINTESI", "Analogico virtuale"),
        ],
        "gancio": "Lo costruisce una ditta svedese di batterie elettroniche, ed è un digitale travestito da analogico",
        "sottotitolo": "Due anni dopo arriva il Nord Lead 2, con 16 voci invece di 4 e la stessa scocca rossa.",
        "la_macchina": (
            "Su un palco lo riconoscete dal colore prima che dal suono. È rosso "
            "acceso, e al posto della rotella del pitch ha un bastoncino di legno. "
            "Sul pannello c'è una manopola per ogni funzione e nessun menu da "
            "sfogliare. Dentro, invece, non c'è un solo circuito analogico che "
            "faccia suono. Il primo, del 1995, ha 4 voci, e con una scheda di "
            "espansione arrivano a 12. Le foto e la registrazione di questa scheda "
            "sono di un Nord Lead 2, che da fuori è quasi uguale. A me "
            "piace per una ragione semplice. È una macchina digitale che si "
            "impara girando le manopole, senza aprire il manuale."
        ),
        "inventore_nome": "Hans Nordelius e Mikael Carlsson",
        "inventore": (
            "Nel 1983 Hans Nordelius e Mikael Carlsson lavorano in uno scantinato "
            "di Stoccolma. Il loro primo prodotto è un pad di batteria digitale, "
            "il Digital Percussion Plate 1. L'anno dopo ne esce una versione "
            "migliore e prende il nome ddrum, e il rosso compare già nel marchio. "
            "Per 12 anni Clavia è conosciuta per le batterie. Il Nord Lead è "
            "il suo primo sintetizzatore, e Nordelius ha raccontato che veniva da "
            "un vecchio sogno, un Prophet-5 tutto digitale, e nel 2015 il "
            "Prophet-5 è ancora il suo synth preferito. Le ddrum Clavia le vende "
            "nel 2005, al suo distributore americano."
        ),
        "come_funziona": (
            "Ogni voce ha 2 oscillatori, con dente di sega, triangolo o onda "
            "quadra a larghezza variabile, poi un filtro con la risonanza, 2 "
            "inviluppi e 2 LFO. È lo schema di un polifonico analogico di fine "
            "anni '70, e Sound On Sound fece notare che somigliava parecchio a un "
            "Prophet-5. Solo che i conti li fa un processore Motorola 56002, che "
            "calcola la forma d'onda mentre suonate invece di leggerla da una "
            "memoria come facevano i campionatori. Clavia chiama questa cosa "
            "«virtual analog». Il nome ha preso, e oggi si usa per qualunque synth "
            "che lavori così, anche per quelli degli altri."
        ),
        "richiami": [
            ("FIG. 1", "Una manopola per funzione"),
            ("FIG. 2", "Pitch a bastoncino di legno"),
            ("FIG. 3", "DSP Motorola 56002"),
        ],
        "chi_lusata": [
            {"artista": "The Prodigy",
             "nota": "Liam Howlett lo ha nel rack già nel 1996",
             "ig": "theprodigyofficial"},
            {"artista": "Jean-Michel Jarre",
             "nota": "è fra le macchine di «Oxygène 7–13» (1997), e nel tour di quell'anno lo mette in mostra",
             "ig": "jeanmicheljarre"},
        ],
        "menzioni_extra": [
            {"ig": "nordkeyboards",
             "riga": "Le tastiere rosse le fa ancora Clavia, che su Instagram è @nordkeyboards."},
        ],
        "da_ascoltare": {"brano": "Funky Shit", "artista": "The Prodigy", "anno": "1997",
                         "cosa": "Liam Howlett ci usa un preset di fabbrica del primo Nord Lead, quello che si chiama Funky."},
        "aneddoto": (
            "Nel 1998 una rivista inglese chiede a Liam Howlett del suo Nord. Lui "
            "risponde che lo adora e che secondo lui ha fissato il nuovo standard "
            "dell'analogico, e lo dice di una macchina digitale. Poi aggiunge che piace "
            "anche agli altri tre del gruppo, perché è bello rosso. Le fonti non "
            "sono d'accordo su quale rivista fosse, Mixmag di settembre o The Mix "
            "di ottobre. Sulla frase sì."
        ),
        "avvertenza": "Il pitch qui si piega con un bastoncino di legno. Se cercate una rotella da girare, quella accanto è la modulazione.",
        "foto": {
            "file": "assets/foto/nordlead/principale.jpg",
            "autore": "John Athayde",
            "licenza": "CC BY 2.0",
            "fonte": "Wikimedia Commons",
            "didascalia": "Un Nord Lead 2 appoggiato su un Yamaha DX7: la scocca rossa è quella del primo",
        },
        "foto_extra": [
            {"file": "assets/foto/nordlead/tasto.jpg",
             "autore": "John Athayde", "licenza": "CC BY 2.0", "fonte": "Wikimedia Commons",
             "didascalia": "La scocca rossa e i tasti del Nord Lead 2, visti da vicino"},
        ],
        "fonti": [
            {"titolo": "«Clavia Nord» — Sound On Sound, maggio 1995",
             "url": "https://www.soundonsound.com/reviews/clavia-nord", "data": "2026-10-20"},
            {"titolo": "«Clavia Nord Lead 2.0» — Sound On Sound, dicembre 1996",
             "url": "https://www.soundonsound.com/reviews/clavia-nord-lead-20", "data": "2026-10-20"},
            {"titolo": "«Clavia Nord Lead 2» — Sound On Sound, settembre 1997",
             "url": "https://www.soundonsound.com/reviews/clavia-nord-lead-2", "data": "2026-10-20"},
            {"titolo": "«Clavia Nord Lead A1» — Sound On Sound, 2015 (Nordelius sul Prophet-5)",
             "url": "https://www.soundonsound.com/reviews/clavia-nord-lead-a1", "data": "2026-10-20"},
            {"titolo": "«Inside Nord's Stockholm factory» — MusicRadar",
             "url": "https://www.musicradar.com/news/tech/in-pictures-inside-nords-stockholm-factory-613549", "data": "2026-10-20"},
            {"titolo": "I 40 anni di ddrum — Music Inc., 2023",
             "url": "https://www.musicincmag.com/news/detail/ddrum-shares-statement-on-its-40th-anniversary", "data": "2026-10-20"},
            {"titolo": "«Nord Lead» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Nord_Lead", "data": "2026-10-20"},
            {"titolo": "Il Nord Lead di Liam Howlett — theprodigy.info",
             "url": "https://theprodigy.info/equipment/clavia-nord-lead-synthesiser.html", "data": "2026-10-20"},
            {"titolo": "«Synthopedia: Nord Lead» — VICE, 2014",
             "url": "https://www.vice.com/es/article/synthopedia-nord-lead/", "data": "2026-10-20"},
            {"titolo": "«Oxygène 7–13», strumenti dalle note di copertina — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Oxyg%C3%A8ne_7%E2%80%9313", "data": "2026-10-20"},
        ],
        "hashtags": ["#nordlead", "#clavia", "#sintetizzatore", "#theprodigy", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 067", "Il Nord Lead lo costruisce una ditta di batterie"),
            ("STOCCOLMA · 1983", "Hans Nordelius e Mikael Carlsson fanno pad di batteria in uno scantinato."),
            ("DDRUM · 1984", "Le loro batterie si chiamano ddrum, e il marchio è già rosso."),
            ("CLAVIA · 1995", "Esce il Nord Lead, digitale, rosso, con una manopola per ogni funzione."),
            ("THE PRODIGY · 1998", "Liam Howlett dice che piace a tutto il gruppo, perché è bello rosso."),
        ],
        "reel_cta": "Mandalo a chi ha una tastiera rossa sul palco",
        "reel_audio": {
            "file": "assets/audio/nordlead/registrazione.mp3", "inizio": 0,
            "autore": "KatHakaku", "licenza": "CC0 1.0",
            "fonte": "freesound.org/s/60282",
            "url": "https://freesound.org/s/60282/",
            "cosa": "un Nord Lead 2, il modello del 1997 e non il primo: la stessa sequenza suonata più volte cambiando le impostazioni",
        },
        "verificata": True,
    },
    # ---------------------------------------------------------------- 68
    # Rifornimento del 20/10/2026. Audio: «inizio» è 0 perché il file è già
    # l'estratto tagliato (tratto scelto sullo spettrogramma, vedi sotto).
    # Scheda «mc202» — scritta il 2026-10-20.
    #
    # FOTO (viste entrambe: thumbnail scaricati con WebFetch e guardati)
    # principale: https://commons.wikimedia.org/wiki/File:Roland_MC-202_Synthesizer_at_SMEM_Playroom.jpg
    #   1904.CC (categoria nascosta «Images by Manuel Schmalstieg»), CC BY 4.0,
    #   «Own work», 4032x3024, 14/01/2026, iPhone 12 Pro Max. Museo SMEM di
    #   Friburgo (Svizzera): le coordinate della foto cadono a Friburgo.
    #   thumb 1280: https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Roland_MC-202_Synthesizer_at_SMEM_Playroom.jpg/1280px-Roland_MC-202_Synthesizer_at_SMEM_Playroom.jpg
    #   Macchina intera vista dall'alto e di fronte, su uno scaffale di legno con
    #   le piastrelle bianche dietro. Si leggono LFO / VCO / SOURCE MIXER / VCF /
    #   VCA / ENV, la targa «Roland MC-202 MicroComposer», l'LCD, la manopola
    #   ACCENT, e sotto i tastini bianchi i numeri 1-9 e 0. Ai lati, tagliate dal
    #   bordo, due altre Roland (a sinistra una TR-505, a destra una macchina
    #   argento di cui si legge solo «TD»/«TB»): la macchina più leggibile è il
    #   202. La macchina occupa ~75% della larghezza: se la copertina taglia i
    #   lati non si perde niente di importante; se taglia sopra/sotto, meglio
    #   "ritaglio": True per non perdere la fila dei tasti.
    # extra 1: https://commons.wikimedia.org/wiki/File:Roland_MC-202.jpg
    #   Brandon Daniel (Sunnyvale, CA), CC BY-SA 2.0, Flickr
    #   https://www.flickr.com/photos/54581307@N00/3796065022/ (licenza verificata
    #   dal bot Flickr il 14/01/2010), 3872x2592, 2009.
    #   thumb 1280: https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Roland_MC-202.jpg/1280px-Roland_MC-202.jpg
    #   Primo piano di sbieco, profondità di campo corta: a fuoco la scritta
    #   «Roland MC-202 MicroComposer» e sotto l'LCD con a sinistra PLAY / PITCH /
    #   STEP / GATE; sopra, sfocati, i cursori. La targa sta al centro della
    #   foto: con un ritaglio centrato si vede sempre.
    # Scartate: File:Roland_mc202.jpg (604x403, troppo piccola) e
    #   File:Synthesizers_at_SMEM_Playroom.jpg (il 202 è piccolo in mezzo a uno
    #   scaffale di altre macchine).
    #
    # AUDIO
    # pagina: https://commons.wikimedia.org/wiki/File:Mc202example.ogg
    #   ricontrollata il 2026-10-20: «small looped example using the built in
    #   sequencer, filter and controls; no additional effects». Autore Sven
    #   Buresch per Wikipedia (utente Audioschotter.net su en.wikipedia), caricata
    #   il 20/09/2005, PUBBLICO DOMINIO dichiarato dall'autore, con permesso VRT
    #   #2007053110008626. 4:55, Ogg Vorbis 79 kbps, mono 44,1 kHz. La pagina ha
    #   il bollino «requires review» del trasferimento da en.wikipedia: è un
    #   controllo di forma del bot, la licenza è confermata dal ticket VRT. È
    #   anche il file d'esempio della voce Wikipedia «Roland MC-202».
    # file: https://upload.wikimedia.org/wikipedia/commons/e/ee/Mc202example.ogg
    #   mp3 (transcodifica di Commons, 129 kbps, schema standard, non provato dal
    #   container): https://upload.wikimedia.org/wikipedia/commons/transcoded/e/ee/Mc202example.ogg/Mc202example.ogg.mp3
    #   Io l'ho scaricato tramite WebFetch (2,8 MB) e misurato con ffmpeg.
    # TRATTO: 65-110 s. Fino a 65 s suona solo una sequenza acuta, piu' bassa di
    #   volume (-19/-20 dB RMS) con buchi a 40-60 s; a 65,0 s entra di colpo il
    #   basso (sotto i 200 Hz si passa da -54 a -25 dB in mezzo secondo) e da lì
    #   il pezzo è pieno, -9/-12 dB RMS. Quindi «inizio»: 65 attacca col pezzo
    #   pieno dal fotogramma 0. Fra 115 e 135 s nello spettrogramma si vede una
    #   apertura del filtro (la manopola che gira): se il reel vuole quella, il
    #   tratto alternativo è 100-145 s. A 162-166 s il basso si ferma per 4 s:
    #   non far cadere lì nessun taglio. Niente silenzi in tutto il file.
    #
    # NOTA TECNICA: suoni.VOCE_SCHEDA non ha «mc202»: va aggiunto (la
    #   famiglia è quella della tb303, «acido», o della sh101, «sega»), o
    #   valida_scheda rifiuta la scheda.
    # FONTI PER FATTO (chi regge cosa; tutte aperte il 2026-10-20)
    # - 1983, Roland: Wikipedia; SOS 1995; E&MM maggio 1983.
    # - 365 sterline: E&MM 1983 («£365 inc VAT»); One Two Testing dic. 1983.
    # - 34x20 cm, alto 5 (13½ x 8 x 2 pollici): E&MM 1983; One Two Testing 1983.
    # - 6 pile da 1,5 V (formato C per E&MM) o alimentatore: E&MM; One Two
    #   Testing; Wikipedia.
    # - 2.729 note su 2 piste: E&MM 1983; Vintage Synth Explorer
    #   (https://www.vintagesynth.com/roland/mc-202). SOS e One Two Testing
    #   dicono «2600»: arrotondano.
    # - memoria persa allo spegnimento, salvataggio su cassetta: E&MM; One Two
    #   Testing; SOS 1995; Wikipedia.
    # - POWER SAVE tiene viva la memoria a synth spento: E&MM («Power Save
    #   function»); One Two Testing («disconnect the synth from the six 1.5V
    #   cells so just the memory is kept alive»); la scritta POWER SAVE è sopra
    #   i tasti nella foto principale.
    # - 2 ottave e mezza di tastini: E&MM; Wikipedia («rubber buttons»).
    # - tasti bianchi numerati 0-9 come un tastierino: One Two Testing; si
    #   leggono nella foto principale.
    # - LCD che mostra numeri (note, step, gate): SOS 1995; foto extra.
    # - uscita cuffia: E&MM; SOS 1995.
    # - synth = SH-101 senza rumore, con ritardo sull'LFO; 1 VCO con dente di
    #   sega, impulso, sub; passa-basso 24 dB; 1 inviluppo: SOS 1995; Wikipedia;
    #   Vintage Synth Explorer.
    # - immissione in tre passate (altezze, poi step time, poi gate time) e
    #   registrazione a tempo col metronomo: E&MM; One Two Testing; SOS 1995.
    # - accento e portamento per nota, come la TB-303: Wikipedia; SOS 1995
    #   («Portamento and accent are set in step-edit mode»); Vintage Synth.
    # - una pista suona il synth interno, l'altra un synth esterno da CV/gate:
    #   Wikipedia; SOS 1995; E&MM.
    # - Ralph Dyck canadese, prototipo a un canale, tastierino da calcolatrice,
    #   primi anni '70 (1971 per SOS, 1972 per l'Enciclopedia canadese, «circa
    #   1972» per lui stesso): SOS 1997; Wikipedia MC-8; intervista a Dyck
    #   (https://rolandmc8.wordpress.com/2010/01/25/exclusive-interview-with-ralph-dyck-godfather-of-the-mc-8/).
    # - MC-8 1977, 8 canali, 16 KB, ~200 venduti: Wikipedia MC-8; SOS nov. 2004
    #   «The History Of Roland Part 1» (https://www.soundonsound.com/sos/nov04/articles/roland.htm);
    #   intervista a Dyck (8 canali, 1977).
    # - prezzo MC-8: 4.795 $ per SOS 1997 e Wikipedia; «around eight thousand
    #   dollars» per SOS 2004. Scritto in scheda che non concordano.
    # - Cortini nato a Bologna, Nine Inch Nails dal vivo: Wikipedia
    #   (https://en.wikipedia.org/wiki/Alessandro_Cortini); nin.com
    #   (https://www.nin.com/music/alessandro-cortini-sonno/, «lead electronics
    #   performer in Nine Inch Nails' live unit»).
    # - «Sonno» 2014, Hospital Productions, 9 pezzi, camere d'albergo, MC 202 +
    #   pedale di delay, registrato diretto o in una piccola cassa portatile:
    #   nin.com; Soundohm (https://www.soundohm.com/product/sonno, HOS-412);
    #   Resident Advisor 2014; Juno Daily 11/06/2014
    #   (https://www.juno.co.uk/junodaily/2014/06/11/hospital-productions-to-issue-album-from-alessandro-cortini);
    #   The Quietus 2015.
    # - il registratore in mano, rubinetti/porte/finestre: Resident Advisor;
    #   Soundohm (stessa citazione di Cortini).
    # - «Voltaggio Solitario» seconda traccia di «Sonno»: Resident Advisor;
    #   Juno Daily.
    # - «Risveglio» l'anno dopo, con una TB-303 sincronizzata al 202: The Quietus
    #   28/08/2015 (https://thequietus.com/?p=18655); Juno 18/06/2015
    #   (https://www.juno.co.uk/reviews/2015/06/18/alessandro-cortini-returns-with-risveglio/);
    #   anno 2015 anche su Wikipedia.
    # - Autechre: SOS aprile 2004 (Booth: «It's batty, totally upside down, but
    #   it's brilliant to use once you understand the numbers»); Elektron
    #   Stories 2006, intervista di Jon Mårtensson (Booth: «A Roland MC202 is
    #   mental really, that sequencer still spins me out»), copia su
    #   https://aepages.org/wiki/Elektron_Stories:_Sean_Booth,_2006.
    # - Frusciante ne ha 6: Premier Guitar 03/03/2014 (con la citazione «one of
    #   my favorite instruments»); Vice Italia 06/04/2016
    #   (https://www.vice.com/it/article/lo-studio-di-john-frusciante-il-paradiso-degli-smanettoni/,
    #   «sei MC-202»).
    # - Daft Punk, MC-202 nella lista di «Homework»: MusicTech 25/02/2021; Mixmag
    #   23/02/2021 (https://mixmag.net/read/daft-punk-homework-tech-gear-equipment-news).
    #   ATTENZIONE: tutte e due riprendono lo stesso ritaglio di una rivista
    #   giapponese (1999 per loro; Equipboard dice Sound & Recording 1997). Le
    #   testate sono indipendenti, il documento è uno. Per questo la nota dice
    #   «nella lista», non «suonato in» un brano preciso.
    #
    # FATTI SCARTATI (una fonte sola, o fonti che si copiano)
    # - Human League su «Rock Me Again…» (Hysteria, 1984): lo dice solo Ian
    #   Burden in Electronic Soundmaker, ott. 1984 (muzines 3390). Che i Human
    #   League l'abbiano usato lo dicono due fonti (quella e SOS 1995), il brano
    #   una sola: tolti dalla lista per non metterli senza disco.
    # - Vince Clarke, Bomb The Bass, K-Klass: solo SOS 1995, nessun brano.
    # - 17 mesi di produzione: solo SOS 1995 (Matrixsynth ricopia la stessa
    #   frase); Wikipedia dice 1983-1985.
    # - 595 dollari di listino: solo Wikipedia (infobox, senza nota).
    # - oscillatore su chip Curtis 3340: solo E&MM 1983.
    # - nome «MicroComposer» scelto per non dire «computer»: solo One Two
    #   Testing, ed è detto mezzo per scherzo.
    # - «la peggio venduta delle Roland del decennio»: MusicRadar, ma la pagina
    #   non si apre (testo non leggibile), quindi non verificato.
    # - svendita a 159 sterline da Soho Soundhouse nel 1986: solo la pagina di
    #   Zoe Blade che cita la pubblicità; la pubblicità non l'ho trovata.
    # - prezzi dell'usato nel 1995 (100 sterline, poi 200-250; la 303 sopra le
    #   500): solo SOS 1995.
    # - Autechre: il 202 come seconda macchina dopo la TR-606: solo SOS 2004.
    # - Frusciante: sei 202 programmati per sembrare un Wurlitzer in «Foregrow»
    #   (solo Vice 2016); melodia di «After Below» di Trickfinger su un 202
    #   (solo Groove.de 2015, e lui dice «probably»); una corda di chitarra per
    #   macchina (solo Premier Guitar).
    # - Josh Wink, «Higher State of Consciousness» col 202: leggenda smentita
    #   (è una 303).
    # - MC-303 (1996) erede digitale: solo Wikipedia.
    # - Kakehashi in visita allo studio di Dyck nel 1976: solo l'intervista a
    #   Dyck.
    # - handle Instagram: nessuno verificato da un sito ufficiale in questa
    #   sessione, quindi tutti None e niente menzioni_extra.
    {
        "slug": "mc202",
        "numero": 68,
        "serie": "I SINTETIZZATORI",
        "strumento": "Roland MC-202 MicroComposer",
        "anno": "1983",
        "luogo": "Giappone",
        "costruttore": "Roland",
        "specifiche": [
            ("USCITA", "1983"),
            ("PREZZO", "365 £"),
            ("MEMORIA", "2.729 note"),
            ("PILE", "6 da 1,5 V"),
        ],
        "gancio": "Il fratello della TB-303 col sequencer dentro. Va a pile, e le note si scrivono coi numeri",
        "sottotitolo": "Un synth monofonico, 2 piste di sequencer e l'uscita per la cuffia, in una scatola grigia di 34 centimetri per 20.",
        "la_macchina": (
            "A vederlo sembra un SH-101 a cui hanno tolto la tastiera. Al suo posto "
            "ci sono 2 ottave e mezza di tastini di plastica, e sotto quelli bianchi "
            "sono stampati i numeri da 0 a 9. Sopra c'è uno schermo a cristalli "
            "liquidi che mostra numeri e basta. Le note in memoria sono 2.729, divise "
            "fra 2 piste. Si salvano su una cassetta qualsiasi, e se non lo fate le "
            "perdete. Va a 6 pile da 1,5 volt o con l'alimentatore. In Inghilterra, "
            "nel 1983, costava 365 sterline. A me è sempre sembrato più bello da "
            "guardare che comodo da usare, e credo sia per questo che tanti ci si "
            "affezionano."
        ),
        "inventore_nome": "Ralph Dyck, e Roland",
        "inventore": (
            "Un progettista con nome e cognome l'MC-202 non ce l'ha. Ha un nonno. "
            "Nei primi anni '70 Ralph Dyck, musicista canadese, si costruisce in "
            "casa un sequencer digitale a un canale solo, e le note le batte su un "
            "tastierino da calcolatrice. A Roland l'idea piace. Nel 1977 esce "
            "l'MC-8 MicroComposer, 8 canali e 16 KB di memoria, e ne vendono circa "
            "200 in tutto il mondo. Sul prezzo le fonti non concordano. Sound On "
            "Sound nel 1997 scrive 4.795 dollari, nel 2004 «circa 8.000». Sei anni "
            "dopo l'MC-202 si porta dietro la stessa idea, le note scritte in "
            "numeri, in una scatola da mettere in borsa."
        ),
        "come_funziona": (
            "Il synth è quello dell'SH-101 senza il generatore di rumore e con in "
            "più un ritardo sull'LFO. Un oscillatore con dente di sega, impulso e "
            "sub, un filtro passa-basso a 24 dB, un inviluppo. La parte strana è il "
            "sequencer. Le note si possono suonare col metronomo, ma il "
            "modo vero è scriverle in tre passate. Prima le altezze, una dopo "
            "l'altra. Poi quanto dura ogni passo, poi quanto resta aperta la nota. "
            "Ogni nota può avere l'accento e il portamento, come sulla TB-303, e una "
            "delle 2 piste può suonare un altro synth dalle prese CV e gate. "
            "Provate a scrivere un giro così e vi accorgerete che state pensando in "
            "numeri."
        ),
        "richiami": [
            ("FIG. 1", "Tasti numerati da 0 a 9"),
            ("FIG. 2", "2 piste, 2.729 note"),
            ("FIG. 3", "Accento e portamento per nota"),
        ],
        "chi_lusata": [
            {"artista": "Alessandro Cortini", "nota": "«Sonno» (2014): un album intero con un MC-202 e un pedale di delay", "ig": None},
            {"artista": "Autechre", "nota": "Sean Booth, 2004: il sequencer è «matto, tutto al contrario», e geniale quando capisci i numeri", "ig": None},
            {"artista": "John Frusciante", "nota": "ne ha 6, e per lui è «uno dei miei strumenti preferiti» (2014)", "ig": None},
            {"artista": "Daft Punk", "nota": "nella lista delle macchine di «Homework» (1997)", "ig": None},
        ],
        "menzioni_extra": [],
        "da_ascoltare": {"brano": "Voltaggio Solitario", "artista": "Alessandro Cortini", "anno": "2014",
                         "cosa": "Un synth che suona una nota alla volta e un pedale di delay. Ascoltatelo sapendo che non c'è nient'altro."},
        "aneddoto": (
            "Alessandro Cortini è nato a Bologna e da anni suona le macchine dal "
            "vivo coi Nine Inch Nails. Nel 2014 pubblica «Sonno» con Hospital "
            "Productions, 9 pezzi registrati in camere d'albergo con un MC-202 che "
            "passa in un pedale di delay. Il suono va dritto nel registratore, a "
            "volte esce da una piccola cassa portatile. Cortini racconta che girava "
            "per la stanza col registratore in mano, per sentire dove la sequenza "
            "suonava meglio. Apriva i rubinetti, le porte, le finestre, e stava a "
            "sentire come quei rumori si mescolavano al 202. L'anno dopo esce "
            "«Risveglio», con una TB-303 sincronizzata allo stesso MC-202."
        ),
        "avvertenza": "Spegnendo si perdono tutte le 2.729 note. Prima la cassetta, oppure POWER SAVE, che tiene viva la memoria e spegne il synth.",
        "foto": {
            "file": "assets/foto/mc202/principale.jpg",
            "autore": "1904.CC",
            "licenza": "CC BY 4.0",
            "fonte": "Wikimedia Commons",
            "didascalia": "Un MC-202 nella sala prove del museo SMEM di Friburgo, in Svizzera",
        },
        "foto_extra": [
            {"file": "assets/foto/mc202/targa.jpg",
             "autore": "Brandon Daniel", "licenza": "CC BY-SA 2.0", "fonte": "Wikimedia Commons",
             "didascalia": "La targa MicroComposer e lo schermo, che mostra solo numeri"},
        ],
        "fonti": [
            {"titolo": "«Roland MC-202» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Roland_MC-202", "data": "2026-10-20"},
            {"titolo": "«The MC-202 MicroComposer» — E&MM, 1983",
             "url": "https://www.muzines.co.uk/articles/the-mc-202-microcomposer/6017", "data": "2026-10-20"},
            {"titolo": "«Roland MC202 Microcomposer» — One Two Testing, 1983",
             "url": "https://www.muzines.co.uk/articles/roland-mc202-microcomposer/4760", "data": "2026-10-20"},
            {"titolo": "«Roland MC202» — Sound On Sound, 1995",
             "url": "https://www.soundonsound.com/reviews/roland-mc202", "data": "2026-10-20"},
            {"titolo": "«Roland MC8» — Sound On Sound, 1997",
             "url": "https://www.soundonsound.com/reviews/roland-mc8", "data": "2026-10-20"},
            {"titolo": "«Roland MC-8 Microcomposer» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Roland_MC-8_Microcomposer", "data": "2026-10-20"},
            {"titolo": "«Autechre» — Sound On Sound, 2004",
             "url": "https://www.soundonsound.com/people/autechre", "data": "2026-10-20"},
            {"titolo": "«Sonno» di Alessandro Cortini — Resident Advisor, 2014",
             "url": "https://ra.co/news/25102", "data": "2026-10-20"},
            {"titolo": "«John Frusciante: War and Peace» — Premier Guitar, 2014",
             "url": "https://www.premierguitar.com/artists/john-frusciante-war-and-peace", "data": "2026-10-20"},
            {"titolo": "La lista delle macchine di «Homework» — MusicTech, 2021",
             "url": "https://musictech.com/news/daft-punk-gear-list-1997-homework-album/", "data": "2026-10-20"},
        ],
        "hashtags": ["#mc202", "#roland", "#sintetizzatore", "#daftpunk", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 068", "Un album intero, registrato in hotel con un Roland MC-202"),
            ("ROLAND · 1983", "L'MC-202 è un synth col sequencer dentro, 2 piste e 6 pile."),
            ("COME LA TB-303", "Ogni nota ha accento e portamento, e si scrive coi numeri."),
            ("«SONNO» · 2014", "Alessandro Cortini dei Nine Inch Nails suona l'MC-202 in hotel, col delay."),
            ("IL REGISTRATORE IN MANO", "Cortini gira la stanza col registratore, e apre rubinetti e finestre."),
        ],
        "reel_cta": "Mandalo a chi compone in camera d'albergo",
        "reel_audio": {
            # inizio = secondi nel file intero di Commons (4:55). Vedi TRATTO sopra.
            "file": "assets/audio/mc202/registrazione.mp3", "inizio": 0,
            "autore": "Sven Buresch (Audioschotter.net)", "licenza": "Pubblico dominio",
            "fonte": "Wikimedia Commons",
            "url": "https://commons.wikimedia.org/wiki/File:Mc202example.ogg",
            "cosa": "un Roland MC-202 vero che suona un giro dal suo sequencer, col filtro e le manopole del pannello, senza effetti aggiunti",
        },
        "verificata": True,
    },
    # ---------------------------------------------------------------- 69
    # Prima scheda dopo il 1988 (decisione del proprietario, 16/10/2026:
    # «fino a oggi, Auto-Tune sì, una su quattro va bene»), messa avanti
    # in coda su sua richiesta. Fatti con due fonti indipendenti; SCARTATI
    # perché a fonte singola: prezzo di lancio, anno dell'ATR-1 (solo Sound
    # On Sound), «un milione di moltiplicazioni ridotte a quattro», il
    # produttore pagato 60.000 dollari, l'esempio di Eiffel 65 (era un
    # harmonizer MIDI, non Auto-Tune), Radiohead (solo The Wire).
    # Controverso e quindi taciuto: chi volle la velocità zero (Hildebrand
    # «per gioco» secondo Priceonomics, il marketing secondo Ironic Sans).
    # Nessuna registrazione libera dimostrabile di Auto-Tune VERO su
    # Commons o Freesound: il reel usa la sigla.
    {
        "slug": "autotune",
        "numero": 69,
        "serie": "GLI EFFETTI",
        "strumento": "Antares Auto-Tune",
        "anno": "1997",
        "luogo": "Scotts Valley, California",
        "costruttore": "Antares Audio Technologies",
        "specifiche": [
            ("ANNO", "1997"),
            ("COSTRUTTORE", "Antares"),
            ("PRINCIPIO", "Autocorrelazione"),
            ("FORMATO", "Plug-in per Pro Tools"),
        ],
        "gancio": "L'ha inventato un ingegnere che cercava il petrolio nei dati sismici",
        "sottotitolo": "Doveva aggiustare le stonature senza farsi sentire. Lo conosciamo tutti per la volta che si è fatto sentire.",
        "la_macchina": "Nel 1997 Auto-Tune è un programma, un plug-in per Pro Tools. Ascolta una voce, capisce che nota sta cantando e la sposta sulla più vicina della scala che gli avete indicato. Se la nota è già giusta la lascia stare. Prima, per avere una voce intonata, in studio si registravano decine di prese e si montavano i pezzi buoni. Da qui in poi si può tenere la prima, che spesso è la migliore. Secondo me è la macchina più odiata di tutto il catalogo, e anche quella che si sente di più alla radio.",
        "inventore_nome": "Andy Hildebrand",
        "inventore": "Harold «Andy» Hildebrand da ragazzo suona il flauto da professionista, poi nel 1976 prende un dottorato in ingegneria elettrica all'Università dell'Illinois. Va alla Exxon a leggere i dati sismici, cioè a capire dove trivellare, e per farlo usa l'autocorrelazione, una formula che trova il punto in cui un segnale si ripete. Verso i 40 anni smette con il petrolio e nel 1989 va a studiare composizione alla Rice di Houston. Nel 1990 fonda Jupiter Systems, che diventerà Antares. Il primo prodotto è un campionatore software, Infinity.",
        "come_funziona": "La voce è un'onda che si ripete, e il tempo di una ripetizione è la nota. Auto-Tune lo misura con la stessa autocorrelazione dei dati sismici, lo confronta con la nota giusta e ricampiona l'onda quel tanto che basta. Si pensava che quel calcolo fosse troppo pesante per farlo mentre uno canta: Hildebrand ne ha tagliato quasi tutto. Poi c'è una manopola, Retune Speed, che decide quanto in fretta la nota viene spinta al suo posto. Lenta, non la sentite. A zero la nota salta di colpo da un gradino all'altro senza scivolare, e la voce diventa un robot.",
        "richiami": [
            ("FIG. 1", "Trova la nota (autocorrelazione)"),
            ("FIG. 2", "La sposta sulla scala scelta"),
            ("FIG. 3", "Retune Speed a zero: il robot"),
        ],
        "chi_lusata": [
            {"artista": "Cher", "nota": "«Believe» (1998), da cui il nome «Cher effect»", "ig": None},
            {"artista": "T-Pain", "nota": "«Rappa Ternt Sanga» (2005), e da lì il suo marchio", "ig": "tpain"},
            {"artista": "Kanye West", "nota": "«808s & Heartbreak» (2008), quasi tutto cantato così", "ig": None},
            {"artista": "Daft Punk", "nota": "la voce di Romanthony in «One More Time» (2000)", "ig": None},
        ],
        "menzioni_extra": [
            {"ig": "autotune",
             "riga": "Antares lo vende ancora, e il suo account si chiama come lui: @autotune."},
        ],
        "aneddoto": "A metà anni '90, a pranzo durante il NAMM, Hildebrand chiede agli amici cosa ci sarebbe ancora da inventare. Una donna risponde scherzando: una scatola che mi faccia cantare intonata. Nel 1998 Mark Taylor e Brian Rawling producono «Believe» di Cher e sulla sua voce mettono la Retune Speed a zero. La casa discografica vuole togliere quell'effetto, e Cher risponde che si cambia solo passando sul suo cadavere. A Sound On Sound, nel 1999, i produttori raccontano che è un pedale, un DigiTech Talker. Il disco va al primo posto nel Regno Unito e in America.",
        "avvertenza": "Retune Speed a zero non corregge la voce: la trasforma. L'inventore pensava che nessuno sano di mente l'avrebbe girata fin lì.",
        "da_ascoltare": {"brano": "Believe", "artista": "Cher",
                          "anno": "1998",
                          "cosa": "Nelle strofe la voce salta da una nota all'altra senza scivolare. È Auto-Tune con la Retune Speed a zero."},
        "foto": {
            "file": "assets/foto/autotune/principale.jpg",
            "autore": "Georges Seguin (Okki), ritagliata",
            "licenza": "CC BY-SA 3.0",
            "fonte": "Wikimedia Commons",
            "didascalia": "Un Antares AVP-1 in un rack da concerto: Auto-Tune sta qui dentro",
        },
        # Non esiste un'altra foto libera di hardware Antares: questa è un
        # ritaglio verticale della stessa, sul logo e sul display, che nel
        # reel riempie lo schermo invece di stare in una fascia.
        "foto_extra": [
            {"file": "assets/foto/autotune/display.jpg",
             "autore": "Georges Seguin (Okki), ritagliata", "licenza": "CC BY-SA 3.0",
             "fonte": "Wikimedia Commons", "posizione": "center",
             "didascalia": "Il display dell'AVP-1, «antares vocal producer»"},
        ],
        "fonti": [
            {"titolo": "«Instrumental Instruments: Auto-Tune» — RBMA Daily, 2017",
             "url": "https://daily.redbullmusicacademy.com/2017/09/instrumental-instruments-auto-tune", "data": "2026-10-16"},
            {"titolo": "«The Inventor of Auto-Tune» — Priceonomics",
             "url": "https://priceonomics.com/the-inventor-of-auto-tune/", "data": "2026-10-16"},
            {"titolo": "«Auto-Tune: Why Pop Music Sounds Perfect» — Time, 2009",
             "url": "https://time.com/archive/6687593/auto-tune-why-pop-music-sounds-perfect/", "data": "2026-10-16"},
            {"titolo": "Hildebrand fra gli ex studenti — ECE Illinois, 2016",
             "url": "https://ece.illinois.edu/news/alumni-news/field-report/4430", "data": "2026-10-16"},
            {"titolo": "«From Rocks to Rock» — AAPG Explorer, 2012",
             "url": "https://www.aapg.org/news-and-media/details/explorer/articleid/2104/from-rocks-to-rock-his-ideas-sound-good", "data": "2026-10-16"},
            {"titolo": "Il Grammy tecnico 2023 a Hildebrand — Grammy.com",
             "url": "https://www.grammy.com/news/dr-andy-hildebrand-honored-recording-academy-special-merit-award", "data": "2026-10-16"},
            {"titolo": "Brevetto US 5.973.252 — Google Patents",
             "url": "https://patents.google.com/patent/US5973252A/en", "data": "2026-10-16"},
            {"titolo": "«Recording Cher's 'Believe'» — Sound On Sound, febbraio 1999",
             "url": "https://www.soundonsound.com/techniques/recording-cher-believe", "data": "2026-10-16"},
            {"titolo": "«Antares Auto-tune» — Sound On Sound, agosto 2000",
             "url": "https://www.soundonsound.com/reviews/antares-auto-tune", "data": "2026-10-16"},
            {"titolo": "«Believe» e il ritorno di Cher — Mental Floss",
             "url": "https://www.mentalfloss.com/posts/cher-believe-1990s-music-comeback", "data": "2026-10-16"},
            {"titolo": "«Believe» 25 anni dopo — NPR, 2023",
             "url": "https://www.cfpublic.org/2023-10-19/25-years-ago-cher-released-a-song-that-would-change-the-sound-of-pop-music", "data": "2026-10-16"},
            {"titolo": "«808s & Heartbreak» — Spin, 2008",
             "url": "https://www.spinmagazine.com/2008/11/album-review-kanye-wests-808s-and-heartbreak/", "data": "2026-10-16"},
            {"titolo": "«Antares AVP-1» — Sound On Sound, 2002",
             "url": "https://www.soundonsound.com/reviews/antares-avp1", "data": "2026-10-16"},
            {"titolo": "«Discovery» 20 anni dopo — Grammy.com",
             "url": "https://grammy.com/news/record-daft-punk-discovery-album-20-year-anniversary", "data": "2026-10-16"},
        ],
        "hashtags": ["#autotune", "#antares", "#effettiaudio", "#cher", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 069", "La voce robot di Cher nasce da chi cercava il petrolio"),
            ("EXXON · ANNI '70", "Andy Hildebrand legge i dati sismici con una formula, l'autocorrelazione."),
            ("NAMM · ANNI '90", "A pranzo una donna gli chiede una scatola per cantare intonata."),
            ("ANTARES · 1997", "Auto-Tune nasce dalla formula del petrolio, usata sulla voce."),
            ("CHER · 1998", "In «Believe» la correzione è a zero: la voce salta di nota in nota."),
        ],
        "reel_cta": "Mandalo a chi giura di non usare l'autotune",
        "verificata": True,
    },
    {
        "slug": "lowrey",
        "numero": 70,
        "serie": "GLI ORGANI",
        "strumento": "Lowrey DSO",
        "anno": "1965",
        "luogo": "Chicago, USA",
        "costruttore": "Lowrey Organ Company",
        "specifiche": [
            ("PRIMO ORGANO", "1955"),
            ("MODELLO DSO", "1965"),
            ("MANUALI", "2 + pedaliera"),
            ("GENERAZIONE", "valvole"),
        ],
        "gancio": "L'organo da salotto americano, e le otto note che aprono «Lucy in the Sky with Diamonds»",
        "sottotitolo": "Lowrey costruiva organi per le case, non per i palchi, e non ha mai avuto una ruota fonica: tutto elettronico dal primo giorno.",
        "la_macchina": (
            "Un mobile di legno con due tastiere, la pedaliera sotto e il leggio "
            "sopra, fatto per stare in un soggiorno americano. I registri sono "
            "tabulatori bianchi e rossi a sinistra di ogni manuale, con sopra "
            "scritto il nome dello strumento da imitare. Negli anni Sessanta e "
            "Settanta Lowrey era il più grande costruttore di organi elettronici "
            "del mondo, e li vendeva a gente che non sapeva suonare: c'era "
            "l'accompagnamento automatico, e dal 1968 anche i ritmi. "
            "All'esemplare in copertina qualcuno ha avvitato sotto la tastiera una "
            "scatola di ritmi comprata a parte, che non è roba Lowrey."
        ),
        "inventore_nome": "Frederick Lowrey",
        "inventore": (
            "Lowrey era un industriale di Chicago, non un musicista. La ditta "
            "parte da un'idea pratica: si attacca al pianoforte di casa un "
            "aggeggio che gli aggiunge i registri d'organo su 60 note e lo lascia "
            "pianoforte. Si chiama Organo, esce nel 1949 e serve a contendere a "
            "Hammond il mercato del Solovox. Il primo organo vero arriva nel "
            "1955, il Model S Berkshire. La differenza con Hammond sta alla "
            "radice e non cambierà mai: in un Hammond il suono lo fanno delle "
            "ruote dentate che girano davanti a delle calamite, in un Lowrey non "
            "si muove niente."
        ),
        "come_funziona": (
            "Oscillatori a valvola e divisori, e i tabulatori aprono filtri che "
            "colorano quello che esce: flauto, oboe, clarinetto, arpa. Il punto è "
            "che potete tenerne premuti quattro insieme. Nessuno dei quattro "
            "somiglia davvero allo strumento che ha scritto sopra, e quattro "
            "imitazioni mediocri sovrapposte danno un timbro che in natura non "
            "esiste. Un organo da casa fa male il mestiere che dichiara, e "
            "proprio per questo ne ha trovato un altro. Se ne provate uno, non "
            "cercate il flauto: provate ad aprirne quattro a caso."
        ),
        "richiami": [
            ("FIG. 1", "2 manuali e pedaliera"),
            ("FIG. 2", "Tabulatori dei registri"),
            ("FIG. 3", "Ritmi automatici, dal 1968"),
        ],
        "chi_lusata": [
            {"artista": "Paul McCartney", "nota": "l'introduzione di «Lucy in the Sky with Diamonds» (1967)", "ig": None},
            {"artista": "I Beatles", "nota": "e ancora un Lowrey su «Being for the Benefit of Mr. Kite!», stesso disco", "ig": None},
        ],
        "menzioni_extra": [],
        "da_ascoltare": {"brano": "Lucy in the Sky with Diamonds", "artista": "The Beatles", "anno": "1967",
                         "cosa": "Le prime otto note. Non è un clavicembalo: è un organo da salotto con quattro registri aperti tutti insieme."},
        "aneddoto": (
            "Il 1° marzo 1967 McCartney si mette al Lowrey che stava ad Abbey "
            "Road e cerca il suono per l'attacco del pezzo. Non ne apre uno, ne "
            "apre quattro: clavicembalo, vibrafono, carillon e chitarra. Quelle "
            "otto note le riconoscono tutti e quasi nessuno sa che escono da un "
            "mobile che si comprava a rate, con l'accompagnamento automatico "
            "incluso e il leggio di legno sopra. Se ne trovate uno in un "
            "mercatino, i tabulatori ci sono ancora e si chiamano ancora così."
        ),
        "avvertenza": "Dentro ci sono valvole e un alimentatore vecchio di sessant'anni. Un DSO rimasto in cantina non si accende e basta: prima i condensatori.",
        "foto": {
            "file": "assets/foto/lowrey/principale.jpg",
            "autore": "Human-potato hybrid",
            "licenza": "CC BY-SA 4.0",
            "fonte": "Wikimedia Commons",
        },
        "foto_extra": [
            {"file": "assets/foto/lowrey/acceso.jpg",
             "autore": "Brokephotography7D", "licenza": "CC BY-SA 4.0", "fonte": "Wikimedia Commons",
             "didascalia": "Un Lowrey Citation acceso: i tabulatori colorati sono i registri"},
            {"file": "assets/foto/lowrey/c500.jpg",
             "autore": "Emily Harrison", "licenza": "CC BY-SA 2.0", "fonte": "Wikimedia Commons",
             "didascalia": "Un modello del 1977: mobile, panca, pedaliera"},
        ],
        "fonti": [
            {"titolo": "«Lowrey organ» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Lowrey_organ", "data": "2026-10-05"},
            {"titolo": "«Lucy In The Sky With Diamonds» — The Beatles Bible: il Lowrey DSO-1 Heritage Deluxe e i quattro registri aperti insieme",
             "url": "https://www.beatlesbible.com/songs/lucy-in-the-sky-with-diamonds/", "data": "2026-10-05"},
            {"titolo": "«Lucy in the Sky with Diamonds» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Lucy_in_the_Sky_with_Diamonds", "data": "2026-10-05"},
        ],
        "hashtags": ["#lowreyorgan", "#lowrey", "#organo", "#beatles", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 070", "Quel clavicembalo dei Beatles è un organo da salotto"),
            ("ABBEY ROAD · 1° MARZO 1967", "McCartney cerca l'attacco di «Lucy in the Sky with Diamonds»."),
            ("LOWREY DSO · CHICAGO", "Il Lowrey si compra a rate, accompagnamento automatico incluso."),
            ("4 REGISTRI INSIEME", "McCartney ne apre 4: clavicembalo, vibrafono, carillon e chitarra."),
            ("LE PRIME 8 NOTE", "4 imitazioni mediocri sommate: un timbro che in natura non esiste."),
        ],
        "reel_cta": "Mandalo a chi pensava fosse un clavicembalo",
        "verificata": True,
    },
    {
        "slug": "wasp",
        "numero": 71,
        "serie": "I SINTETIZZATORI",
        "strumento": "EDP Wasp",
        "anno": "1978",
        "luogo": "Inghilterra",
        "costruttore": "Electronic Dream Plant",
        "specifiche": [
            ("USCITA", "1978"),
            ("PREZZO", "199 £"),
            ("TASTIERA", "stampata, 2 ottave"),
            ("FILTRO", "CMOS, 12 dB"),
        ],
        "gancio": "La tastiera è un adesivo. Sotto ci sono piastrine di rame, e tutto costava 199 sterline",
        "sottotitolo": "Nero e giallo come l'insetto, con l'altoparlante dentro e le pile: due inglesi tagliano tutto quello che non è il suono.",
        "la_macchina": (
            "Una scatola di plastica nera e gialla, grande come un libro grosso. "
            "Dove dovrebbe esserci la tastiera c'è un adesivo di vinile "
            "serigrafato e sotto l'adesivo delle piastrine di rame piatte: si "
            "suona toccando il disegno dei tasti, che sono due ottave. Dentro ci "
            "stanno due oscillatori digitali, due inviluppi, un filtro "
            "commutabile, un altoparlante da 4 pollici per 2 e il posto per sei "
            "pile mezza torcia. Sul pannello, in basso a destra, c'è scritto "
            "Electronic Dream Plant Limited, England."
        ),
        "inventore_nome": "Adrian Wagner e Chris Huggett",
        "inventore": (
            "Wagner faceva il musicista, Huggett progettava elettronica. Nel 1977 "
            "aprono la ditta con 10.000 sterline prestate da un negozio di "
            "strumenti di Londra e decidono una cosa sola, tagliare tutto quello "
            "che non è il suono. Via la tastiera meccanica, via il mobile, via le "
            "rifiniture. Huggett costruisce gli oscillatori con logica TTL, che è "
            "roba da computer e non da sintetizzatori, e grazie a quella restano "
            "accordati meglio di tanti analogici dell'epoca. È lo stesso uomo "
            "che pochi anni dopo progetterà l'OSCar."
        ),
        "come_funziona": (
            "Due oscillatori digitali e un filtro analogico fatto con chip CMOS, "
            "cioè componenti logici messi a fare un mestiere per cui non erano "
            "nati. Il filtro taglia 12 dB per ottava e si commuta fra passa-basso, "
            "passa-banda e passa-alto; il passa-banda è quello che dà al Wasp il "
            "suono stretto e nasale da cui lo riconoscete. Due prese DIN a 7 poli "
            "sul fianco si chiamano LINK e servono a collegarne due fra loro, "
            "anni prima che esistesse il MIDI. La tastiera stampata non ha né "
            "dinamica né corsa: o tocchi o non tocchi."
        ),
        "richiami": [
            ("FIG. 1", "Tastiera a piastrine di rame"),
            ("FIG. 2", "2 oscillatori digitali"),
            ("FIG. 3", "Prese LINK, prima del MIDI"),
        ],
        "chi_lusata": [
            {"artista": "Robert Rental e Thomas Leer", "nota": "due Wasp per tastiere e percussioni su «The Bridge» (1979)", "ig": None},
            {"artista": "Chris Carter", "nota": "dei Throbbing Gristle: ne comprò uno dopo aver sentito «The Bridge»", "ig": None},
            {"artista": "Dave Stewart", "nota": "degli Eurythmics, registrava col microfono davanti all'altoparlante interno", "ig": None},
        ],
        "menzioni_extra": [],
        "da_ascoltare": {"brano": "The Bridge", "artista": "Robert Rental e Thomas Leer", "anno": "1979",
                         "cosa": "Le tastiere e buona parte delle percussioni escono da due Wasp, non da una batteria elettronica."},
        "aneddoto": (
            "Gerald Casale dei Devo raccontava che col sudore delle dita il Wasp "
            "si metteva a suonare da solo: le piastrine sotto l'adesivo leggono "
            "il contatto, e il sudore è un contatto. La ditta non è durata molto "
            "di più. Nel 1980 Electronic Dream Plant fallisce, schiacciata dai "
            "debiti coi fornitori, e chiude nel 1982. Dell'ultimo modello, il "
            "Wasp Deluxe con la tastiera vera, ne erano usciti circa 80. Wagner "
            "prova ad andare avanti da solo con un marchio chiamato Wasp "
            "Synthesizers e non arriva all'anno."
        ),
        "avvertenza": "La tastiera è un adesivo su piastrine di rame. Non si gratta e non si pulisce con l'alcol: sotto non c'è un contatto di ricambio.",
        "foto": {
            "file": "assets/foto/wasp/principale.jpg",
            "autore": "R. Bartz",
            "licenza": "CC BY-SA 2.5",
            "fonte": "Wikimedia Commons",
            "ritaglio": True,
        },
        "foto_extra": [
            {"file": "assets/foto/wasp/pannello.jpg",
             "autore": "Julian Fincham", "licenza": "CC BY-SA 3.0", "fonte": "Wikimedia Commons",
             "didascalia": "Il pannello giallo su nero, e i tasti che sono solo disegnati"},
            {"file": "assets/foto/wasp/deluxe.jpg",
             "autore": "Julian Fincham", "licenza": "CC BY-SA 3.0", "fonte": "Wikimedia Commons",
             "didascalia": "Il Wasp Deluxe, l'ultimo modello: qui la tastiera è vera"},
        ],
        "fonti": [
            {"titolo": "«Electronic Dream Plant» — Wikipedia (EN)",
             "url": "https://en.wikipedia.org/wiki/Electronic_Dream_Plant", "data": "2026-10-05"},
            {"titolo": "«EDP Wasp» — Sound On Sound: altoparlante, pile, prese LINK e «The Bridge» di Rental e Leer",
             "url": "https://www.soundonsound.com/reviews/edp-wasp", "data": "2026-10-05"},
        ],
        "hashtags": ["#edpwasp", "#edp", "#sintetizzatore", "#eurythmics", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 071", "Casale dei Devo: col sudore delle dita suona da solo"),
            ("1977 · 10.000 STERLINE", "Wagner suona, Huggett progetta. Presta i soldi un negozio di Londra."),
            ("1978 · 199 STERLINE", "Il Wasp taglia tutto: al posto dei tasti, un adesivo sopra il rame."),
            ("GERALD CASALE · DEVO", "Le piastrine leggono il contatto, e il sudore è un contatto."),
            ("ELECTRONIC DREAM PLANT", "Anche la ditta dura poco: nel 1980 fallisce, schiacciata dai debiti."),
        ],
        "reel_cta": "Mandalo a chi suona con le mani sudate",
        "verificata": True,
    },
    {
        "slug": "elkarhapsody",
        "numero": 72,
        "serie": "GLI ORGANI",
        "strumento": "Elka Rhapsody 490",
        "anno": "1975 circa",
        "luogo": "Italia",
        "costruttore": "Elka",
        "specifiche": [
            ("PRODUZIONE", "1972-80?"),
            ("TASTI", "49"),
            ("SUONI", "2"),
            ("COMANDI", "4"),
        ],
        "gancio": "Due pulsanti e due manopole. Non c'è nient'altro da toccare, e non serve",
        "sottotitolo": "Una string machine italiana con quattro comandi in tutto: violoncello, archi, quanto dura la nota, quanto forte.",
        "la_macchina": (
            "Un parallelepipedo nero su gambe, 49 tasti, e a sinistra un "
            "pannellino grande come una mano. Sopra ci sono due pulsanti, "
            "VIOLONCELLO e STRINGS, e due manopole, SUSTAIN e VOLUME. Fine. "
            "Niente filtro da aprire, niente inviluppo da regolare, niente "
            "memorie da salvare. Si sceglie il registro basso o quello alto o "
            "tutti e due, si decide quanto le note restano appese dopo che hai "
            "tolto il dito, e si suona. La sorella maggiore, la 610, ha 61 tasti "
            "e quattro suoni."
        ),
        "inventore_nome": "Elka",
        "inventore": (
            "Elka era un costruttore italiano di organi e strumenti elettronici, "
            "e la Rhapsody è il prodotto con cui esce dai confini. In mezza "
            "Europa non si chiamava nemmeno Rhapsody: fuori dall'Italia la "
            "vendeva la tedesca Hohner col proprio marchio, bianca invece che "
            "nera, e sopra c'era scritto StringVox. All'epoca lo facevano tutti e "
            "serviva ad avere una rete di negozi senza costruirsela. Spiega anche "
            "perché certe macchine di quegli anni sembrano due modelli diversi e "
            "sono lo stesso identico strumento."
        ),
        "come_funziona": (
            "Lavora come un organo, non come un sintetizzatore. In cima c'è un "
            "oscillatore solo che fa le dodici note più acute, e una catena di "
            "divisori le porta giù di ottava in ottava, quindi potete premere "
            "tutti e 49 i tasti insieme e suonano tutti. Ogni tasto ha poi la sua "
            "scheda, che gli dà forma e inviluppo, e il filtraggio cambia man "
            "mano che si sale lungo la tastiera. Sopra a tutto c'è il coro, che "
            "sdoppia il segnale e lo stona appena. È quello, più che le forme "
            "d'onda, a far sembrare archi una cosa che archi non è."
        ),
        "richiami": [
            ("FIG. 1", "Oscillatore unico e divisori"),
            ("FIG. 2", "2 registri: violoncello e archi"),
            ("FIG. 3", "4 comandi in tutto"),
        ],
        "chi_lusata": [
            {"artista": "Christopher Franke", "nota": "dei Tangerine Dream: in concerto dal 1975 ai primi anni Ottanta", "ig": None},
            {"artista": "Peter Baumann", "nota": "sempre Tangerine Dream, nel 1976 e nel 1977", "ig": None},
            {"artista": "Klaus Schulze", "nota": "per un paio di tournée a metà anni Settanta", "ig": None},
            {"artista": "Tony Banks", "nota": "dei Genesis", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": (
            "Non si riesce a stabilire di che anno sia. Wikipedia dice che la "
            "produzione comincia nel 1974. Il museo svizzero degli strumenti "
            "elettronici, che ne ha una in vetrina, scrive 1972. Till Kopper, che "
            "ripara queste macchine da decenni e tiene una delle schede tecniche "
            "più consultate, scrive 1975. Tre fonti serie, tre anni diversi, e "
            "nessun ufficio a cui telefonare per chiedere. Succede spesso con "
            "l'elettronica musicale italiana di quegli anni, e ogni volta mi "
            "dispiace: le macchine sono rimaste, la memoria di chi le ha fatte no."
        ),
        "avvertenza": "I comandi sono quattro e nessuno dei quattro è un filtro. Il timbro non si corregge, si prende: ascoltatela prima di comprarla.",
        "foto": {
            "file": "assets/foto/elkarhapsody/principale.jpg",
            "autore": "Alison Cassidy",
            "licenza": "CC BY-SA 4.0",
            "fonte": "Wikimedia Commons",
            "ritaglio": True,
        },
        "foto_extra": [
            {"file": "assets/foto/elkarhapsody/r610.jpg",
             "autore": "Dominik Müller", "licenza": "CC BY-SA 3.0", "fonte": "Wikimedia Commons",
             "didascalia": "La sorella maggiore, la 610, appoggiata su un Rhodes"},
        ],
        "fonti": [
            {"titolo": "«Elka Rhapsody» — Wikipedia (EN): produzione 1974-1980, i due modelli e i loro registri",
             "url": "https://en.wikipedia.org/wiki/Elka_Rhapsody", "data": "2026-10-05"},
            {"titolo": "«Elka Rhapsody 490» — SMEM, museo svizzero degli strumenti elettronici: datazione 1972-1980 e il marchio Hohner StringVox",
             "url": "https://www.smemmusic.ch/en/elka-rhapsody-490-analog-string-synthesizer", "data": "2026-10-05"},
            {"titolo": "«ELKA Rhapsody 610» — Till Kopper: datazione 1975-1980, i divisori, e chi la usava dal vivo",
             "url": "http://www.till-kopper.de/elka.html", "data": "2026-10-05"},
        ],
        "hashtags": ["#elkarhapsody", "#elka", "#stringmachine", "#genesis", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 072", "I Tangerine Dream la suonano. Nessuno sa quando è nata"),
            ("ELKA · ITALIA", "È la Elka Rhapsody 490: 49 tasti e 4 comandi in tutto."),
            ("TRE FONTI, TRE ANNI", "Wikipedia dice 1974, un museo svizzero 1972, chi le ripara 1975."),
            ("HOHNER STRINGVOX", "All'estero la vende la tedesca Hohner, bianca e col nome StringVox."),
            ("GENESIS · KLAUS SCHULZE", "Ci suonano Tony Banks dei Genesis e Klaus Schulze."),
        ],
        "reel_cta": "Mandalo a chi ascolta i Tangerine Dream",
        "verificata": True,
    },
    {
        "slug": "taurus",
        "numero": 73,
        "serie": "I SINTETIZZATORI",
        "strumento": "Moog Taurus",
        "anno": "1975",
        "luogo": "Stati Uniti",
        "costruttore": "Moog Music",
        "specifiche": [
            ("PRODUZIONE", "1975-81"),
            ("PEDALI", "13"),
            ("OSCILLATORI", "2"),
            ("FILTRO", "24 dB/ott."),
        ],
        "gancio": "Un sintetizzatore senza tastiera. Si suona con i piedi, e doveva essere solo un pezzo di un sistema più grande",
        "sottotitolo": "13 pedali di legno e plastica, due slider da muovere con la scarpa e una sola nota alla volta.",
        "la_macchina": (
            "Una pedaliera con sopra un pannello nero. I pedali sono 13, "
            "cioè le note di un'ottava più una. A sinistra lo slider LOUDNESS, "
            "a destra FILTER: li spostate col piede mentre suonate. Sul "
            "pannello 7 pulsanti, quattro per scegliere il suono (VARIABLE, "
            "TAURUS, TUBA, BASS, e uno è quello che programmate voi) e tre "
            "che si chiamano GLIDE, DECAY e OCTAVE. Dentro, due oscillatori e "
            "un filtro da 24 dB per ottava. Una nota sola per volta, quindi "
            "niente accordi."
        ),
        "inventore_nome": "Moog Music",
        "inventore": (
            "La Taurus doveva essere il terzo pezzo di un sistema chiamato "
            "Constellation, con altre due macchine a tastiera, Apollo e Lyra. "
            "Il sistema non è mai uscito. Secondo Wikipedia ne è stata usata una "
            "versione su Brain Salad Surgery di Emerson, Lake & Palmer, nel "
            "1973. L'Apollo diventa poi la Polymoog, che sta in un'altra scheda, "
            "e la pedaliera esce da sola, con un nome da toro. Anche sull'anno "
            "le fonti non vanno d'accordo: 1975 per quasi tutte, 1976 per una."
        ),
        "come_funziona": (
            "Ogni pedale chiude un contatto e manda una tensione diversa, e "
            "quella tensione dice agli oscillatori quale nota fare. Non c'è "
            "niente di digitale. I due oscillatori fanno onde diverse a seconda "
            "della fonte: Vintage Synth Explorer scrive quadra e dente di "
            "sega, Wikipedia un solo dente di sega distorto, e io non so dire "
            "chi ha ragione. Poi c'è il filtro, con taglio, contorno e "
            "risonanza, e un amplificatore controllato in tensione che decide "
            "il volume."
        ),
        "richiami": [
            ("FIG. 1", "13 pedali, 2 oscillatori"),
            ("FIG. 2", "LOUDNESS e FILTER sotto il piede"),
            ("FIG. 3", "Taurus III del 2010, con display"),
        ],
        "chi_lusata": [
            {"artista": "Mike Rutherford", "nota": "dei Genesis: ha messo da parte le sue vecchie pedaliere Dewtron", "ig": None},
            {"artista": "Geddy Lee", "nota": "dei Rush, fra i nomi che le fonti fanno per primi", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": (
            "La Taurus I esce di produzione nel 1981 e la sostituisce la II, con "
            "18 pedali invece di 13 e in più un'onda a impulso. Poi il silenzio "
            "per quasi trent'anni. Nel 2010 Moog rimette in produzione la III, "
            "e il suo capo dice che la farà solo se ne arrivano 250 ordini. "
            "Arrivano, e ne escono in tutto 1.000, con 52 memorie e un display "
            "che sulla vecchia nemmeno si immaginava. Chi ne ha una della prima "
            "serie, secondo me, la tenga dove si vede."
        ),
        "avvertenza": "Una nota alla volta, e due slider da muovere con la scarpa. Se pensavate di suonarci un accordo, cercate un altro strumento.",
        "foto": {
            "file": "assets/foto/taurus/principale.jpg",
            "autore": "glacial23",
            "licenza": "CC BY-SA 2.0",
            "fonte": "Wikimedia Commons",
            "ritaglio": True,
        },
        "foto_extra": [
            {"file": "assets/foto/taurus/pedali3.jpg",
             "autore": "glacial23", "licenza": "CC BY-SA 2.0", "fonte": "Wikimedia Commons",
             "didascalia": "La Taurus III del 2010: più comandi, e sopra un display"},
        ],
        "fonti": [
            {"titolo": "«Moog Taurus» — Wikipedia (EN): modelli, pedali, oscillatori, Constellation, la serie del 2010",
             "url": "https://en.wikipedia.org/wiki/Moog_Taurus", "data": "2026-10-13"},
            {"titolo": "«Moog Taurus I» — Vintage Synth Explorer: 13 pedali, 2 oscillatori, filtro, slider, memorie",
             "url": "https://www.vintagesynth.com/moog/taurus-i", "data": "2026-10-13"},
            {"titolo": "«Moog Model 205A Taurus Bass Pedal Synthesizer» — SMEM, museo svizzero degli strumenti elettronici",
             "url": "https://www.smemmusic.ch/fr/node/1972", "data": "2026-10-13"},
        ],
        "hashtags": ["#moogtaurus", "#moog", "#sintetizzatore", "#genesis", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 073", "Il synth che Genesis e Rush suonano coi piedi"),
            ("MOOG TAURUS", "13 pedali, 2 oscillatori e un filtro da 24 dB per ottava."),
            ("IL SISTEMA MAI USCITO", "È il terzo pezzo del Constellation, che non uscirà mai."),
            ("DA SOLA", "L'Apollo diventa la Polymoog. La pedaliera esce per conto suo."),
            ("GENESIS · RUSH", "Ci suonano Mike Rutherford dei Genesis e Geddy Lee dei Rush."),
        ],
        "reel_cta": "Mandalo a chi suona il basso coi piedi",
        "verificata": True,
    },
    {
        "slug": "echoplex",
        "numero": 74,
        "serie": "GLI EFFETTI",
        "strumento": "Maestro Echoplex",
        "anno": "1959",
        "luogo": "Stati Uniti",
        "costruttore": "Market Electronics, per Maestro",
        "specifiche": [
            ("PRIMA SERIE", "1959"),
            ("PRIMI VENDUTI", "500"),
            ("EP-3", "1970-91"),
            ("TESTINA", "scorrevole"),
        ],
        "gancio": "Un anello di nastro e una testina che scorre. L'eco si regola spostando un pezzo di metallo",
        "sottotitolo": "L'inventore non amava il modello che è rimasto in catalogo più a lungo, e lasciò la ditta.",
        "la_macchina": (
            "Una scatola nera con un coperchio che si alza. Sotto, un nastro "
            "chiuso a cerchio e due ruote di plastica bianca. Sul pannello "
            "ECHO REPEATS, quante volte l'eco si ripete, e un cursore che va da "
            "SHORT a LONG, cioè da eco corta a eco lunga. Due prese per i "
            "pedali, una per il playback e una per accendere e spegnere l'eco. "
            "Il primo modello è a valvole; l'EP-3 del 1970 è a transistor."
        ),
        "inventore_nome": "Mike Battle",
        "inventore": (
            "Mike Battle lavorava alla Goodyear di Akron, Ohio, e vendeva un "
            "registratore con due testine. Don Dixon, un chitarrista che "
            "provava a fare l'eco col nastro, gli telefona per quello. Il "
            "primo prototipo è fatto con pezzi di un volano e di un motorino "
            "da ventilatore, in una scatola di latta: «piuttosto grezzo, ma "
            "funziona bene». Battle voleva una testina che si spostasse. Nel 1959, "
            "racconta, i primi 500 esemplari vanno alla Chicago Musical "
            "Instruments, che li vende col marchio Maestro. La Market "
            "Electronics di Cleveland ne compra il brevetto nel 1962 per "
            "Wikipedia e nel 1964 per Battle: le date non tornano."
        ),
        "come_funziona": (
            "Il nastro è un anello e gira sempre. Una testina registra quello "
            "che suonate, un'altra, più avanti, lo rilegge qualche istante "
            "dopo, ed ecco l'eco. Il ritardo dipende da quanto sono lontane le "
            "due testine e da quanto è veloce il nastro. Qui il nastro va sempre "
            "alla stessa velocità e si sposta la testina, quindi cambiare tempo "
            "non cambia l'intonazione. Per fare ripetere l'eco, parte del suono "
            "riletto torna alla testina che registra e rifà il giro."
        ),
        "richiami": [
            ("FIG. 1", "Nastro in anello, due ruote"),
            ("FIG. 2", "Cursore ECHO DELAY: da corta a lunga"),
            ("FIG. 3", "Manopola ECHO REPEATS"),
        ],
        "chi_lusata": [
            {"artista": "Jimmy Page", "nota": "dei Led Zeppelin: l'eco corta, quasi un rimbalzo, sulle chitarre soliste", "ig": None},
            {"artista": "Brian May", "nota": "dei Queen: a quanto si legge ne ha modificati, per le armonie di «Brighton Rock»", "ig": None},
            {"artista": "Eddie Van Halen", "nota": "con l'EP-3", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": (
            "Nel 1970 Market Electronics chiede a Battle un Echoplex a "
            "transistor, e lui lo costruisce: è l'EP-3. Poi lo dice chiaro: "
            "quella direzione non gli piaceva, e lasciò la ditta. Preferiva le "
            "valvole, perché secondo i musicisti scaldano di più il suono. "
            "L'EP-3 invece resta in produzione fino al 1991, più di qualsiasi "
            "altro modello. Quale dei due suoni meglio non so dirlo. Se ne "
            "trovate uno a valvole e uno a transistor, provateli uno dopo "
            "l'altro."
        ),
        "avvertenza": "Il tempo dell'eco sta su un cursore che sposta davvero una testina. Guardate che scorra, prima di comprarlo.",
        "foto": {
            "file": "assets/foto/echoplex/principale.jpg",
            "autore": "evan p. cordes",
            "licenza": "CC BY 2.0",
            "fonte": "Wikimedia Commons",
            "ritaglio": True,
        },
        "foto_extra": [
            {"file": "assets/foto/echoplex/ep4.jpg",
             "autore": "Drunem2010", "licenza": "CC BY 3.0", "fonte": "Wikimedia Commons",
             "didascalia": "Il cursore ECHO DELAY e le manopole, visti dall'alto",
             "ritaglio": True},
        ],
        "fonti": [
            {"titolo": "«Echoplex» — Wikipedia (EN): Battle, Market Electronics, Maestro, i modelli EP-2, EP-3, EP-4",
             "url": "https://en.wikipedia.org/wiki/Echoplex", "data": "2026-10-13"},
            {"titolo": "«Mike Battle» — Looper's Delight: i primi 500 del 1959, il brevetto, il registratore dell'amico, EP-3",
             "url": "https://loopersdelight.com/musings/Mike_Battle/Mike_Battle.html", "data": "2026-10-13"},
            {"titolo": "«Echoplex, Part I: Pre-Echoplex Days» — Vintage Guitar: Dixon, Battle, Market Electronics",
             "url": "https://www.vintageguitar.com/1950/echoplex-part-i-pre-echoplex-days", "data": "2026-10-13"},
        ],
        "hashtags": ["#echoplex", "#maestro", "#effettichitarra", "#ledzeppelin", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 074", "L'eco di Jimmy Page e Van Halen: un anello di nastro"),
            ("MAESTRO ECHOPLEX", "Nel 1959 se ne vendono i primi 500, a Chicago."),
            ("LA TESTINA", "Si sposta la testina, non la velocità: l'intonazione non cambia."),
            ("EP-3, 1970", "Mike Battle, l'inventore, non ama il transistor e lascia la ditta."),
            ("RESTA IN CATALOGO", "Quell'EP-3 si fa fino al 1991. Più di ogni altro modello."),
        ],
        "reel_cta": "Mandalo a un chitarrista che ama l'eco",
        "verificata": True,
    },
    {
        "slug": "pianet",
        "numero": 75,
        "serie": "GLI ELETTROMECCANICI",
        "strumento": "Hohner Pianet",
        "anno": "1962",
        "luogo": "Trossingen, Germania",
        "costruttore": "Hohner",
        "specifiche": [
            ("PRIMO MODELLO", "1962"),
            ("TASTI", "61"),
            ("SUONO", "ance d'acciaio"),
            ("PROGETTISTA", "E. Zacharias"),
        ],
        "gancio": "Dentro ci sono delle lamelle d'acciaio e dei cuscinetti che si appiccicano. Con l'età i cuscinetti si sfaldano",
        "sottotitolo": "Il pianoforte elettrico a lamelle di «She's Not There» degli Zombies.",
        "la_macchina": (
            "Il Pianet è un pianoforte elettrico a lamelle. Ogni tasto alza "
            "un cuscinetto da sopra una lamella d'acciaio accordata, la "
            "lamella vibra e un pickup porta la vibrazione all'amplificatore. "
            "Senza amplificatore non lo sentite. I tasti sono 61, da Fa a Fa. "
            "Ci sono una decina di versioni (C, L, N, il Combo, T, M…) e fra l'una "
            "e l'altra cambiano i cuscinetti, le lamelle e il pickup."
        ),
        "inventore_nome": "Ernst Zacharias",
        "inventore": (
            "Lo disegna Ernst Zacharias, ingegnere tedesco, che alla Hohner di "
            "Trossingen lavora dal 1954 e che prima aveva fatto il Cembalet. Il "
            "Pianet è un parente stretto del Cembalet, che era pensato per le "
            "case. Dopo, Zacharias disegnerà anche il "
            "Clavinet, che è arrivato nel 1964. Le date del Pianet non sono "
            "uguali ovunque: Wikipedia dà 1962-1983 per l'intera famiglia, "
            "altre fonti parlano di fine anni '50 per il Cembalet."
        ),
        "come_funziona": (
            "Fino al 1977 la lamella è d'acciaio inox lavorato, il pickup è "
            "capacitivo e il cuscinetto è di pelle. Dopo il 1977, secondo "
            "Wikipedia, le lamelle sono d'acciaio arrotolato, il pickup è "
            "elettromagnetico e il cuscinetto è di gomma siliconica. Quello "
            "di pelle con la schiuma sotto invecchia e smette di funzionare: "
            "molti Pianet degli anni '60 sono rimasti muti finché non si è "
            "tornati a produrre i ricambi."
        ),
        "richiami": [
            ("FIG. 1", "Tastiera da 61 tasti"),
            ("FIG. 2", "Lamella accordata sotto ogni tasto"),
            ("FIG. 3", "Cuscinetto che si stacca dalla lamella"),
        ],
        "chi_lusata": [
            {"artista": "The Zombies", "nota": "Rod Argent su «She's Not There», 1964", "ig": None},
            {"artista": "Beatles", "nota": "su «I Am the Walrus», 1967", "ig": None},
            {"artista": "Bryan Ferry", "nota": "nei primi dischi dei Roxy Music, per esempio «Editions of You»", "ig": None},
        ],
        "menzioni_extra": [],
        "aneddoto": (
            "Il Pianet T, quello del 1977, non ha bisogno di corrente: il pickup "
            "elettromagnetico si arrangia con la vibrazione delle lamelle. E le sue ventose di plastica, per Wikipedia, "
            "sono state brevettate dalla NASA. Questa non l'ho trovata "
            "in nessun'altra parte, quindi prendetela come una cosa da "
            "verificare. Quello che dicono tutti è che a un certo punto "
            "il Pianet è sparito dai cataloghi e il Clavinet gli è passato "
            "davanti."
        ),
        "avvertenza": "Il cuscinetto di pelle del Pianet N si sfalda con gli anni. Prima di comprarne uno, premete ogni tasto e controllate che la lamella suoni.",
        "foto": {
            "file": "assets/foto/pianet/pianet.jpg",
            "autore": "Formication (derivato: Vonvon)",
            "licenza": "CC BY 2.0",
            "fonte": "Wikimedia Commons",
            "ritaglio": True,
        },
        "foto_extra": [
            {"file": "assets/foto/pianet/combo.jpg",
             "autore": "Docrobbie", "licenza": "CC BY-SA 3.0", "fonte": "Wikimedia Commons",
             "ritaglio": True,
             "didascalia": "Un Combo Pianet, prodotto dal 1972, non restaurato"},
        ],
        "fonti": [
            {"titolo": "«Hohner Pianet» — Wikipedia (EN): Zacharias, modelli, lamelle e cuscinetti, chi lo ha usato",
             "url": "https://en.wikipedia.org/wiki/Hohner_Pianet", "data": "2026-10-16"},
            {"titolo": "«Clavinet» — Wikipedia (EN): Ernst Zacharias, Hohner dal 1954, Cembalet e Pianet",
             "url": "https://en.wikipedia.org/wiki/Clavinet", "data": "2026-10-16"},
            {"titolo": "«She's Not There» — Wikipedia (EN): Rod Argent suona un Hohner Pianet, sessione del 22 giugno 1964",
             "url": "https://en.wikipedia.org/wiki/She%27s_Not_There", "data": "2026-10-16"},
        ],
        "hashtags": ["#pianet", "#hohner", "#pianoelettrico", "#beatles", "#storiadellamusica"],
        "reel_battute": [
            ("ELETTROFONI · N. 075", "«She's Not There» degli Zombies: un Pianet da casa"),
            ("HOHNER · 1962", "Un pianoforte elettrico a lamelle, da casa, progettato da Ernst Zacharias."),
            ("COME SUONA", "Un tasto alza il cuscinetto, la lamella vibra, un pickup la amplifica."),
            ("IL GUAIO", "I cuscinetti invecchiano. Molti Pianet anni '60 sono rimasti muti."),
            ("1964", "Rod Argent lo suona su «She's Not There» degli Zombies."),
        ],
        "reel_cta": "Mandalo a un tastierista da lamelle",
        "verificata": True,
    },
    # ---------------------------------------------------------------- 75
    # Rifornimento del 20/10/2026. Audio: «inizio» è 0 perché il file è già
    # l'estratto tagliato (tratto scelto sullo spettrogramma, vedi sotto).
    # Scheda «ans» — sintetizzatore ANS di Evgenij Murzin (URSS, prototipo 1958).
    # Scritta il 2026-10-20. Ogni fatto qui sotto ha almeno 2 fonti indipendenti
    # (elenco in «fonti»); i fatti a fonte singola sono in fondo, scartati.
    #
    # Serie: «LE ORIGINI», non «GLI ANTENATI». In contenuti.py «LE ORIGINI» tiene
    # gli strumenti unici da laboratorio e da studio (theremin, ondes, trautonium,
    # Telharmonium, Synket), «GLI ANTENATI» i prodotti di serie che precedono il
    # synth (Mellotron, Ondioline, Novachord). L'ANS è un esemplare unico, mai
    # prodotto in serie: sta con i primi.
    #
    # FOTO PRINCIPALE
    #   Pagina:    https://commons.wikimedia.org/wiki/File:ANS_Synthesiser,_Glinka_Museum.jpg
    #   Thumbnail: https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/ANS_Synthesiser%2C_Glinka_Museum.jpg/1280px-ANS_Synthesiser%2C_Glinka_Museum.jpg
    #   Originale 2576x1936 (orizzontale). Charles Hutchins su Flickr (su Commons
    #   il campo autore dice «Celesteh», che è il suo nome utente), 11/05/2013,
    #   CC BY 2.0. Guardata a 500 px: la macchina intera di fronte, a sinistra la
    #   colonna nera delle manopole, al centro il telaio della lastra con una
    #   scala a tasti in verticale, in basso la pulsantiera; la scritta «АНС» è
    #   tagliata dal bordo alto, quindi la didascalia non la cita.
    #
    # FOTO EXTRA (tavola 2, sotto «la_macchina»)
    #   Pagina:    https://commons.wikimedia.org/wiki/File:ANS_synthesizer_01623.jpg
    #   Thumbnail: https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/ANS_synthesizer_01623.jpg/1280px-ANS_synthesizer_01623.jpg
    #   Originale 1632x1224. Stardancer, «taken by myself», Theremin Center di
    #   Mosca, febbraio 2006, CC BY-SA 3.0 (doppia licenza con GFDL). Si vede la
    #   lastra nera nel telaio, graffiata, con la colonna delle manopole a sinistra.
    #   Scartate: «ANS synthesizer.jpg» (gli alimentatori da PC dentro la macchina:
    #   nella foto non c'è niente che dica ANS) e il ritaglio della lastra
    #   («...scratched on a glass plate covered with black mastic (clip).jpg»,
    #   864x1320, CC BY-SA 3.0): è quasi tutto nero, e con multiply sulla carta
    #   diventerebbe un rettangolo bruno. Se serve una terza foto, è quella.
    #
    # REGISTRAZIONE
    #   Pagina:  https://commons.wikimedia.org/wiki/File:The_ANS_Synthesizer_playing_doodles_(live).ogg
    #   File:    https://upload.wikimedia.org/wikipedia/commons/3/33/The_ANS_Synthesizer_playing_doodles_%28live%29.ogg
    #   MP3 transcodificato (stesso file, 192 kbps):
    #            https://upload.wikimedia.org/wikipedia/commons/transcoded/3/33/The_ANS_Synthesizer_playing_doodles_%28live%29.ogg/The_ANS_Synthesizer_playing_doodles_%28live%29.ogg.mp3
    #   octopusvision (Maxim Tarashchenko), CC BY-SA 3.0 Unported, 172 s, Ogg
    #   Vorbis. Ricontrollato sulla pagina il 20/10/2026: licenza CC BY-SA 3.0;
    #   descrizione «The ANS Synthesizer playing doodles scratched onto the
    #   mastic-covered glass substrate», «recorded at a live demonstration on 21
    #   October 2009», estratto dall'audio del video YouTube gM4O593Pzm4.
    #   È la macchina VERA: di ANS ne esiste uno solo, e Synthtopia (23/10/2009,
    #   https://www.synthtopia.com/?p=17854) colloca lo stesso video di
    #   Octopusvision al concerto del 21/10/2009 al Museo Glinka per i 95 anni
    #   di Murzin. Non è Virtual ANS né un'emulazione.
    #   Tratto: dal container sia l'originale sia il transcodificato hanno dato
    #   429, quindi NON l'ho ascoltato. Proposta provvisoria 0:00-0:45, «inizio»
    #   0; va confermato all'ascolto (è l'audio di una dimostrazione dal vivo:
    #   controllare che all'inizio non ci siano voci o applausi, e nel caso
    #   spostare «inizio»).
    #
    # HANDLE: nessuno. Il Museo Glinka non ha un account Instagram linkato dal
    # suo sito ufficiale che io abbia potuto verificare (e Instagram in Russia è
    # bloccato dal 2022); Coil e Murzin non ci sono. menzioni_extra vuota.
    # FATTI E FONTI, campo per campo (per il controllo):
    # - Murzin 1914 Samara, morto 1970: Wikipedia «Yevgeny Murzin», Snob, 120years.
    # - ingegnere militare, tiro contraereo / difesa aerea: 120years, Snob (NII-5),
    #   TechInsider (sistemi di difesa aerea), Wikipedia Murzin.
    # - Skrjabin come passione: Snob, 120years, TechInsider.
    # - idea dal sonoro ottico del cinema: Krejči, 120years, TechInsider, Wikipedia Murzin.
    # - anno dell'idea discorde: 1937 (Wikipedia ANS), 1938 (Krejči, Wikipedia
    #   Murzin, Snob, Electronic Sound), 1939 (RBMA). 120years dice «around 1948».
    # - la guerra lo ferma: TechInsider, Snob (riprende nel 1946).
    # - vent'anni, senza lo Stato, nel tempo libero: RBMA e Electronic Sound
    #   (Smirnov: «did not wait for state support»), Snob (soldi suoi),
    #   Wikipedia Murzin (hobby).
    # - prototipo pronto nel 1958: TechInsider, Snob, Krejči (laboratorio 1958),
    #   Electronic Sound.
    # - A.N.S. = Aleksandr Nikolaevič Skrjabin; Skrjabin e il suono-luce:
    #   Wikipedia, Krejči, RBMA, 120years, EEFB (sinestesia).
    # - 5 dischi x 144 piste = 720 toni puri, 1/72 d'ottava = 1/6 di semitono,
    #   10 ottave: Wikipedia, Krejči, 120years, RBMA, EEFB, TechInsider (72 per ottava, 10 ottave).
    # - procedimento di stampa dei dischi inventato da Murzin: Wikipedia, RBMA.
    # - lastra di vetro, mastice nero che non asciuga, si gratta; verticale
    #   altezza, orizzontale tempo, «come la notazione»: Wikipedia, Krejči, 120years.
    # - correzione spalmando il mastice: Krejči, 120years.
    # - luce proiettata dietro la lastra: RBMA, Wikipedia.
    # - 20 fotocellule, 20 amplificatori e filtri passa-banda: Wikipedia, Krejči, 120years.
    # - scorrimento a motore o a mano, fino a fermarsi; tempo senza cambiare
    #   intonazione: Wikipedia, Krejči, RBMA (a mano).
    # - graffio verticale = tutte le note / rumore bianco: 120years, Krejči
    #   («fino al rumore bianco»), Wikipedia (tutte le 720 insieme).
    # - casa-museo di Skrjabin, intorno al 1960 (1959 o 1960 a seconda della
    #   fonte): Wikipedia, RBMA, 120years (1960), Snob.
    # - primo studio di musica elettronica dell'URSS: 120years, Snob.
    # - Krejči dal 1961, compositore e tecnico del suono: Krejči, 120years.
    # - Schnittke, Gubajdulina, Denisov, Artem'ev: Wikipedia, Krejči, 120years, Snob, Electronic Sound.
    # - raccolta Melodija «Muzykal'noe prinošenie» 1990: Krejči, Wikipedia,
    #   Electronic Sound (ristampa Cold Spring).
    # - disco «ANS» di Krejči, Melodija 1970: Krejči, 120years.
    # - studio assorbito dalla Melodija, mai prodotto in serie: Snob, TechInsider.
    # - secondo esemplare al Museo Glinka, prototipo perduto: Wikipedia, RBMA,
    #   Electronic Sound («only two were built»), TechInsider (Museo Glinka).
    # - «Solaris» 1972 con l'ANS: Wikipedia, Wikipedia Murzin, RBMA, Snob,
    #   EEFB, Synthtopia (?p=32401), Electronic Sound.
    # - «Lo specchio»: Snob, TechInsider, RBMA.
    # - «Il braccio di diamante» (Brilliantovaja ruka): TechInsider, Snob.
    # - Coil, «ANS»: Wikipedia, RBMA, Electronic Sound (anno discorde, 2003 o
    #   2004, quindi omesso).
    # - DA ASCOLTARE: organo di Bach in apertura di «Solaris» (EEFB, Under the
    #   Radar); l'ANS nei passaggi astratti / onirici (Wikipedia «abstract,
    #   sci-fi effect», Under the Radar «more abstract passages», EEFB «oneiric scenes»).

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
        # nome: nota, non nome (nota) — con «Nick Rhodes (Duran Duran)» le
        # parentesi si raddoppiavano e la riga sembrava un modulo.
        usi.append(f"{nome}: {u['nota']}")
    if usi:
        # «L'hanno resa leggenda» era una formula da copertina di rivista: si dice chi.
        righe.append("Chi ci ha suonato:")
        righe.extend(f"· {u}" for u in usi)
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


def foto_del_reel(scheda):
    """Le foto che il reel mostra, nell'ordine: la principale e le extra
    che non chiedono una didascalia per essere capite (nel_reel=False).
    Sta qui e non in genera_reel.py perché anche la didascalia del reel
    deve saperlo: ogni foto mostrata va accreditata."""
    return [scheda["foto"]] + [f for f in (scheda.get("foto_extra") or [])
                               if f.get("nel_reel", True)]


def componi_didascalia_reel(scheda, menzioni=True):
    """La didascalia del reel. NON è quella del carosello.

    LEZIONE IMPARATA (07/10/2026). Il reel usciva con la didascalia del
    carosello: prima riga «MINIMOOG MODEL D · 1970», poi il gancio, poi
    600 caratteri di «la macchina». Sotto un reel se ne vedono due righe,
    e chi non ci segue legge quelle o niente: il nome e l'anno non sono
    una ragione per fermarsi. Adesso la prima riga è la prima battuta,
    cioè la stessa frase che sta sullo schermo nel primo fotogramma, e
    sotto c'è la storia del reel per chi vuole rileggerla con calma.
    La CTA è quella del reel (mandarlo a qualcuno), non quella del
    carosello: per chi non ci segue gli invii pesano più dei commenti
    (Mosseri, 21/01/2025)."""
    b = scheda["reel_battute"]

    def frase(t):
        # Sullo schermo le battute non hanno il punto finale (sono righe
        # da leggere al volo); in didascalia si leggono di fila e senza
        # punto si attaccherebbero l'una all'altra.
        t = t.strip()
        return t if t[-1] in ".!?…" else t + "."
    # La seconda riga dice dove sta il resto (15/10/2026, il proprietario:
    # «se qualcuno vuole sapere qualcosa di più, come fa?»). Un link
    # cliccabile verso il carosello l'API non lo permette (non nelle
    # didascalie, non nelle storie: vedi CLAUDE.md, 29/09/2026); una
    # menzione sì, ed è cliccabile anche nell'anteprima di due righe sotto
    # il reel. Prima questa indicazione stava alla quarta riga, cioè dopo
    # «…altro», dove non la leggeva nessuno.
    righe = [frase(b[0][1]),
             f"Le 6 slide con tutta la storia e le fonti: @elettrofoni, "
             f"il post «{scheda['strumento']}».", ""]
    righe.append(" ".join(frase(t) for _, t in b[1:]))
    righe.append("")
    usi = [f"@{u['ig']}" if (u.get("ig") and menzioni) else u["artista"]
           for u in scheda["chi_lusata"]]
    if usi:
        righe.append("Chi ci ha suonato: " + ", ".join(usi))
        righe.append("")
    righe.append(scheda["reel_cta"] + ".")
    righe.append("")
    if scheda["fonti"]:
        righe.append("Fonti: " + " · ".join(f["titolo"] for f in scheda["fonti"]))
    # Ogni foto che passa nel reel è una licenza da rispettare, e nel reel
    # non c'è un credito sullo schermo: sta tutto qui.
    crediti = []
    for f in foto_del_reel(scheda):
        c = f"{f['autore']} ({f['licenza']}, {f['fonte']})"
        if c not in crediti:
            crediti.append(c)
    righe.append("Foto: " + "; ".join(crediti))
    a = scheda.get("reel_audio")
    if a:
        # Si dice COSA suona, non solo chi l'ha registrato: il theremin
        # della registrazione è un Moog Etherwave, non uno di Termen, e
        # chi legge deve saperlo.
        righe.append(f"Audio: {a['cosa']}. Registrazione di {a['autore']} ({a['licenza']}, {a['fonte']})")
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
    # Il timbro del reel non ha un ripiego silenzioso: o la macchina sta in
    # VOCE_SCHEDA, o la scheda non passa. Vedi il commento in suoni.py.
    import suoni  # solo libreria standard, nessun ciclo di import
    if scheda["slug"] not in suoni.VOCE_SCHEDA:
        errori.append("nessun timbro in suoni.VOCE_SCHEDA: il reel userebbe il ripiego")
    # Il reel (formato 2). Niente testo di riserva: una scheda senza le
    # sue battute non ha un reel, e qui lo si scopre scrivendo.
    rb = scheda.get("reel_battute") or []
    if (rb or REEL_OBBLIGATORIE) and len(rb) != REEL_BATTUTE:
        errori.append(f"reel_battute: {len(rb)} battute (ne servono {REEL_BATTUTE})")
    for i, coppia in enumerate(rb, start=1):
        if len(coppia) != 2:
            errori.append(f"reel_battute #{i}: serve (kick, testo)"); continue
        kick, testo = coppia
        lim = MAX_REEL_GANCIO if i == 1 else MAX_REEL_BATTUTA
        if len(testo) > lim:
            errori.append(f"reel_battute #{i}: {len(testo)} caratteri (max {lim})")
        if len(kick) > MAX_REEL_KICK:
            errori.append(f"reel_battute #{i} kick: {len(kick)} caratteri (max {MAX_REEL_KICK})")
    if not scheda.get("reel_cta"):
        if rb or REEL_OBBLIGATORIE:
            errori.append("manca reel_cta")
    elif len(scheda["reel_cta"]) > MAX_REEL_CTA:
        errori.append(f"reel_cta {len(scheda['reel_cta'])} caratteri (max {MAX_REEL_CTA})")
    a = scheda.get("reel_audio")
    if a:
        # «url» e' la pagina della registrazione (Commons o Freesound): dal
        # 16/10/2026 il suono va anche sul sito, e li' il credito di una
        # licenza CC vuole il link all'opera, non solo «Wikimedia Commons».
        mancanti = [k for k in ("file", "autore", "licenza", "fonte", "url", "cosa") if not a.get(k)]
        if mancanti:
            errori.append(f"reel_audio incompleto, mancano: {mancanti}")
        elif not a["url"].startswith("https://"):
            errori.append(f"reel_audio: url non valido {a['url']}")
        else:
            import pathlib
            if not (pathlib.Path(__file__).resolve().parent / a["file"]).exists():
                errori.append(f"reel_audio: file assente {a['file']}")
    if rb and scheda.get("reel_cta"):
        n = _len_utf16(componi_didascalia_reel(scheda))
        if n > MAX_DIDASCALIA_UTF16:
            errori.append(f"didascalia del reel {n} unità UTF-16 (max {MAX_DIDASCALIA_UTF16})")
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
    # Ogni foto in piu' e' una licenza in piu' da rispettare: il credito
    # e' obbligatorio su TUTTE, non solo sulla principale.
    for i, f in enumerate(scheda.get("foto_extra") or [], start=1):
        if not f.get("file") or not f.get("autore") or not f.get("licenza"):
            errori.append(f"foto_extra #{i}: file/autore/licenza obbligatori")
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
    # Dopo il 1988 (decisione del proprietario, 16/10/2026: «fino a oggi,
    # Auto-Tune sì, una su quattro va bene»). Fino a quel giorno nessuna
    # delle 68 schede era posteriore al 1988, senza che nessuno l'avesse
    # deciso: il rifornimento pescava sempre dagli stessi classici. Qui si
    # conta, così chi rifornisce vede la quota invece di ricordarsela.
    import json, re
    from pathlib import Path
    f = Path(__file__).with_name("stato.json")
    usciti = {q["slug"] for q in json.loads(f.read_text())["pubblicati"]} if f.exists() else set()
    coda = [s for s in SCHEDE if s["verificata"] and s["slug"] not in usciti]
    recenti = [s["strumento"] for s in coda
               if (m := re.search(r"\d{4}", str(s["anno"]))) and int(m.group()) > 1988]
    # Il suono vero (proprietario, 17/10/2026: «voglio che ci sia in ogni
    # prossimo post/storia/reel»): quante uscite sono coperte prima che
    # tocchi a una scheda senza registrazione.
    pronte = 0
    for s in coda:
        if not s.get("reel_audio"):
            break
        pronte += 1
    print(f"Col suono vero: {sum(1 for s in coda if s.get('reel_audio'))} su {len(coda)} in coda"
          f" — le prossime {pronte} uscite sono coperte"
          + ("" if pronte == len(coda) else f", poi tocca a {coda[pronte]['slug']} che non ce l'ha"))
    print(f"In coda: {len(coda)} — dopo il 1988: {len(recenti)} (obiettivo: almeno 1 su 4)"
          + (f" — {', '.join(recenti)}" if recenti else ""))
    raise SystemExit(1 if problemi else 0)
