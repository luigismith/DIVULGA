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

STILE = """
*{margin:0;padding:0;box-sizing:border-box}
body{background:#f4e9d2;color:#38291d;font-family:Georgia,serif;line-height:1.6}
header{background:#38291d;color:#f4e9d2;padding:28px 6vw;display:flex;align-items:center;gap:18px;flex-wrap:wrap}
header .q{width:44px;height:44px;background:#d9702e;display:flex;align-items:center;justify-content:center;flex:none}
header .q svg{width:30px;height:30px}
header h1{font-size:30px;letter-spacing:.1em}
header p{width:100%;font-size:15px;color:#e9d9b8}
.strip{height:10px;background:#d9702e}
main{max-width:980px;margin:0 auto;padding:40px 5vw}
.scheda{display:flex;gap:26px;border:2px solid #38291d;background:#fff8ea;margin-bottom:30px;text-decoration:none;color:inherit}
.scheda img{width:280px;height:350px;object-fit:cover;flex:none}
.scheda .info{padding:22px 24px}
.scheda h2{font-size:26px;text-transform:uppercase}
.scheda .anno{color:#d9702e;font-weight:bold;font-size:14px;letter-spacing:.15em}
.scheda p{margin-top:10px;font-size:16px}
.slides{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px;margin:26px 0}
.slides img{width:100%;display:block;border:2px solid #38291d}
.fonti{font-size:14px;color:#6b5138;border-top:2px solid #38291d;margin-top:26px;padding-top:14px}
footer{background:#d9702e;color:#38291d;text-align:center;padding:20px;font-size:14px;letter-spacing:.08em;font-weight:bold}
a.ig{display:inline-block;margin-top:14px;background:#38291d;color:#f4e9d2;padding:10px 18px;text-decoration:none;font-size:14px;letter-spacing:.1em}
@media(max-width:640px){.scheda{flex-direction:column}.scheda img{width:100%;height:auto}}
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
<title>{html.escape(titolo)}</title><style>{STILE}</style></head>
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
