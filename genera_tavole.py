# -*- coding: utf-8 -*-
"""
ELETTROFONI — generatore grafico.

HTML + CSS resi in JPEG 1080×1350 con Playwright e Chromium headless.
HTML e non un tool di grafica perché il testo cambia lunghezza a ogni
scheda e serve un autofit che rimpicciolisce il carattere finché entra.

Output: docs/tavole/<slug>/01.jpg ... 06.jpg  (docs/ è la radice di
GitHub Pages: l'API di Instagram non accetta upload di file, scarica
da un URL pubblico).

IMPAGINATO (rifatto il 13/09/2026 dopo che il proprietario ha bocciato
la prima revisione: «puoi fare sicuramente di meglio»). La prima
revisione aveva cambiato i font e infilato foto diverse negli stessi
buchi: la struttura restava quella di un documento — testata alta,
titolo, otto righe di testo, una foto graffettata in fondo. Un carosello
si sfoglia su un telefono a braccio teso, e lì lo strumento deve essere
il protagonista. Ora:
  - la foto è a tutta larghezza, senza cornice, e su ogni tavola sta in
    una posizione diversa (copertina: sopra il nome; 2: sopra il testo;
    3: sotto il testo; 4: sopra, con la legenda incollata; 5 e 6 sono
    tipografiche, che è il cambio di ritmo);
  - le foto sono fuse con la carta (`mix-blend-mode: multiply`): i
    ritagli su fondo bianco, che su Commons sono la maggioranza, non
    galleggiano più in un rettangolo bianco ma stanno sulla crema come
    in un catalogo stampato;
  - ogni sezione ha il suo numerone in arancio, la testata è un marchio
    di 66px e non un'intestazione da 117;
  - il testo corrente è a 32px (era 29-31): sul telefono un pixel della
    tavola vale un terzo di pixel dello schermo.

Uso:
    python genera_tavole.py            # genera le tavole di tutte le schede
    python genera_tavole.py minimoog   # solo una scheda
"""
import os
import struct
import sys
import pathlib

import contenuti

RADICE = pathlib.Path(__file__).parent
FONTS = (RADICE / "template" / "fonts").as_uri()

# Palette e identità (decise in fase 0 — non cambiarle a caso: la
# riconoscibilità è metà del progetto)
CREMA = "#f4e9d2"
CREMA2 = "#e9d9b8"
BRUNO = "#38291d"
ARANCIO = "#d9702e"
BRUNO2 = "#5a4530"   # prosa secondaria (note, didascalie lunghe)

AUTOMA_SVG = """
<svg viewBox="0 0 200 200" fill="none" stroke="{c}">
  <line x1="100" y1="40" x2="100" y2="22" stroke-width="8"/>
  <circle cx="100" cy="16" r="7" fill="{c}" stroke="none"/>
  <rect x="52" y="44" width="96" height="90" rx="14" stroke-width="9"/>
  <rect x="34" y="74" width="14" height="26" rx="4" fill="{c}" stroke="none"/>
  <rect x="152" y="74" width="14" height="26" rx="4" fill="{c}" stroke="none"/>
  <circle cx="80" cy="80" r="14" stroke-width="7" stroke="{occhi}"/>
  <circle cx="120" cy="80" r="14" stroke-width="7" stroke="{occhi}"/>
  <circle cx="80" cy="80" r="4" fill="{occhi}" stroke="none"/>
  <circle cx="120" cy="80" r="4" fill="{occhi}" stroke="none"/>
  <line x1="79" y1="106" x2="79" y2="120" stroke-width="6" stroke-linecap="round"/>
  <line x1="93" y1="106" x2="93" y2="120" stroke-width="6" stroke-linecap="round"/>
  <line x1="107" y1="106" x2="107" y2="120" stroke-width="6" stroke-linecap="round"/>
  <line x1="121" y1="106" x2="121" y2="120" stroke-width="6" stroke-linecap="round"/>
</svg>"""


def _automa(colore, occhi):
    return AUTOMA_SVG.format(c=colore, occhi=occhi)


# ---------------------------------------------------------------- CSS ---

def css_base():
    return f"""
@font-face{{font-family:'Oswald';src:url({FONTS}/Oswald-700.woff2) format('woff2');font-weight:700}}
@font-face{{font-family:'Oswald';src:url({FONTS}/Oswald-500.woff2) format('woff2');font-weight:500}}
@font-face{{font-family:'PlexMono';src:url({FONTS}/IBMPlexMono-400.woff2) format('woff2');font-weight:400}}
@font-face{{font-family:'PlexMono';src:url({FONTS}/IBMPlexMono-400i.woff2) format('woff2');font-weight:400;font-style:italic}}
@font-face{{font-family:'PlexMono';src:url({FONTS}/IBMPlexMono-600.woff2) format('woff2');font-weight:600}}
/* SCELTA TIPOGRAFICA (13/09/2026, richiesta dal proprietario: «usa coppie
   di font compatibili»). Prima c'erano due sole facce e tutta la prosa
   lunga stava in IBM Plex Mono a 28-30px: il monospazio e' una faccia da
   DATI, e su otto righe di racconto stanca l'occhio e fa sembrare la
   tavola un terminale invece di una pagina di catalogo.
   Ora i ruoli sono tre:
     Oswald      -> display: nome della macchina, titoli, numeroni, valori
     PlexSerif   -> testo corrente, tutta la prosa (il gancio in corsivo)
     PlexMono    -> solo dati: etichette, sigle, specifiche, fonti, crediti
   Il serif e' della STESSA superfamiglia del mono: stesso scheletro,
   stessa altezza-x, disegnati per stare insieme. La compatibilita' della
   coppia e' una proprieta' del disegno, non un'opinione. */
@font-face{{font-family:'PlexSerif';src:url({FONTS}/IBMPlexSerif-400.woff2) format('woff2');font-weight:400}}
@font-face{{font-family:'PlexSerif';src:url({FONTS}/IBMPlexSerif-600.woff2) format('woff2');font-weight:600}}
@font-face{{font-family:'PlexSerif';src:url({FONTS}/IBMPlexSerif-400i.woff2) format('woff2');font-weight:400;font-style:italic}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;overflow:hidden;background:{CREMA};color:{BRUNO};
  font-family:'Oswald';display:flex;flex-direction:column;position:relative}}
/* La testata e' un marchio, non un'intestazione: 66px. Era 117 e su
   sei tavole uguali pesava come la riga di un modulo. */
.testata{{flex:none;height:66px;background:{BRUNO};color:{CREMA};padding:0 44px;
  display:flex;align-items:center;justify-content:space-between}}
.blocco-logo{{display:flex;align-items:center;gap:16px}}
.quadratino{{width:38px;height:38px;background:{ARANCIO};display:flex;align-items:center;justify-content:center;flex:none}}
.quadratino svg{{width:27px;height:27px}}
.nome{{font-weight:700;font-size:30px;letter-spacing:.14em;line-height:1}}
.serie{{text-align:right;font-family:'PlexMono';font-size:12px;letter-spacing:.14em;line-height:1.6;color:{CREMA2}}}
.strip{{flex:none;height:6px;background:{ARANCIO}}}
.corpo{{flex:1;position:relative;display:flex;flex-direction:column;min-height:0}}
.kicker{{font-family:'PlexMono';font-weight:600;font-size:15px;letter-spacing:.24em;color:{ARANCIO}}}
/* Intesta di sezione: numerone arancio + etichetta + titolo, su una riga
   di base comune. E' l'unico ornamento delle tavole interne, e porta
   informazione (a che punto del carosello sei). */
.intesta{{flex:none;display:flex;align-items:flex-end;gap:24px;margin:28px 52px 0;
  padding-bottom:16px;border-bottom:3px solid {BRUNO}}}
.numerone{{flex:none;font-weight:700;font-size:104px;line-height:.78;color:{ARANCIO};letter-spacing:-.03em}}
.intesta-testi{{flex:1;min-width:0;display:flex;flex-direction:column;gap:10px}}
/* LEZIONE IMPARATA: un titolo dentro un contenitore flex viene compresso
   e l'autofit lo taglia — quindi flex:none sui titoli, sempre. */
.titolo,.titolone{{flex:none;font-weight:700;font-size:50px;line-height:1;text-transform:uppercase}}
.testo{{font-family:'PlexSerif';font-size:34px;line-height:1.5;margin:22px 52px 0;overflow:hidden;min-height:0}}
/* Foto a tutta larghezza. `multiply` fonde la foto con la carta: i
   ritagli su fondo bianco (la maggioranza, su Commons) non galleggiano
   piu' in un rettangolo bianco sulla crema. */
.fotobanda{{flex:none;position:relative;overflow:hidden;background:{CREMA};display:flex;align-items:center;justify-content:center}}
.fotobanda img{{display:block;width:100%;height:100%;object-fit:cover;mix-blend-mode:multiply}}
.didascalia{{position:absolute;left:52px;bottom:16px;background:{ARANCIO};color:{BRUNO};
  font-family:'PlexMono';font-weight:600;font-size:13px;letter-spacing:.14em;padding:7px 12px}}
/* Il credito e' un obbligo di licenza, non una decorazione: su una foto
   chiara il grigio all'80% spariva. Fondino scuro e testo pieno. */
.credito{{position:absolute;right:0;bottom:0;font-family:'PlexMono';font-size:11px;
  color:{CREMA};letter-spacing:.04em;background:rgba(20,14,9,.66);padding:5px 10px}}
.pager{{flex:none;margin:auto 52px 0;display:flex;align-items:center;justify-content:space-between;
  border-top:3px solid {BRUNO};padding:14px 0 20px;font-family:'PlexMono';font-weight:600;font-size:14px;letter-spacing:.16em}}
.pager .num{{color:{ARANCIO}}}
.pager .qui{{font-family:'Oswald';font-weight:700;font-size:22px;letter-spacing:.04em}}
.zoccolo{{flex:none;background:{ARANCIO};color:{BRUNO};padding:18px 52px;display:flex;align-items:center;justify-content:space-between}}
.motto{{font-family:'PlexMono';font-weight:600;font-size:15px;letter-spacing:.12em}}
.handle{{font-weight:700;font-size:22px;letter-spacing:.14em}}
.autofit{{min-height:0}}
"""


AUTOFIT_JS = """
// Autofit: rimpicciolisce il carattere finché il testo entra nel suo
// contenitore. Gira dopo il caricamento dei font E delle immagini:
// data-pronto su fonts.ready poteva scattare prima del decode della foto.
Promise.all([document.fonts.ready,
             ...Array.from(document.images).map(i => i.decode().catch(() => null))]).then(() => {
  for (const el of document.querySelectorAll('.autofit')) {
    let size = parseFloat(getComputedStyle(el).fontSize);
    const min = parseFloat(el.dataset.min || '18');
    while ((el.scrollHeight > el.clientHeight || el.scrollWidth > el.clientWidth) && size > min) {
      size -= 1;
      el.style.fontSize = size + 'px';
    }
  }
  // Riquadri adattivi (copertina, storia): la foto riempie lo spazio che
  // resta, ma il ritaglio e' limitato a data-cap (1.25 = si perde al
  // massimo il 20% del lato lungo). Oltre, meglio un bordo di crema che
  // una macchina senza tastiera.
  for (const box of document.querySelectorAll('.fotobanda[data-cap]')) {
    const img = box.querySelector('img');
    if (!img.naturalWidth) continue;
    const asp = img.naturalWidth / img.naturalHeight;
    const cap = parseFloat(box.dataset.cap);
    const h = Math.min(box.clientHeight, box.clientWidth / asp * cap);
    img.style.height = Math.round(h) + 'px';
  }
  document.body.dataset.pronto = '1';
});
"""


def _pagina(corpo_html, css_extra=""):
    return f"""<!doctype html><html><head><meta charset="utf-8">
<style>{css_base()}{css_extra}</style></head>
<body>{corpo_html}<script>{AUTOFIT_JS}</script></body></html>"""


def _testata(scheda):
    return f"""
  <div class="testata">
    <div class="blocco-logo">
      <div class="quadratino">{_automa(BRUNO, CREMA)}</div>
      <div class="nome">ELETTROFONI</div>
    </div>
    <div class="serie">CATALOGO DELLE MACCHINE SONORE<br>SCHEDA {scheda['numero']:03d} · {scheda['serie']}</div>
  </div>
  <div class="strip"></div>"""


def _pager(scheda, n):
    return f"""<div class="pager"><span class="qui">{scheda['strumento'].upper()}</span><span class="num">{n} / 6 →</span></div>"""


def _zoccolo():
    return f"""<div class="zoccolo"><div class="motto">{contenuti.FIRMA}</div><div class="handle">@ELETTROFONI</div></div>"""


def _intesta(n, etichetta, titolo, max_h=120, min_px=30):
    return f"""<div class="intesta">
    <div class="numerone">{n:02d}</div>
    <div class="intesta-testi">
      <div class="kicker">{etichetta}</div>
      <div class="titolo autofit" data-min="{min_px}" style="height:auto;max-height:{max_h}px">{titolo}</div>
    </div>
  </div>"""


# -------------------------------------------------------------- foto ---

def _dimensioni(path):
    """(larghezza, altezza) in pixel di un JPEG o PNG, leggendo solo
    l'intestazione: niente Pillow, che nel container non c'e'."""
    d = pathlib.Path(path).read_bytes()
    if d[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", d[16:24])
    if d[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(d):
            if d[i] != 0xFF:
                i += 1
                continue
            m = d[i + 1]
            if m == 0xFF:
                i += 1
                continue
            if m in (0xD8, 0x01) or 0xD0 <= m <= 0xD7:
                i += 2
                continue
            lung = struct.unpack(">H", d[i + 2:i + 4])[0]
            if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                h, w = struct.unpack(">HH", d[i + 5:i + 9])
                return w, h
            i += 2 + lung
    return None


def _aspetto(foto):
    dim = _dimensioni(RADICE / foto["file"])
    if not dim or not dim[1]:
        return 1.5
    return dim[0] / dim[1]


def foto_di(scheda, i=0):
    """La i-esima foto della scheda: 0 e' la principale, 1.. sono le
    «foto_extra». Se l'indice non esiste si ricade sulla principale.

    LEZIONE IMPARATA (13/09/2026, segnalata dal proprietario: «ove
    possibile piu' immagini dello strumento»). Le slide 2 e 3 una banda
    fotografica ce l'avevano gia' — ma pescavano tutte da scheda["foto"],
    cioe' mostravano TRE VOLTE LA STESSA IMMAGINE. Non mancavano le
    fotografie: mancava la varieta', ed e' un difetto che si vede solo
    scorrendo il carosello intero, non guardando una tavola alla volta.
    REGOLA: quando un layout ripete un elemento, verificare che ripeta la
    STRUTTURA e non il CONTENUTO."""
    extra = scheda.get("foto_extra") or []
    if i == 0 or i > len(extra):
        return scheda["foto"]
    return extra[i - 1]


def _ripetuta(scheda, i):
    """True se la slide i non ha una foto sua e ricade sulla principale."""
    return i > 0 and i > len(scheda.get("foto_extra") or [])


# Quando la scheda non ha foto extra, la principale torna sulle tavole
# interne con un ritaglio diverso per tavola (ingrandimento + punto di
# messa a fuoco): copertina = la macchina intera, dentro = i dettagli.
# Non e' una seconda foto, ma non e' nemmeno la stessa immagine tre volte.
# Chiave = indice della foto (1 = slide 2, 2 = slide 3, 3 = slide 4).
RITAGLI = {
    1: ("1.55", "30% 45%", "Dettaglio"),
    2: ("1.55", "72% 55%", "Dettaglio"),
    3: ("2.1", "50% 40%", "Dettaglio"),
    4: ("1.4", "50% 62%", "Dettaglio"),
}


def _foto_credito(scheda, foto=None):
    f = foto or scheda["foto"]
    return f"Foto: {f['autore']} · {f['licenza']} · {f['fonte']}"


def _banda(scheda, i, altezza=None, stile="", extra_html=""):
    """Banda fotografica a tutta larghezza con la i-esima foto della
    scheda, didascalia e credito della SUA licenza.

    `altezza` in px; senza, il riquadro prende tutto lo spazio che resta
    nella colonna (copertina, storia) e la foto lo riempie ritagliando al
    massimo il 20% (`data-cap`, vedi AUTOFIT_JS): oltre, restano bordi di
    crema piuttosto che perdere la macchina.

    Foto con `ritaglio: True` (scontornate su fondo bianco, la maggioranza
    su Commons): si mostrano INTERE (`contain`). Col `multiply` il bianco
    diventa crema e la macchina sta sulla carta senza rettangolo."""
    foto = foto_di(scheda, i)
    uri = (RADICE / foto["file"]).as_uri()
    pos = foto.get("posizione", "center")
    did = foto.get("didascalia")
    img_stile = f"object-position:{pos}"
    box_attr = ""
    if foto.get("ritaglio"):
        img_stile += ";object-fit:contain"
    elif altezza is None:
        box_attr = ' data-cap="1.25"'
    if _ripetuta(scheda, i) and i in RITAGLI:
        zoom, origine, did = RITAGLI[i]
        img_stile += f";transform:scale({zoom});transform-origin:{origine}"
    box_stile = f"height:{altezza}px;" if altezza else "flex:1 1 auto;min-height:0;"
    did_html = f'<div class="didascalia">{did.upper()}</div>' if did else ""
    return (f'<div class="fotobanda"{box_attr} style="{box_stile}{stile}">'
            f'<img src="{uri}" style="{img_stile}">{did_html}{extra_html}'
            f'<div class="credito">{_foto_credito(scheda, foto)}</div></div>')


# ------------------------------------------------------------- slides ---

def slide_copertina(scheda):
    spec = "".join(
        f'<div class="spec"><div class="k">{k}</div><div class="v">{v}</div></div>'
        for k, v in scheda["specifiche"]
    )
    css = f"""
.blocco{{flex:none;display:flex;flex-direction:column;padding:24px 52px 26px}}
.kicker{{flex:none}}
/* LEZIONE IMPARATA (30/08/2026): la copertina non portava il nome dello
   strumento. Da nessuna parte. Nella griglia del profilo si vede solo la
   copertina, e chi scorre non sa di che macchina si parla. Ora il nome
   e' la cosa piu' grande della tavola dopo la foto; il gancio sta sotto,
   in corsivo serif, come l'occhiello di una rivista. */
.nome-macchina{{flex:none;font-weight:700;font-size:110px;line-height:.94;text-transform:uppercase;
  letter-spacing:-.012em;margin-top:10px}}
.gancio{{flex:none;font-family:'PlexSerif';font-style:italic;font-size:44px;line-height:1.28;margin-top:20px;max-width:980px}}
.specifiche{{flex:none;margin-top:34px;display:flex;border-top:3px solid {BRUNO};border-bottom:3px solid {BRUNO};padding:14px 0}}
.spec{{flex:1;padding:0 18px;border-left:2px solid {BRUNO}}}
.spec:first-child{{padding-left:0;border-left:none}}
.spec .k{{font-family:'PlexMono';font-weight:600;font-size:12px;letter-spacing:.18em;color:{ARANCIO}}}
.spec .v{{font-weight:700;font-size:25px;line-height:1.15;text-transform:uppercase;margin-top:6px}}
"""
    corpo = f"""
{_testata(scheda)}
{_banda(scheda, 0)}
<div class="blocco">
  <div class="kicker">{scheda['anno']} · {scheda['luogo'].upper()}</div>
  <div class="nome-macchina autofit" data-min="56" style="height:auto;max-height:220px">{scheda['strumento']}</div>
  <div class="gancio autofit" data-min="28" style="height:auto;max-height:180px">{scheda['gancio']}</div>
  <div class="specifiche">{spec}</div>
</div>
{_zoccolo()}
"""
    return _pagina(corpo, css)


def slide_macchina(scheda):
    css = ".testo{flex:1 1 auto}"
    corpo = f"""
{_testata(scheda)}
{_banda(scheda, 1, 500)}
{_intesta(2, "LA MACCHINA", "Che cos'è")}
<div class="testo autofit" data-min="22">{scheda['la_macchina']}</div>
{_pager(scheda, 2)}
"""
    return _pagina(corpo, css)


def slide_inventore(scheda):
    # Tavola specchiata rispetto alla 2: prima il testo, la foto in fondo.
    # Due tavole uguali di fila si sfogliano senza vederle.
    css = """
.testo{flex:0 1 auto}
.fotobanda{margin-top:auto}
.pager{margin-top:0}
"""
    corpo = f"""
{_testata(scheda)}
{_intesta(3, "CHI L'HA COSTRUITA", scheda['inventore_nome'])}
<div class="testo autofit" data-min="22" style="margin-bottom:26px">{scheda['inventore']}</div>
{_banda(scheda, 2, 470)}
{_pager(scheda, 3)}
"""
    return _pagina(corpo, css)


def slide_funzionamento(scheda):
    # La legenda (i tre «FIG.») sta incollata sotto la foto, su fondo
    # bruno: foto + didascalia tecnica, come la figura di un manuale.
    voci = "".join(
        f'<div class="voce"><div class="fig">{k}</div><div class="txt">{v}</div></div>'
        for k, v in scheda.get("richiami", [])
    )
    css = f"""
.legenda{{flex:none;display:flex;background:{BRUNO};color:{CREMA};padding:0 52px}}
.voce{{flex:1;padding:16px 18px 18px;border-left:2px solid rgba(244,233,210,.22)}}
.voce:first-child{{padding-left:0;border-left:none}}
.voce .fig{{font-family:'PlexMono';font-weight:600;font-size:12px;letter-spacing:.2em;color:{ARANCIO}}}
.voce .txt{{font-weight:500;font-size:22px;line-height:1.15;text-transform:uppercase;letter-spacing:.03em;margin-top:5px}}
.testo{{flex:1 1 auto}}
"""
    corpo = f"""
{_testata(scheda)}
{_banda(scheda, 3, 420)}
<div class="legenda">{voci}</div>
{_intesta(4, "COME FUNZIONA", "La tecnologia, semplice")}
<div class="testo autofit" data-min="22">{scheda['come_funziona']}</div>
{_pager(scheda, 4)}
"""
    return _pagina(corpo, css)


def slide_artisti(scheda):
    righe = "".join(
        f"""<div class="artista"><div class="idx">{i:02d}</div><div class="art">
            <div class="chi">{u['artista']}</div><div class="cosa">{u['nota']}</div></div></div>"""
        for i, u in enumerate(scheda["chi_lusata"], start=1)
    )
    # Tutto in em sul contenitore: cosi' l'autofit, che tocca solo il
    # font-size della .lista, riduce nomi, note e spazi insieme. Con le
    # misure in px sui figli l'autofit girava a vuoto.
    css = f"""
.lista{{flex:1 1 auto;min-height:0;margin:0 52px;display:flex;flex-direction:column;
  justify-content:space-evenly;overflow:hidden;font-size:62px}}
.artista{{display:flex;align-items:flex-start;gap:.5em;padding:.32em 0;border-bottom:2px solid {BRUNO}}}
.artista:last-child{{border-bottom:none}}
.idx{{flex:none;font-family:'PlexMono';font-weight:600;font-size:.27em;letter-spacing:.16em;color:{ARANCIO};padding-top:.55em}}
.art{{flex:1;min-width:0}}
.chi{{font-weight:700;font-size:1em;line-height:1;text-transform:uppercase;letter-spacing:.01em}}
.cosa{{font-family:'PlexSerif';font-size:.43em;line-height:1.45;color:{BRUNO2};margin-top:.16em}}
.ascolto{{flex:none;margin:22px 52px 0;display:flex;align-items:center;gap:26px;
  border:3px solid {BRUNO};background:{CREMA2};padding:20px 26px}}
.disco{{flex:none;width:96px;height:96px;border-radius:50%;position:relative;
  background:repeating-radial-gradient(circle,{BRUNO} 0 3px,#4d3a2b 3px 5px)}}
.disco::after{{content:'';position:absolute;inset:32px;border-radius:50%;background:{ARANCIO};
  box-shadow:0 0 0 3px {BRUNO}}}
.ascolto .et{{font-family:'PlexMono';font-weight:600;font-size:13px;letter-spacing:.22em;color:{ARANCIO}}}
.ascolto .brano{{font-weight:700;font-size:32px;line-height:1.1;margin-top:6px}}
.ascolto .nota{{font-family:'PlexSerif';font-size:22px;line-height:1.4;color:{BRUNO2};margin-top:6px}}
"""
    # Il riquadro sta qui e non sulla slide 6 per due motivi: e' la
    # continuazione naturale di «chi l'ha usata», e la slide 5 aveva un
    # buco di spazio vuoto in fondo su tutte le schede.
    a = scheda.get("da_ascoltare")
    ascolto = ""
    if a:
        ascolto = (f'<div class="ascolto"><div class="disco"></div><div>'
                   f'<div class="et">DA ASCOLTARE</div>'
                   f'<div class="brano">{a["artista"]}, «{a["brano"]}» ({a["anno"]})</div>'
                   f'<div class="nota">{a["cosa"]}</div></div></div>')
    # Con uno o due nomi (e' il caso di parecchie macchine italiane, che
    # hanno un solo grande interprete documentato) la lista galleggiava
    # in mezzo a mezza tavola vuota. Lo spazio che avanza lo prende una
    # quarta foto: una riga ~210px per nome, il riquadro d'ascolto ~210.
    n = len(scheda["chi_lusata"])
    avanzo = 1350 - 72 - 28 - 116 - 64 - (212 if a else 0) - n * 210 - 30
    banda = ""
    if avanzo >= 220:
        banda = _banda(scheda, 4, min(480, avanzo), stile="margin-top:22px")
    corpo = f"""
{_testata(scheda)}
{_intesta(5, "CHI L'HA USATA", "Dai laboratori ai dischi")}
<div class="lista autofit" data-min="30">{righe}</div>
{ascolto}
{banda}
{_pager(scheda, 5)}
"""
    return _pagina(corpo, css)


# ATTENZIONE (04/09/2026): la slide 6 porta anche la CTA. Le tavole delle
# schede GIA' USCITE non vanno rigenerate — devono continuare a
# corrispondere ai post pubblicati, come per «DINAMO DICE». Il workflow
# genera solo la prossima scheda, quindi succede da solo; il rischio c'e'
# solo se qualcuno le rigenera tutte a mano.
def _etichetta_chiusura(scheda):
    """«AVVERTENZE» sulle schede nuove, «DINAMO DICE» sulle prime quattro.
    Quelle quattro erano gia' pubblicate quando la regola e' cambiata: le
    tavole online devono continuare a corrispondere ai post usciti."""
    return "AVVERTENZE" if scheda.get("avvertenza") else "DINAMO DICE"


def _testo_chiusura(scheda):
    if scheda.get("avvertenza"):
        return scheda["avvertenza"]
    return f"«{scheda['battuta_dinamo']}»"


def slide_aneddoto(scheda):
    fonti = "".join(f"<div>· {f['titolo']} — verificata {f['data']}</div>" for f in scheda["fonti"])
    css = f"""
.testo{{flex:none;max-height:420px}}
/* L'avvertenza e' un'etichetta da manuale d'uso: bordo pieno, costa
   arancio, l'automa che compila il catalogo. */
.avviso{{flex:none;display:flex;align-items:center;gap:24px;margin:26px 52px 0;
  background:{CREMA2};border:3px solid {BRUNO};border-left:16px solid {ARANCIO};padding:20px 26px 20px 22px}}
.avviso svg{{width:104px;height:104px;flex:none}}
.avviso .chi{{font-family:'PlexMono';font-weight:600;font-size:14px;letter-spacing:.22em;color:{ARANCIO};margin-bottom:8px}}
.avviso .frase{{font-weight:500;font-size:31px;line-height:1.25}}
.fonti{{flex:none;margin:auto 52px 0;padding-top:22px;font-family:'PlexMono';font-size:13px;line-height:1.6;color:#6b5138;overflow:hidden;max-height:150px}}
.fonti b{{font-weight:600;letter-spacing:.18em}}
/* La CTA e' la cosa che chi arriva dal reel deve vedere: grande, sopra
   lo zoccolo, con la freccia che indica i commenti. */
.cta{{flex:none;margin:22px 52px 0;display:flex;align-items:center;gap:24px;border-top:3px solid {ARANCIO};padding:20px 0 22px}}
.cta .freccia{{flex:none;font-weight:700;font-size:64px;line-height:1;color:{ARANCIO}}}
.cta .frase{{font-weight:700;font-size:44px;line-height:1.1;text-transform:uppercase}}
"""
    corpo = f"""
{_testata(scheda)}
{_intesta(6, "L'ANEDDOTO", "Per chiudere")}
<div class="testo autofit" data-min="20">{scheda['aneddoto']}</div>
<div class="avviso">
  {_automa(ARANCIO, BRUNO)}
  <div><div class="chi">{_etichetta_chiusura(scheda)}</div><div class="frase">{_testo_chiusura(scheda)}</div></div>
</div>
<div class="fonti autofit" data-min="10"><b>FONTI</b><br>{fonti}</div>
<div class="cta"><div class="freccia">↓</div><div class="frase autofit" data-min="26" style="height:auto;max-height:150px">{contenuti.cta(scheda)}</div></div>
{_zoccolo()}
"""
    return _pagina(corpo, css)


# ---------------------------------------------------------- storia ---

def slide_storia(scheda):
    """Tavola verticale 1080x1920 per le Storie: stesso mondo visivo, ma
    formato 9:16. E' la riserva del reel (che di norma fa da storia): se
    fallisce non blocca niente (vedi pubblica.py)."""
    css = f"""
body{{height:1920px}}
.testata{{height:84px;padding:0 60px}}
.nome{{font-size:38px}}
.quadratino{{width:48px;height:48px}}
.quadratino svg{{width:34px;height:34px}}
.serie{{font-size:14px}}
.blocco{{flex:none;display:flex;flex-direction:column;padding:34px 60px 44px}}
.kicker{{flex:none;font-size:19px}}
.nome-macchina{{flex:none;font-weight:700;font-size:126px;line-height:.94;text-transform:uppercase;letter-spacing:-.012em;margin-top:12px}}
.gancio{{flex:none;font-family:'PlexSerif';font-style:italic;font-size:50px;line-height:1.28;margin-top:24px}}
.sottotitolo{{flex:none;font-family:'PlexSerif';font-size:32px;line-height:1.45;color:{BRUNO2};margin-top:22px}}
.invito{{flex:none;margin-top:44px;display:flex;align-items:center;gap:30px;border-top:3px solid {ARANCIO};padding-top:30px}}
.invito .freccia{{flex:none;font-weight:700;font-size:96px;line-height:1;color:{ARANCIO}}}
.invito .riga{{font-family:'PlexMono';font-weight:600;font-size:22px;letter-spacing:.2em;color:{ARANCIO}}}
.invito .grande{{font-weight:700;font-size:58px;text-transform:uppercase;line-height:1.05;margin-top:8px}}
.zoccolo{{padding:24px 60px}}
.motto{{font-size:18px}}
.handle{{font-size:27px}}
"""
    corpo = f"""
{_testata(scheda)}
{_banda(scheda, 0)}
<div class="blocco">
  <div class="kicker">{scheda['anno']} · {scheda['luogo'].upper()}</div>
  <div class="nome-macchina autofit" data-min="60" style="height:auto;max-height:240px">{scheda['strumento']}</div>
  <div class="gancio autofit" data-min="30" style="height:auto;max-height:260px">{scheda['gancio']}</div>
  <div class="sottotitolo">{scheda['sottotitolo']}</div>
  <div class="invito"><div class="freccia">↓</div><div><div class="riga">LA SCHEDA COMPLETA</div><div class="grande">nel profilo</div></div></div>
</div>
{_zoccolo()}
"""
    return _pagina(corpo, css)


SLIDES = [slide_copertina, slide_macchina, slide_inventore,
          slide_funzionamento, slide_artisti, slide_aneddoto]


# ------------------------------------------------------------- render ---

def rendi_scheda(scheda, page, out_dir=None):
    out_dir = out_dir or (RADICE / "docs" / "tavole" / scheda["slug"])
    out_dir.mkdir(parents=True, exist_ok=True)
    for i, costruisci in enumerate(SLIDES, start=1):
        html = costruisci(scheda)
        tmp = out_dir / f"_{i:02d}.html"
        tmp.write_text(html, encoding="utf-8")
        page.goto(tmp.as_uri())
        page.wait_for_selector("body[data-pronto='1']")
        page.screenshot(path=str(out_dir / f"{i:02d}.jpg"), type="jpeg", quality=90,
                        clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
        tmp.unlink()

    # tavola verticale per la Storia (1080x1920)
    tmp = out_dir / "_story.html"
    tmp.write_text(slide_storia(scheda), encoding="utf-8")
    page.set_viewport_size({"width": 1080, "height": 1920})
    page.goto(tmp.as_uri())
    page.wait_for_selector("body[data-pronto='1']")
    page.screenshot(path=str(out_dir / "story.jpg"), type="jpeg", quality=90,
                    clip={"x": 0, "y": 0, "width": 1080, "height": 1920})
    tmp.unlink()
    page.set_viewport_size({"width": 1080, "height": 1350})
    print(f"[tavole] {scheda['slug']}: 6 slide + storia in {out_dir}")


def main():
    from playwright.sync_api import sync_playwright

    filtro = sys.argv[1] if len(sys.argv) > 1 else None
    if filtro == "--prossima":
        # Solo la prossima scheda in coda (usato dal workflow di pubblicazione)
        import json
        stato_file = RADICE / "stato.json"
        gia = set()
        if stato_file.exists():
            gia = {p["slug"] for p in json.loads(stato_file.read_text())["pubblicati"]}
        prossima = contenuti.scheda_da_pubblicare(gia)
        if prossima is None:
            print("[tavole] nessuna scheda verificata in coda: niente da generare")
            return
        filtro = prossima["slug"]
    schede = [s for s in contenuti.SCHEDE if filtro in (None, s["slug"])]
    if not schede:
        print(f"Nessuna scheda trovata per '{filtro}'"); raise SystemExit(1)
    for s in schede:
        errs = contenuti.valida_scheda(s)
        if errs:
            print(f"[STOP] scheda '{s['slug']}' non valida: {errs}")
            raise SystemExit(1)

    # ELETTROFONI_TAVOLE_OUT: cartella alternativa per le PROVE di layout,
    # cosi' si puo' guardare una scheda gia' pubblicata senza toccare le
    # tavole online (che devono restare uguali al post uscito).
    out_base = os.environ.get("ELETTROFONI_TAVOLE_OUT")
    exe = os.environ.get("ELETTROFONI_CHROMIUM")  # override locale; in CI usa il chromium di Playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=exe, args=["--no-sandbox", "--force-color-profile=srgb"])
        page = browser.new_page(viewport={"width": 1080, "height": 1350})
        for s in schede:
            out = pathlib.Path(out_base) / s["slug"] if out_base else None
            rendi_scheda(s, page, out)
        browser.close()


if __name__ == "__main__":
    main()
