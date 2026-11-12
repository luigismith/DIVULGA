# -*- coding: utf-8 -*-
"""
ELETTROFONI — sito-archivio su GitHub Pages.

Elenca SOLO i post già usciti (la coda non si mostra): è gratis, è
indicizzabile e porta traffico. Ricostruito a ogni pubblicazione.

RIFATTO IL 16/10/2026 (il proprietario: «puoi farlo più bello?», e poi
«se possiamo mettere anche i suoni reali sul sito sarebbe fico»). Prima
era una colonna di copertine del carosello dalla più vecchia alla più
nuova: chi arrivava vedeva per prima la scheda di agosto, e ogni riga
ripeteva in piccolo una tavola piena di testo. Adesso:
- la più nuova sta in cima, e le schede si riconoscono dalla FOTO della
  macchina (non dalla tavola), su carta crema col multiply come nelle
  tavole;
- ricerca e filtri per famiglia (`serie`); la ricerca legge anche gli
  artisti, così chi cerca «Kraftwerk» trova le macchine;
- il suono vero: dove la scheda ha `reel_audio`, un estratto a -16 LUFS
  (lo stesso volume dei reel) col credito e il link alla registrazione;
- ogni scheda porta alla precedente, alla successiva e a quelle della
  stessa famiglia, e i dati strutturati dicono a Google chi pubblica
  (Organization, WebSite) e dove sta la pagina (BreadcrumbList).
Foto, suoni e copertine dei reel per il web si fanno UNA volta e restano
in docs/: `docs/media.json` tiene l'impronta del file d'origine, e si
rifanno solo quando l'origine cambia.

RIDISEGNATO IL 12/11/2026 (il proprietario: «Rifai il SITO STUPENDO»).
La struttura del 16/10 resta (home = catalogo, suoni in pagina loro, una
pagina per scheda): cambia come si presenta.
- Home: una COPERTINA con la vetrina delle ultime cinque macchine (la
  prima schermata fa vedere più macchine, non una: regola del 16/10), il
  nastro coi nomi, la fascia del suono vero con un lettore solo, e nella
  griglia la «linea del tempo» (una colonna per epoca, alta quanto le
  schede che ha) e l'ordine per anno della macchina.
- Schede della griglia senza scatola: la foto in un riquadro di carta, il
  nome sotto, come in un catalogo.
- Pagina della scheda: foto incorniciata, dati tecnici su una targa
  bruna, il reel di fianco al racconto (resta fermo mentre si legge), le
  tavole che si aprono in grande con le frecce (la «lente»),
  l'avvertenza con la banda a righe da etichetta.
- Carta con la grana, testata che resta in alto, le sezioni che entrano
  salendo, e il passaggio fra le pagine dove il browser lo sa fare
  (`@view-transition`: la foto della griglia diventa quella della scheda).
- Dinamo di latta (assets/dinamo/dinamo_reale_b.png, scelto dal
  proprietario il 12/11) nel bollo dell'invito a seguire la pagina.
Niente file pesanti in più: Pages ha un tetto di 1 GB e il sito è già a
722 MB. Tutto il resto è HTML e CSS.
"""
import hashlib
import html
import json
import pathlib
import re
import shutil
import subprocess
import unicodedata
from urllib.parse import urlparse

import contenuti

RADICE = pathlib.Path(__file__).parent
DOCS = RADICE / "docs"
# Indirizzo pubblico dell'archivio (og:, canonical, sitemap, dati
# strutturati). I link FRA le pagine sono tutti relativi: se un giorno
# cambia l'indirizzo, si cambia questa riga e basta.
BASE = "https://luigismith.github.io/DIVULGA"
# La 404 viene servita a QUALSIASI indirizzo sbagliato, anche tre cartelle
# sotto: lì i link relativi non funzionano, servono assoluti.
PERCORSO = urlparse(BASE).path.rstrip("/")
INSTAGRAM = "https://www.instagram.com/elettrofoni/"

# Verifica di Google Search Console: incollare qui SOLO il valore del
# meta tag (l'attributo content=""), non il tag intero. Serve una volta
# sola: Google lo rilegge a ogni controllo, quindi va lasciato.
VERIFICA_GOOGLE = "0vfIqQS7qWidmaUT612RKvzIQcODP0mePQOechm3OO0"

LARGHEZZE_FOTO = (320, 640, 1280)   # srcset: miniature / elenco / apertura
SECONDI_SUONO = 45             # tetto dell'estratto audio sul sito
# Cambiarla rifà foto, suoni e copertine di tutte le schede.
VERSIONE_MEDIA = "1"

e = html.escape

FONT_LINK = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
             '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
             '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
             'family=Oswald:wght@500;600;700&'
             'family=IBM+Plex+Serif:ital,wght@0,400;0,600;1,400&'
             'family=IBM+Plex+Mono:wght@400;600&display=swap">')

# I tre ruoli tipografici delle tavole valgono anche qui: Oswald per nomi,
# titoli e numeri, IBM Plex Serif per la prosa, IBM Plex Mono SOLO per
# dati, etichette, fonti e crediti.
# Arancio: #d9702e va bene per i fondi e per le cose grandi; per il testo
# piccolo su crema il contrasto è 2,8:1 e non si legge. Per quello c'è
# --ruggine (#a84f17, 4,6:1).
def _onda_css():
    """La forma d'onda della barra del lettore: 72 stanghette di altezze
    diverse, sempre le stesse (niente caso: lo stile deve avere
    un'impronta stabile, VERSIONE_CSS)."""
    import math
    barre = []
    for i in range(72):
        h = min(1.0, 0.28 + 0.36 * abs(math.sin(i * 0.53))
                + 0.34 * abs(math.sin(i * 0.19 + 1.3)) * abs(math.cos(i * 0.91)))
        barre.append(f"%3Crect x='{i * 5}' y='{(1 - h) * 15:.1f}' width='3' height='{h * 30:.1f}'/%3E")
    return ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 360 30' "
            "preserveAspectRatio='none'%3E" + "".join(barre) + "%3C/svg%3E\")")


STILE = """
:root{--crema:#f4e9d2;--carta:#fbf4e4;--sabbia:#ead9b6;--bruno:#38291d;--notte:#2a1e15;--bruno2:#5e4733;
--bruno3:#86705a;--arancio:#d9702e;--ruggine:#a84f17;--filo:rgba(56,41,29,.18);--filo-chiaro:rgba(244,233,210,.18);
--display:'Oswald','Arial Narrow',Impact,sans-serif;--serif:'IBM Plex Serif',Georgia,serif;
--mono:'IBM Plex Mono',ui-monospace,Menlo,Consolas,monospace;
--grana:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 .22 0 0 0 0 .16 0 0 0 0 .11 0 0 0 .13 0'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23g)'/%3E%3C/svg%3E")}
*,*::before,*::after{box-sizing:border-box}
*{margin:0;padding:0}
[hidden]{display:none!important}
.nobr{white-space:nowrap}
h1,h2{text-wrap:balance}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth;scroll-padding-top:78px;overflow-x:clip}
@view-transition{navigation:auto}
body{background-color:var(--crema);background-image:var(--grana);color:var(--bruno);font-family:var(--serif);font-size:17px;
  line-height:1.62;min-height:100vh;display:flex;flex-direction:column;-webkit-font-smoothing:antialiased}
main{flex:1}
img,video{max-width:100%;display:block}
a{color:inherit;text-decoration-thickness:1px;text-underline-offset:3px}
button{font:inherit;color:inherit}
:focus-visible{outline:3px solid var(--arancio);outline-offset:3px}
::selection{background:var(--arancio);color:var(--bruno)}
.contenitore{width:100%;max-width:1240px;margin:0 auto;padding-left:18px;padding-right:18px}
@media(min-width:700px){body{font-size:18px}.contenitore{padding-left:36px;padding-right:36px}}
.kicker{font-family:var(--mono);font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;
  font-weight:600;color:var(--ruggine)}
/* Le sezioni entrano salendo di poco quando arrivano sullo schermo. Solo
   con JavaScript (la classe .js la mette lo script in testa alla pagina):
   senza, tutto si vede subito. */
.js .rivela{opacity:0;transform:translateY(18px);transition:opacity .7s ease,transform .7s ease}
.js .rivela.vista{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}.js .rivela{opacity:1;transform:none;transition:none}}

/* testata */
.testata{position:sticky;top:0;z-index:20;background:var(--bruno);color:var(--crema);border-bottom:6px solid var(--arancio)}
.testata .contenitore{display:flex;align-items:center;gap:10px 22px;min-height:58px}
/* Il marchio cede spazio e il menu no: col carattere di ripiego (finché
   Oswald non è caricato, o se non arriva) le scritte sono più larghe, e
   sul telefono la testata usciva di 25 px dallo schermo (12/11/2026:
   trovato provando le pagine coi font bloccati). */
.marchio{display:flex;align-items:center;gap:11px;text-decoration:none;margin-right:auto;min-width:0}
.marchio>span:last-child{min-width:0;overflow:hidden}
.marchio .q{width:36px;height:36px;background:var(--arancio);display:grid;place-items:center;flex:none}
.marchio .q svg{width:26px;height:26px}
.marchio b{display:block;font-family:var(--display);font-weight:700;font-size:20px;letter-spacing:.14em;line-height:1;
  white-space:nowrap;overflow:hidden;text-overflow:clip}
.marchio small{display:none;font-family:var(--mono);font-size:10px;letter-spacing:.16em;
  text-transform:uppercase;color:#dcc7a0;margin-top:5px}
.testata nav{display:flex;gap:0;flex:none}
.testata nav a{position:relative;font-family:var(--display);font-weight:500;font-size:13.5px;letter-spacing:.14em;
  text-transform:uppercase;text-decoration:none;padding:10px 9px}
.testata nav a::after{content:"";position:absolute;left:9px;right:9px;bottom:5px;height:2px;background:var(--arancio);
  transform:scaleX(0);transform-origin:left;transition:transform .2s}
.testata nav a:hover::after{transform:scaleX(1)}
.testata .largo{display:none}
@media(min-width:700px){.testata .contenitore{min-height:68px}.marchio .q{width:42px;height:42px}.marchio .q svg{width:30px;height:30px}
  .marchio b{font-size:24px}.marchio small{display:block}.testata .largo{display:block}.testata nav a{font-size:14px;padding:10px 12px}
  .testata nav a::after{left:12px;right:12px}}
.filetto{display:none}

/* bottoni */
.bottoni{display:flex;flex-wrap:wrap;gap:10px;margin-top:24px}
.bottone{display:inline-flex;align-items:center;gap:8px;font-family:var(--display);font-weight:500;
  font-size:15px;letter-spacing:.12em;text-transform:uppercase;text-decoration:none;padding:12px 20px;
  border:2px solid var(--bruno);color:var(--bruno);background:transparent;
  transition:background .15s,color .15s,border-color .15s,transform .15s,box-shadow .15s}
.bottone:hover{background:var(--bruno);color:var(--crema)}
.bottone.pieno{background:var(--bruno);color:var(--crema)}
.bottone.pieno:hover{background:var(--arancio);border-color:var(--bruno);color:var(--bruno);transform:translate(-2px,-2px);box-shadow:4px 4px 0 var(--bruno)}

/* home: la copertina. Il testo a sinistra, a destra la VETRINA: le
   ultime cinque macchine, perché la prima schermata deve far vedere più
   macchine e non una (regola del 16/10/2026). Sul telefono la vetrina è
   una fila che scorre col dito. */
.copertina{padding-top:26px}
.copertina .contenitore{display:grid;gap:22px;grid-template-areas:"testo" "vetrina" "cifre"}
.cop-testo{grid-area:testo;min-width:0}
.copertina h1{font-family:var(--display);font-weight:700;font-size:clamp(46px,7vw,100px);line-height:.9;
  text-transform:uppercase;letter-spacing:-.012em;margin-top:14px;text-wrap:wrap}
.copertina h1 em{font-style:normal;color:var(--arancio)}
.copertina .lead{font-size:clamp(17px,1.6vw,20px);line-height:1.5;max-width:46ch;margin-top:18px;color:var(--bruno2)}
.vetrina{grid-area:vetrina;display:grid;grid-auto-flow:column;grid-auto-columns:46%;gap:10px;overflow-x:auto;
  scroll-snap-type:x mandatory;margin:0 -18px;padding:0 18px 6px;scrollbar-width:none}
.vetrina::-webkit-scrollbar{display:none}
.tessera{position:relative;display:flex;flex-direction:column;height:196px;background:var(--carta);text-decoration:none;
  border:2px solid var(--bruno);overflow:hidden;scroll-snap-align:start;transition:transform .2s,box-shadow .2s}
.tessera .ft{display:block;flex:1;min-height:0;overflow:hidden}
.tessera img{width:100%;height:100%;object-fit:cover;mix-blend-mode:multiply;transition:transform .6s ease}
.tessera .et{display:flex;align-items:baseline;gap:8px;padding:7px 10px 8px;border-top:2px solid var(--bruno);background:var(--crema);
  transition:background .2s}
.tessera .et i{font-style:normal;font-family:var(--mono);font-size:10.5px;font-weight:600;letter-spacing:.1em;color:var(--ruggine);flex:none}
.tessera .et b{font-family:var(--display);font-weight:700;font-size:15px;line-height:1.1;text-transform:uppercase;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tessera:hover img{transform:scale(1.06)}
.tessera:hover .et{background:var(--arancio)}
.tessera:hover .et i{color:var(--bruno)}
.bollino{position:absolute;top:0;left:0;z-index:1;background:var(--arancio);color:var(--bruno);font-family:var(--mono);
  font-size:11px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;padding:5px 9px}
.cifre{grid-area:cifre;display:grid;grid-template-columns:repeat(2,1fr);border-top:2px solid var(--bruno);border-bottom:2px solid var(--bruno)}
.cifre span{display:flex;flex-direction:column;gap:2px;padding:12px 0 11px;font-family:var(--mono);font-size:11px;
  letter-spacing:.14em;text-transform:uppercase;color:var(--bruno2)}
.cifre span:nth-child(-n+2){border-bottom:1px solid var(--filo)}
.cifre b{font-family:var(--display);font-weight:700;font-size:34px;line-height:1;letter-spacing:0;color:var(--bruno)}
@media(min-width:700px){.cifre{grid-template-columns:repeat(4,1fr)}.cifre span{padding:16px 0 14px 22px;border-left:1px solid var(--filo)}
  .cifre span:first-child{padding-left:0;border-left:none}.cifre span:nth-child(-n+2){border-bottom:none}.cifre b{font-size:46px}}
@media(min-width:980px){
  .copertina{padding-top:44px}
  .copertina .contenitore{grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:34px 52px;align-items:center;
    grid-template-areas:"testo vetrina" "cifre cifre"}
  .vetrina{grid-auto-flow:row;grid-template-columns:repeat(3,1fr);grid-template-rows:minmax(0,1.3fr) minmax(0,1fr);gap:12px;
    height:clamp(400px,58vh,520px);overflow:visible;margin:0;padding:0}
  .tessera{height:auto}
  .tessera.grande{grid-column:span 2}
  .tessera.grande .et{padding:10px 14px 12px}
  .tessera.grande .et b{font-size:26px}
  .tessera:hover{transform:translate(-3px,-3px);box-shadow:7px 7px 0 var(--arancio)}
}

/* home: il nastro coi nomi delle macchine */
.nastro{margin-top:34px;background:var(--bruno);color:var(--crema);overflow:hidden}
.nastro div{display:flex;width:max-content;animation:scorri 90s linear infinite}
.nastro span{font-family:var(--display);font-weight:600;font-size:15px;letter-spacing:.16em;text-transform:uppercase;
  padding:12px 0;white-space:nowrap}
.nastro span::after{content:"";display:inline-block;width:7px;height:7px;background:var(--arancio);margin:0 20px 2px;
  vertical-align:middle;transform:rotate(45deg)}
.nastro:hover div{animation-play-state:paused}
@keyframes scorri{to{transform:translateX(-50%)}}
@media(prefers-reduced-motion:reduce){.nastro div{animation:none}}

/* home: la fascia del suono vero (una riga, non l'elenco: 16/10/2026) */
.ascolta{background:var(--notte);color:var(--crema);border-top:1px solid var(--filo-chiaro)}
.ascolta .contenitore{display:grid;gap:14px 34px;align-items:center;padding-top:22px;padding-bottom:24px}
.ascolta .kicker{color:var(--arancio)}
.ascolta h2{font-family:var(--display);font-weight:700;font-size:clamp(24px,2.6vw,32px);line-height:1.05;text-transform:uppercase;margin-top:6px}
.ascolta .lettore{margin:0;padding:0;background:none;border-left:none}
@media(max-width:699px){.ascolta .lettore-cosa{display:none}}
.ascolta .verso{font-family:var(--display);font-weight:500;font-size:15px;letter-spacing:.12em;text-transform:uppercase;
  text-decoration:none;border:2px solid var(--crema);padding:11px 18px;justify-self:start;white-space:nowrap;transition:background .15s,color .15s}
.ascolta .verso:hover{background:var(--arancio);border-color:var(--arancio);color:var(--bruno)}
@media(min-width:900px){.ascolta .contenitore{grid-template-columns:auto minmax(0,1fr) auto}}

/* gancio e sottotitolo (testa delle schede) */
.gancio{font-family:var(--display);font-weight:500;font-size:clamp(22px,2.5vw,29px);line-height:1.2;margin-top:16px}
.sottotitolo{color:var(--bruno2);margin-top:12px;max-width:52ch}
/* lettore del suono vero */
.lettore{display:grid;grid-template-columns:auto 1fr;gap:6px 16px;align-items:center;background:var(--bruno);
  color:var(--crema);padding:18px 20px;margin-top:24px;border-left:6px solid var(--arancio)}
.lettore audio{grid-column:1/-1;width:100%}
.lettore .play{width:58px;height:58px;border-radius:50%;border:none;background:var(--arancio);color:var(--bruno);
  display:grid;place-items:center;cursor:pointer;transition:transform .12s,box-shadow .2s}
.lettore .play:hover{transform:scale(1.06)}
.lettore.suona .play{box-shadow:0 0 0 6px rgba(217,112,46,.28)}
.lettore .play svg{width:24px;height:24px;fill:currentColor}
.lettore .i-pausa,.lettore.suona .i-play{display:none}
.lettore.suona .i-pausa{display:block}
.lettore-info{display:flex;flex-direction:column;gap:6px;min-width:0}
.lettore-titolo{font-family:var(--mono);font-size:12px;letter-spacing:.16em;text-transform:uppercase;
  font-weight:600;color:var(--arancio);display:flex;align-items:center;gap:10px}
.lettore-cosa{font-size:16px;line-height:1.4;color:#efe2c6}
/* la barra è una forma d'onda: la maschera la disegna, il colore la riempie */
.barra{height:30px;background:rgba(244,233,210,.26);cursor:pointer;position:relative;margin-top:2px;
  -webkit-mask:__ONDA__ center/100% 100% no-repeat;mask:__ONDA__ center/100% 100% no-repeat}
.barra i{position:absolute;left:0;top:0;bottom:0;width:0;background:var(--arancio)}
.lettore-tempo{font-family:var(--mono);font-size:12px;color:#cdb894}
.lettore:not(.js) .play,.lettore:not(.js) .barra,.lettore:not(.js) .lettore-tempo{display:none}
.lettore.js audio{display:none}
.onde{display:inline-flex;gap:2px;align-items:flex-end;height:12px}
.onde i{width:3px;height:4px;background:currentColor}
.lettore.suona .onde i{animation:onda .7s ease-in-out infinite alternate}
.lettore.suona .onde i:nth-child(2){animation-delay:.25s}
.lettore.suona .onde i:nth-child(3){animation-delay:.5s}
@keyframes onda{from{height:3px}to{height:12px}}
@media(prefers-reduced-motion:reduce){.lettore.suona .onde i{animation:none;height:10px}}
.credito-suono{font-family:var(--mono);font-size:12px;line-height:1.55;color:var(--bruno2);margin-top:8px}
.credito-suono a{color:var(--ruggine)}

/* la pagina dei suoni */
.suoni{background:var(--notte);color:var(--crema);padding:48px 0 70px;min-height:60vh}
.suoni .kicker{color:var(--arancio)}
.suoni h1,.suoni h2{font-family:var(--display);font-weight:700;font-size:clamp(44px,7vw,96px);text-transform:uppercase;line-height:.92;margin-top:12px}
.suoni h1 em{font-style:normal;color:var(--arancio)}
.suoni .lead{color:#e3d2b0;max-width:60ch;margin-top:18px}
.dischi{list-style:none;display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:16px;margin-top:36px}
.disco{display:grid;grid-template-columns:76px 1fr;gap:10px 14px;align-items:center;padding:14px;
  border:1px solid var(--filo-chiaro);background:rgba(244,233,210,.045);transition:border-color .2s,background .2s}
.disco:hover,.disco:has(.suona){border-color:var(--arancio);background:rgba(244,233,210,.08)}
.disco-foto{display:block;width:76px;height:76px;background:var(--crema);overflow:hidden}
.disco-foto img{width:100%;height:100%;object-fit:cover;mix-blend-mode:multiply}
.disco-nome{font-family:var(--display);font-weight:600;font-size:20px;text-transform:uppercase;
  text-decoration:none;line-height:1.1;display:block}
.disco-nome:hover{color:var(--arancio)}
.disco-meta{font-family:var(--mono);font-size:11.5px;letter-spacing:.1em;color:#cdb894;text-transform:uppercase}
.disco .lettore{grid-column:1/-1;margin:0;padding:0;background:none;border:none;gap:4px 12px}
.lettore.mini{border-left:none}
.lettore.mini .play{width:44px;height:44px}
.lettore.mini .play svg{width:18px;height:18px}
.lettore.mini .barra{height:24px}
.disco-credito{grid-column:1/-1;font-family:var(--mono);font-size:11px;color:#b9a382;line-height:1.45}
.disco-credito a{color:#ecdab4}

/* home: archivio */
.archivio{padding-top:46px;padding-bottom:76px}
.testa-sezione{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:8px 20px;
  border-bottom:2px solid var(--bruno);padding-bottom:14px}
.testa-sezione>div{min-width:0}
.testa-sezione h2{font-family:var(--display);font-weight:700;font-size:clamp(36px,5.4vw,66px);
  text-transform:uppercase;line-height:.95;margin-top:8px;overflow-wrap:anywhere}
.conta{font-family:var(--mono);font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:var(--bruno2)}
.strumenti{display:grid;gap:18px 40px;padding-top:20px}
.cerca{width:100%;font-family:var(--mono);font-size:16px;padding:13px 14px 13px 44px;border:2px solid var(--bruno);
  color:var(--bruno);border-radius:0;-webkit-appearance:none;appearance:none;
  background:var(--carta) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2338291d' stroke-width='2.4'%3E%3Ccircle cx='10.5' cy='10.5' r='6.5'/%3E%3Cpath d='M15.5 15.5 21 21'/%3E%3C/svg%3E") 14px center/20px no-repeat}
.cerca::placeholder{color:var(--bruno3)}
.cerca:focus{outline:none;box-shadow:5px 5px 0 var(--arancio)}
.etichetta{display:block;font-family:var(--mono);font-size:11px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;
  color:var(--ruggine);margin-bottom:8px}
/* la linea del tempo: una colonna per epoca, alta quanto le schede che ha */
.epoche{display:flex;align-items:flex-end;gap:6px}
.epoca{flex:1;min-width:0;display:flex;flex-direction:column;gap:5px;background:none;border:none;cursor:pointer;
  font-family:var(--mono);font-size:10.5px;letter-spacing:.02em;color:var(--bruno2);text-align:center;padding:0;white-space:nowrap}
.epoca i{display:block;height:calc(8px + var(--h)*46px);background:var(--sabbia);border:2px solid var(--bruno);transition:background .15s}
.epoca:hover i{background:var(--arancio)}
.epoca[aria-pressed="true"]{color:var(--bruno);font-weight:600}
.epoca[aria-pressed="true"] i{background:var(--bruno)}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{flex:none;font-family:var(--display);font-weight:500;font-size:14px;letter-spacing:.08em;text-transform:uppercase;
  border:2px solid var(--bruno);background:transparent;color:var(--bruno);padding:6px 12px;cursor:pointer;border-radius:0;
  transition:background .15s,color .15s}
.chip span{font-family:var(--mono);font-size:11px;margin-left:6px;opacity:.7}
.chip:hover{background:var(--sabbia)}
.chip[aria-pressed="true"]{background:var(--bruno);color:var(--crema)}
.riga-chips{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px 24px}
.ordina{display:flex;align-items:center;gap:0;font-family:var(--mono);font-size:11.5px;letter-spacing:.1em;text-transform:uppercase}
.ordina span{color:var(--bruno2);margin-right:10px}
.ordina button{background:none;border:2px solid var(--bruno);padding:6px 10px;cursor:pointer;font-family:var(--mono);
  font-size:11.5px;letter-spacing:.1em;text-transform:uppercase}
.ordina button+button{border-left:none}
.ordina button[aria-pressed="true"]{background:var(--bruno);color:var(--crema)}
@media(max-width:699px){.chips{flex-wrap:nowrap;overflow-x:auto;margin:0 -18px;padding:0 18px 6px;scrollbar-width:none;max-width:100vw}
  .riga-chips{display:grid}}
@media(min-width:900px){.strumenti{grid-template-columns:minmax(280px,400px) minmax(0,1fr);align-items:end}.riga-chips{grid-column:1/-1}}
.griglia{display:grid;grid-template-columns:repeat(auto-fill,minmax(262px,1fr));gap:38px 26px;margin-top:30px}
.card{display:flex;flex-direction:column;text-decoration:none}
.card-foto{display:block;position:relative;aspect-ratio:4/3;background:var(--carta);border:2px solid var(--bruno);overflow:hidden;
  transition:transform .2s ease,box-shadow .2s ease}
.card-foto img{width:100%;height:100%;object-fit:cover;mix-blend-mode:multiply;transition:transform .6s ease}
img.intera{object-fit:contain!important;padding:8px}
.card:hover .card-foto{transform:translate(-3px,-3px);box-shadow:7px 7px 0 var(--arancio)}
.card:hover .card-foto img{transform:scale(1.05)}
.nota{position:absolute;right:8px;bottom:8px;z-index:1;width:30px;height:30px;border-radius:50%;background:var(--bruno);color:var(--crema);
  display:grid;place-items:center;font-size:15px;line-height:1}
.card-testo{display:flex;flex-direction:column;gap:5px;padding:12px 2px 0}
.card-meta{display:flex;flex-wrap:wrap;gap:2px 10px;font-family:var(--mono);font-size:11.5px;
  letter-spacing:.1em;font-weight:600;color:var(--ruggine);text-transform:uppercase}
.card-meta span+span::before{content:"·";margin-right:10px;color:var(--bruno3)}
.card-nome{font-family:var(--display);font-weight:700;font-size:26px;line-height:1.04;text-transform:uppercase;
  text-decoration:underline;text-decoration-color:transparent;text-decoration-thickness:3px;text-underline-offset:5px;transition:text-decoration-color .2s}
.card:hover .card-nome{text-decoration-color:var(--arancio)}
.card-gancio{font-size:15.5px;line-height:1.42;color:var(--bruno2);display:-webkit-box;-webkit-box-orient:vertical;
  -webkit-line-clamp:3;line-clamp:3;overflow:hidden}
.nessuna{padding:40px 0;font-size:18px;color:var(--bruno2)}
/* sul telefono due colonne, come le pagine di un catalogo: la foto e il
   nome bastano a riconoscere la macchina, il gancio sta nella sua pagina */
@media(max-width:559px){
  .griglia{grid-template-columns:repeat(2,minmax(0,1fr));gap:22px 12px}
  .card:hover .card-foto{transform:none;box-shadow:none}
  .card-testo{padding-top:8px;gap:3px}
  .card-meta{font-size:10px;letter-spacing:.06em;gap:2px 6px}
  .card-meta span+span::before{margin-right:6px}
  .card-meta .fam{display:none}
  .card-nome{font-size:18px;line-height:1.08}
  .card-gancio{display:none}
  .nota{width:26px;height:26px;font-size:13px;right:6px;bottom:6px}
}

/* pagina della scheda */
.briciole{font-family:var(--mono);font-size:12.5px;letter-spacing:.06em;padding-top:18px;color:var(--bruno2)}
.briciole ol{list-style:none;display:flex;flex-wrap:wrap;gap:6px}
.briciole li+li::before{content:"/";margin-right:6px;color:var(--bruno3)}
.briciole a{color:var(--ruggine)}
.sc-apertura{display:grid;gap:24px;padding-top:20px;padding-bottom:36px}
.sc-foto{position:relative}
.sc-foto .quadro{background:var(--carta);border:2px solid var(--bruno);box-shadow:10px 10px 0 var(--sabbia)}
.sc-foto img{width:100%;height:auto;max-height:min(70vh,640px);object-fit:contain;mix-blend-mode:multiply;margin:0 auto}
.sc-foto figcaption{font-family:var(--mono);font-size:11.5px;color:var(--bruno3);margin-top:18px;letter-spacing:.04em}
.sc-testo{min-width:0}
.sc-testo h1{font-family:var(--display);font-weight:700;font-size:clamp(48px,8.6vw,108px);line-height:.9;
  text-transform:uppercase;letter-spacing:-.012em;margin-top:12px;overflow-wrap:break-word}
.sc-testo .gancio{padding-left:16px;border-left:6px solid var(--arancio)}
@media(min-width:900px){
  .sc-apertura{grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:60px;align-items:center;padding-top:34px;padding-bottom:56px}
  .sc-foto{order:2}
}
.specifiche{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));background:var(--bruno);color:var(--crema)}
.specifiche div{padding:15px 16px;border-bottom:1px solid var(--filo-chiaro);border-right:1px solid var(--filo-chiaro)}
.specifiche dt{font-family:var(--mono);font-size:11px;letter-spacing:.16em;text-transform:uppercase;font-weight:600;color:var(--arancio)}
.specifiche dd{font-family:var(--display);font-weight:700;font-size:22px;text-transform:uppercase;line-height:1.12;margin-top:5px;
  overflow-wrap:anywhere}
@media(min-width:700px){
  .specifiche{grid-template-columns:repeat(auto-fit,minmax(160px,1fr))}
  .specifiche div{border-bottom:none;padding:20px 22px}
  .specifiche div:last-child{border-right:none}
}
/* il racconto a sinistra, il reel a destra che resta fermo mentre si legge */
.sc-corpo{display:grid;gap:0 64px;padding-top:14px}
.corpo{max-width:800px;min-width:0;padding-bottom:12px}
@media(min-width:1040px){.sc-corpo.col-reel{grid-template-columns:minmax(0,1fr) 320px;align-items:start}
  .sc-corpo .lato{position:sticky;top:98px;padding:34px 0 40px}}
.lato{padding:34px 0;border-top:2px solid var(--bruno)}
@media(min-width:1040px){.lato{border-top:none}}
.lato h2{font-family:var(--display);font-weight:700;font-size:30px;text-transform:uppercase;line-height:1;margin-top:8px}
.lato video{width:100%;max-width:320px;height:auto;aspect-ratio:9/16;background:var(--bruno);border:2px solid var(--bruno);
  margin-top:16px;box-shadow:8px 8px 0 var(--arancio)}
.lato p.nota-reel{font-size:15px;line-height:1.5;color:var(--bruno2);margin-top:20px;max-width:34ch}
.lato p.nota-reel a{color:var(--ruggine)}
.sezione{display:grid;grid-template-columns:64px 1fr;gap:4px 18px;padding:36px 0;border-top:2px solid var(--bruno)}
.sezione:first-child{border-top:none}
.sezione .num{font-family:var(--display);font-weight:700;font-size:54px;line-height:.86;color:var(--arancio)}
.sezione h2{font-family:var(--display);font-weight:700;font-size:clamp(28px,3.4vw,38px);text-transform:uppercase;line-height:1.04}
.sezione h2 .kicker{display:block;margin-bottom:6px}
.sezione .testo{grid-column:2}
.sezione p{margin-top:14px;max-width:64ch}
.sezione:first-child .testo>p:first-child::first-letter{font-family:var(--display);font-weight:700;font-size:3.5em;line-height:.8;
  float:left;margin:.06em .1em 0 0;color:var(--arancio)}
@media(max-width:599px){.sezione{grid-template-columns:1fr}.sezione .num{font-size:40px}.sezione .testo{grid-column:1}}
.artisti{list-style:none;margin-top:10px}
.artisti li{padding:13px 0;border-bottom:1px solid var(--filo)}
.artisti li:last-child{border-bottom:none}
.artisti b{display:block;font-family:var(--display);font-weight:600;font-size:21px;letter-spacing:.02em;text-transform:uppercase;line-height:1.15}
.riquadro{border:2px solid var(--bruno);background:var(--carta);padding:20px 22px;margin-top:22px;box-shadow:6px 6px 0 var(--sabbia)}
.riquadro .brano{font-family:var(--display);font-weight:600;font-size:23px;line-height:1.2;margin-top:8px}
.riquadro p{margin-top:8px}
/* l'avvertenza è un'etichetta da manuale: la banda a righe in testa */
.avvertenza{display:grid;grid-template-columns:56px 1fr;gap:16px;align-items:start;background:var(--sabbia);
  border:2px solid var(--bruno);padding:30px 22px 20px;margin-top:24px;position:relative}
.avvertenza::before{content:"";position:absolute;left:0;right:0;top:0;height:12px;border-bottom:2px solid var(--bruno);
  background:repeating-linear-gradient(-45deg,var(--bruno) 0 10px,var(--arancio) 10px 20px)}
.avvertenza svg{width:56px;height:56px}
.avvertenza p{font-family:var(--display);font-weight:500;font-size:21px;line-height:1.3;margin-top:6px}
.blocco{padding:44px 0;border-top:2px solid var(--bruno)}
.blocco h2{font-family:var(--display);font-weight:700;font-size:clamp(32px,4.2vw,48px);text-transform:uppercase;line-height:1;margin-top:8px}
.tavole{display:grid;grid-auto-flow:column;grid-auto-columns:min(72%,290px);gap:14px;overflow-x:auto;
  scroll-snap-type:x mandatory;margin-top:24px;padding-bottom:12px}
.tavole a{scroll-snap-align:start;display:block;border:2px solid var(--bruno);overflow:hidden;transition:transform .2s,box-shadow .2s;cursor:zoom-in}
.tavole a:hover{transform:translate(-3px,-3px);box-shadow:6px 6px 0 var(--arancio)}
.tavole img{width:100%;height:auto;aspect-ratio:4/5;object-fit:cover}
@media(min-width:980px){.tavole{grid-auto-flow:row;grid-template-columns:repeat(6,1fr);gap:16px;overflow:visible;padding-bottom:0}}
/* la lente: una tavola in grande, con le frecce */
.lente{position:fixed;inset:0;z-index:60;background:rgba(30,21,14,.95);display:grid;place-items:center;padding:14px}
.lente img{max-width:min(94vw,760px);max-height:90vh;width:auto;height:auto;box-shadow:0 20px 70px rgba(0,0,0,.6)}
.lente button{position:absolute;width:52px;height:52px;border-radius:50%;border:2px solid var(--crema);background:rgba(42,30,21,.7);
  color:var(--crema);font-family:var(--display);font-size:24px;line-height:1;cursor:pointer;display:grid;place-items:center}
.lente button:hover{background:var(--arancio);border-color:var(--arancio);color:var(--bruno)}
.lente .chiudi{top:14px;right:14px}
.lente .prima{left:14px;top:50%;transform:translateY(-50%)}
.lente .dopo{right:14px;top:50%;transform:translateY(-50%)}
.lente .conto{position:absolute;bottom:14px;left:50%;transform:translateX(-50%);font-family:var(--mono);font-size:12px;
  letter-spacing:.16em;color:var(--crema)}
.fonti{font-family:var(--mono);font-size:13.5px;line-height:1.7;color:var(--bruno2)}
.fonti h2{color:var(--bruno)}
.fonti ol{padding-left:22px;margin-top:16px;max-width:900px}
.fonti li{margin-bottom:8px}
.fonti li::marker{color:var(--ruggine);font-weight:600}
.fonti a{color:var(--ruggine);overflow-wrap:anywhere}
.fonti .data{color:var(--bruno3)}
.crediti{margin-top:20px}
.crediti p{margin-top:6px}
.vicine{display:grid;grid-template-columns:minmax(0,1fr);gap:14px;padding:40px 0;border-top:2px solid var(--bruno)}
@media(min-width:700px){.vicine{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
.vicina>span:last-child{min-width:0}
.vicina .nobr{white-space:normal}
.vicina{display:flex;gap:16px;align-items:center;border:2px solid var(--bruno);background:var(--carta);padding:12px;
  text-decoration:none;transition:box-shadow .15s,transform .15s}
.vicina:hover{transform:translate(-3px,-3px);box-shadow:7px 7px 0 var(--arancio)}
.vicina .ft{width:104px;height:104px;flex:none;background:var(--crema);overflow:hidden}
.vicina .ft img{width:100%;height:100%;object-fit:cover;mix-blend-mode:multiply}
.vicina .dir{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--ruggine);font-weight:600}
.vicina b{display:block;font-family:var(--display);font-weight:700;font-size:24px;text-transform:uppercase;line-height:1.08;margin-top:4px;
  overflow-wrap:anywhere}
.vicina.dopo{flex-direction:row-reverse;text-align:right}
.vicina.vuota{display:none}
@media(min-width:700px){.vicina.vuota{display:block;visibility:hidden}}
.famiglia{padding-bottom:64px}

/* invito e piede */
.invito{background:var(--arancio);color:var(--bruno);border-top:2px solid var(--bruno)}
.invito .contenitore{display:flex;flex-wrap:wrap;align-items:center;gap:18px 30px;padding-top:34px;padding-bottom:34px}
.invito .bollo{flex:none;width:104px;height:104px;border-radius:50%;border:4px solid var(--bruno);overflow:hidden;background:var(--crema);
  box-shadow:5px 5px 0 var(--bruno)}
.invito .bollo img{width:100%;height:100%;object-fit:cover;object-position:50% 30%;transform:scale(1.25)}
.invito .kicker{color:var(--bruno)}
.invito-testo{font-family:var(--display);font-weight:700;font-size:clamp(26px,3.6vw,42px);text-transform:uppercase;line-height:1.05;max-width:24ch;margin-top:6px}
.invito .dove{flex:1;min-width:240px}
@media(min-width:700px){.invito .bollo{width:150px;height:150px}.invito .contenitore{padding-top:42px;padding-bottom:42px}}
.piede{background:var(--bruno);color:var(--crema)}
.piede .firma{font-family:var(--display);font-weight:700;font-size:clamp(30px,6.2vw,84px);letter-spacing:-.005em;text-transform:uppercase;
  line-height:.95;padding-top:48px;max-width:16ch}
.piede .firma em{font-style:normal;color:var(--arancio)}
.piede .righe{display:flex;flex-wrap:wrap;gap:8px 22px;font-family:var(--mono);font-size:12.5px;color:#d6c29c;padding:26px 0 40px;
  margin-top:34px;border-top:1px solid var(--filo-chiaro)}
.piede a{color:var(--crema)}
.errore{padding-top:70px;padding-bottom:90px}
.errore h1{font-family:var(--display);font-weight:700;font-size:clamp(44px,8vw,96px);text-transform:uppercase;line-height:.92;margin-top:12px}
.errore p{margin-top:16px;max-width:50ch}
""".replace("__ONDA__", _onda_css())
VERSIONE_CSS = hashlib.sha1(STILE.encode()).hexdigest()[:8]

AUTOMA = """<svg viewBox="0 0 200 200" fill="none" stroke="#38291d" aria-hidden="true">
<line x1="100" y1="40" x2="100" y2="22" stroke-width="8"/><circle cx="100" cy="16" r="7" fill="#38291d" stroke="none"/>
<rect x="52" y="44" width="96" height="90" rx="14" stroke-width="9"/>
<rect x="34" y="74" width="14" height="26" rx="4" fill="#38291d" stroke="none"/>
<rect x="152" y="74" width="14" height="26" rx="4" fill="#38291d" stroke="none"/>
<circle cx="80" cy="80" r="14" stroke-width="7" stroke="#f4e9d2"/><circle cx="120" cy="80" r="14" stroke-width="7" stroke="#f4e9d2"/>
<circle cx="80" cy="80" r="4" fill="#f4e9d2" stroke="none"/><circle cx="120" cy="80" r="4" fill="#f4e9d2" stroke="none"/>
<line x1="79" y1="106" x2="79" y2="120" stroke-width="6" stroke-linecap="round"/><line x1="93" y1="106" x2="93" y2="120" stroke-width="6" stroke-linecap="round"/>
<line x1="107" y1="106" x2="107" y2="120" stroke-width="6" stroke-linecap="round"/><line x1="121" y1="106" x2="121" y2="120" stroke-width="6" stroke-linecap="round"/>
</svg>"""

ICONA_PLAY = '<svg class="i-play" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4.5v15l13-7.5z"/></svg>'
ICONA_PAUSA = '<svg class="i-pausa" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 4h4.5v16H6zM13.5 4H18v16h-4.5z"/></svg>'

# Il lettore funziona anche senza JavaScript: c'è l'<audio controls> del
# browser. Lo script lo nasconde e accende il bottone; uno solo suona alla
# volta, perché due macchine insieme non sono un ascolto ma un pasticcio.
JS_LETTORE = """<script>(function(){
var tutti=[].slice.call(document.querySelectorAll('.lettore'));
function mmss(s){s=Math.max(0,Math.floor(s||0));return Math.floor(s/60)+':'+(s%60<10?'0':'')+(s%60)}
tutti.forEach(function(l){
var a=l.querySelector('audio'),b=l.querySelector('.play'),i=l.querySelector('.barra i'),barra=l.querySelector('.barra'),ora=l.querySelector('.ora');
a.removeAttribute('controls');l.classList.add('js');
b.addEventListener('click',function(){if(a.paused){tutti.forEach(function(x){if(x!==l){x.querySelector('audio').pause()}});a.play()}else{a.pause()}});
a.addEventListener('play',function(){l.classList.add('suona');b.setAttribute('aria-pressed','true')});
a.addEventListener('pause',function(){l.classList.remove('suona');b.setAttribute('aria-pressed','false')});
a.addEventListener('timeupdate',function(){var d=a.duration||+l.getAttribute('data-secondi');i.style.width=(100*a.currentTime/d)+'%';ora.textContent=mmss(a.currentTime)});
a.addEventListener('ended',function(){a.currentTime=0;i.style.width='0'});
barra.addEventListener('click',function(ev){if(!a.duration)return;var r=barra.getBoundingClientRect();a.currentTime=Math.max(0,Math.min(1,(ev.clientX-r.left)/r.width))*a.duration});
});
})();</script>"""

# Ricerca e filtri: senza JavaScript la griglia si vede tutta e i comandi
# restano nascosti, così nessuno vede un bottone che non fa niente.
# Tre filtri che si sommano (famiglia, epoca, testo) e due ordini: quello
# d'uscita e quello dell'anno della macchina.
JS_ARCHIVIO = """<script>(function(){
var q=document.getElementById('cerca'),chips=[].slice.call(document.querySelectorAll('.chip')),
ep=[].slice.call(document.querySelectorAll('.epoca')),ord=[].slice.call(document.querySelectorAll('.ordina button')),
g=document.getElementById('griglia'),cards=[].slice.call(g.querySelectorAll('.card')),conta=document.getElementById('conta'),
vuoto=document.getElementById('nessuna'),filtro='tutte',epoca='';
document.getElementById('strumenti').hidden=false;
function norm(t){return t.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'')}
function aggiorna(){var t=norm(q.value.trim()),n=0;
cards.forEach(function(c){var ok=(filtro==='tutte'||(filtro==='suono'?c.getAttribute('data-suono')==='1':c.getAttribute('data-serie')===filtro))&&(!epoca||c.getAttribute('data-epoca')===epoca)&&(!t||c.getAttribute('data-testo').indexOf(t)>=0);c.hidden=!ok;if(ok)n++});
conta.textContent=n===1?'1 scheda':n+' schede';vuoto.hidden=n>0}
chips.forEach(function(b){b.addEventListener('click',function(){chips.forEach(function(x){x.setAttribute('aria-pressed','false')});b.setAttribute('aria-pressed','true');filtro=b.getAttribute('data-filtro');aggiorna()})});
ep.forEach(function(b){b.addEventListener('click',function(){var su=b.getAttribute('aria-pressed')==='true';ep.forEach(function(x){x.setAttribute('aria-pressed','false')});if(su){epoca=''}else{b.setAttribute('aria-pressed','true');epoca=b.getAttribute('data-epoca')}aggiorna()})});
ord.forEach(function(b){b.addEventListener('click',function(){ord.forEach(function(x){x.setAttribute('aria-pressed','false')});b.setAttribute('aria-pressed','true');var k=b.getAttribute('data-ordine');
cards.slice().sort(function(a,c){var n=a.getAttribute('data-n')-c.getAttribute('data-n');return k==='anno'?((a.getAttribute('data-anno')-c.getAttribute('data-anno'))||n):n}).forEach(function(c){g.appendChild(c)})})});
q.addEventListener('input',aggiorna);
var f=(location.search.match(/[?&]famiglia=([a-z0-9-]+)/)||[])[1];
chips.forEach(function(b){if(f&&b.getAttribute('data-filtro')===f){b.click()}});
})();</script>"""

# Su tutte le pagine: le sezioni con la classe .rivela entrano quando
# arrivano sullo schermo. La classe .js sull'<html> la mette uno script in
# testa alla pagina: senza JavaScript non si nasconde niente.
JS_COMUNE = """<script>(function(){
var el=[].slice.call(document.querySelectorAll('.rivela'));
if(!('IntersectionObserver' in window)){el.forEach(function(x){x.classList.add('vista')});return}
var o=new IntersectionObserver(function(v){v.forEach(function(t){if(t.isIntersecting){t.target.classList.add('vista');o.unobserve(t.target)}})},{rootMargin:'0px 0px -6% 0px'});
el.forEach(function(x){o.observe(x)});
})();</script>"""

# La lente: una tavola in grande sopra la pagina, con le frecce (anche da
# tastiera) e Esc per chiudere. Senza JavaScript il link apre il JPEG.
JS_LENTE = """<script>(function(){
var a=[].slice.call(document.querySelectorAll('.tavole a'));if(!a.length)return;var l=null,k=0;
function mostra(){var im=l.querySelector('img');im.src=a[k].getAttribute('href');im.alt=a[k].querySelector('img').alt;l.querySelector('.conto').textContent=(k+1)+' / '+a.length}
function tasto(ev){if(ev.key==='Escape')chiudi();if(ev.key==='ArrowRight')vai(1);if(ev.key==='ArrowLeft')vai(-1)}
function chiudi(){if(l){document.body.removeChild(l);l=null;document.removeEventListener('keydown',tasto);a[k].focus()}}
function vai(d){k=(k+d+a.length)%a.length;mostra()}
a.forEach(function(x,i){x.addEventListener('click',function(ev){ev.preventDefault();k=i;
l=document.createElement('div');l.className='lente';l.setAttribute('role','dialog');l.setAttribute('aria-modal','true');l.setAttribute('aria-label','Le tavole in grande');
l.innerHTML='<img alt=""><button class="chiudi" type="button" aria-label="Chiudi">\\u00d7</button><button class="prima" type="button" aria-label="Tavola precedente">\\u2190</button><button class="dopo" type="button" aria-label="Tavola successiva">\\u2192</button><span class="conto"></span>';
l.addEventListener('click',function(e2){if(e2.target===l)chiudi()});
l.querySelector('.chiudi').addEventListener('click',chiudi);
l.querySelector('.prima').addEventListener('click',function(){vai(-1)});
l.querySelector('.dopo').addEventListener('click',function(){vai(1)});
document.body.appendChild(l);document.addEventListener('keydown',tasto);mostra();l.querySelector('.chiudi').focus()})});
})();</script>"""


# ------------------------------------------------------------- utilità ---

def _senza_accenti(t):
    return "".join(ch for ch in unicodedata.normalize("NFD", t)
                   if unicodedata.category(ch) != "Mn").lower()


def _anno(s):
    m = re.search(r"\d{4}", str(s["anno"]))
    return int(m.group(0)) if m else None


def _epoca(s):
    """La colonna della linea del tempo: «pre» fino al 1949, poi il decennio."""
    a = _anno(s)
    if not a:
        return ""
    return "pre" if a < 1950 else str(a // 10 * 10)


def _epoca_nome(k):
    if k == "pre":
        return "&lt;1950", "Prima del 1950"
    d = int(k)
    return (f"'{d % 100:02d}" if d < 2000 else str(d)), f"Anni {d}"


def _serie_nome(serie):
    """«I SINTETIZZATORI» → «I sintetizzatori»."""
    return serie[:1] + serie[1:].lower()


def _serie_breve(serie):
    """«I SINTETIZZATORI» → «Sintetizzatori», per il piede delle schede."""
    t = re.sub(r"^(I|IL|LO|LA|LE|GLI|L')\s*", "", serie.strip())
    return t[:1] + t[1:].lower()


def _serie_id(serie):
    return re.sub(r"[^a-z0-9]+", "-", _senza_accenti(serie)).strip("-")


def _mmss(secondi):
    s = int(round(secondi))
    return f"{s // 60}:{s % 60:02d}"


def _nome(t):
    """Il nome della macchina, escapato, con le parole col trattino che non
    si spezzano: a 96 px «ROLAND TR-808» andava a capo come «TR-» e «808»."""
    return re.sub(r"(\S+-\S+)", r'<span class="nobr">\1</span>', e(t))


def _maiuscola(t):
    return t[:1].upper() + t[1:]


def _ld(dati):
    # «</» dentro un <script> chiuderebbe il tag: un titolo con «</» (o un
    # URL strano in una fonte) basterebbe a rompere la pagina.
    return ('<script type="application/ld+json">'
            + json.dumps(dati, ensure_ascii=False).replace("</", "<\\/")
            + "</script>")


def _impronta(path, *extra):
    h = hashlib.sha1(pathlib.Path(path).read_bytes()).hexdigest()[:16]
    return "-".join([h, *map(str, extra), VERSIONE_MEDIA])


# ------------------------------------------------- foto, suoni, copertine ---

def _foto_web(s, indice):
    """Le foto della macchina in due larghezze per il web.

    Gli originali su Commons pesano fino a 5,7 MB: sull'elenco ne
    servirebbero 54. Pillow, e non ffmpeg, perché ffmpeg ignora il tag
    EXIF di rotazione (lezione del reel, 07/10/2026) mentre il browser
    lo rispetta: la stessa foto uscirebbe dritta in un posto e coricata in
    un altro. exif_transpose la raddrizza prima di togliere l'EXIF.
    Se Pillow manca la scheda ripiega sulla copertina del carosello, e lo
    dice: un ripiego che non si vede non lo controlla nessuno."""
    src = RADICE / s["foto"]["file"]
    if not src.exists():
        print(f"[archivio] AVVISO: foto assente {s['foto']['file']}, uso la copertina")
        return None
    firma = _impronta(src, *LARGHEZZE_FOTO)
    nomi = {str(w): f"foto/{s['slug']}-{w}.jpg" for w in LARGHEZZE_FOTO}
    rec = indice.get(s["slug"])
    if rec and rec.get("firma") == firma and all((DOCS / n).exists() for n in nomi.values()):
        return rec
    try:
        from PIL import Image, ImageOps
    except ImportError:
        print(f"[archivio] AVVISO: manca Pillow, {s['slug']} usa la copertina del carosello")
        return None
    (DOCS / "foto").mkdir(exist_ok=True)
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)
        if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
            # Le macchine scontornate (PNG trasparenti): fondo BIANCO, che
            # col multiply diventa crema. Un convert() secco darebbe il nero.
            im = im.convert("RGBA")
            fondo = Image.new("RGB", im.size, (255, 255, 255))
            fondo.paste(im, mask=im.split()[3])
            im = fondo
        else:
            im = im.convert("RGB")
        dims = {}
        for w in LARGHEZZE_FOTO:
            c = im.copy()
            c.thumbnail((w, w * 3), Image.LANCZOS)
            c.save(DOCS / nomi[str(w)], "JPEG", quality=80, optimize=True, progressive=True)
            dims[str(w)] = list(c.size)
    rec = {"firma": firma, **nomi, "dimensioni": dims}
    indice[s["slug"]] = rec
    print(f"[archivio] foto per il web: {s['slug']}")
    return rec


def _ffmpeg():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None


def _durata(ff, path):
    r = subprocess.run([ff, "-hide_banner", "-i", str(path)], capture_output=True, text=True)
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr)
    if not m:
        raise RuntimeError(f"durata illeggibile: {path}")
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def _suono_web(s, indice, ff):
    """L'estratto della registrazione vera (`reel_audio`) per il sito.

    Parte da `inizio`, cioè dal punto già scelto e riascoltato per il reel
    (sul Juno-106 prima di lì il file satura), e dura al massimo
    SECONDI_SUONO. Volume: loudnorm a -16 LUFS come nei reel, così passando
    da una macchina all'altra non si salta sulla sedia."""
    a = s.get("reel_audio")
    if not a:
        return None
    src = RADICE / a["file"]
    if not src.exists():
        print(f"[archivio] AVVISO: registrazione assente {a['file']}: {s['slug']} senza suono")
        return None
    inizio = a.get("inizio", 0)
    firma = _impronta(src, inizio, SECONDI_SUONO)
    nome = f"suoni/{s['slug']}.mp3"
    rec = indice.get(s["slug"])
    if rec and rec.get("firma") == firma and (DOCS / nome).exists():
        return rec
    if not ff:
        print(f"[archivio] AVVISO: manca ffmpeg, {s['slug']} esce senza il suono vero")
        return None
    (DOCS / "suoni").mkdir(exist_ok=True)
    durata = min(SECONDI_SUONO, _durata(ff, src) - inizio)
    coda = min(1.5, durata / 4)
    r = subprocess.run(
        [ff, "-y", "-loglevel", "error", "-ss", str(inizio), "-i", str(src), "-t", f"{durata:.2f}",
         "-af", f"afade=t=in:d=0.02,afade=t=out:st={durata - coda:.2f}:d={coda:.2f},"
                "loudnorm=I=-16:TP=-1.5:LRA=11",
         "-ar", "44100", "-ac", "2", "-map_metadata", "-1",
         "-c:a", "libmp3lame", "-b:a", "128k", str(DOCS / nome)],
        capture_output=True, text=True)
    if r.returncode != 0:
        print(f"[archivio] AVVISO: estratto audio fallito per {s['slug']}: {r.stderr[-300:]}")
        return None
    rec = {"firma": firma, "file": nome, "secondi": round(durata, 1)}
    indice[s["slug"]] = rec
    print(f"[archivio] suono vero per il web: {s['slug']} ({durata:.1f} s)")
    return rec


def _copertina_reel(s, indice, ff):
    """La copertina del video sulla pagina: il primo fotogramma del reel,
    che è fatto apposta per agganciare (foto + prima battuta).
    NON story.jpg: ha in fondo «tocca il nome in alto», che sul sito non
    vuol dire niente."""
    video = DOCS / "tavole" / s["slug"] / "reel2.mp4"
    if not video.exists():
        return None
    firma = _impronta(video)
    nome = f"tavole/{s['slug']}/reel2.jpg"
    rec = indice.get(s["slug"])
    if rec and rec.get("firma") == firma and (DOCS / nome).exists():
        return rec
    if not ff:
        print(f"[archivio] AVVISO: manca ffmpeg, il reel di {s['slug']} resta senza copertina")
        return {"firma": None, "file": None}
    r = subprocess.run([ff, "-y", "-loglevel", "error", "-ss", "0.4", "-i", str(video),
                        "-frames:v", "1", "-q:v", "4", str(DOCS / nome)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(f"[archivio] AVVISO: copertina del reel fallita per {s['slug']}")
        return {"firma": None, "file": None}
    rec = {"firma": firma, "file": nome}
    indice[s["slug"]] = rec
    return rec


# ------------------------------------------------------------ mattoni ---

def _img(s, foto, prefisso, sizes, *, lazy=True, priorita=False, box=None, passaggio=False):
    """`box` è il rapporto del riquadro (4/3 per le schede dell'elenco):
    se riempirlo taglierebbe più del 20% della foto, la foto entra intera
    e avanza un bordo di crema. Stessa regola della copertina delle
    tavole: meglio il bordo che una macchina senza tastiera (l'Eventide
    H910 è largo 4,8 volte l'altezza: col ritaglio si vedeva un display)."""
    alt = f"{s['strumento']} ({s['anno']})"
    pos = e(s["foto"].get("posizione") or "center")
    intera = s["foto"].get("ritaglio")
    if foto and box and not intera:
        w, h = foto["dimensioni"]["640"]
        intera = 1 - (box * h / w if w / h > box else (w / h) / box) > 0.20
    classe = ' class="intera"' if intera else ""
    carica = ' loading="lazy" decoding="async"' if lazy else (' fetchpriority="high"' if priorita else "")
    # `passaggio`: la stessa foto ha lo stesso nome nella griglia e in testa
    # alla scheda, e il browser che sa farlo (`@view-transition`) la porta
    # da un posto all'altro. Il nome deve essere UNICO nella pagina, o il
    # passaggio salta tutto: per questo lo hanno solo le carte della
    # griglia e la foto d'apertura, non la vetrina né le «vicine».
    if passaggio:
        pos += ";view-transition-name:f-" + re.sub(r"[^a-z0-9-]", "-", s["slug"].lower())
    if foto:
        w, h = foto["dimensioni"]["640"]
        srcset = ", ".join(f'{prefisso}{foto[str(x)]} {x}w' for x in LARGHEZZE_FOTO)
        return (f'<img src="{prefisso}{foto["640"]}" srcset="{srcset}" sizes="{sizes}" '
                f'width="{w}" height="{h}" alt="{e(alt)}" style="object-position:{pos}"{classe}{carica}>')
    return (f'<img src="{prefisso}tavole/{s["slug"]}/01.jpg" width="1080" height="1350" '
            f'alt="{e(alt)}"{carica}>')


def _testata(prefisso):
    casa = prefisso or "./"
    return f"""<header class="testata"><div class="contenitore">
<a class="marchio" href="{casa}"><span class="q">{AUTOMA}</span><span><b>ELETTROFONI</b><small>Catalogo delle macchine sonore</small></span></a>
<nav aria-label="Menu"><a href="{casa}#archivio">Schede</a><a href="{casa}suoni/">Suoni</a><a class="largo" href="{INSTAGRAM}" rel="noopener">Instagram ↗</a></nav>
</div></header>"""


def _firma():
    """La firma, con «QUASI MAI.» in arancio."""
    f = e(contenuti.FIRMA)
    return re.sub(r"(QUASI MAI\.?)$", r"<em>\1</em>", f)


def _piede(prefisso):
    bollo = ""
    if (DOCS / "dinamo.jpg").exists():
        bollo = (f'<span class="bollo"><img src="{prefisso}dinamo.jpg" width="520" height="520" loading="lazy" '
                 'decoding="async" alt="Dinamo, l\'automa che compila il catalogo"></span>')
    return f"""<section class="invito"><div class="contenitore">
{bollo}<div class="dove"><p class="kicker">Compila il catalogo: Dinamo</p>
<p class="invito-testo">Una macchina nuova ogni sera alle 18, su Instagram</p></div>
<a class="bottone pieno" href="{INSTAGRAM}" rel="noopener">Segui @elettrofoni ↗</a>
</div></section>
<footer class="piede"><div class="contenitore">
<p class="firma">{_firma()}</p>
<p class="righe"><a href="{INSTAGRAM}" rel="noopener">@elettrofoni su Instagram</a><a href="{prefisso or './'}">Tutte le schede</a><a href="{prefisso}suoni/">Il suono vero</a><span>Foto e registrazioni con licenza libera: i crediti sono in ogni scheda</span><a href="{prefisso}privacy.html">Privacy</a><a href="{prefisso}cancellazione-dati.html">Cancellazione dei dati</a></p>
</div></footer>"""


def _pagina(titolo, corpo, descrizione, *, canonical, prefisso, og_image=None,
            og_tipo="website", pubblicata=None, verifica=False, ld=None, script=""):
    meta = [
        f'<meta name="description" content="{e(descrizione)}">',
        f'<link rel="canonical" href="{canonical}">',
        f'<meta property="og:title" content="{e(titolo)}">',
        f'<meta property="og:description" content="{e(descrizione)}">',
        f'<meta property="og:type" content="{og_tipo}">',
        f'<meta property="og:url" content="{canonical}">',
        '<meta property="og:site_name" content="Elettrofoni">',
        '<meta property="og:locale" content="it_IT">',
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="theme-color" content="#38291d">',
        f'<link rel="icon" type="image/png" href="{prefisso}logo.png">',
        f'<link rel="apple-touch-icon" href="{prefisso}logo.png">',
    ]
    if og_image:
        meta.append(f'<meta property="og:image" content="{og_image}">')
    if pubblicata:
        meta.append(f'<meta property="article:published_time" content="{pubblicata}">')
    if verifica and VERIFICA_GOOGLE:
        meta.append(f'<meta name="google-site-verification" content="{VERIFICA_GOOGLE}">')
    return f"""<!doctype html><html lang="it"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(titolo)}</title>
<script>document.documentElement.className='js'</script>
{"".join(meta)}
{FONT_LINK}<link rel="stylesheet" href="{prefisso}stile.css?v={VERSIONE_CSS}">{_ld(ld) if ld else ""}</head>
<body>{corpo}{script}{JS_COMUNE}</body></html>"""


def _org():
    return {
        "@type": "Organization", "@id": f"{BASE}/#org", "name": "Elettrofoni",
        "url": f"{BASE}/",
        "logo": {"@type": "ImageObject", "url": f"{BASE}/logo.png"},
        "sameAs": [INSTAGRAM],
    }


def _lettore(s, suono, prefisso, *, mini=False, etichetta=None):
    a = s["reel_audio"]
    titolo = etichetta or "Il suono vero"
    cosa = "" if mini else f'<p class="lettore-cosa">{e(_maiuscola(a["cosa"].rstrip(".")))}.</p>'
    intesta = "" if mini else (f'<p class="lettore-titolo">{e(titolo)} · {_mmss(suono["secondi"])}'
                               '<span class="onde" aria-hidden="true"><i></i><i></i><i></i></span></p>')
    return f"""<div class="lettore{' mini' if mini else ''}" data-secondi="{suono['secondi']}">
<button class="play" type="button" aria-pressed="false" aria-label="Ascolta il suono vero: {e(s['strumento'])}">{ICONA_PLAY}{ICONA_PAUSA}</button>
<div class="lettore-info">{intesta}{cosa}<div class="barra" aria-hidden="true"><i></i></div>
<p class="lettore-tempo"><span class="ora">0:00</span> / {_mmss(suono['secondi'])}</p></div>
<audio controls preload="none" src="{prefisso}{suono['file']}"></audio>
</div>"""


def _credito_suono(a, suono, breve=False):
    sito = "Freesound" if "freesound.org" in a["url"] else a["fonte"]
    if breve:
        return (f'Registrazione di <a href="{e(a["url"])}" rel="nofollow noopener">{e(a["autore"])}</a>'
                f' · {e(a["licenza"])}')
    return (f'Registrazione di {e(a["autore"])} · {e(a["licenza"])} · '
            f'<a href="{e(a["url"])}" rel="nofollow noopener">{e(sito)}</a> · '
            f'estratto di {round(suono["secondi"])} s, volume normalizzato')


def _card(s, foto, suono, prefisso, sizes, *, nuova=False, lazy=True, n=0):
    testo = " ".join([s["strumento"], s["costruttore"], str(s["anno"]), s["luogo"],
                      s["inventore_nome"], s["serie"]]
                     + [u["artista"] for u in s["chi_lusata"]])
    nota = '<span class="nota" title="C\'è il suono vero" aria-label="C\'è il suono vero">♪</span>' if suono else ""
    return f"""<a class="card" href="{prefisso}tavole/{s['slug']}/" data-serie="{_serie_id(s['serie'])}" data-suono="{1 if suono else 0}" data-epoca="{_epoca(s)}" data-anno="{_anno(s) or 0}" data-n="{n}" data-testo="{e(_senza_accenti(testo))}">
<span class="card-foto">{'<span class="bollino">Ultima uscita</span>' if nuova else ''}{_img(s, foto, prefisso, sizes, lazy=lazy, box=4 / 3, passaggio=True)}{nota}</span>
<span class="card-testo"><span class="card-meta"><span>N. {s['numero']:03d}</span><span>{e(str(s['anno']))}</span><span class="fam">{e(_serie_breve(s['serie']))}</span></span>
<span class="card-nome">{_nome(s['strumento'])}</span>
<span class="card-gancio">{e(s['gancio'])}</span></span></a>"""


# ------------------------------------------------------ pagina scheda ---

def _pagina_scheda(s, p, i, uscite, media, reel_link):
    slug = s["slug"]
    pre = "../../"
    foto = media["foto"].get(slug)
    suono = media["suoni"].get(slug)
    copertina = media["copertine"].get(slug)
    url = f"{BASE}/tavole/{slug}/"

    bottoni = []
    if p.get("permalink"):
        bottoni.append(f'<a class="bottone pieno" href="{e(p["permalink"])}" rel="noopener">Il post su Instagram ↗</a>')
    if reel_link.get(slug):
        bottoni.append(f'<a class="bottone" href="{e(reel_link[slug])}" rel="noopener">Il reel ↗</a>')
    bottoni.append('<a class="bottone" href="#tavole">Le 6 tavole ↓</a>')

    lettore = ""
    if suono:
        lettore = (_lettore(s, suono, pre)
                   + f'<p class="credito-suono">{_credito_suono(s["reel_audio"], suono)}</p>')

    specifiche = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in s["specifiche"])
    artisti = "".join(f"<li><b>{e(u['artista'])}</b>{e(u['nota'])}</li>" for u in s["chi_lusata"])

    a = s.get("da_ascoltare")
    ascolto = ""
    if a:
        ascolto = (f'<div class="riquadro"><p class="kicker">Da ascoltare</p>'
                   f'<p class="brano">{e(a["artista"])}, «{e(a["brano"])}» ({e(str(a["anno"]))})</p>'
                   f'<p>{e(a["cosa"])}</p></div>')
    # Chiusura della scheda: «AVVERTENZE» sulle schede nuove, la vecchia
    # battuta sulle prime quattro (erano gia' pubblicate quando la regola
    # e' cambiata; la pagina d'archivio deve corrispondere al post uscito).
    if s.get("avvertenza"):
        etichetta, chiusura = "Avvertenze", e(s["avvertenza"])
    else:
        etichetta, chiusura = "Dinamo dice", f"«{e(s['battuta_dinamo'])}»"

    sezioni = [
        ("La macchina", "Che cos'è", f"<p>{e(s['la_macchina'])}</p>"),
        ("Chi l'ha costruita", s["inventore_nome"], f"<p>{e(s['inventore'])}</p>"),
        ("Come funziona", "Cosa c'è dentro", f"<p>{e(s['come_funziona'])}</p>"),
        ("Chi l'ha usata", "Nei dischi", f'<ul class="artisti">{artisti}</ul>{ascolto}'),
        ("L'aneddoto", "Una storia",
         f'<p>{e(s["aneddoto"])}</p><div class="avvertenza">{AUTOMA}<div>'
         f'<p class="kicker">{etichetta}</p><p>{chiusura}</p></div></div>'),
    ]
    corpo_sezioni = "".join(
        f'<section class="sezione{" rivela" if n > 1 else ""}"><div class="num" aria-hidden="true">{n:02d}</div>'
        f'<h2><span class="kicker">{e(k)}</span>{e(t)}</h2><div class="testo">{html_testo}</div></section>'
        for n, (k, t, html_testo) in enumerate(sezioni, 1))

    # LEZIONE IMPARATA (27/08/2026): prima qui finivano solo le sei
    # immagini, e Google non legge il testo dentro un JPEG: ogni pagina
    # aveva ~126 parole indicizzabili, tutte di servizio. Il contenuto vero
    # resta nelle tavole PER IL LETTORE, ma sta anche qui in HTML.
    tavole = "".join(
        f'<a href="{n:02d}.jpg"><img src="{n:02d}.jpg" width="1080" height="1350" loading="lazy" '
        f'decoding="async" alt="{e(contenuti.alt_slide(s, n))[:300]}"></a>'
        for n in range(1, 7))

    video = ""
    if (DOCS / "tavole" / slug / "reel2.mp4").exists():
        poster = f' poster="reel2.jpg"' if copertina and copertina.get("file") else ""
        link = (f' <a href="{e(reel_link[slug])}" rel="noopener">Aprilo su Instagram ↗</a>'
                if reel_link.get(slug) else "")
        video = f"""<aside class="lato" id="reel"><p class="kicker">Il reel</p><h2>La versione corta</h2>
<video controls playsinline preload="none"{poster} width="720" height="1280"><source src="reel2.mp4" type="video/mp4"></video>
<p class="nota-reel">Le cose da sapere in fila, una schermata alla volta, col suono della macchina quando ne esiste una registrazione libera.{link}</p></aside>"""

    fonti = "".join(
        f'<li><a href="{e(f["url"])}" rel="nofollow noopener">{e(f["titolo"])}</a> '
        f'<span class="data">verificata il {e(f["data"])}</span></li>'
        for f in s["fonti"])
    crediti = [f"Foto: {e(s['foto']['autore'])} · {e(s['foto']['licenza'])} · {e(s['foto']['fonte'])}"]
    for fx in s.get("foto_extra") or []:
        crediti.append(f"Foto nelle tavole: {e(fx['autore'])} · {e(fx['licenza'])} · {e(fx['fonte'])}")
    if suono:
        crediti.append("Suono: " + _credito_suono(s["reel_audio"], suono))
    crediti_html = "".join(f"<p>{c}</p>" for c in crediti)

    # Le vicine in ordine di uscita, e la famiglia: chi arriva da Google su
    # una scheda deve trovare la strada per la seconda.
    prima = uscite[i - 1][1] if i > 0 else None
    dopo = uscite[i + 1][1] if i + 1 < len(uscite) else None

    def vicina(x, verso):
        if not x:
            return '<span class="vicina vuota"></span>'
        etich = "← La precedente" if verso == "prima" else "La successiva →"
        return (f'<a class="vicina {verso}" href="{pre}tavole/{x["slug"]}/">'
                f'<span class="ft">{_img(x, media["foto"].get(x["slug"]), pre, "104px")}</span>'
                f'<span><span class="dir">{etich}</span><b>{_nome(x["strumento"])}</b></span></a>')

    stessa = sorted((j for j, (_, x) in enumerate(uscite) if x["serie"] == s["serie"] and j != i),
                    key=lambda j: abs(j - i))[:4]
    famiglia = ""
    if stessa:
        carte = "".join(_card(uscite[j][1], media["foto"].get(uscite[j][1]["slug"]),
                              media["suoni"].get(uscite[j][1]["slug"]), pre,
                              "(min-width: 1180px) 270px, (min-width: 560px) 45vw, 50vw")
                        for j in stessa)
        famiglia = (f'<section class="famiglia rivela"><div class="testa-sezione"><div><p class="kicker">Della stessa famiglia</p>'
                    f'<h2>{e(_serie_nome(s["serie"]))}</h2></div></div><div class="griglia">{carte}</div></section>')

    corpo = f"""{_testata(pre)}<main>
<div class="contenitore">
<nav class="briciole" aria-label="Sei qui"><ol><li><a href="{pre}">Archivio</a></li><li><a href="{pre}?famiglia={_serie_id(s['serie'])}#archivio">{e(_serie_nome(s['serie']))}</a></li><li aria-current="page">{e(s['strumento'])}</li></ol></nav>
<article>
<header class="sc-apertura">
<figure class="sc-foto"><div class="quadro">{_img(s, foto, pre, "(min-width: 900px) 580px, 100vw", lazy=False, priorita=True, passaggio=True)}</div>
<figcaption>Foto: {e(s['foto']['autore'])} · {e(s['foto']['licenza'])} · {e(s['foto']['fonte'])}</figcaption></figure>
<div class="sc-testo">
<p class="kicker">Scheda {s['numero']:03d} · {e(str(s['anno']))} · {e(s['luogo'])}</p>
<h1>{_nome(s['strumento'])}</h1>
<p class="gancio">{e(s['gancio'])}</p>
<p class="sottotitolo">{e(s['sottotitolo'])}</p>
{lettore}
<p class="bottoni">{''.join(bottoni)}</p>
</div>
</header>
<dl class="specifiche">{specifiche}</dl>
<div class="sc-corpo{' col-reel' if video else ''}"><div class="corpo">{corpo_sezioni}</div>{video}</div>
<section class="blocco rivela" id="tavole"><p class="kicker">Il carosello · si aprono in grande</p><h2>Le 6 tavole</h2><div class="tavole">{tavole}</div></section>
<section class="blocco fonti rivela"><p class="kicker">Da dove viene</p><h2>Fonti</h2><ol>{fonti}</ol><div class="crediti">{crediti_html}</div></section>
</article>
<nav class="vicine" aria-label="Altre schede">{vicina(prima, "prima")}{vicina(dopo, "dopo")}</nav>
{famiglia}
</div>
</main>{_piede(pre)}"""

    # Dati strutturati.
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
    # usa un tipo più generico. Per questo il reel NON è marcato
    # VideoObject: Google pretende uploadDate e miniatura, e su una pagina
    # dove il video non è il contenuto principale lo segnalerebbe e basta.
    immagini = [f"{BASE}/tavole/{slug}/01.jpg"]
    if foto:
        immagini.insert(0, f"{BASE}/{foto['1280']}")
    titolo_art = f"{s['strumento']} ({s['anno']}) — {s['gancio']}"
    ld = {"@context": "https://schema.org", "@graph": [
        {
            "@type": "Article", "@id": f"{url}#scheda",
            "headline": titolo_art if len(titolo_art) <= 110 else titolo_art[:109].rstrip() + "…",
            "description": s["sottotitolo"],
            "image": immagini,
            "datePublished": p.get("quando", ""),
            "dateModified": p.get("quando", ""),
            "inLanguage": "it",
            "mainEntityOfPage": url,
            "author": {"@type": "Organization", "name": "Elettrofoni", "url": f"{BASE}/"},
            "publisher": {"@id": f"{BASE}/#org"},
            "about": {
                "@type": "Thing", "name": s["strumento"],
                "description": (f"Strumento musicale elettronico del {s['anno']}, "
                                f"costruito da {s['costruttore']} ({s['luogo']})."),
            },
            "citation": [f["titolo"] for f in s["fonti"]],
        },
        {
            "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Archivio", "item": f"{BASE}/"},
                {"@type": "ListItem", "position": 2, "name": _serie_nome(s["serie"]),
                 "item": f"{BASE}/?famiglia={_serie_id(s['serie'])}"},
                {"@type": "ListItem", "position": 3, "name": s["strumento"], "item": url},
            ],
        },
        _org(),
    ]}
    descrizione = (f"{s['strumento']} ({s['anno']}): {s['sottotitolo']} Storia, tecnologia e artisti, "
                   "con fonti verificate." + (" E il suono vero della macchina." if suono else ""))
    (DOCS / "tavole" / slug).mkdir(parents=True, exist_ok=True)
    (DOCS / "tavole" / slug / "index.html").write_text(
        _pagina(f"{s['strumento']} ({s['anno']}) — storia e come funziona | Elettrofoni",
                corpo, descrizione, canonical=url, prefisso=pre,
                og_image=f"{BASE}/tavole/{slug}/01.jpg", og_tipo="article",
                pubblicata=p.get("quando"), ld=ld,
                script=(JS_LETTORE if suono else "") + JS_LENTE),
        encoding="utf-8")


# --------------------------------------------------------------- home ---

def _home(uscite, media, reel_link):
    recenti = list(reversed(uscite))
    con_suono = [(p, s) for p, s in recenti if media["suoni"].get(s["slug"])]
    anni = [a for a in (_anno(s) for _, s in uscite) if a]
    famiglie = {}
    for _, s in uscite:
        famiglie[s["serie"]] = famiglie.get(s["serie"], 0) + 1

    # La vetrina: le ultime cinque, la più nuova grande. È la prima cosa
    # che si vede, e fa vedere PIÙ macchine (regola del 16/10/2026).
    tessere = "".join(
        f'<a class="tessera{" grande" if n == 0 else ""}" href="tavole/{s["slug"]}/">'
        + ('<span class="bollino">Ultima uscita</span>' if n == 0 else "")
        + f'<span class="ft">{_img(s, media["foto"].get(s["slug"]), "", "(min-width: 980px) 340px, 46vw", lazy=False, priorita=(n == 0), box=(5 / 3 if n == 0 else 6 / 5))}</span>'
        f'<span class="et"><i>N. {s["numero"]:03d}</i><b>{e(s["strumento"])}</b></span></a>'
        for n, (_, s) in enumerate(recenti[:5]))
    intro = f"""<section class="copertina"><div class="contenitore">
<div class="cop-testo">
<p class="kicker">Elettrofoni · l'archivio delle schede</p>
<h1>Catalogo delle macchine <em>sonore</em></h1>
<p class="lead">Sintetizzatori, drum machine, organi, campionatori, effetti. Per ognuna c'è chi l'ha costruita, cosa c'è dentro, chi ci ha suonato e una storia, con le fonti in fondo.</p>
<p class="bottoni"><a class="bottone pieno" href="#archivio">Sfoglia le schede ↓</a>{'<a class="bottone" href="suoni/">Ascolta le macchine →</a>' if con_suono else ''}</p>
</div>
<div class="vetrina">{tessere}</div>
<p class="cifre"><span><b>{len(uscite)}</b>schede</span><span><b>{min(anni) if anni else ''}–{max(anni) if anni else ''}</b>gli anni</span><span><b>{len(famiglie)}</b>famiglie</span><span><b>{len(con_suono)}</b>col suono vero</span></p>
</div></section>"""

    # Il nastro: i nomi di tutte le macchine, due volte di fila perché
    # scorrendo non si veda la giunta. È decorazione: aria-hidden.
    nomi_nastro = "".join(f"<span>{e(s['strumento'])}</span>" for _, s in recenti)
    nastro = f'<div class="nastro" aria-hidden="true"><div>{nomi_nastro}{nomi_nastro}</div></div>' if recenti else ""

    # Una fascia sola verso la pagina dei suoni (16/10/2026: niente elenco
    # in home), ma con un lettore vero: l'ultima macchina registrata.
    verso = ""
    if con_suono:
        _, s0 = con_suono[0]
        verso = f"""<section class="ascolta"><div class="contenitore">
<div><p class="kicker">Il suono vero</p><h2>{len(con_suono)} macchine registrate davvero</h2></div>
{_lettore(s0, media["suoni"][s0["slug"]], "", etichetta="Ascolta: " + s0["strumento"])}
<a class="verso" href="suoni/">Tutte le registrazioni →</a>
</div></section>"""

    chips = [f'<button class="chip" type="button" data-filtro="tutte" aria-pressed="true">Tutte<span>{len(uscite)}</span></button>']
    if con_suono:
        chips.append(f'<button class="chip" type="button" data-filtro="suono" aria-pressed="false">♪ Suono vero<span>{len(con_suono)}</span></button>')
    for serie, n in sorted(famiglie.items(), key=lambda kv: (-kv[1], kv[0])):
        chips.append(f'<button class="chip" type="button" data-filtro="{_serie_id(serie)}" aria-pressed="false">'
                     f'{e(_serie_breve(serie))}<span>{n}</span></button>')
    # La linea del tempo: una colonna per epoca, alta quanto le schede.
    per_epoca = {}
    for _, s in uscite:
        k = _epoca(s)
        if k:
            per_epoca[k] = per_epoca.get(k, 0) + 1
    ordine_epoche = sorted(per_epoca, key=lambda k: 0 if k == "pre" else int(k))
    tetto = max(per_epoca.values(), default=1)
    epoche = "".join(
        f'<button class="epoca" type="button" data-epoca="{k}" aria-pressed="false" style="--h:{per_epoca[k] / tetto:.2f}" '
        f'aria-label="{_epoca_nome(k)[1]}: {per_epoca[k]} schede" title="{_epoca_nome(k)[1]}: {per_epoca[k]} schede">'
        f'<i></i>{_epoca_nome(k)[0]}</button>'
        for k in ordine_epoche)
    carte = "".join(_card(s, media["foto"].get(s["slug"]), media["suoni"].get(s["slug"]), "",
                          "(min-width: 1240px) 280px, (min-width: 560px) 45vw, 50vw",
                          nuova=(n == 0), n=n)
                    for n, (_, s) in enumerate(recenti))
    archivio = f"""<section class="archivio contenitore" id="archivio">
<div class="testa-sezione"><div><p class="kicker">La più nuova per prima</p><h2>Tutte le schede</h2></div><p class="conta" id="conta" aria-live="polite">{len(uscite)} schede</p></div>
<div class="strumenti" id="strumenti" hidden>
<div><label class="etichetta" for="cerca">Cerca</label><input id="cerca" class="cerca" type="search" placeholder="Moog, 1982, Kraftwerk…" aria-label="Cerca una macchina, un costruttore o un artista" autocomplete="off"></div>
<div><span class="etichetta">Linea del tempo</span><div class="epoche" role="group" aria-label="Epoche">{epoche}</div></div>
<div class="riga-chips"><div class="chips" role="group" aria-label="Famiglie">{''.join(chips)}</div>
<div class="ordina" role="group" aria-label="Ordine delle schede"><span>Ordina</span><button type="button" data-ordine="uscita" aria-pressed="true">Uscita</button><button type="button" data-ordine="anno" aria-pressed="false">Anno</button></div></div>
</div>
<div class="griglia" id="griglia">{carte}</div>
<p class="nessuna" id="nessuna" hidden>Nessuna scheda trovata. Provate col nome del costruttore o di chi ci ha suonato.</p>
</section>"""

    vuoto = '<p class="contenitore nessuna">Le prime schede stanno arrivando.</p>' if not uscite else ""
    corpo = f"{_testata('')}<main>{intro}{vuoto}{nastro}{verso}{archivio}</main>{_piede('')}"
    ld = {"@context": "https://schema.org", "@graph": [
        _org(),
        {"@type": "WebSite", "@id": f"{BASE}/#sito", "name": "Elettrofoni",
         "alternateName": "Elettrofoni — Catalogo delle macchine sonore",
         "url": f"{BASE}/", "inLanguage": "it", "publisher": {"@id": f"{BASE}/#org"}},
    ]}
    og_idx = f"{BASE}/tavole/{recenti[0][1]['slug']}/01.jpg" if recenti else None
    (DOCS / "index.html").write_text(
        _pagina("Elettrofoni — storia dei sintetizzatori e degli strumenti elettronici",
                corpo,
                "Sintetizzatori, drum machine, organi e campionatori: chi li ha inventati, "
                "come funzionano e chi li ha suonati, con il suono vero dove c'è. "
                "Una scheda al giorno, con fonti verificate.",
                canonical=f"{BASE}/", prefisso="", og_image=og_idx, verifica=True, ld=ld,
                script=JS_ARCHIVIO + (JS_LETTORE if con_suono else "")),
        encoding="utf-8")
    _pagina_suoni(con_suono, media)


def _pagina_suoni(con_suono, media):
    """La pagina «Il suono vero»: tutte le registrazioni, la più nuova per prima."""
    pre = "../"
    dischi = []
    for _, s in con_suono:
        suono = media["suoni"][s["slug"]]
        dischi.append(f"""<li class="disco">
<a class="disco-foto" href="{pre}tavole/{s['slug']}/" tabindex="-1" aria-hidden="true">{_img(s, media['foto'].get(s['slug']), pre, '76px')}</a>
<div><a class="disco-nome" href="{pre}tavole/{s['slug']}/">{_nome(s['strumento'])}</a><span class="disco-meta">{e(str(s['anno']))} · {e(_serie_breve(s['serie']))}</span></div>
{_lettore(s, suono, pre, mini=True)}
<p class="disco-credito">{_credito_suono(s['reel_audio'], suono, breve=True)}</p>
</li>""")
    corpo = f"""{_testata(pre)}<main class="suoni"><div class="contenitore">
<p class="kicker">Da sentire · {len(con_suono)} registrazioni</p>
<h1>Il suono <em>vero</em></h1>
<p class="lead">Registrazioni libere delle macchine vere, da Wikimedia Commons e da Freesound. Niente dischi, solo la macchina, a volume pareggiato: si può passare dall'una all'altra senza toccare la manopola. Il nome porta alla scheda.</p>
<ul class="dischi">{''.join(dischi)}</ul>
</div></main>{_piede(pre)}"""
    (DOCS / "suoni").mkdir(exist_ok=True)
    (DOCS / "suoni" / "index.html").write_text(
        _pagina("Il suono vero: le registrazioni delle macchine | Elettrofoni", corpo,
                f"{len(con_suono)} registrazioni libere di sintetizzatori, drum machine e organi veri: "
                + ", ".join(s["strumento"] for _, s in con_suono[:5]) + " e gli altri.",
                canonical=f"{BASE}/suoni/", prefisso=pre, script=JS_LETTORE),
        encoding="utf-8")


def _pagina_404():
    pre = f"{PERCORSO}/"
    corpo = f"""{_testata(pre)}<main class="contenitore errore">
<p class="kicker">Errore 404</p>
<h1>Questa macchina non è in catalogo</h1>
<p>La pagina non c'è, o non c'è più. Le schede uscite sono tutte nell'archivio.</p>
<p class="bottoni"><a class="bottone pieno" href="{pre}">Vai all'archivio →</a></p>
</main>{_piede(pre)}"""
    (DOCS / "404.html").write_text(
        _pagina("Pagina non trovata | Elettrofoni", corpo, "Pagina non trovata.",
                canonical=f"{BASE}/", prefisso=pre), encoding="utf-8")


# --------------------------------------------------------------- main ---

def main():
    stato = json.loads((RADICE / "stato.json").read_text()) if (RADICE / "stato.json").exists() \
        else {"pubblicati": []}
    per_slug = {s["slug"]: s for s in contenuti.SCHEDE}
    DOCS.mkdir(exist_ok=True)
    uscite = [(p, per_slug[p["slug"]]) for p in stato["pubblicati"] if p["slug"] in per_slug]

    # Il permalink del reel di ogni scheda; se c'è un rifacimento nel
    # formato 2, vince quello.
    reel_link = {}
    for r in stato.get("reel", []):
        if r.get("permalink") and r.get("slug") in per_slug and \
                (r.get("formato") == 2 or r["slug"] not in reel_link):
            reel_link[r["slug"]] = r["permalink"]

    file_media = DOCS / "media.json"
    try:
        media = json.loads(file_media.read_text())
    except (FileNotFoundError, ValueError):
        media = {}
    for k in ("foto", "suoni", "copertine"):
        media.setdefault(k, {})
    ff = _ffmpeg()
    if not ff:
        print("[archivio] AVVISO: ffmpeg non trovato: i suoni e le copertine nuove restano da fare")
    # Le pagine usano SOLO quello che le funzioni restituiscono oggi: se una
    # scheda perde la registrazione (scartata dopo un riascolto) il lettore
    # deve sparire, non restare in piedi sull'indice di ieri.
    attivi = {"foto": {}, "suoni": {}, "copertine": {}}
    for _, s in uscite:
        for k, fz in (("foto", lambda s: _foto_web(s, media["foto"])),
                      ("suoni", lambda s: _suono_web(s, media["suoni"], ff)),
                      ("copertine", lambda s: _copertina_reel(s, media["copertine"], ff))):
            r = fz(s)
            if r and (k != "copertine" or r.get("file")):
                attivi[k][s["slug"]] = r
    media = attivi
    file_media.write_text(json.dumps(media, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")

    (DOCS / "stile.css").write_text(STILE.strip() + "\n", encoding="utf-8")
    logo = RADICE / "assets" / "marchio" / "icona-app-meta.png"
    if logo.exists():
        shutil.copyfile(logo, DOCS / "logo.png")
    else:
        print("[archivio] AVVISO: manca assets/marchio/icona-app-meta.png, niente logo né favicon")

    # Dinamo di latta per il bollo dell'invito: 520 px, una volta sola.
    din_src = RADICE / "assets" / "dinamo" / "dinamo_reale_b.png"
    din = DOCS / "dinamo.jpg"
    if din_src.exists() and not din.exists():
        try:
            from PIL import Image
            with Image.open(din_src) as im:
                im = im.convert("RGB")
                im.thumbnail((520, 520), Image.LANCZOS)
                im.save(din, "JPEG", quality=82, optimize=True, progressive=True)
        except ImportError:
            print("[archivio] AVVISO: manca Pillow, l'invito esce senza Dinamo")

    for i, (p, s) in enumerate(uscite):
        _pagina_scheda(s, p, i, uscite, media, reel_link)
    _home(uscite, media, reel_link)
    _pagina_404()

    # Pages non deve passare da Jekyll (servirebbe solo a rompere i path)
    (DOCS / ".nojekyll").write_text("")
    # SEO: sitemap con le sole pagine pubblicate + robots che la indica.
    # <lastmod> dice a Google quando la pagina è cambiata: senza, ogni
    # ripassata è alla cieca. La home porta la data dell'ultimo post,
    # ogni scheda la propria data di pubblicazione.
    ultimo = max((q["quando"][:10] for q in stato["pubblicati"]), default=None)
    voci = [(f"{BASE}/", ultimo, "daily"), (f"{BASE}/suoni/", ultimo, "weekly")]
    voci += [(f"{BASE}/tavole/{q['slug']}/", q["quando"][:10], "monthly")
             for q, _ in uscite]
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
    print(f"[archivio] {len(uscite)} schede pubblicate in docs/, "
          f"{sum(1 for _, s in uscite if media['suoni'].get(s['slug']))} col suono vero")


if __name__ == "__main__":
    main()
