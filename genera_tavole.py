# -*- coding: utf-8 -*-
"""
ELETTROFONI — generatore grafico.

HTML + CSS resi in JPEG 1080×1350 con Playwright e Chromium headless.
HTML e non un tool di grafica perché il testo cambia lunghezza a ogni
scheda e serve un autofit che rimpicciolisce il carattere finché entra.

Output: docs/tavole/<slug>/01.jpg ... 06.jpg  (docs/ è la radice di
GitHub Pages: l'API di Instagram non accetta upload di file, scarica
da un URL pubblico).

Uso:
    python genera_tavole.py            # genera le tavole di tutte le schede
    python genera_tavole.py minimoog   # solo una scheda
"""
import os
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
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;overflow:hidden;background:{CREMA};color:{BRUNO};
  font-family:'Oswald';display:flex;flex-direction:column;position:relative}}
.testata{{flex:none;background:{BRUNO};color:{CREMA};padding:26px 56px;display:flex;align-items:center;justify-content:space-between}}
.blocco-logo{{display:flex;align-items:center;gap:20px}}
.quadratino{{width:48px;height:48px;background:{ARANCIO};display:flex;align-items:center;justify-content:center;flex:none}}
.quadratino svg{{width:34px;height:34px}}
.nome{{font-weight:700;font-size:42px;letter-spacing:.12em;line-height:1}}
.serie{{text-align:right;font-family:'PlexMono';font-size:14px;letter-spacing:.13em;line-height:1.8;color:{CREMA2}}}
.strip{{flex:none;height:12px;background:{ARANCIO}}}
.corpo{{flex:1;position:relative;display:flex;flex-direction:column;padding:44px 56px 0;min-height:0}}
.kicker{{flex:none;display:flex;align-items:center;gap:16px;font-family:'PlexMono';font-weight:600;font-size:17px;letter-spacing:.2em;color:{ARANCIO}}}
.kicker::after{{content:'';flex:1;height:2px;background:{BRUNO};opacity:.25}}
/* LEZIONE IMPARATA: un titolo dentro un contenitore flex viene compresso
   e l'autofit lo taglia — quindi flex:none sui titoli, sempre. */
.titolone{{flex:none;font-weight:700;line-height:1.04;text-transform:uppercase;margin-top:14px}}
.pager{{flex:none;margin-top:auto;display:flex;align-items:center;justify-content:space-between;
  border-top:3px solid {BRUNO};padding:16px 0 22px;font-family:'PlexMono';font-weight:600;font-size:15px;letter-spacing:.16em}}
.pager .num{{color:{ARANCIO}}}
.zoccolo{{flex:none;background:{ARANCIO};color:{BRUNO};padding:20px 56px;display:flex;align-items:center;justify-content:space-between}}
.motto{{font-family:'PlexMono';font-weight:600;font-size:16px;letter-spacing:.12em}}
.handle{{font-weight:700;font-size:22px;letter-spacing:.14em}}
.credito{{position:absolute;right:10px;bottom:12px;font-family:'PlexMono';font-size:10.5px;color:rgba(244,233,210,.8);letter-spacing:.04em}}
.autofit{{min-height:0}}
"""


AUTOFIT_JS = """
// Autofit: rimpicciolisce il carattere finché il testo entra nel suo
// contenitore. Gira dopo il caricamento dei font.
document.fonts.ready.then(() => {
  for (const el of document.querySelectorAll('.autofit')) {
    let size = parseFloat(getComputedStyle(el).fontSize);
    const min = parseFloat(el.dataset.min || '18');
    while ((el.scrollHeight > el.clientHeight || el.scrollWidth > el.clientWidth) && size > min) {
      size -= 1;
      el.style.fontSize = size + 'px';
    }
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
    return f"""<div class="pager"><span>{scheda['strumento'].upper()}</span><span class="num">{n} / 6 →</span></div>"""


def _foto_credito(scheda):
    f = scheda["foto"]
    return f"Foto: {f['autore']} · {f['licenza']} · {f['fonte']}"


# ------------------------------------------------------------- slides ---

def slide_copertina(scheda):
    foto_uri = (RADICE / scheda["foto"]["file"]).as_uri()
    pos = scheda["foto"].get("posizione", "center")
    spec = "".join(
        f'<div class="spec"><div class="k">{k}</div><div class="v">{v}</div></div>'
        for k, v in scheda["specifiche"]
    )
    css = f"""
.ghost{{position:absolute;top:2px;right:40px;font-weight:700;font-size:200px;line-height:1;color:{CREMA2};z-index:0}}
.titolone{{position:relative;z-index:1;font-size:86px}}
.sottotitolo{{flex:none;position:relative;z-index:1;font-weight:500;font-size:29px;margin-top:12px;color:#6b5138;max-width:850px;line-height:1.3}}
.fototel{{flex:none;position:relative;z-index:1;margin-top:30px;border-top:8px solid {BRUNO};border-bottom:8px solid {BRUNO};background:#111}}
.fototel img{{display:block;width:100%;height:500px;object-fit:cover;object-position:{pos}}}
.etichetta-foto{{position:absolute;left:0;bottom:8px;background:{ARANCIO};color:{BRUNO};font-family:'PlexMono';font-weight:600;font-size:15px;letter-spacing:.12em;padding:9px 16px}}
.specifiche{{flex:none;display:flex;margin-top:30px;border:2px solid {BRUNO}}}
.spec{{flex:1;padding:16px 20px;border-right:2px solid {BRUNO}}}
.spec:last-child{{border-right:none}}
.spec .k{{font-family:'PlexMono';font-size:13px;letter-spacing:.16em;color:{ARANCIO};font-weight:600}}
.spec .v{{font-weight:700;font-size:27px;text-transform:uppercase;margin-top:6px}}
.corpo{{padding-bottom:0}}
"""
    corpo = f"""
{_testata(scheda)}
<div class="corpo">
  <div class="ghost">{scheda['numero']:03d}</div>
  <div class="kicker">{scheda['anno']} · {scheda['luogo'].upper()}</div>
  <div class="titolone autofit" data-min="46" style="height:auto;max-height:300px">{scheda['gancio']}</div>
  <div class="sottotitolo">{scheda['sottotitolo']}</div>
  <div class="fototel">
    <img src="{foto_uri}">
    <div class="etichetta-foto">LA MACCHINA, DAL VERO</div>
    <div class="credito">{_foto_credito(scheda)}</div>
  </div>
  <div class="specifiche">{spec}</div>
</div>
<div style="flex:1"></div>
<div class="zoccolo"><div class="motto">{contenuti.FIRMA}</div><div class="handle">@ELETTROFONI</div></div>
"""
    return _pagina(corpo, css)


def _slide_testo(scheda, n, etichetta, titolo, testo, foto_alta=None):
    """Layout comune delle slide interne: kicker, titolo, testo grande in
    autofit, eventuale banda fotografica, pager."""
    css = f"""
.titolone{{font-size:64px}}
.testo{{flex:1 1 auto;font-family:'PlexMono';font-size:30px;line-height:1.62;margin-top:30px;
  overflow:hidden;max-width:940px}}
.fotobanda{{flex:none;position:relative;margin:26px -56px 0;border-top:6px solid {BRUNO};background:#111}}
.fotobanda img{{display:block;width:100%;height:{foto_alta or 0}px;object-fit:cover;object-position:{scheda["foto"].get("posizione", "center")}}}
"""
    foto_html = ""
    if foto_alta:
        foto_uri = (RADICE / scheda["foto"]["file"]).as_uri()
        foto_html = f"""<div class="fotobanda"><img src="{foto_uri}">
        <div class="credito">{_foto_credito(scheda)}</div></div>"""
    corpo = f"""
{_testata(scheda)}
<div class="corpo">
  <div class="kicker">{n:02d} · {etichetta}</div>
  <div class="titolone autofit" data-min="40" style="height:auto;max-height:160px">{titolo}</div>
  <div class="testo autofit" data-min="21">{testo}</div>
  {foto_html}
  {_pager(scheda, n)}
</div>
"""
    return _pagina(corpo, css)


def slide_macchina(scheda):
    return _slide_testo(scheda, 2, "LA MACCHINA", "Che cos'è", scheda["la_macchina"], foto_alta=360)


def slide_inventore(scheda):
    return _slide_testo(scheda, 3, "CHI L'HA COSTRUITA", scheda["inventore_nome"], scheda["inventore"], foto_alta=300)


def slide_funzionamento(scheda):
    richiami = "".join(
        f'<div class="richiamo"><div class="fig">{k}</div><div class="txt">{v}</div></div>'
        for k, v in scheda.get("richiami", [])
    )
    extra = ""
    if richiami:
        extra = f'<div class="richiami">{richiami}</div>'
    css = f"""
.titolone{{font-size:64px}}
.testo{{flex:0 1 auto;font-family:'PlexMono';font-size:29px;line-height:1.6;margin-top:28px;overflow:hidden;max-width:940px}}
.richiami{{flex:none;display:flex;border:2px solid {BRUNO};margin-top:34px}}
.richiamo{{flex:1;text-align:center;padding:16px 10px;border-right:2px solid {BRUNO}}}
.richiamo:last-child{{border-right:none}}
.richiamo .fig{{font-family:'PlexMono';font-weight:600;font-size:14px;letter-spacing:.14em;color:{ARANCIO}}}
.richiamo .txt{{font-weight:700;font-size:23px;letter-spacing:.06em;margin-top:5px;text-transform:uppercase}}
"""
    corpo = f"""
{_testata(scheda)}
<div class="corpo">
  <div class="kicker">04 · COME FUNZIONA</div>
  <div class="titolone autofit" data-min="40" style="height:auto;max-height:160px">La tecnologia, semplice</div>
  <div class="testo autofit" data-min="21">{scheda['come_funziona']}</div>
  {extra}
  {_pager(scheda, 4)}
</div>
"""
    return _pagina(corpo, css)


def slide_artisti(scheda):
    righe = "".join(
        f"""<div class="artista"><div class="chi">{u['artista']}</div><div class="cosa">{u['nota']}</div></div>"""
        for u in scheda["chi_lusata"]
    )
    css = f"""
.titolone{{font-size:64px}}
.lista{{flex:1 1 auto;margin-top:30px;overflow:hidden}}
.artista{{display:flex;align-items:baseline;justify-content:space-between;gap:24px;
  border-bottom:2px solid {BRUNO};padding:34px 0}}
.artista:first-child{{border-top:2px solid {BRUNO}}}
.chi{{font-weight:700;font-size:46px;text-transform:uppercase;letter-spacing:.02em;flex:none}}
.cosa{{font-family:'PlexMono';font-size:22px;color:#6b5138;text-align:right;line-height:1.45}}
.ascolto{{flex:none;border:2px solid {BRUNO};background:{CREMA2};padding:22px 26px;margin-top:26px}}
.ascolto .et{{font-family:'PlexMono';font-weight:600;font-size:14px;letter-spacing:.18em;
  color:{ARANCIO};margin-bottom:10px}}
.ascolto .brano{{font-weight:700;font-size:34px;line-height:1.15;margin-bottom:8px}}
.ascolto .nota{{font-family:'PlexMono';font-size:21px;line-height:1.5;color:#5a4530}}
"""
    # Il riquadro sta qui e non sulla slide 6 per due motivi: e' la
    # continuazione naturale di «chi l'ha usata», e la slide 5 aveva un
    # buco di spazio vuoto in fondo su tutte le schede.
    a = scheda.get("da_ascoltare")
    ascolto = ""
    if a:
        ascolto = (f'<div class="ascolto"><div class="et">DA ASCOLTARE</div>'
                   f'<div class="brano">{a["artista"]}, «{a["brano"]}» ({a["anno"]})</div>'
                   f'<div class="nota">{a["cosa"]}</div></div>')
    corpo = f"""
{_testata(scheda)}
<div class="corpo">
  <div class="kicker">05 · CHI L'HA USATA</div>
  <div class="titolone autofit" data-min="40" style="height:auto;max-height:160px">Dai laboratori ai dischi</div>
  <div class="lista autofit" data-min="16">{righe}</div>
  {ascolto}
  {_pager(scheda, 5)}
</div>
"""
    return _pagina(corpo, css)


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
.titolone{{font-size:64px}}
.testo{{flex:none;font-family:'PlexMono';font-size:28px;line-height:1.6;margin-top:26px;overflow:hidden;max-width:940px;max-height:330px}}
.dinamo{{flex:none;display:flex;align-items:center;gap:26px;margin-top:34px;
  background:{CREMA2};border:2px solid {BRUNO};padding:24px 30px}}
.dinamo svg{{width:120px;height:120px;flex:none}}
.balloon{{font-weight:500;font-size:30px;line-height:1.3}}
.balloon .chi{{font-family:'PlexMono';font-weight:600;font-size:14px;letter-spacing:.18em;color:{ARANCIO};margin-bottom:8px}}
.fonti{{flex:1 1 auto;font-family:'PlexMono';font-size:15px;line-height:1.7;color:#6b5138;margin-top:26px;overflow:hidden}}
.corpo{{padding-bottom:0}}
"""
    corpo = f"""
{_testata(scheda)}
<div class="corpo">
  <div class="kicker">06 · L'ANEDDOTO</div>
  <div class="titolone autofit" data-min="40" style="height:auto;max-height:160px">Per chiudere</div>
  <div class="testo autofit" data-min="20">{scheda['aneddoto']}</div>
  <div class="dinamo">
    {_automa(ARANCIO, BRUNO)}
    <div class="balloon"><div class="chi">{_etichetta_chiusura(scheda)}</div>{_testo_chiusura(scheda)}</div>
  </div>
  <div class="fonti autofit" data-min="11"><b>FONTI</b><br>{fonti}</div>
</div>
<div class="zoccolo"><div class="motto">{contenuti.FIRMA}</div><div class="handle">@ELETTROFONI</div></div>
"""
    return _pagina(corpo, css)


# ---------------------------------------------------------- storia ---

def slide_storia(scheda):
    """Tavola verticale 1080x1920 per le Storie: stesso mondo visivo, ma
    formato 9:16. La storia e' il megafono, il post e' la missione: se
    fallisce non blocca niente (vedi pubblica.py)."""
    foto_uri = (RADICE / scheda["foto"]["file"]).as_uri()
    pos = scheda["foto"].get("posizione", "center")
    css = f"""
body{{height:1920px}}
.corpo{{padding:0 60px;justify-content:center;gap:0}}
.kicker{{font-size:20px;letter-spacing:.22em}}
.titolone{{font-size:82px;margin-top:20px}}
.sottotitolo{{flex:none;font-weight:500;font-size:32px;margin-top:18px;color:#6b5138;line-height:1.32}}
.fotostoria{{flex:none;position:relative;margin-top:46px;border:6px solid {BRUNO};background:#111}}
.fotostoria img{{display:block;width:100%;height:640px;object-fit:cover;object-position:{pos}}}
.etichetta-foto{{position:absolute;left:0;bottom:10px;background:{ARANCIO};color:{BRUNO};
  font-family:'PlexMono';font-weight:600;font-size:18px;letter-spacing:.12em;padding:11px 20px}}
.invito{{flex:none;margin-top:52px;text-align:center}}
.invito .riga{{font-family:'PlexMono';font-weight:600;font-size:23px;letter-spacing:.15em;color:{ARANCIO}}}
.invito .grande{{font-weight:700;font-size:54px;text-transform:uppercase;margin-top:14px;line-height:1.1}}
.freccia{{font-size:60px;margin-top:18px;color:{ARANCIO}}}
.testata{{padding:34px 60px}}
.nome{{font-size:50px}}
.zoccolo{{padding:26px 60px}}
.motto{{font-size:19px}}
.handle{{font-size:27px}}
"""
    corpo = f"""
{_testata(scheda)}
<div class="corpo">
  <div class="kicker">{scheda['anno']} · {scheda['luogo'].upper()}</div>
  <div class="titolone autofit" data-min="48" style="height:auto;max-height:340px">{scheda['gancio']}</div>
  <div class="sottotitolo">{scheda['sottotitolo']}</div>
  <div class="fotostoria">
    <img src="{foto_uri}">
    <div class="etichetta-foto">SCHEDA {scheda['numero']:03d}</div>
    <div class="credito">{_foto_credito(scheda)}</div>
  </div>
  <div class="invito">
    <div class="riga">LA SCHEDA COMPLETA</div>
    <div class="grande">nel profilo</div>
    <div class="freccia">↓</div>
  </div>
</div>
<div class="zoccolo"><div class="motto">{contenuti.FIRMA}</div><div class="handle">@ELETTROFONI</div></div>
"""
    return _pagina(corpo, css)


SLIDES = [slide_copertina, slide_macchina, slide_inventore,
          slide_funzionamento, slide_artisti, slide_aneddoto]


# ------------------------------------------------------------- render ---

def rendi_scheda(scheda, page):
    out_dir = RADICE / "docs" / "tavole" / scheda["slug"]
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

    exe = os.environ.get("ELETTROFONI_CHROMIUM")  # override locale; in CI usa il chromium di Playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=exe, args=["--no-sandbox", "--force-color-profile=srgb"])
        page = browser.new_page(viewport={"width": 1080, "height": 1350})
        for s in schede:
            rendi_scheda(s, page)
        browser.close()


if __name__ == "__main__":
    main()
