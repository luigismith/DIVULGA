# -*- coding: utf-8 -*-
"""ELETTROFONI — il reel della scheda.

PERCHÉ ESISTE. Il carosello lo vedono i follower; il reel è l'unico
formato che Instagram mostra a chi non ci segue. Su un account nuovo è
la leva di crescita più forte, e a costo zero.

COSA NON È. Non sono le sei tavole del carosello incollate una dopo
l'altra: quelle sono 4:5 e piene di testo lungo, illeggibili in verticale
e a quel ritmo. Il reel ha scene proprie, poche parole per schermata, e
il ritmo della sigla — quattro secondi a scena, sette scene, ventotto
secondi. Un reel sotto i trenta secondi viene guardato fino in fondo, e
la percentuale di completamento è quello che conta davvero: l'ultima
scena è la domanda, da sola, perché è l'unico posto in cui qualcuno che
non ci segue può ancora leggerla.

SPECIFICHE (imparate a fatica, NON toccarle senza rileggerle):
720x1280 — a 1080x1920 i video lunghi vengono rifiutati; H.264 profilo
main; yuv420p; GOP chiuso (-g 60 -sc_threshold 0); niente B-frame
(-bf 0); AAC 44.1 kHz stereo; seconda passata di remux con
`-use_editlist 0`. Le scene si disegnano comunque a 1080x1920 e si
riducono in ffmpeg: rimpicciolire un testo già renderizzato a 720 lo
rende impastato.

IL BUDGET È IL VERO VINCOLO. L'elaborazione video dell'account si
esaurisce dopo una dozzina di container, e anche i tentativi falliti la
consumano. Quindi: si costruisce e si verifica QUI, in locale, quante
volte serve; si pubblica UNA volta sola. Questo file non pubblica niente.
"""
import pathlib
import shutil
import subprocess
import sys

import contenuti
import genera_tavole as gt
import suoni

RADICE = pathlib.Path(__file__).resolve().parent
L, H = 1080, 1920          # come si disegna
LARG, ALT = 720, 1280      # come si esporta
FPS = 30
SEC_SCENA = 4.0
DISSOLVENZA = 0.35


def _ff(nome="ffmpeg"):
    if shutil.which(nome):
        return nome
    raise RuntimeError(f"{nome} non trovato: il reel non si può montare")


def _esegui(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{cmd[0]} fallito:\n{r.stderr[-1500:]}")


def _taglia(testo, massimo):
    """Taglia alla fine di una frase, non a metà parola. Nel reel il testo
    lungo non si legge: meglio una frase intera che tre monche."""
    if len(testo) <= massimo:
        return testo
    pezzo = testo[:massimo]
    for sep in (". ", "; ", ": ", ", "):
        i = pezzo.rfind(sep)
        if i > massimo * 0.5:
            return pezzo[:i + 1].strip()
    return pezzo.rsplit(" ", 1)[0] + "…"


# ------------------------------------------------------------- scene ---

def _css():
    return f"""
body{{width:{L}px;height:{H}px}}
/* Nel carosello il testo parte dall'alto e va bene: chi legge scorre.
   In un reel no — restano quattro secondi e un buco di schermo vuoto
   sotto sembra una diapositiva non finita. Qui si centra tutto. */
.corpo{{padding:70px;justify-content:center}}
.kicker{{font-size:24px;letter-spacing:.22em}}
.grande{{flex:none;font-weight:700;text-transform:uppercase;line-height:1.02;
  font-size:104px;margin-top:26px}}
.media{{flex:none;font-family:'PlexMono';font-size:40px;line-height:1.5;margin-top:34px}}
.pieno{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.velo{{position:absolute;inset:0;background:linear-gradient(180deg,
  rgba(56,41,29,.25) 0%, rgba(56,41,29,.55) 45%, rgba(56,41,29,.92) 100%)}}
.sopra{{position:relative;z-index:2;display:flex;flex-direction:column;height:100%;
  padding:70px;color:{gt.CREMA}}}
.sopra .grande{{color:{gt.CREMA};margin-top:auto}}
.sopra .kicker{{color:{gt.ARANCIO}}}
.sopra .coda{{flex:none;font-family:'PlexMono';font-size:30px;margin-top:24px;color:{gt.CREMA2}}}
.figure{{flex:none;margin-top:40px}}
.fig{{display:flex;align-items:baseline;gap:26px;border-bottom:3px solid {gt.BRUNO};padding:30px 0}}
.fig .n{{font-family:'PlexMono';font-weight:600;font-size:26px;color:{gt.ARANCIO};flex:none}}
.fig .v{{font-weight:700;font-size:52px;text-transform:uppercase;line-height:1.05}}
.riquadro{{flex:none;border:4px solid {gt.BRUNO};background:{gt.CREMA2};padding:44px 48px}}
.riquadro .et{{font-family:'PlexMono';font-weight:600;font-size:24px;letter-spacing:.2em;color:{gt.ARANCIO};margin-bottom:18px}}
.riquadro .t{{font-weight:700;font-size:56px;line-height:1.1}}
.riquadro .s{{font-family:'PlexMono';font-size:32px;line-height:1.45;margin-top:18px}}
.chiusa{{flex:none;margin-top:70px;text-align:center}}
.chiusa .firma{{font-weight:700;font-size:64px;line-height:1.1;text-transform:uppercase}}
.chiusa .cta{{font-family:'PlexMono';font-size:34px;margin-top:34px;color:{gt.ARANCIO}}}
.chiusa .tag{{font-weight:700;font-size:52px;letter-spacing:.1em;margin-top:26px}}
.avviso{{justify-content:center}}
.avviso .automa{{flex:none;margin-top:40px}}
.avviso .automa svg{{width:200px;height:200px}}
.avviso .grande{{font-size:80px;margin-top:30px}}
.domanda{{justify-content:center;text-align:center}}
.domanda .kicker{{color:{gt.ARANCIO}}}
/* La domanda deve essere la cosa piu' grande della schermata: e' l'unica
   ragione per cui questa scena esiste. flex:none perche' dentro un flex
   verrebbe compressa e l'autofit la rimpicciolirebbe fino a sparire —
   e' il primo errore del progetto, gia' scritto nel CSS di base. */
.domanda .grande{{flex:none;height:auto;font-size:96px;line-height:1.06;margin-top:34px}}
.domanda .chiusa{{margin-top:96px}}
.domanda .chiusa .firma{{font-size:30px;letter-spacing:.05em;color:#6b5138}}
.domanda .chiusa .tag{{font-size:62px;margin-top:20px}}
"""


def scene(scheda):
    """Le sei schermate del reel, in HTML. Poche parole per volta."""
    foto = (RADICE / scheda["foto"]["file"]).as_uri()
    s = []

    # 1 — il gancio, sulla foto
    s.append(f"""<img class="pieno" src="{foto}"><div class="velo"></div>
<div class="sopra">
  <div class="kicker">SCHEDA {scheda['numero']:03d} · {scheda['anno']} · {scheda['luogo'].upper()}</div>
  <div class="grande autofit" data-min="52" style="max-height:760px">{scheda['gancio']}</div>
  <div class="coda">{scheda['strumento'].upper()}</div>
</div>""")

    # 2 — che cos'è
    s.append(f"""{gt._testata(scheda)}<div class="corpo">
  <div class="kicker">CHE COS'È</div>
  <div class="grande autofit" data-min="46" style="max-height:520px">{scheda['strumento']}</div>
  <div class="media autofit" data-min="26" style="max-height:600px">{scheda['sottotitolo']}</div>
</div>""")

    # 3 — chi l'ha costruita
    s.append(f"""{gt._testata(scheda)}<div class="corpo">
  <div class="kicker">CHI L'HA COSTRUITA</div>
  <div class="grande autofit" data-min="44" style="max-height:420px">{scheda['inventore_nome']}</div>
  <div class="media autofit" data-min="24" style="max-height:700px">{_taglia(scheda['inventore'], 260)}</div>
</div>""")

    # 4 — come funziona, in tre righe
    figure = "".join(
        f'<div class="fig"><div class="n">{n}</div><div class="v">{v}</div></div>'
        for n, v in scheda["richiami"])
    s.append(f"""{gt._testata(scheda)}<div class="corpo">
  <div class="kicker">COME FUNZIONA</div>
  <div class="grande autofit" data-min="46" style="max-height:280px">In tre pezzi</div>
  <div class="figure">{figure}</div>
</div>""")

    # 5 — da ascoltare (se manca, l'avvertenza prende il suo posto)
    a = scheda.get("da_ascoltare")
    if a:
        dentro = (f'<div class="et">DA ASCOLTARE</div>'
                  f'<div class="t">{a["artista"]}<br>«{a["brano"]}» ({a["anno"]})</div>'
                  f'<div class="s">{a["cosa"]}</div>')
    else:
        dentro = (f'<div class="et">L\'ANEDDOTO</div>'
                  f'<div class="s">{_taglia(scheda["aneddoto"], 300)}</div>')
    s.append(f"""{gt._testata(scheda)}<div class="corpo">
  <div class="kicker">{"DA ASCOLTARE" if a else "ANEDDOTO"}</div>
  <div class="riquadro">{dentro}</div>
</div>""")

    # 6 — l'avvertenza, da sola
    chiusura = scheda.get("avvertenza") or scheda.get("battuta_dinamo", "")
    etichetta = "AVVERTENZE" if scheda.get("avvertenza") else "DINAMO DICE"
    # Con la CTA spostata nella scena 7 questa restava mezza vuota: due
    # righe di testo in mezzo a uno schermo verticale. Ci sta Dinamo, che
    # e' chi le avvertenze le scrive — la stessa figura della tavola 6.
    s.append(f"""{gt._testata(scheda)}<div class="corpo avviso">
  <div class="kicker">{etichetta}</div>
  <div class="automa">{gt._automa(gt.ARANCIO, gt.BRUNO)}</div>
  <div class="grande autofit" data-min="44" style="height:auto;max-height:820px">{chiusura}</div>
</div>""")

    # 7 — la domanda, e basta.
    #
    # LEZIONE IMPARATA (04/09/2026): la CTA stava qui sotto, nella scena 6,
    # a 34px — il testo PIU' PICCOLO della schermata piu' affollata del
    # reel, schiacciato fra l'avvertenza, la firma a 64px e l'handle a
    # 52px, negli ultimi quattro secondi, cioe' esattamente quando si
    # scrolla via. Il reel e' l'unica cosa che esce dal recinto (46 di
    # copertura contro 6,6 dei caroselli): se la domanda va fatta in un
    # posto solo, va fatta qui, e da sola.
    # Il reel passa da 24 a 28 secondi: resta sotto i trenta, che e' la
    # soglia oltre la quale la percentuale di completamento crolla.
    s.append(f"""{gt._testata(scheda)}<div class="corpo domanda">
  <div class="kicker">ORA TOCCA A VOI</div>
  <div class="grande autofit" data-min="56" style="height:auto;max-height:900px">{contenuti.cta(scheda)}</div>
  <div class="chiusa">
    <div class="firma">{contenuti.FIRMA}</div>
    <div class="tag">@ELETTROFONI</div>
  </div>
</div>""")
    return s


# ------------------------------------------------------------ montaggio ---

def costruisci(scheda, cartella=None):
    from playwright.sync_api import sync_playwright
    import os

    cartella = cartella or (RADICE / "docs" / "tavole" / scheda["slug"])
    cartella.mkdir(parents=True, exist_ok=True)
    lavoro = cartella / "_reel"
    lavoro.mkdir(exist_ok=True)

    png = []
    exe = os.environ.get("ELETTROFONI_CHROMIUM")
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe, args=["--no-sandbox", "--force-color-profile=srgb"])
        pg = b.new_page(viewport={"width": L, "height": H})
        for i, corpo in enumerate(scene(scheda), start=1):
            # LEZIONE IMPARATA (28/08/2026): qui c'era set_content(), e la
            # pagina finiva con origine about:blank — da cui Chromium
            # BLOCCA le sottorisorse file://. Risultato: niente font nostri
            # (usciva un serif di sistema) e niente foto nella prima scena,
            # senza un solo errore in console. Le tavole del carosello
            # scrivono un file e fanno goto(): stessa cosa qui, stesso motivo.
            tmp = lavoro / f"s{i}.html"
            tmp.write_text(gt._pagina(corpo, _css()), encoding="utf-8")
            pg.goto(tmp.as_uri())
            pg.wait_for_selector("body[data-pronto='1']", timeout=20000)
            # L'autofit parte su fonts.ready, che puo' arrivare PRIMA che la
            # foto sia decodificata: senza questa attesa la prima scena esce
            # con il velo sopra il vuoto.
            pg.wait_for_function(
                "Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)",
                timeout=20000)
            f = lavoro / f"s{i}.png"
            pg.screenshot(path=str(f))
            png.append(f)
        b.close()

    ff = _ff()
    clip = []
    for i, f in enumerate(png, start=1):
        c = lavoro / f"c{i}.mp4"
        # Una lenta spinta in avanti: senza, sei schermate ferme sembrano
        # una presentazione. Con, sembra un video.
        n = int(SEC_SCENA * FPS)
        vf = (f"scale={L}:{H},zoompan=z='min(1+0.00055*on,1.035)':"
              f"d={n}:s={LARG}x{ALT}:fps={FPS},"
              f"fade=t=in:st=0:d={DISSOLVENZA},"
              f"fade=t=out:st={SEC_SCENA - DISSOLVENZA}:d={DISSOLVENZA},format=yuv420p")
        _esegui([ff, "-y", "-loglevel", "error", "-loop", "1", "-framerate", str(FPS),
                 "-i", str(f), "-vf", vf, "-t", str(SEC_SCENA),
                 "-c:v", "libx264", "-profile:v", "main", "-pix_fmt", "yuv420p",
                 "-r", str(FPS), "-g", str(FPS * 2), "-sc_threshold", "0", "-bf", "0",
                 "-preset", "medium", "-crf", "21", str(c)])
        clip.append(c)

    elenco = lavoro / "elenco.txt"
    elenco.write_text("".join(f"file '{c.name}'\n" for c in clip))
    muto = lavoro / "muto.mp4"
    _esegui([ff, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
             "-i", str(elenco), "-c", "copy", str(muto)])

    durata = SEC_SCENA * len(clip)
    wav = lavoro / "musica.wav"
    suoni.genera(scheda, wav, durata=durata)

    grezzo = lavoro / "grezzo.mp4"
    _esegui([ff, "-y", "-loglevel", "error", "-i", str(muto), "-i", str(wav),
             "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2",
             "-shortest", str(grezzo)])

    finale = cartella / "reel.mp4"
    _esegui([ff, "-y", "-loglevel", "error", "-i", str(grezzo), "-c", "copy",
             "-movflags", "+faststart", "-use_editlist", "0", str(finale)])

    for f in lavoro.iterdir():
        f.unlink()
    lavoro.rmdir()
    return finale


def verifica(percorso):
    r = subprocess.run(
        [_ff("ffprobe"), "-v", "error", "-show_entries",
         "stream=codec_name,codec_type,profile,width,height,channels,sample_rate,has_b_frames",
         "-show_entries", "format=duration", "-of", "default=nw=1", str(percorso)],
        capture_output=True, text=True)
    d = r.stdout
    problemi = []
    if "codec_type=audio" not in d: problemi.append("NESSUN AUDIO")
    if "codec_name=h264" not in d: problemi.append("video non H.264")
    if "codec_name=aac" not in d: problemi.append("audio non AAC")
    if f"width={LARG}" not in d or f"height={ALT}" not in d:
        problemi.append(f"non è {LARG}x{ALT}")
    if "has_b_frames=0" not in d: problemi.append("contiene B-frame")
    return d, problemi


if __name__ == "__main__":
    slug = sys.argv[1] if len(sys.argv) > 1 else "dx7"
    if slug == "--prossima":
        import json
        stato = RADICE / "stato.json"
        gia = set()
        if stato.exists():
            gia = {x["slug"] for x in json.loads(stato.read_text())["pubblicati"]}
        prossima = contenuti.scheda_da_pubblicare(gia)
        if prossima is None:
            print("[reel] nessuna scheda in coda: niente da costruire")
            raise SystemExit(0)
        slug = prossima["slug"]
    scheda = next((s for s in contenuti.SCHEDE if s["slug"] == slug), None)
    if scheda is None:
        print(f"nessuna scheda '{slug}'"); raise SystemExit(1)
    out = costruisci(scheda)
    d, problemi = verifica(out)
    print(f"[reel] {slug}: {out.stat().st_size/1e6:.1f} MB — "
          + ("OK" if not problemi else "PROBLEMI: " + ", ".join(problemi)))
    print(d)
    if problemi:
        raise SystemExit(1)
