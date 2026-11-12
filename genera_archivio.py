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
             'family=Geist:wght@400..700&family=Geist+Mono:wght@400..600&display=swap">')

# Il sito NON ha l'aspetto delle tavole (12/11/2026, il proprietario: «non
# mi piace devi svecchiare, deve essere un bel sito del 2040, non del
# 1996»). Le tavole restano il catalogo anni '70; il sito è la vetrina di
# oggi: fondo quasi nero, Geist e Geist Mono, l'arancio come luce e non
# come inchiostro. Le foto stanno in «teche» chiare (--teca) con
# mix-blend-mode multiply, così le macchine scontornate di Commons (fondo
# bianco) si posano sulla teca invece di stare in un rettangolo bianco su
# fondo nero. Testo piccolo: mai l'arancio pieno su nero per righe lunghe;
# --ambra (#ffb547) per etichette, --testo2 per la prosa secondaria.
STILE = """
:root{--fondo:#08080a;--fondo2:#0f0f12;--fondo3:#16161a;--vetro:rgba(255,255,255,.045);--vetro2:rgba(255,255,255,.075);
--bordo:rgba(255,255,255,.085);--bordo2:rgba(255,255,255,.16);--testo:#f5f2ed;--testo2:#b4aea6;--testo3:#7c776f;
--arancio:#ff7a2e;--ambra:#ffb547;--brace:#ff4d1a;--su-arancio:#170a03;
--grad:linear-gradient(100deg,#ff5a1f 0%,#ff8a2e 45%,#ffc46b 100%);
--teca:radial-gradient(125% 95% at 50% 12%,#fbfaf8 0%,#eeece8 52%,#d8d5cf 100%);
--alone:0 0 0 1px rgba(255,122,46,.45),0 24px 70px -22px rgba(255,110,40,.55);
--sans:'Geist','Inter',system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;
--mono:'Geist Mono',ui-monospace,'SF Mono',Menlo,Consolas,monospace;
--r1:14px;--r2:22px;--r3:30px;--gutter:clamp(16px,4vw,40px)}
*,*::before,*::after{box-sizing:border-box}
*{margin:0;padding:0}
[hidden]{display:none!important}
.nobr{white-space:nowrap}
html{background:var(--fondo);color-scheme:dark;overflow-x:clip;scroll-behavior:smooth;-webkit-text-size-adjust:100%}
@view-transition{navigation:auto}
body{font-family:var(--sans);font-size:17px;line-height:1.6;color:var(--testo);background:var(--fondo);
-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale;text-rendering:optimizeLegibility;overflow-x:clip;position:relative;min-height:100vh}
body::before{content:"";position:fixed;inset:0;z-index:-1;pointer-events:none;
background:radial-gradient(60vw 45vw at 8% -8%,rgba(255,96,32,.20),transparent 62%),
radial-gradient(48vw 38vw at 100% 6%,rgba(122,92,255,.11),transparent 60%),
radial-gradient(70vw 50vw at 50% 115%,rgba(255,150,60,.08),transparent 60%)}
::selection{background:var(--arancio);color:var(--su-arancio)}
img,video,canvas{display:block;max-width:100%}
a{color:inherit;text-decoration:none}
a:focus-visible,button:focus-visible,input:focus-visible{outline:2px solid var(--ambra);outline-offset:3px;border-radius:10px}
button{font:inherit;color:inherit;background:none;border:0;cursor:pointer}
.contenitore{max-width:1280px;margin:0 auto;padding:0 var(--gutter)}
main{display:block}
h1,h2,h3{font-weight:600;letter-spacing:-.035em;line-height:1.02;text-wrap:balance}
em{font-style:normal}
h1 em,h2 em,.firma em{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.kicker{font-family:var(--mono);font-size:12px;font-weight:500;letter-spacing:.14em;text-transform:uppercase;color:var(--testo3);display:block}
.lead{font-size:clamp(17px,1.5vw,20px);line-height:1.55;color:var(--testo2);max-width:36em;text-wrap:pretty}
.etichetta{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--testo3);display:block;margin-bottom:10px}

/* --- testata: una pillola di vetro che resta in alto --- */
.testata{position:sticky;top:0;z-index:50;padding:12px var(--gutter) 0}
.testata .contenitore{display:flex;align-items:center;justify-content:space-between;gap:12px;height:58px;max-width:1240px;
padding:0 8px 0 16px;border-radius:999px;background:rgba(14,14,17,.62);border:1px solid var(--bordo);
-webkit-backdrop-filter:blur(20px) saturate(1.5);backdrop-filter:blur(20px) saturate(1.5);box-shadow:0 10px 40px -18px rgba(0,0,0,.8)}
.marchio{display:flex;align-items:center;gap:11px;min-width:0}
.marchio .q{flex:none;width:32px;height:32px;border-radius:50%;display:grid;place-items:center;background:var(--grad);
color:var(--su-arancio);box-shadow:0 0 22px rgba(255,110,40,.55)}
.marchio .q svg{width:20px;height:20px}
.marchio b{display:block;font-weight:650;font-size:15px;letter-spacing:.16em}
.marchio small{display:block;font-family:var(--mono);font-size:10.5px;letter-spacing:.08em;color:var(--testo3);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.marchio>span:last-child{min-width:0;line-height:1.25}
nav{flex:none}
.testata nav{display:flex;gap:2px}
.testata nav a{font-size:14px;font-weight:500;color:var(--testo2);padding:9px 14px;border-radius:999px;transition:background .2s,color .2s}
.testata nav a:hover{background:var(--vetro2);color:var(--testo)}
@media(max-width:599px){.testata nav .largo,.marchio small{display:none}.testata nav a{padding:9px 11px}}

/* --- bottoni --- */
.bottoni{display:flex;flex-wrap:wrap;gap:10px}
.bottone{display:inline-flex;align-items:center;gap:8px;min-height:46px;padding:0 20px;border-radius:999px;font-size:15px;font-weight:550;
border:1px solid var(--bordo2);background:var(--vetro);color:var(--testo);transition:transform .2s,background .2s,box-shadow .25s,border-color .2s}
.bottone:hover{background:var(--vetro2);border-color:rgba(255,255,255,.28);transform:translateY(-1px)}
.bottone.pieno{background:var(--grad);border-color:transparent;color:var(--su-arancio);box-shadow:0 10px 34px -10px rgba(255,100,30,.7)}
.bottone.pieno:hover{box-shadow:0 14px 44px -8px rgba(255,110,40,.85)}

/* --- copertina --- */
.copertina{position:relative;padding:clamp(40px,7vw,96px) 0 clamp(28px,4vw,48px)}
.copertina::before{content:"";position:absolute;inset:0 0 auto;height:640px;z-index:-1;pointer-events:none;
background-image:linear-gradient(rgba(255,255,255,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.045) 1px,transparent 1px);
background-size:56px 56px;-webkit-mask-image:radial-gradient(80% 70% at 50% 0%,#000 25%,transparent 75%);mask-image:radial-gradient(80% 70% at 50% 0%,#000 25%,transparent 75%)}
.copertina .contenitore{display:grid;grid-template-columns:minmax(0,1fr);gap:36px}
.cop-testo .kicker{display:inline-flex;align-items:center;gap:10px;padding:7px 14px 7px 10px;border:1px solid var(--bordo);border-radius:999px;background:var(--vetro);color:var(--testo2)}
.cop-testo .kicker::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--arancio);box-shadow:0 0 0 4px rgba(255,122,46,.18),0 0 14px var(--arancio);animation:battito 2.4s ease-in-out infinite}
@keyframes battito{50%{box-shadow:0 0 0 7px rgba(255,122,46,0),0 0 18px var(--arancio)}}
.cop-testo h1{font-size:clamp(46px,7.6vw,112px);margin:22px 0 22px;letter-spacing:-.055em;line-height:.94}
.cop-testo .lead{margin-bottom:28px}
.vetrina{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.tessera{position:relative;display:block;border-radius:var(--r2);overflow:hidden;background:var(--teca);aspect-ratio:6/5;isolation:isolate;
transition:transform .35s cubic-bezier(.2,.8,.2,1),box-shadow .35s}
.tessera.grande{grid-column:span 2;aspect-ratio:5/3}
.tessera .ft,.tessera .ft img{position:absolute;inset:0;width:100%;height:100%}
.tessera .ft img{object-fit:cover;mix-blend-mode:multiply;transition:transform .6s cubic-bezier(.2,.8,.2,1)}
.card-foto,.sc-foto .quadro,.vicina .ft,.disco-foto{position:relative}
img.sfondo{position:absolute!important;inset:0;width:100%;height:100%;object-fit:cover;filter:blur(22px) saturate(1.3) brightness(.9);transform:scale(1.25);mix-blend-mode:normal!important}
img.intera{position:relative;z-index:1;object-fit:contain!important;padding:7%;mix-blend-mode:normal!important;filter:drop-shadow(0 18px 30px rgba(0,0,0,.35))}
.tessera .ft img.intera{position:absolute}
.tessera:hover{transform:translateY(-3px);box-shadow:var(--alone)}
.tessera:hover .ft img{transform:scale(1.04)}
.tessera .et{position:absolute;left:10px;right:10px;bottom:10px;z-index:2;display:flex;align-items:baseline;gap:10px;padding:9px 13px;
border-radius:14px;background:rgba(12,12,15,.72);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);border:1px solid rgba(255,255,255,.1);min-width:0}
.tessera .et i{font-style:normal;font-family:var(--mono);font-size:11px;color:var(--ambra);flex:none}
.tessera .et b{font-weight:600;font-size:14.5px;letter-spacing:-.01em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
.tessera.grande .et b{font-size:clamp(16px,2vw,22px)}
.bollino{position:absolute;top:12px;left:12px;z-index:3;display:inline-flex;align-items:center;gap:8px;padding:6px 12px 6px 10px;border-radius:999px;
font-family:var(--mono);font-size:11px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;background:rgba(12,12,15,.8);color:var(--testo);
-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}
.bollino::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--arancio);box-shadow:0 0 10px var(--arancio);animation:battito 2.4s ease-in-out infinite}
.cifre{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
.cifre span{padding:18px 20px;border-radius:var(--r2);background:var(--vetro);border:1px solid var(--bordo);font-family:var(--mono);font-size:11.5px;
letter-spacing:.12em;text-transform:uppercase;color:var(--testo3)}
.cifre b{display:block;font-family:var(--sans);font-size:clamp(28px,3.4vw,42px);font-weight:600;letter-spacing:-.04em;line-height:1.1;color:var(--testo);
text-transform:none;margin-bottom:2px;font-variant-numeric:tabular-nums}
@media(max-width:599px){.copertina{padding-top:28px}.cop-testo h1{margin:16px 0 14px}.cop-testo .lead{font-size:16px;margin-bottom:20px}
.cop-testo .bottone{min-height:42px;padding:0 16px;font-size:14px}.copertina .contenitore{gap:24px}}
@media(min-width:980px){
.copertina .contenitore{grid-template-columns:minmax(0,5fr) minmax(0,7fr);align-items:center;column-gap:56px;row-gap:40px}
.vetrina{grid-template-columns:repeat(4,minmax(0,1fr));grid-template-rows:repeat(2,minmax(0,1fr))}
.tessera{aspect-ratio:auto;min-height:190px}
.tessera.grande{grid-row:span 2;aspect-ratio:auto}
.cifre{grid-column:1/-1;grid-template-columns:repeat(4,minmax(0,1fr))}}

/* --- nastro --- */
.nastro{overflow:hidden;border-block:1px solid var(--bordo);background:rgba(255,255,255,.02);padding:14px 0;
-webkit-mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent)}
.nastro div{display:flex;width:max-content;animation:nastro 140s linear infinite}
.nastro span{font-family:var(--mono);font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:var(--testo3);white-space:nowrap;padding:0 22px;position:relative}
.nastro span::after{content:"";position:absolute;right:-3px;top:50%;width:5px;height:5px;margin-top:-2.5px;border-radius:50%;background:var(--arancio);opacity:.7}
@keyframes nastro{to{transform:translateX(-50%)}}

/* --- fascia del suono --- */
.ascolta{padding:clamp(40px,6vw,72px) 0 0}
.ascolta .contenitore{position:relative;display:grid;grid-template-columns:minmax(0,1fr);gap:22px;align-items:center;padding-block:clamp(24px,3vw,36px);
border-radius:var(--r3);background:linear-gradient(135deg,rgba(255,110,40,.16),rgba(255,255,255,.03) 45%,rgba(122,92,255,.08));border:1px solid var(--bordo);
max-width:calc(1280px - 2 * var(--gutter));width:calc(100% - 2 * var(--gutter));overflow:hidden}
.ascolta h2{font-size:clamp(28px,3.4vw,44px);margin-top:8px}
.ascolta .kicker{color:var(--ambra)}
.ascolta .lettore{background:rgba(8,8,10,.55)}
.verso{font-weight:550;color:var(--testo);display:inline-flex;gap:6px;white-space:nowrap}
.verso:hover{color:var(--ambra)}
@media(min-width:980px){.ascolta .contenitore{grid-template-columns:minmax(0,4fr) minmax(0,7fr) auto;gap:36px}}
@media(max-width:699px){.ascolta .lettore-cosa{display:none}}

/* --- lettore, con l'oscilloscopio --- */
.lettore{display:grid;grid-template-columns:auto minmax(0,1fr);gap:8px 18px;align-items:center;padding:18px;border-radius:var(--r2);
background:var(--vetro);border:1px solid var(--bordo);margin:26px 0 8px;position:relative}
.play{width:58px;height:58px;border-radius:50%;display:grid;place-items:center;background:var(--grad);color:var(--su-arancio);
box-shadow:0 0 0 6px rgba(255,122,46,.12),0 10px 30px -8px rgba(255,100,30,.8);transition:transform .2s,box-shadow .3s;align-self:start}
.play:hover{transform:scale(1.06)}
.play svg{width:22px;height:22px;fill:currentColor}
.play .i-pausa,.lettore.suona .play .i-play{display:none}
.lettore.suona .play .i-pausa{display:block}
.lettore.suona .play{box-shadow:0 0 0 10px rgba(255,122,46,.14),0 0 46px rgba(255,110,40,.75)}
.lettore-info{min-width:0}
.lettore-titolo{font-family:var(--mono);font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--ambra);display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.onde{display:inline-flex;gap:2px;align-items:flex-end;height:12px}
.onde i{width:3px;height:3px;border-radius:2px;background:currentColor}
.lettore.suona .onde i{animation:onda .9s ease-in-out infinite}
.lettore.suona .onde i:nth-child(2){animation-delay:-.3s}.lettore.suona .onde i:nth-child(3){animation-delay:-.6s}
@keyframes onda{50%{height:12px}}
.lettore-cosa{font-size:15px;color:var(--testo2);margin-top:6px;line-height:1.45}
.oscillo{width:100%;height:64px;margin-top:12px;border-radius:12px;background:
linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px) 0 50%/100% 16px,
linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px) 0 0/24px 100%,rgba(0,0,0,.35);border:1px solid rgba(255,255,255,.06)}
.barra{position:relative;height:6px;margin-top:12px;border-radius:99px;background:rgba(255,255,255,.1);cursor:pointer;overflow:hidden}
.barra::after{content:"";position:absolute;inset:-8px 0}
.barra i{position:absolute;left:0;top:0;bottom:0;width:0;border-radius:99px;background:var(--grad);box-shadow:0 0 12px rgba(255,122,46,.8)}
.lettore-tempo{font-family:var(--mono);font-size:12px;color:var(--testo3);margin-top:8px;font-variant-numeric:tabular-nums}
.lettore audio{grid-column:1/-1;width:100%}
.lettore.js audio{display:none}
.lettore.mini{margin:0;padding:10px 14px 10px 10px;gap:4px 12px;background:rgba(0,0,0,.25)}
.lettore.mini .play{width:44px;height:44px;box-shadow:0 0 0 4px rgba(255,122,46,.1)}
.lettore.mini .play svg{width:17px;height:17px}
.lettore.mini .barra{margin-top:4px}
.lettore.mini .lettore-tempo{margin-top:6px;font-size:11px}
.credito-suono{font-family:var(--mono);font-size:11.5px;color:var(--testo3);line-height:1.6}
.credito-suono a,.disco-credito a,.crediti a,.sc-foto figcaption a{color:var(--testo2);text-decoration:underline;text-decoration-color:rgba(255,255,255,.25);text-underline-offset:3px}

/* --- archivio --- */
.archivio{padding-top:clamp(48px,7vw,96px);padding-bottom:clamp(40px,6vw,80px)}
.testa-sezione{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:24px}
.testa-sezione h2{font-size:clamp(34px,5vw,64px);margin-top:10px}
.conta{font-family:var(--mono);font-size:13px;color:var(--testo3);font-variant-numeric:tabular-nums}
.strumenti{display:grid;grid-template-columns:minmax(0,1fr);gap:20px;padding:20px;margin-bottom:28px;border-radius:var(--r3);
background:var(--vetro);border:1px solid var(--bordo);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px)}
@media(min-width:980px){.strumenti{grid-template-columns:minmax(0,5fr) minmax(0,7fr)}.riga-chips{grid-column:1/-1}}
.cerca{width:100%;height:52px;padding:0 18px 0 48px;border-radius:16px;border:1px solid var(--bordo2);font:inherit;font-size:16px;color:var(--testo);
background:rgba(0,0,0,.35) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%237c776f' stroke-width='2' stroke-linecap='round'%3E%3Ccircle cx='11' cy='11' r='7'/%3E%3Cpath d='m20 20-3.5-3.5'/%3E%3C/svg%3E") 16px 50%/20px no-repeat;
transition:border-color .2s,box-shadow .2s}
.cerca::placeholder{color:var(--testo3)}
.cerca:focus{outline:none;border-color:rgba(255,122,46,.7);box-shadow:0 0 0 4px rgba(255,122,46,.15)}
.epoche{display:flex;gap:6px;align-items:flex-end;height:96px;overflow-x:auto;scrollbar-width:none}
.epoche::-webkit-scrollbar{display:none}
.epoca{flex:1 0 34px;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:7px;height:100%;
font-family:var(--mono);font-size:10.5px;color:var(--testo3);letter-spacing:.02em;white-space:nowrap;transition:color .2s}
.epoca i{display:block;width:100%;max-width:44px;height:calc(6px + var(--h) * 60px);border-radius:8px 8px 3px 3px;
background:linear-gradient(to top,rgba(255,122,46,.25),rgba(255,181,71,.55));transition:background .25s,box-shadow .25s,transform .25s}
.epoca:hover{color:var(--testo)}
.epoca:hover i{transform:scaleY(1.04);transform-origin:bottom}
.epoca[aria-pressed=true]{color:var(--testo)}
.epoca[aria-pressed=true] i{background:var(--grad);box-shadow:0 0 22px rgba(255,122,46,.7)}
.riga-chips{display:flex;flex-wrap:wrap;gap:14px;justify-content:space-between;align-items:center}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{display:inline-flex;align-items:center;gap:8px;height:38px;padding:0 15px;border-radius:999px;border:1px solid var(--bordo2);
font-size:14px;font-weight:500;color:var(--testo2);transition:all .2s}
.chip span{font-family:var(--mono);font-size:11px;color:var(--testo3)}
.chip:hover{color:var(--testo);border-color:rgba(255,255,255,.3)}
.chip[aria-pressed=true]{background:var(--testo);border-color:var(--testo);color:#0b0b0d}
.chip[aria-pressed=true] span{color:#6b665f}
.ordina{display:inline-flex;align-items:center;gap:2px;padding:4px;border-radius:999px;background:rgba(0,0,0,.35);border:1px solid var(--bordo)}
.ordina span{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--testo3);padding:0 10px}
.ordina button{height:32px;padding:0 14px;border-radius:999px;font-size:13.5px;font-weight:500;color:var(--testo2)}
.ordina button[aria-pressed=true]{background:var(--vetro2);color:var(--testo);box-shadow:inset 0 0 0 1px var(--bordo2)}
.griglia{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
@media(min-width:700px){.griglia{grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}
@media(min-width:1100px){.griglia{grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}}
.card{display:flex;flex-direction:column;border-radius:var(--r2);overflow:hidden;background:var(--fondo2);border:1px solid var(--bordo);
transition:transform .35s cubic-bezier(.2,.8,.2,1),box-shadow .35s,border-color .35s;min-width:0}
.card:hover{transform:translateY(-4px);box-shadow:var(--alone);border-color:transparent}
.card-foto{position:relative;display:block;aspect-ratio:4/3;background:var(--teca);overflow:hidden;isolation:isolate}
.card-foto img{width:100%;height:100%;object-fit:cover;mix-blend-mode:multiply;transition:transform .6s cubic-bezier(.2,.8,.2,1)}
.card:hover .card-foto img{transform:scale(1.05)}
.nota{position:absolute;top:10px;right:10px;width:30px;height:30px;border-radius:50%;display:grid;place-items:center;font-size:14px;
background:rgba(12,12,15,.8);color:var(--ambra);box-shadow:0 0 14px rgba(255,140,50,.45);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px)}
.card-testo{display:flex;flex-direction:column;gap:6px;padding:14px 16px 18px;min-width:0}
.card-meta{display:flex;flex-wrap:wrap;gap:4px 10px;font-family:var(--mono);font-size:11px;color:var(--testo3);letter-spacing:.04em}
.card-meta .fam{color:var(--ambra);opacity:.85}
.card-nome{font-size:clamp(16px,1.6vw,20px);font-weight:600;letter-spacing:-.02em;line-height:1.15;overflow-wrap:anywhere}
.card-gancio{font-size:14px;line-height:1.45;color:var(--testo2);display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
@media(max-width:559px){.card-gancio{display:none}.card-testo{padding:12px 13px 14px}}
.nessuna{padding:48px 0;color:var(--testo2);text-align:center}

/* --- pagina della scheda --- */
.briciole{padding:28px 0 8px}
.briciole ol{list-style:none;display:flex;flex-wrap:wrap;gap:6px;font-family:var(--mono);font-size:12px;color:var(--testo3)}
.briciole li+li::before{content:"/";margin-right:6px;opacity:.5}
.briciole a:hover{color:var(--testo)}
.sc-apertura{display:grid;grid-template-columns:minmax(0,1fr);gap:28px;padding:18px 0 36px}
@media(min-width:900px){.sc-apertura{grid-template-columns:minmax(0,11fr) minmax(0,10fr);gap:56px;align-items:center}}
.sc-foto .quadro{position:relative;aspect-ratio:4/3;border-radius:var(--r3);overflow:hidden;background:var(--teca);isolation:isolate;
box-shadow:0 40px 100px -40px rgba(255,110,40,.35),0 0 0 1px rgba(255,255,255,.06)}
.sc-foto img{width:100%;height:100%;object-fit:cover;mix-blend-mode:multiply}
.sc-foto figcaption{font-family:var(--mono);font-size:11px;color:var(--testo3);margin-top:10px;line-height:1.5}
.sc-testo h1{font-size:clamp(42px,6.4vw,92px);letter-spacing:-.05em;line-height:.95;margin:16px 0 18px;overflow-wrap:anywhere}
.sc-testo .kicker{color:var(--ambra)}
.gancio{font-size:clamp(20px,2vw,25px);line-height:1.35;font-weight:500;letter-spacing:-.015em;text-wrap:pretty}
.sottotitolo{color:var(--testo2);margin-top:12px;text-wrap:pretty}
.sc-testo .bottoni{margin-top:22px}
.specifiche{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,190px),1fr));gap:10px;margin-bottom:clamp(40px,6vw,72px)}
.specifiche div{padding:16px 18px;border-radius:18px;background:var(--vetro);border:1px solid var(--bordo);min-width:0}
.specifiche dt{font-family:var(--mono);font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--testo3)}
.specifiche dd{font-size:16.5px;font-weight:550;margin-top:5px;line-height:1.35;overflow-wrap:anywhere}
.sc-corpo{display:grid;grid-template-columns:minmax(0,1fr);gap:48px}
@media(min-width:1040px){.sc-corpo.col-reel{grid-template-columns:minmax(0,1fr) 330px;gap:64px}}
.sezione{display:grid;grid-template-columns:minmax(0,1fr);gap:8px 32px;padding:36px 0;border-top:1px solid var(--bordo)}
.sezione:first-child{border-top:0;padding-top:0}
@media(min-width:760px){.sezione{grid-template-columns:96px minmax(0,1fr)}.sezione .testo{grid-column:2}}
.num{font-family:var(--mono);font-size:13px;font-weight:600;color:var(--arancio);letter-spacing:.1em;padding-top:6px}
@media(min-width:760px){.num{grid-row:span 2;font-family:var(--sans);font-size:64px;font-weight:600;letter-spacing:-.06em;line-height:.9;padding:0;
background:linear-gradient(180deg,#ffb547,#ff5a1f 70%,rgba(255,90,31,.15));-webkit-background-clip:text;background-clip:text;color:transparent}}
.sezione h2{font-size:clamp(26px,3vw,38px)}
.sezione h2 .kicker{margin-bottom:10px}
.testo{margin-top:14px}
.testo>p{font-size:18px;line-height:1.72;color:#d6d1c9;max-width:40em;text-wrap:pretty}
.artisti{list-style:none;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:10px}
.artisti li{padding:16px 18px;border-radius:18px;background:var(--vetro);border:1px solid var(--bordo);font-size:15px;line-height:1.5;color:var(--testo2)}
.artisti b{display:block;color:var(--testo);font-weight:600;font-size:16.5px;margin-bottom:3px}
.riquadro{margin-top:16px;padding:20px 22px;border-radius:var(--r2);background:linear-gradient(135deg,rgba(255,122,46,.13),rgba(255,255,255,.03));border:1px solid rgba(255,140,60,.3)}
.riquadro .kicker{color:var(--ambra)}
.riquadro p{color:var(--testo2);font-size:16px;margin-top:6px}
.riquadro .brano{color:var(--testo);font-size:19px;font-weight:600;letter-spacing:-.01em}
.avvertenza{display:flex;gap:18px;align-items:flex-start;margin-top:24px;padding:20px 22px;border-radius:var(--r2);
background:repeating-linear-gradient(-45deg,rgba(255,181,71,.07) 0 10px,transparent 10px 20px),rgba(255,255,255,.03);border:1px solid rgba(255,181,71,.35)}
.avvertenza svg{flex:none;width:52px;height:52px;color:var(--ambra)}
.avvertenza .kicker{color:var(--ambra)}
.avvertenza p:last-child{font-size:16.5px;color:var(--testo);margin-top:4px;line-height:1.5}
.lato{align-self:start}
@media(min-width:1040px){.lato{position:sticky;top:96px}}
.lato h2{font-size:26px;margin:8px 0 14px}
.lato video{width:100%;max-width:360px;aspect-ratio:9/16;height:auto;border-radius:var(--r2);background:#000;border:1px solid var(--bordo);box-shadow:0 30px 80px -30px rgba(255,110,40,.4)}
.nota-reel{font-size:14px;color:var(--testo2);margin-top:12px;max-width:360px}
.nota-reel a{color:var(--ambra)}
.blocco{padding:clamp(48px,6vw,80px) 0 0}
.blocco h2{font-size:clamp(30px,4vw,48px);margin:10px 0 22px}
.tavole{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
@media(min-width:760px){.tavole{grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}
.tavole a{display:block;border-radius:16px;overflow:hidden;border:1px solid var(--bordo);transition:transform .3s,box-shadow .3s}
.tavole a:hover{transform:translateY(-3px);box-shadow:var(--alone)}
.tavole img{width:100%;height:auto}
.fonti ol{list-style:none;counter-reset:f;display:grid;gap:2px}
.fonti li{counter-increment:f;display:grid;grid-template-columns:40px minmax(0,1fr);gap:4px 0;padding:12px 0;border-bottom:1px solid var(--bordo);font-size:15.5px}
.fonti li::before{content:counter(f,decimal-leading-zero);font-family:var(--mono);font-size:12px;color:var(--arancio);padding-top:3px;grid-row:span 2}
.fonti li a{color:var(--testo);overflow-wrap:anywhere}
.fonti li a:hover{color:var(--ambra)}
.data{font-family:var(--mono);font-size:11.5px;color:var(--testo3);grid-column:2}
.crediti{margin-top:22px;display:grid;gap:4px;font-family:var(--mono);font-size:11.5px;color:var(--testo3);line-height:1.6;overflow-wrap:anywhere}
.vicine{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;padding:clamp(48px,6vw,80px) 0 0}
.vicina{display:flex;align-items:center;gap:14px;padding:12px;border-radius:var(--r2);background:var(--vetro);border:1px solid var(--bordo);min-width:0;transition:border-color .25s,box-shadow .25s}
.vicina:hover{box-shadow:var(--alone);border-color:transparent}
.vicina.dopo{flex-direction:row-reverse;text-align:right}
.vicina .ft{flex:none;width:64px;height:64px;border-radius:12px;overflow:hidden;background:var(--teca);isolation:isolate}
.vicina .ft img{width:100%;height:100%;object-fit:cover;mix-blend-mode:multiply}
.vicina>span:last-child{min-width:0}
.vicina b{display:block;font-weight:600;font-size:15.5px;line-height:1.25;overflow-wrap:anywhere}
.dir{font-family:var(--mono);font-size:11px;color:var(--testo3);letter-spacing:.06em;display:block;margin-bottom:3px}
.vicina.vuota{background:none;border:0}
@media(max-width:559px){.vicina .ft{display:none}}
.famiglia{padding:clamp(48px,6vw,80px) 0 clamp(40px,6vw,72px)}
.famiglia .testa-sezione h2{font-size:clamp(28px,3.6vw,44px)}

/* --- la lente --- */
.lente{position:fixed;inset:0;z-index:100;display:grid;place-items:center;background:rgba(5,5,7,.9);-webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px);padding:56px 12px}
.lente img{max-width:100%;max-height:calc(100vh - 112px);width:auto;height:auto;border-radius:12px;box-shadow:0 40px 120px rgba(0,0,0,.6)}
.lente button{position:absolute;width:48px;height:48px;border-radius:50%;background:rgba(255,255,255,.1);border:1px solid var(--bordo2);font-size:22px;color:var(--testo);
-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}
.lente button:hover{background:rgba(255,255,255,.18)}
.lente .chiudi{top:12px;right:12px}
.lente .prima{left:12px;top:50%;margin-top:-24px}
.lente .dopo{right:12px;top:50%;margin-top:-24px}
.lente .conto{position:absolute;bottom:16px;left:50%;transform:translateX(-50%);font-family:var(--mono);font-size:12px;color:var(--testo2)}

/* --- pagina dei suoni --- */
.suoni{padding:clamp(40px,6vw,80px) 0}
.suoni h1{font-size:clamp(46px,7vw,100px);letter-spacing:-.055em;margin:16px 0 18px}
.suoni .kicker{color:var(--ambra)}
.dischi{list-style:none;display:grid;grid-template-columns:minmax(0,1fr);gap:12px;margin-top:40px}
@media(min-width:900px){.dischi{grid-template-columns:repeat(2,minmax(0,1fr))}}
.disco{display:grid;grid-template-columns:64px minmax(0,1fr);gap:12px 16px;align-items:center;padding:14px;border-radius:var(--r2);background:var(--vetro);border:1px solid var(--bordo)}
.disco-foto{display:block;width:64px;height:64px;border-radius:14px;overflow:hidden;background:var(--teca);isolation:isolate}
.disco-foto img{width:100%;height:100%;object-fit:cover;mix-blend-mode:multiply}
.disco-nome{display:block;font-weight:600;font-size:18px;letter-spacing:-.015em;line-height:1.2}
.disco-nome:hover{color:var(--ambra)}
.disco-meta{font-family:var(--mono);font-size:11.5px;color:var(--testo3)}
.disco .lettore{grid-column:1/-1}
.disco-credito{grid-column:1/-1;font-family:var(--mono);font-size:11px;color:var(--testo3);overflow-wrap:anywhere}

/* --- invito e piede --- */
.invito{padding:clamp(48px,7vw,96px) 0 0}
.invito .contenitore{position:relative;display:grid;grid-template-columns:minmax(0,1fr);gap:22px;justify-items:start;align-items:center;
padding-block:clamp(28px,4vw,48px);border-radius:var(--r3);background:radial-gradient(90% 140% at 0% 0%,rgba(255,110,40,.22),transparent 55%),var(--fondo2);
border:1px solid var(--bordo);max-width:calc(1280px - 2 * var(--gutter));width:calc(100% - 2 * var(--gutter));overflow:hidden}
@media(min-width:820px){.invito .contenitore{grid-template-columns:auto minmax(0,1fr) auto;gap:32px}}
.bollo{display:block;width:104px;height:104px;border-radius:50%;overflow:hidden;box-shadow:0 0 0 3px var(--fondo2),0 0 0 5px var(--arancio),0 0 50px rgba(255,110,40,.55)}
.bollo img{width:100%;height:100%;object-fit:cover}
.dove .kicker{color:var(--ambra)}
.invito-testo{font-size:clamp(24px,3vw,38px);font-weight:600;letter-spacing:-.035em;line-height:1.1;margin-top:8px;text-wrap:balance}
.piede{padding:clamp(48px,6vw,80px) 0 40px}
.firma{font-size:clamp(30px,6.4vw,88px);font-weight:650;letter-spacing:-.05em;line-height:.95;text-wrap:balance;max-width:14em}
.righe{display:flex;flex-wrap:wrap;gap:8px 22px;margin-top:36px;padding-top:22px;border-top:1px solid var(--bordo);font-family:var(--mono);font-size:12px;color:var(--testo3)}
.righe a:hover{color:var(--testo)}

/* --- 404 --- */
.errore{padding:clamp(64px,10vw,140px) var(--gutter);text-align:left}
.errore h1{font-size:clamp(40px,6vw,80px);margin:14px 0 16px;letter-spacing:-.05em}
.errore p{color:var(--testo2);margin-bottom:22px}

/* --- comparsa --- */
.js .rivela{opacity:0;transform:translateY(26px);filter:blur(8px);transition:opacity .8s cubic-bezier(.2,.8,.2,1),transform .8s cubic-bezier(.2,.8,.2,1),filter .8s}
.js .rivela.vista{opacity:1;transform:none;filter:none}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}
.js .rivela{opacity:1;transform:none;filter:none}}
"""
VERSIONE_CSS = hashlib.sha1(STILE.encode()).hexdigest()[:8]

AUTOMA = """<svg viewBox="0 0 200 200" fill="none" stroke="currentColor" aria-hidden="true">
<line x1="100" y1="40" x2="100" y2="22" stroke-width="8"/><circle cx="100" cy="16" r="7" fill="currentColor" stroke="none"/>
<rect x="52" y="44" width="96" height="90" rx="14" stroke-width="9"/>
<rect x="34" y="74" width="14" height="26" rx="4" fill="currentColor" stroke="none"/>
<rect x="152" y="74" width="14" height="26" rx="4" fill="currentColor" stroke="none"/>
<circle cx="80" cy="80" r="14" stroke-width="7"/><circle cx="120" cy="80" r="14" stroke-width="7"/>
<circle cx="80" cy="80" r="4" fill="currentColor" stroke="none"/><circle cx="120" cy="80" r="4" fill="currentColor" stroke="none"/>
<line x1="79" y1="106" x2="79" y2="120" stroke-width="6" stroke-linecap="round"/><line x1="93" y1="106" x2="93" y2="120" stroke-width="6" stroke-linecap="round"/>
<line x1="107" y1="106" x2="107" y2="120" stroke-width="6" stroke-linecap="round"/><line x1="121" y1="106" x2="121" y2="120" stroke-width="6" stroke-linecap="round"/>
</svg>"""

# Il segno del marchio nella testata: un'onda in un tondo arancio.
SEGNO = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" '
         'stroke-linejoin="round" aria-hidden="true"><path d="M2 12h3l2.5-6 4 12 3.5-9 2.5 6H22"/></svg>')

ICONA_PLAY = '<svg class="i-play" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4.5v15l13-7.5z"/></svg>'
ICONA_PAUSA = '<svg class="i-pausa" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 4h4.5v16H6zM13.5 4H18v16h-4.5z"/></svg>'

# Il lettore funziona anche senza JavaScript: c'è l'<audio controls> del
# browser. Lo script lo nasconde e accende il bottone; uno solo suona alla
# volta, perché due macchine insieme non sono un ascolto ma un pasticcio.
# L'oscilloscopio (12/11/2026) disegna la forma d'onda VERA del file che
# sta suonando (Web Audio, AnalyserNode): niente onde finte. Se il browser
# non ha Web Audio, resta la riga ferma e il suono va lo stesso.
JS_LETTORE = """<script>(function(){
var tutti=[].slice.call(document.querySelectorAll('.lettore')),ac=null;
function mmss(s){s=Math.max(0,Math.floor(s||0));return Math.floor(s/60)+':'+(s%60<10?'0':'')+(s%60)}
function scopio(l,a){var c=l.querySelector('.oscillo');if(!c||!c.getContext)return null;
var g=c.getContext('2d'),an=null,buf=null,raf=0,dpr=window.devicePixelRatio||1;
function misura(){dpr=window.devicePixelRatio||1;c.width=Math.round(c.clientWidth*dpr);c.height=Math.round(c.clientHeight*dpr)}
function riga(d){var w=c.width,h=c.height;g.clearRect(0,0,w,h);var gr=g.createLinearGradient(0,0,w,0);
gr.addColorStop(0,'#ff5a1f');gr.addColorStop(.5,'#ff8a2e');gr.addColorStop(1,'#ffc46b');
g.strokeStyle=gr;g.lineWidth=2*dpr;g.shadowColor='rgba(255,120,40,.9)';g.shadowBlur=12*dpr;g.globalAlpha=d?1:.45;g.beginPath();
var n=d?d.length:2;for(var i=0;i<n;i++){var v=d?Math.max(-1,Math.min(1,d[i]*1.8)):0,x=i/(n-1)*w,y=h/2-v*h*.42;if(i)g.lineTo(x,y);else g.moveTo(x,y)}g.stroke()}
function giro(){an.getFloatTimeDomainData(buf);var s=0;for(var i=1;i<512;i++){if(buf[i-1]<0&&buf[i]>=0){s=i;break}}
riga(buf.subarray(s,s+1024));raf=requestAnimationFrame(giro)}
misura();riga(null);window.addEventListener('resize',function(){misura();if(!raf)riga(null)});
return{prepara:function(){try{if(!ac){var AC=window.AudioContext||window.webkitAudioContext;if(!AC)return;ac=new AC()}
if(ac.state==='suspended')ac.resume();if(!an){var src=ac.createMediaElementSource(a);an=ac.createAnalyser();an.fftSize=2048;
buf=new Float32Array(an.fftSize);src.connect(an);an.connect(ac.destination)}}catch(e){an=null}},
via:function(){if(an&&!raf)giro()},ferma:function(){cancelAnimationFrame(raf);raf=0;riga(null)}}}
tutti.forEach(function(l){
var a=l.querySelector('audio'),b=l.querySelector('.play'),i=l.querySelector('.barra i'),barra=l.querySelector('.barra'),ora=l.querySelector('.ora'),sc=scopio(l,a);
a.removeAttribute('controls');l.classList.add('js');
b.addEventListener('click',function(){if(a.paused){tutti.forEach(function(x){if(x!==l){x.querySelector('audio').pause()}});if(sc)sc.prepara();a.play()}else{a.pause()}});
a.addEventListener('play',function(){l.classList.add('suona');b.setAttribute('aria-pressed','true');if(sc)sc.via()});
a.addEventListener('pause',function(){l.classList.remove('suona');b.setAttribute('aria-pressed','false');if(sc)sc.ferma()});
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
        # Foto intera: dietro c'è la stessa foto sfocata a riempire la teca
        # (sul fondo chiaro una foto non scontornata restava un rettangolino).
        # Stesso indirizzo, quindi il browser la scarica una volta sola.
        sfondo = (f'<img class="sfondo" src="{prefisso}{foto["640"]}" srcset="{srcset}" sizes="{sizes}" '
                  f'width="{w}" height="{h}" alt="" aria-hidden="true"{carica}>') if intera else ""
        return (sfondo + f'<img src="{prefisso}{foto["640"]}" srcset="{srcset}" sizes="{sizes}" '
                f'width="{w}" height="{h}" alt="{e(alt)}" style="object-position:{pos}"{classe}{carica}>')
    return (f'<img src="{prefisso}tavole/{s["slug"]}/01.jpg" width="1080" height="1350" '
            f'alt="{e(alt)}"{carica}>')


def _testata(prefisso):
    casa = prefisso or "./"
    return f"""<header class="testata"><div class="contenitore">
<a class="marchio" href="{casa}"><span class="q">{SEGNO}</span><span><b>ELETTROFONI</b><small>Catalogo delle macchine sonore</small></span></a>
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
        '<meta name="theme-color" content="#08080a">',
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
<div class="lettore-info">{intesta}{cosa}{"" if mini else '<canvas class="oscillo" aria-hidden="true"></canvas>'}<div class="barra" aria-hidden="true"><i></i></div>
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
<p class="kicker">Una macchina ogni sera alle 18</p>
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
