# -*- coding: utf-8 -*-
"""ELETTROFONI — i contenuti «fuori catalogo».

PERCHÉ UN FILE A PARTE. Il catalogo (`contenuti.py`) è fatto di schede,
una macchina storica per volta, con due fonti per ogni fatto. Qui stanno
le poche cose che la pagina pubblica e che NON sono una scheda: oggi un
reel per Cirmolo, il sistema musicale per la Miyoo Flip fatto da chi cura
questa pagina (richiesta del proprietario, 12/10/2026).

REGOLE, perché un catalogo che diventa vetrina smette di essere seguito:
· si dichiara sempre che è fuori catalogo e che è roba nostra («l'abbiamo
  fatto noi»): niente promozione travestita da divulgazione;
· UN reel per progetto, non una campagna: un contenuto fuori catalogo non
  si ripete e non si rifà;
· i fatti storici che ci entrano (qui l'Omnichord) seguono la stessa
  regola delle schede: due fonti, scritte qui sotto;
· non prende il posto del carosello delle 18: usa la passata delle 12:30,
  quella dei rifacimenti, nel giorno scritto in «quando».

Ogni voce ha la forma che `genera_reel.costruisci` si aspetta da una
scheda (foto, foto_extra, reel_battute, reel_cta), più la didascalia
già scritta, che per un contenuto fuori catalogo non si compone dai campi.
"""

SPECIALI = [
    {
        "slug": "cirmolo",
        "quando": "2026-10-13",          # passata delle 12:30 di quel giorno
        "numero": 0,                     # non è una scheda: niente numero
        "strumento": "Cirmolo",
        "anno": "2026",
        "foto": {"file": "assets/foto/cirmolo/openorc-accordo.png",
                 "autore": "Cirmolo", "licenza": "CC BY-NC 4.0", "fonte": "luigismith.github.io/cirmolo"},
        "foto_extra": [
            {"file": "assets/foto/cirmolo/logo.png",
             "autore": "Cirmolo", "licenza": "CC BY-NC 4.0", "fonte": "luigismith.github.io/cirmolo"},
            {"file": "assets/foto/cirmolo/openorc.png",
             "autore": "Cirmolo", "licenza": "CC BY-NC 4.0", "fonte": "luigismith.github.io/cirmolo"},
            {"file": "assets/foto/cirmolo/synth.png",
             "autore": "Cirmolo", "licenza": "CC BY-NC 4.0", "fonte": "luigismith.github.io/cirmolo"},
            {"file": "assets/foto/cirmolo/musica.png",
             "autore": "Cirmolo", "licenza": "CC BY-NC 4.0", "fonte": "luigismith.github.io/cirmolo"},
        ],
        # L'unico fatto storico è l'Omnichord: Suzuki, OM-27, 1981, pulsanti
        # per gli accordi e piastra da sfiorare. Fonti (verificate il
        # 12/10/2026): en.wikipedia.org/wiki/Omnichord («The Suzuki Musical
        # Instrument Corporation released the first Omnichord, the OM-27, in
        # 1981»); musicradar.com/news/blast-from-past-suzuki-omnichord;
        # perfectcircuit.com/signal/suzuki-omnichord-history.
        # Il resto viene dalla pagina del progetto (luigismith.github.io/cirmolo).
        "reel_battute": [
            ("FUORI CATALOGO", "Abbiamo messo uno studio musicale in una console."),
            ("MIYOO FLIP · CIRMOLO", "Si chiama Cirmolo: un sistema per la Miyoo Flip, tutto in italiano."),
            ("OPENORC", "Un tasto, un accordo. L'idea dell'Omnichord Suzuki del 1981."),
            ("CIRMOLO SYNTH", "8 voci, filtro risonante, sequencer a 16 passi."),
            ("TASTIERA MIDI USB", "Ci attacchi una tastiera MIDI. E registri in WAV."),
        ],
        "reel_cta": "Mandalo a chi ha una Miyoo Flip",
        # Schermate: bordi pieni di testo, quindi solo zoom centrato.
        "reel_moti": ("avanti",),
        "reel_kick_chiusura": "CIRMOLO · LINK NEL PROFILO",
        "didascalia": (
            "Abbiamo messo uno studio musicale in una console.\n\n"
            "Fuori catalogo, per una volta, e roba nostra. Cirmolo è un sistema "
            "per la Miyoo Flip, la console a conchiglia, tutto in italiano. Dentro "
            "c'è OpenOrc, dove un tasto suona un accordo (l'idea è quella "
            "dell'Omnichord, che la Suzuki mise in vendita nel 1981); un synth a 8 "
            "voci con filtro risonante e sequencer a 16 passi; un campionatore a "
            "pad; un pianoforte General MIDI; LittleGPTracker. Si suona coi tasti "
            "della console o con una tastiera MIDI USB, e si registra in WAV.\n\n"
            "È gratuito e il codice è su GitHub (fork di spruceOS, licenza CC BY-NC "
            "4.0). È in sviluppo e provato solo sulla Miyoo Flip: si installa a "
            "proprio rischio.\n\n"
            "Link nel profilo · luigismith.github.io/cirmolo\n\n"
            "Mandalo a chi ha una Miyoo Flip.\n\n"
            "Fonti sull'Omnichord: Wikipedia (EN) · MusicRadar · Perfect Circuit\n\n"
            "LE MACCHINE NON SUONANO DA SOLE. QUASI MAI.\n\n"
            "#miyooflip #spruceos #synth #chiptune #retrohandheld"
        ),
    },
]


def trova(slug):
    return next((s for s in SPECIALI if s["slug"] == slug), None)


def valida(s):
    """Stessi limiti delle schede per le battute: un fuori catalogo non ha
    sconti sulla leggibilità."""
    import contenuti
    errori = []
    rb = s.get("reel_battute") or []
    if len(rb) != contenuti.REEL_BATTUTE:
        errori.append(f"{len(rb)} battute (ne servono {contenuti.REEL_BATTUTE})")
    for i, (kick, testo) in enumerate(rb, start=1):
        lim = contenuti.MAX_REEL_GANCIO if i == 1 else contenuti.MAX_REEL_BATTUTA
        if len(testo) > lim:
            errori.append(f"battuta {i}: {len(testo)} caratteri (max {lim})")
        if len(kick) > contenuti.MAX_REEL_KICK:
            errori.append(f"battuta {i} kick: {len(kick)} caratteri")
    if len(s.get("reel_cta", "")) > contenuti.MAX_REEL_CTA:
        errori.append("reel_cta troppo lunga")
    if len(s.get("reel_kick_chiusura", "")) > contenuti.MAX_REEL_KICK:
        errori.append("reel_kick_chiusura troppo lungo")
    if contenuti._len_utf16(s["didascalia"]) > contenuti.MAX_DIDASCALIA_UTF16:
        errori.append("didascalia troppo lunga")
    if s["didascalia"].count("#") > contenuti.MAX_HASHTAG:
        errori.append("troppi hashtag")
    return errori


if __name__ == "__main__":
    male = False
    for s in SPECIALI:
        e = valida(s)
        print(f"[{'OK ' if not e else 'ERR'}] {s['slug']} ({s['quando']})")
        for x in e:
            print("      -", x); male = True
    raise SystemExit(1 if male else 0)
