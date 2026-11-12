# -*- coding: utf-8 -*-
"""ELETTROFONI — il reel parlato con HeyGen («formato 4», prova del 12/11/2026).

PERCHÉ. Il proprietario, dopo il commento «voci AI di m***a» sul reel
dell'MT-40: «Usa heygen», poi «voce e Dinamo animato», «rendi l'avatar
iperrealistico», «v3 e Dinamo B», «mi piace fa uscire il nuovo reel»,
«Dinamo più grosso». È il formato 3 (genera_reel_voce.py) con due pezzi
cambiati e il resto identico (scene, foto, battute, suono vero sotto):
  · la voce è «ELETTROFONI Dinamo v3», disegnata su HeyGen;
  · Dinamo è il robot di latta iperrealistico (assets/dinamo/
    dinamo_reale_b.png) animato da HeyGen sulla voce, in una cornice più
    grande di quella del formato 3 (620 px contro 440, sotto la foto).

COME SI FA. HeyGen si usa dal connettore MCP della sessione, non dal
runner (il runner non ha una chiave HeyGen). Quindi il reel si costruisce
PRIMA, in sessione, e si committa già fatto in docs/tavole/<slug>/reel4.mp4;
pubblica_reel.py lo pubblica come gli altri quando trova il file.
  1. le frasi (assets/heygen/<slug>/frasi.json, verificate come quelle del
     formato 3) diventano v0..v6.wav con la voce v3 (create_speech);
  2. `python genera_reel_heygen.py piano <slug>` fa la linea del tempo e
     taglia la voce in pezzi da secondi interi (HeyGen anima solo durate
     intere, e con l'audio di riferimento al massimo 15 s): seg_0.wav,
     seg_1.wav…, coi tagli nelle pause fra le frasi, così il cambio di
     clip cade nel silenzio;
  3. i due pezzi vanno a HeyGen (reference_to_video: immagine di Dinamo B
     più l'audio; create_video_from_image rifiuta i volti non umani) e
     tornano come dinamo_0.mp4, dinamo_1.mp4…;
  4. `python genera_reel_heygen.py monta <slug>` monta il reel.
L'audio del reel è la voce di HeyGen messa in fila da noi, NON quella
dentro le clip: le clip servono solo per le immagini.

IL RIASCOLTO resta (regola 10): Whisper ricapisce ogni frase prima del
montaggio. Un nome che Whisper non sa scrivere ma che è detto giusto
(«Autechre» = /ˈɔtekər/, sentito «oteccor») si dichiara in
`nomi_accettati` di frasi.json con la pronuncia usata: non è un controllo
saltato, è un controllo fatto a orecchio e sui fonemi, e resta scritto.

    python genera_reel_heygen.py piano sk1
    python genera_reel_heygen.py monta sk1
"""
import json
import math
import pathlib
import sys

import numpy as np

import contenuti
import genera_reel as gr
import genera_reel_voce as grv

RADICE = pathlib.Path(__file__).resolve().parent
FPS = gr.FPS
NOME_FILE = "reel4.mp4"
SEC_INTRO, SEC_OUTRO = grv.SEC_INTRO, grv.SEC_OUTRO
SEC_PAUSA, SEC_PAUSA_CTA = grv.SEC_PAUSA, grv.SEC_PAUSA_CTA
SR = grv.SR_VOCE
SEG_MAX = 15                     # il tetto di HeyGen per una clip con audio di riferimento

# Impaginato (scala 1080x1920). Il proprietario, 12/11/2026: «Dinamo più
# grosso», poi sulla prima prova (cornice 620 px in basso a sinistra,
# targhetta a destra): «fa schifo. mettilo al centro e più grande». Ora la
# cornice è 760 px, centrata nella colonna libera dai bottoni di Instagram
# (x 160-920), con la base a y 1600 dove cominciano nome e didascalia; la
# foto della macchina sta sopra, alta al massimo 250 (nel formato 3 460),
# e Dinamo ne copre solo l'orlo. La targhetta col nome sta sulla foto, in
# alto a sinistra, su una riga sola (l'anno sotto): nella prima prova
# andava a capo dentro la sigla, «CASIO SK-» / «1».
IMPAGINATO = {"PANNELLO_MAX": 600, "FASCIA_Y": 610, "FASCIA_MAX": 250}
DIN_LATO = 760
DIN_X = 160
DIN_Y = 1600 - DIN_LATO
BORDO = 10
CSS_F4 = (f".hook,.cta .hook{{font-size:{grv.HOOK_PX}px}}"
          f".tag{{left:64px;bottom:auto;top:{IMPAGINATO['FASCIA_Y'] + 16}px;"
          f"white-space:nowrap;font-size:46px;line-height:1.05;z-index:2}}"
          f".tag small{{display:block;margin:6px 0 0}}"
          f".cornice{{position:absolute;left:{DIN_X}px;top:{DIN_Y}px;width:{DIN_LATO}px;height:{DIN_LATO}px;"
          f"box-sizing:border-box;border:{BORDO}px solid #38291d;border-radius:40px;background:#e9dcc3;"
          f"box-shadow:0 14px 34px rgba(0,0,0,.45)}}")


def cartella(slug):
    return RADICE / "assets" / "heygen" / slug


def frasi(slug):
    return json.loads((cartella(slug) / "frasi.json").read_text(encoding="utf-8"))


def piano(slug):
    """La linea del tempo e i due pezzi di voce per HeyGen."""
    scheda = next(s for s in contenuti.SCHEDE if s["slug"] == slug)
    d = frasi(slug)
    n_batt = len(scheda["reel_battute"])
    ruoli = [f["ruolo"] for f in d["frasi"]]
    attesi = [f"battuta{i}" for i in range(1, n_batt + 1)] + ["cta", "chiusura"]
    if ruoli != attesi:
        raise ValueError(f"ruoli {ruoli}, attesi {attesi}")
    ff = gr._ff()
    c = cartella(slug)
    lavoro = c / "_lavoro"
    lavoro.mkdir(exist_ok=True)
    pezzi = [grv._wav_standard(c / f"v{i}.wav", lavoro / f"v{i}.wav", ff) for i in range(len(ruoli))]
    durate = [len(p) / SR for p in pezzi]

    # Prima stesura: come il formato 3.
    pause = [SEC_PAUSA] * n_batt + [SEC_PAUSA_CTA, SEC_PAUSA]
    def inizi_da(pause):
        t, out = SEC_INTRO, []
        for dur, pa in zip(durate, pause):
            out.append(t)
            t += dur + pa
        return out, t
    inizi, fine = inizi_da(pause)
    # I tagli fra le clip. HeyGen anima solo durate intere, e con l'audio
    # di riferimento non va oltre i 15 s: due pezzi da 18 e 19 s sono
    # falliti tutti e due («generation failed», 12/11/2026), quello da 8 s
    # no. Quindi pezzi da al massimo SEG_MAX secondi, ognuno che finisce
    # 0,2 s dopo una frase; la frase dopo parte 0,25 s dopo il taglio
    # (si allunga la pausa che la precede), così il cambio di clip cade
    # nel silenzio.
    tagli = [SEC_INTRO]
    k = 0
    while True:
        inizi, fine = inizi_da(pause)
        fine_voce = inizi[-1] + durate[-1]
        if fine_voce + 0.3 - tagli[-1] <= SEG_MAX:
            break
        # l'ultima frase che finisce entro SEG_MAX dal taglio precedente
        ok = [j for j in range(k, len(durate)) if inizi[j] + durate[j] + 0.2 - tagli[-1] <= SEG_MAX]
        if not ok or ok[-1] == len(durate) - 1:
            raise ValueError("una frase non sta in un pezzo da SEG_MAX secondi")
        j = ok[-1]
        quanto = math.ceil(inizi[j] + durate[j] + 0.2 - tagli[-1])
        taglio = tagli[-1] + quanto
        pause[j] = taglio + 0.25 - (inizi[j] + durate[j])
        tagli.append(taglio)
        k = j + 1
    tagli.append(tagli[-1] + math.ceil(fine_voce + 0.3 - tagli[-1]))
    segmenti = [(a, int(round(b - a))) for a, b in zip(tagli, tagli[1:])]
    if any(not (5 <= q <= SEG_MAX) for _, q in segmenti):
        raise ValueError(f"pezzi {segmenti}: HeyGen anima da 5 a {SEG_MAX} s")
    durata = fine_voce + SEC_PAUSA + SEC_OUTRO

    totale = np.zeros(int(round(durata * SR)), dtype=np.int16)
    for ini, p in zip(inizi, pezzi):
        a = int(round(ini * SR))
        totale[a:a + len(p)] = p[:len(totale) - a]
    grv._scrivi_wav(c / "voce.wav", totale)
    for i, (da, quanto) in enumerate(segmenti):
        a, b = int(round(da * SR)), int(round((da + quanto) * SR))
        seg = np.zeros(b - a, dtype=np.int16)
        pezzo = totale[a:b]
        seg[:len(pezzo)] = pezzo
        grv._scrivi_wav(c / f"seg_{i}.wav", seg)
    p = {"inizi": inizi, "durate": durate, "segmenti": segmenti,
         "fine_voce": fine_voce, "durata": durata, "n_batt": n_batt}
    (c / "piano.json").write_text(json.dumps(p, indent=1), encoding="utf-8")
    import shutil
    shutil.rmtree(lavoro, ignore_errors=True)
    print(f"[reel4] {slug}: parlato {fine_voce - SEC_INTRO:.1f} s, pezzi HeyGen "
          + " + ".join(f"{q} s (da {a:.1f})" for a, q in segmenti) + f", reel {durata:.1f} s")
    return p


def riascolto(slug):
    import voce
    d = frasi(slug)
    accettati = set(d.get("nomi_accettati", {}))
    for i, f in enumerate(d["frasi"]):
        w = cartella(slug) / f"v{i}.wav"
        tr = voce.trascrivi(w)
        e, mancanti = voce.verifica(w, f["scritta"], tr)
        resto = [n for n in mancanti if n not in accettati]
        print(f"[reel4] {f['ruolo']}: WER {e:.2f}" + (f", accettati a orecchio: {mancanti}" if mancanti else ""))
        if e > voce.SOGLIA_WER or resto:
            raise RuntimeError(f"{f['ruolo']}: Dinamo non si capisce (WER {e:.2f}, {resto}) — «{tr}»")


def monta(slug):
    from playwright.sync_api import sync_playwright
    import os
    import shutil
    scheda = next(s for s in contenuti.SCHEDE if s["slug"] == slug)
    c = cartella(slug)
    p = json.loads((c / "piano.json").read_text(encoding="utf-8"))
    riascolto(slug)
    out_dir = RADICE / "docs" / "tavole" / slug
    lavoro = c / "_monta"
    lavoro.mkdir(exist_ok=True)
    ff = gr._ff()
    prima = {k: getattr(gr, k) for k in IMPAGINATO}
    for k, v in IMPAGINATO.items():
        setattr(gr, k, v)
    try:
        scene = gr.battute(scheda)
        n_batt = p["n_batt"]
        confini = [0.0] + [p["inizi"][k] for k in range(1, n_batt + 1)] + [p["durata"]]
        sec_scene = [b - a for a, b in zip(confini, confini[1:])]
        foto = contenuti.foto_del_reel(scheda)
        png = []
        with sync_playwright() as pw:
            b = pw.chromium.launch(executable_path=os.environ.get("ELETTROFONI_CHROMIUM"),
                                   args=["--no-sandbox", "--force-color-profile=srgb"])
            pg = b.new_page(viewport={"width": gr.L, "height": gr.H})
            for i, sc in enumerate(scene):
                tmp = lavoro / f"t{i}.html"
                tmp.write_text(gr._pagina(f"<style>{CSS_F4}</style><div class='cornice'></div>" + sc["html"]),
                               encoding="utf-8")
                pg.goto(tmp.as_uri())
                pg.wait_for_selector("body[data-pronto='1']", timeout=20000)
                if pg.evaluate("document.body.dataset.troppo") == "1":
                    raise RuntimeError(f"battuta {i + 1} troppo lunga: accorciarla")
                f = lavoro / f"t{i}.png"
                pg.screenshot(path=str(f), omit_background=True)
                png.append(f)
            b.close()
        clip = []
        for i, sc in enumerate(scene):
            n = round(sec_scene[i] * FPS)
            f = foto[sc["foto"] % len(foto)]
            cl = lavoro / f"c{i}.mp4"
            gr._esegui([ff, "-y", "-loglevel", "error", "-noautorotate", "-i", str(RADICE / f["file"]),
                        "-loop", "1", "-framerate", str(FPS), "-i", str(png[i]),
                        "-filter_complex", gr._filtro(f, sc["moto"], n)
                        + f";[v1]scale={gr.LARG}:{gr.ALT},setsar=1,format=yuv420p[o]",
                        "-map", "[o]", "-frames:v", str(n), "-r", str(FPS),
                        "-c:v", "libx264", "-profile:v", "main", "-pix_fmt", "yuv420p",
                        "-g", str(FPS * 2), "-sc_threshold", "0", "-bf", "0",
                        "-preset", "medium", "-crf", "20", str(cl)])
            clip.append(cl)
        (lavoro / "elenco.txt").write_text("".join(f"file '{x.name}'\n" for x in clip))
        muto = lavoro / "muto.mp4"
        gr._esegui([ff, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", str(lavoro / "elenco.txt"), "-c", "copy", str(muto)])
        n_tot = sum(round(s * FPS) for s in sec_scene)
    finally:
        for k, v in prima.items():
            setattr(gr, k, v)

    # Dinamo: fermo sul primo fotogramma nell'intro, le due clip di HeyGen
    # di seguito, fermo sull'ultimo fino alla fine. Angoli tondi con una
    # maschera, dentro la cornice disegnata nella scena.
    k = gr.LARG / gr.L
    lato = int(round((DIN_LATO - 2 * BORDO) * k / 2)) * 2
    x = int(round((DIN_X + BORDO) * k))
    y = int(round((DIN_Y + BORDO) * k))
    r = int(round((40 - BORDO) * k))
    from PIL import Image, ImageDraw
    maschera = lavoro / "maschera.png"
    im = Image.new("L", (lato, lato), 0)
    ImageDraw.Draw(im).rounded_rectangle([0, 0, lato - 1, lato - 1], radius=r, fill=255)
    im.save(maschera)
    segmenti = p["segmenti"]
    resto = p["durata"] - SEC_INTRO - sum(q for _, q in segmenti)
    din = lavoro / "dinamo.mov"     # qtrle con alfa: sta solo nel .mov
    n = len(segmenti)
    ingressi, filtri = [], []
    for i, (_, q) in enumerate(segmenti):
        ingressi += ["-i", str(c / f"dinamo_{i}.mp4")]
        filtri.append(f"[{i}:v]fps={FPS},scale={lato}:{lato},setsar=1,trim=duration={q},setpts=PTS-STARTPTS[s{i}]")
    gr._esegui([ff, "-y", "-loglevel", "error", *ingressi, "-loop", "1", "-i", str(maschera),
                "-filter_complex",
                ";".join(filtri) + ";" + "".join(f"[s{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,"
                f"tpad=start_mode=clone:start_duration={SEC_INTRO}:stop_mode=clone:stop_duration={max(resto, 0) + 1:.2f},"
                f"format=rgba[d];[{n}:v]format=gray[m];[d][m]alphamerge[o]",
                "-map", "[o]", "-t", f"{p['durata']:.3f}", "-c:v", "qtrle", str(din)])
    con_din = lavoro / "con_dinamo.mp4"
    gr._esegui([ff, "-y", "-loglevel", "error", "-i", str(muto), "-i", str(din),
                "-filter_complex", f"[0:v][1:v]overlay={x}:{y}:eof_action=repeat,format=yuv420p[v]",
                "-map", "[v]", "-frames:v", str(n_tot), "-r", str(FPS),
                "-c:v", "libx264", "-profile:v", "main", "-pix_fmt", "yuv420p",
                "-g", str(FPS * 2), "-sc_threshold", "0", "-bf", "0",
                "-preset", "medium", "-crf", "20", str(con_din)])

    # Audio: la macchina vera piena in testa e in coda, sotto la voce in
    # mezzo (come il formato 3), e la voce di HeyGen sopra.
    a = scheda["reel_audio"]
    A, B, durata = SEC_INTRO, p["fine_voce"], p["durata"]
    sotto = grv.VOLUME_SOTTO
    vol = (f"if(lt(t,{A - 0.3:.2f}),1,if(lt(t,{A:.2f}),1-{1 - sotto}*(t-{A - 0.3:.2f})/0.3,"
           f"if(lt(t,{B:.2f}),{sotto},if(lt(t,{B + 0.8:.2f}),{sotto}+{1 - sotto}*(t-{B:.2f})/0.8,1))))")
    mix = lavoro / "mix.wav"
    gr._esegui([ff, "-y", "-loglevel", "error",
                "-stream_loop", "-1", "-ss", str(a.get("inizio", 0)), "-i", str(RADICE / a["file"]),
                "-i", str(c / "voce.wav"),
                "-filter_complex",
                f"[0:a]atrim=0:{durata:.2f},afade=t=in:d=0.01,afade=t=out:st={durata - 0.25:.2f}:d=0.25,"
                f"loudnorm=I=-16:TP=-1.5:LRA=11,volume='{vol}':eval=frame,aformat=sample_rates=44100:channel_layouts=stereo[m];"
                f"[1:a]loudnorm=I=-15:TP=-1.5:LRA=9,aformat=sample_rates=44100:channel_layouts=stereo[v];"
                f"[m][v]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[a]",
                "-map", "[a]", "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le", str(mix)])
    grezzo = lavoro / "grezzo.mp4"
    gr._esegui([ff, "-y", "-loglevel", "error", "-i", str(con_din), "-i", str(mix),
                "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2",
                "-shortest", str(grezzo)])
    finale = out_dir / NOME_FILE
    gr._esegui([ff, "-y", "-loglevel", "error", "-i", str(grezzo), "-c", "copy",
                "-movflags", "+faststart", "-use_editlist", "0", str(finale)])
    shutil.rmtree(lavoro, ignore_errors=True)
    d, problemi = gr.verifica(finale)
    print(f"[reel4] {slug}: {finale.stat().st_size / 1e6:.1f} MB, {durata:.1f} s — "
          + ("OK" if not problemi else "PROBLEMI: " + ", ".join(problemi)))
    if problemi:
        raise SystemExit(1)
    return finale


if __name__ == "__main__":
    cosa, slug = sys.argv[1], sys.argv[2]
    {"piano": piano, "monta": monta, "riascolto": riascolto}[cosa](slug)
