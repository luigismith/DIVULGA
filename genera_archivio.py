# -*- coding: utf-8 -*-
"""
ELETTROFONI — sito-archivio su GitHub Pages.

Elenca SOLO i post già usciti (la coda non si mostra): è gratis, è
indicizzabile e porta traffico. Ricostruito a ogni pubblicazione.
"""
import html
import json
import pathlib

import contenuti

RADICE = pathlib.Path(__file__).parent
DOCS = RADICE / "docs"

FONT_LINK = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
             '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
             'family=Oswald:wght@500;700&family=IBM+Plex+Mono:wght@400;600&'
             'family=IBM+Plex+Sans:wght@400;500&display=swap">')

STILE = """
*{margin:0;padding:0;box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{background:#f4e9d2;color:#38291d;font-family:'IBM Plex Sans',system-ui,sans-serif;
  line-height:1.62;font-size:17px;display:flex;flex-direction:column;min-height:100vh}
header{background:#38291d;color:#f4e9d2;padding:26px 6vw 22px;display:flex;align-items:center;gap:18px;flex-wrap:wrap}
header .q{width:46px;height:46px;background:#d9702e;display:flex;align-items:center;justify-content:center;flex:none}
header .q svg{width:32px;height:32px}
header h1{font-family:'Oswald',sans-serif;font-weight:700;font-size:31px;letter-spacing:.11em;line-height:1}
header p{width:100%;font-family:'IBM Plex Mono',monospace;font-size:12.5px;letter-spacing:.09em;color:#e9d9b8;margin-top:4px}
.strip{height:10px;background:#d9702e;flex:none}
main{flex:1;width:100%;max-width:980px;margin:0 auto;padding:44px 5vw 56px}
.vuoto{font-size:18px;color:#6b5138}
.scheda{display:flex;gap:0;border:2px solid #38291d;background:#fdf6e7;margin-bottom:28px;
  text-decoration:none;color:inherit;transition:transform .15s ease,box-shadow .15s ease}
.scheda:hover{transform:translateY(-2px);box-shadow:6px 6px 0 rgba(56,41,29,.18)}
.scheda:focus-visible{outline:3px solid #d9702e;outline-offset:3px}
.scheda img{width:270px;height:338px;object-fit:cover;flex:none;border-right:2px solid #38291d}
.scheda .info{padding:24px 26px}
.scheda h2{font-family:'Oswald',sans-serif;font-weight:700;font-size:27px;text-transform:uppercase;line-height:1.12;margin-top:4px}
.anno{font-family:'IBM Plex Mono',monospace;color:#c25f1d;font-weight:600;font-size:12.5px;letter-spacing:.16em}
.scheda p{margin-top:11px;font-size:16.5px;color:#6b5138}
h2.titolo-scheda{font-family:'Oswald',sans-serif;font-weight:700;font-size:clamp(28px,6vw,36px);
  text-transform:uppercase;margin-top:8px;line-height:1.08}
.slides{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:16px;margin:28px 0}
.slides img{width:100%;display:block;border:2px solid #38291d}
.fonti{font-family:'IBM Plex Mono',monospace;font-size:13.5px;line-height:1.75;color:#6b5138;
  border-top:2px solid #38291d;margin-top:28px;padding-top:16px}
.fonti a{color:#c25f1d}
footer{background:#d9702e;color:#38291d;text-align:center;padding:20px 5vw;flex:none;
  font-family:'IBM Plex Mono',monospace;font-size:13px;letter-spacing:.11em;font-weight:600}
footer a{color:#38291d}
a.ig{display:inline-block;margin-top:16px;background:#38291d;color:#f4e9d2;padding:12px 20px;
  text-decoration:none;font-family:'Oswald',sans-serif;font-weight:500;font-size:15px;letter-spacing:.1em;text-transform:uppercase}
a.ig:hover{background:#c25f1d}
@media(max-width:640px){
  body{font-size:16px}
  .scheda{flex-direction:column}
  .scheda img{width:100%;height:auto;border-right:none;border-bottom:2px solid #38291d}
}
"""

AUTOMA = """<svg viewBox="0 0 200 200" fill="none" stroke="#38291d">
<line x1="100" y1="40" x2="100" y2="22" stroke-width="8"/><circle cx="100" cy="16" r="7" fill="#38291d" stroke="none"/>
<rect x="52" y="44" width="96" height="90" rx="14" stroke-width="9"/>
<rect x="34" y="74" width="14" height="26" rx="4" fill="#38291d" stroke="none"/>
<rect x="152" y="74" width="14" height="26" rx="4" fill="#38291d" stroke="none"/>
<circle cx="80" cy="80" r="14" stroke-width="7" stroke="#f4e9d2"/><circle cx="120" cy="80" r="14" stroke-width="7" stroke="#f4e9d2"/>
<circle cx="80" cy="80" r="4" fill="#f4e9d2" stroke="none"/><circle cx="120" cy="80" r="4" fill="#f4e9d2" stroke="none"/>
<line x1="79" y1="106" x2="79" y2="120" stroke-width="6" stroke-linecap="round"/><line x1="93" y1="106" x2="93" y2="120" stroke-width="6" stroke-linecap="round"/>
<line x1="107" y1="106" x2="107" y2="120" stroke-width="6" stroke-linecap="round"/><line x1="121" y1="106" x2="121" y2="120" stroke-width="6" stroke-linecap="round"/>
</svg>"""


def _testata(sotto=""):
    return f"""<header><div class="q">{AUTOMA}</div><h1>ELETTROFONI</h1>
<p>Le macchine che hanno cambiato la musica, una scheda alla volta.{sotto}</p></header><div class="strip"></div>"""


def _piede():
    return f"""<footer>{html.escape(contenuti.FIRMA)} · <a style="color:#38291d" href="https://www.instagram.com/elettrofoni/">@elettrofoni</a></footer>"""


def _pagina(titolo, corpo, descrizione):
    return f"""<!doctype html><html lang="it"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{html.escape(descrizione)}">
<title>{html.escape(titolo)}</title>{FONT_LINK}<style>{STILE}</style></head>
<body>{corpo}</body></html>"""


def main():
    stato = json.loads((RADICE / "stato.json").read_text()) if (RADICE / "stato.json").exists() \
        else {"pubblicati": []}
    per_slug = {s["slug"]: s for s in contenuti.SCHEDE}
    DOCS.mkdir(exist_ok=True)

    card = []
    for p in stato["pubblicati"]:
        s = per_slug.get(p["slug"])
        if not s:
            continue
        card.append(f"""
<a class="scheda" href="tavole/{s['slug']}/">
  <img src="tavole/{s['slug']}/01.jpg" alt="{html.escape(s['strumento'])}">
  <div class="info"><div class="anno">SCHEDA {s['numero']:03d} · {s['anno']}</div>
  <h2>{html.escape(s['strumento'])}</h2>
  <p>{html.escape(s['gancio'])}.</p></div>
</a>""")
        # pagina della singola scheda
        slides = "".join(f'<img src="{i:02d}.jpg" alt="{html.escape(s["strumento"])} — slide {i}">'
                         for i in range(1, 7))
        fonti = "".join(f"<div>· {html.escape(f['titolo'])} — verificata il {f['data']}</div>"
                        for f in s["fonti"])
        foto = s["foto"]
        corpo = f"""{_testata()}<main>
<div class="anno" style="color:#d9702e;font-weight:bold;letter-spacing:.15em">SCHEDA {s['numero']:03d} · {s['anno']} · {html.escape(s['luogo'])}</div>
<h2 style="font-size:34px;text-transform:uppercase;margin-top:6px">{html.escape(s['strumento'])}</h2>
<p style="margin-top:10px">{html.escape(s['sottotitolo'])}</p>
{f'<a class="ig" href="{p["permalink"]}">VEDI SU INSTAGRAM →</a>' if p.get('permalink') else ''}
<div class="slides">{slides}</div>
<div class="fonti"><b>FONTI</b>{fonti}<br>Foto: {html.escape(foto['autore'])} · {foto['licenza']} · {foto['fonte']}
<br><a href="../../">← tutte le schede</a></div>
</main>{_piede()}"""
        (DOCS / "tavole" / s["slug"] / "index.html").write_text(
            _pagina(f"{s['strumento']} — Elettrofoni", corpo, s["gancio"]), encoding="utf-8")

    vuoto = "<p>Le prime schede stanno arrivando.</p>" if not card else ""
    corpo = f"""{_testata(" L'archivio completo delle schede pubblicate.")}<main>{vuoto}{''.join(card)}</main>{_piede()}"""
    (DOCS / "index.html").write_text(
        _pagina("Elettrofoni — le macchine che hanno cambiato la musica",
                corpo, "Storia e tecnologia degli strumenti musicali elettronici, una scheda alla volta."),
        encoding="utf-8")
    # Pages non deve passare da Jekyll (servirebbe solo a rompere i path)
    (DOCS / ".nojekyll").write_text("")
    print(f"[archivio] {len(card)} schede pubblicate in docs/")


if __name__ == "__main__":
    main()
