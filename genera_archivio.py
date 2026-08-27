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
# Indirizzo pubblico dell'archivio (og:, canonical, sitemap)
BASE = "https://luigismith.github.io/DIVULGA"

# Verifica di Google Search Console: incollare qui SOLO il valore del
# meta tag (l'attributo content=""), non il tag intero. Serve una volta
# sola: Google lo rilegge a ogni controllo, quindi va lasciato.
VERIFICA_GOOGLE = "0vfIqQS7qWidmaUT612RKvzIQcODP0mePQOechm3OO0"

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

article h1.titolo-scheda{font-family:'Oswald',sans-serif;font-weight:700;font-size:clamp(30px,7vw,44px);
  text-transform:uppercase;margin-top:8px;line-height:1.06;text-wrap:balance}
article .occhiello{font-family:'Oswald',sans-serif;font-weight:500;font-size:clamp(20px,3.4vw,26px);
  margin-top:10px;color:#38291d;line-height:1.25}
article .sommario{margin-top:10px;font-size:18px;color:#6b5138;max-width:62ch}
article h2{font-family:'Oswald',sans-serif;font-weight:700;font-size:25px;text-transform:uppercase;
  margin-top:36px;letter-spacing:.02em}
article p{margin-top:12px;max-width:66ch}
.specifiche{display:flex;flex-wrap:wrap;border:2px solid #38291d;margin-top:26px;background:#fdf6e7}
.specifiche .spec{flex:1 1 160px;padding:14px 18px;border-right:2px solid #38291d}
.specifiche .spec:last-child{border-right:none}
.specifiche dt{font-family:'IBM Plex Mono',monospace;font-size:11.5px;letter-spacing:.16em;color:#c25f1d;font-weight:600}
.specifiche dd{font-family:'Oswald',sans-serif;font-weight:700;font-size:23px;text-transform:uppercase;margin-top:4px}
ul.artisti{margin-top:14px;padding-left:20px;max-width:66ch}
ul.artisti li{margin-bottom:9px}
blockquote.dinamo{margin-top:22px;background:#e9dcbf;border:2px solid #38291d;padding:18px 22px;
  font-family:'Oswald',sans-serif;font-weight:500;font-size:23px;line-height:1.3;max-width:66ch}
blockquote.dinamo span{display:block;font-family:'IBM Plex Mono',monospace;font-size:11.5px;
  letter-spacing:.18em;color:#c25f1d;font-weight:600;margin-bottom:7px}
.slides figure{margin:0}
.fonti ol{margin:10px 0 0 20px}
.fonti li{margin-bottom:7px}
.fonti .data{color:#8a7a63}
.credito-foto{margin-top:12px}
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


def _pagina(titolo, corpo, descrizione, og_image=None, canonical=None,
            verifica=False):
    og = (f'<meta property="og:title" content="{html.escape(titolo)}">'
          f'<meta property="og:description" content="{html.escape(descrizione)}">'
          '<meta property="og:type" content="website">')
    if og_image:
        og += f'<meta property="og:image" content="{og_image}">'
    if canonical:
        og += f'<link rel="canonical" href="{canonical}">'
    if verifica and VERIFICA_GOOGLE:
        og += f'<meta name="google-site-verification" content="{VERIFICA_GOOGLE}">'
    return f"""<!doctype html><html lang="it"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{html.escape(descrizione)}">{og}
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
        # pagina della singola scheda.
        # LEZIONE IMPARATA (27/08/2026): prima qui finivano solo le sei
        # immagini, e Google non legge il testo dentro un JPEG: ogni pagina
        # aveva ~126 parole indicizzabili, tutte di servizio. Il contenuto
        # vero (la macchina, l'inventore, come funziona, gli artisti,
        # l'aneddoto) resta nelle tavole PER IL LETTORE, ma da qui in poi
        # va anche in HTML, che è ciò che i motori sanno leggere.
        slides = "".join(
            f'<figure><img src="{i:02d}.jpg" loading="lazy" '
            f'alt="{html.escape(contenuti.alt_slide(s, i))[:300]}"></figure>'
            for i in range(1, 7))
        fonti = "".join(
            f'<li><a href="{html.escape(f["url"])}" rel="nofollow noopener" '
            f'target="_blank">{html.escape(f["titolo"])}</a> '
            f'<span class="data">verificata il {f["data"]}</span></li>'
            for f in s["fonti"])
        artisti = "".join(
            f'<li><strong>{html.escape(u["artista"])}</strong> — {html.escape(u["nota"])}</li>'
            for u in s["chi_lusata"])
        specifiche = "".join(
            f'<div class="spec"><dt>{html.escape(k)}</dt><dd>{html.escape(v)}</dd></div>'
            for k, v in s["specifiche"])
        foto = s["foto"]

        # Dati strutturati: dicono ai motori che questa è una scheda
        # divulgativa su uno strumento musicale, con data e fonti.
        #
        # LEZIONE IMPARATA (27/08/2026): qui l'oggetto della scheda era
        # marcato "@type": "Product". Search Console l'ha bocciato —
        # «Snippet prodotto: 1 elemento non valido» — perché Google
        # convalida i Product come schede di negozio e PRETENDE almeno uno
        # fra offers, review, aggregateRating. Un Minimoog del 1970 non è
        # in vendita e non ha recensioni: non mancava un campo, era
        # sbagliato il tipo. Thing descrive la stessa entità senza
        # promettere un prezzo che non esiste.
        # REGOLA: mai Product per qualcosa che non si compra. Prima di
        # aggiungere un tipo schema.org, controllare se Google ci attacca
        # un rich result: se sì, o si rispettano i campi obbligatori o si
        # usa un tipo più generico.
        strutturati = json.dumps({
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": f"{s['strumento']} ({s['anno']}) — {s['gancio']}",
            "description": s["sottotitolo"],
            "image": f"{BASE}/tavole/{s['slug']}/01.jpg",
            "datePublished": p.get("quando", "")[:10],
            "inLanguage": "it",
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": f"{BASE}/tavole/{s['slug']}/",
            },
            "author": {"@type": "Organization", "name": "Elettrofoni"},
            "publisher": {"@type": "Organization", "name": "Elettrofoni"},
            "about": {
                "@type": "Thing",
                "name": s["strumento"],
                "description": (f"Strumento musicale elettronico del {s['anno']}, "
                                f"costruito da {s['costruttore']} ({s['luogo']})."),
            },
            "citation": [f["titolo"] for f in s["fonti"]],
        }, ensure_ascii=False)

        corpo = f"""{_testata()}<main>
<article>
<div class="anno">SCHEDA {s['numero']:03d} · {s['anno']} · {html.escape(s['luogo'])}</div>
<h1 class="titolo-scheda">{html.escape(s['strumento'])}</h1>
<p class="occhiello">{html.escape(s['gancio'])}</p>
<p class="sommario">{html.escape(s['sottotitolo'])}</p>
{f'<a class="ig" href="{p["permalink"]}" rel="noopener">VEDI IL POST SU INSTAGRAM →</a>' if p.get('permalink') else ''}

<dl class="specifiche">{specifiche}</dl>

<h2>Che cos'è</h2>
<p>{html.escape(s['la_macchina'])}</p>

<h2>Chi l'ha costruita: {html.escape(s['inventore_nome'])}</h2>
<p>{html.escape(s['inventore'])}</p>

<h2>Come funziona</h2>
<p>{html.escape(s['come_funziona'])}</p>

<h2>Chi l'ha usata</h2>
<ul class="artisti">{artisti}</ul>

<h2>L'aneddoto</h2>
<p>{html.escape(s['aneddoto'])}</p>
<blockquote class="dinamo"><span>Dinamo dice</span>«{html.escape(s['battuta_dinamo'])}»</blockquote>

<div class="slides">{slides}</div>

<div class="fonti">
<h2>Fonti</h2>
<ol>{fonti}</ol>
<p class="credito-foto">Foto: {html.escape(foto['autore'])} · {foto['licenza']} · {foto['fonte']}</p>
<p><a href="../../">← tutte le schede</a></p>
</div>
</article>
</main>{_piede()}
<script type="application/ld+json">{strutturati}</script>"""

        descrizione = f"{s['strumento']} ({s['anno']}): {s['sottotitolo']} Storia, tecnologia e artisti, con fonti verificate."
        (DOCS / "tavole" / s["slug"]).mkdir(parents=True, exist_ok=True)
        (DOCS / "tavole" / s["slug"] / "index.html").write_text(
            _pagina(f"{s['strumento']} ({s['anno']}) — storia e come funziona | Elettrofoni",
                    corpo, descrizione,
                    og_image=f"{BASE}/tavole/{s['slug']}/01.jpg",
                    canonical=f"{BASE}/tavole/{s['slug']}/"),
            encoding="utf-8")

    vuoto = "<p>Le prime schede stanno arrivando.</p>" if not card else ""
    corpo = f"""{_testata(" L'archivio completo delle schede pubblicate.")}<main>{vuoto}{''.join(card)}</main>{_piede()}"""
    og_idx = f"{BASE}/tavole/{stato['pubblicati'][-1]['slug']}/01.jpg" if stato["pubblicati"] else None
    (DOCS / "index.html").write_text(
        _pagina("Elettrofoni — storia dei sintetizzatori e degli strumenti elettronici",
                corpo,
                "Sintetizzatori, drum machine, organi e campionatori: chi li ha inventati, "
                "come funzionano e chi li ha suonati. Una scheda al giorno, con fonti verificate.",
                verifica=True,
                og_image=og_idx, canonical=f"{BASE}/"),
        encoding="utf-8")
    # Pages non deve passare da Jekyll (servirebbe solo a rompere i path)
    (DOCS / ".nojekyll").write_text("")
    # SEO: sitemap con le sole pagine pubblicate + robots che la indica.
    # <lastmod> dice a Google quando la pagina è cambiata: senza, ogni
    # ripassata è alla cieca. La home porta la data dell'ultimo post,
    # ogni scheda la propria data di pubblicazione.
    ultimo = max((q["quando"][:10] for q in stato["pubblicati"]), default=None)
    voci = [(f"{BASE}/", ultimo, "daily")]
    voci += [(f"{BASE}/tavole/{q['slug']}/", q["quando"][:10], "monthly")
             for q in stato["pubblicati"]]
    righe_sm = "".join(
        f"<url><loc>{u}</loc>"
        + (f"<lastmod>{d}</lastmod>" if d else "")
        + f"<changefreq>{f}</changefreq></url>"
        for u, d, f in voci)
    (DOCS / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"{righe_sm}</urlset>", encoding="utf-8")
    # NOTA (27/08/2026): su GitHub Pages in un sottopercorso questo
    # robots.txt NON viene letto dai crawler — vale solo quello alla
    # radice del dominio (luigismith.github.io/robots.txt), che non è
    # nostro. Lo teniamo perché è innocuo e diventerà valido il giorno
    # in cui il sito avrà un dominio proprio. La sitemap va comunque
    # dichiarata a mano in Search Console, come abbiamo fatto.
    (DOCS / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    print(f"[archivio] {len(card)} schede pubblicate in docs/")


if __name__ == "__main__":
    main()
