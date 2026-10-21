# -*- coding: utf-8 -*-
"""ELETTROFONI — il reel PARLATO («formato 3», prototipo del 21/10/2026).

PERCHÉ. Il proprietario ha chiesto «reels parlanti (con voce sintetica)
e animati con la mascotte di elettrofoni che racconta (in un angolo)
mentre le slide scorrono», con strumenti gratuiti e senza fare niente
lui. Questo file costruisce quel reel. NON è collegato ai workflow: è
una prova, da giudicare sui numeri contro il formato 2 (CLAUDE.md, «I
numeri»: una modifica al reel si giudica sulle metriche, non a occhio).

COM'È FATTO. Le scene sono quelle del formato 2 (genera_reel.py: foto che
si muove, pannello con la battuta, targhetta), con tre differenze:
  · ogni scena dura quanto Dinamo impiega a DIRE la sua frase
    (`reel_voce`: per ogni battuta una frase un po' più piena dello
    stesso fatto, poi la CTA e la chiusura), non quanto serve a leggerla;
  · Dinamo sta in basso a sinistra, accanto alla targhetta, e muove la
    bocca sull'inviluppo della voce (dinamo.py); la targhetta si sposta
    a destra per fargli posto;
  · l'audio: SEC_INTRO secondi di sola macchina (il gancio resta il suono
    vero, regola del 17/10), poi la voce con la macchina sotto a volume
    ridotto, e SEC_OUTRO secondi di sola macchina in chiusura.
La voce è voce.py (motore scelto lì); prima di consegnare il file la
voce viene RIASCOLTATA da Whisper (voce.verifica): se un nome esce
storpiato il reel non si costruisce. Una verifica che non può dire di no
non è una verifica (regola 10).

Le specifiche del file sono le stesse del formato 2 (vedi genera_reel.py).

    python genera_reel_voce.py cz101 <cartella> [--testo frasi.json]
"""
import json
import os
import pathlib
import subprocess
import sys
import wave

import numpy as np

import contenuti
import genera_reel as gr
import genera_tavole as gt

RADICE = pathlib.Path(__file__).resolve().parent
FPS = gr.FPS
SEC_INTRO = 2.5            # sola macchina, col gancio già sullo schermo
SEC_OUTRO = 3.0            # sola macchina, con la CTA sullo schermo
SEC_PAUSA = 0.4            # fra una frase e l'altra
SEC_PAUSA_CTA = 0.3        # fra la CTA e «le slide e le fonti…»
VOLUME_SOTTO = 0.22        # la macchina sotto la voce (≈ -13 dB)
SR_VOCE = 24000
# Dinamo: 280 px nel disegno a 1080, in basso a sinistra, col bordo
# inferiore allineato alla targhetta (bottom:440px in genera_reel._css).
DINAMO_PX = 280
DINAMO_X = 64
DINAMO_BOTTOM = 440
TAG_LEFT = DINAMO_X + DINAMO_PX + 24
NOME_FILE = "reel3.mp4"


def frasi_di(scheda, file_testo=None):
    """Le frasi che Dinamo dice: dal JSON della prova o da `reel_voce`
    della scheda. Ogni voce ha «detta» (per il TTS) e «scritta» (per il
    controllo con Whisper). Niente ripiego sulle battute: una frase che
    manca è un errore, non un reel un po' più muto."""
    if file_testo:
        dati = json.loads(pathlib.Path(file_testo).read_text(encoding="utf-8"))
        frasi = dati["frasi"]
    else:
        frasi = scheda.get("reel_voce")
    if not frasi:
        raise ValueError(f"la scheda '{scheda['slug']}' non ha reel_voce")
    ruoli = [f["ruolo"] for f in frasi]
    attesi = [f"battuta{i}" for i in range(1, len(scheda["reel_battute"]) + 1)] + ["cta", "chiusura"]
    if ruoli != attesi:
        raise ValueError(f"ruoli delle frasi {ruoli}, attesi {attesi}")
    return frasi


def _wav_standard(src, dst, ff):
    """Tutti i pezzi di voce nello stesso formato (mono, SR_VOCE, 16 bit),
    così si incollano con numpy senza sorprese."""
    gr._esegui([ff, "-y", "-loglevel", "error", "-i", str(src),
                "-ar", str(SR_VOCE), "-ac", "1", "-c:a", "pcm_s16le", str(dst)])
    with wave.open(str(dst)) as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)


def _scrivi_wav(dst, campioni):
    with wave.open(str(dst), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR_VOCE)
        w.writeframes(campioni.astype(np.int16).tobytes())


def costruisci(scheda, cartella, file_testo=None):
    import dinamo
    import voce
    from playwright.sync_api import sync_playwright

    cartella = pathlib.Path(cartella)
    cartella.mkdir(parents=True, exist_ok=True)
    lavoro = cartella / "_reel3"
    lavoro.mkdir(exist_ok=True)
    ff = gr._ff()

    frasi = frasi_di(scheda, file_testo)
    scene = gr.battute(scheda)          # html, foto e moto come nel formato 2
    n_batt = len(scheda["reel_battute"])

    # 1. La voce, una frase per volta: la durata di ogni frase decide la
    #    durata della sua scena.
    pezzi = []
    for i, f in enumerate(frasi):
        grezzo = lavoro / f"v{i}_grezzo.wav"
        voce.sintetizza(f["detta"], grezzo)
        pezzi.append(_wav_standard(grezzo, lavoro / f"v{i}.wav", ff))
    durate = [len(p) / SR_VOCE for p in pezzi]

    # 2. La linea del tempo. Scena k (k < n_batt): la frase k più la
    #    pausa; la prima ha davanti l'intro; l'ultima scena ha CTA,
    #    chiusura e l'outro.
    inizi = []          # quando parte ogni frase, in secondi
    sec_scene = []
    t = SEC_INTRO
    for k in range(n_batt):
        inizi.append(t)
        d = durate[k] + SEC_PAUSA
        sec_scene.append((SEC_INTRO if k == 0 else 0) + d)
        t += d
    inizi.append(t)                                  # cta
    t += durate[n_batt] + SEC_PAUSA_CTA
    inizi.append(t)                                  # chiusura
    t += durate[n_batt + 1] + SEC_PAUSA
    fine_voce = t
    sec_scene.append(durate[n_batt] + SEC_PAUSA_CTA + durate[n_batt + 1] + SEC_PAUSA + SEC_OUTRO)
    durata = sum(sec_scene)

    # 3. La traccia della voce intera, e il suo controllo con Whisper.
    totale = np.zeros(int(round(durata * SR_VOCE)), dtype=np.int16)
    for ini, p in zip(inizi, pezzi):
        a = int(round(ini * SR_VOCE))
        totale[a:a + len(p)] = p[:len(totale) - a]
    voce_wav = lavoro / "voce.wav"
    _scrivi_wav(voce_wav, totale)
    atteso = " ".join(f["scritta"] for f in frasi)
    wer, mancanti = voce.verifica(voce_wav, atteso)
    print(f"[reel3] voce: {fine_voce - SEC_INTRO:.1f} s di parlato, WER {wer:.2f}"
          + (f", parole non riconosciute: {mancanti}" if mancanti else ""))
    if mancanti or wer > voce.WER_MAX:
        raise RuntimeError(f"Dinamo non si capisce (WER {wer:.2f}, mancano {mancanti}): "
                           "correggere il lessico in voce.py o la frase")

    # 4. Le scene video, come nel formato 2 ma con la targhetta spostata
    #    a destra per far posto a Dinamo. Lo <style> dentro il body vale.
    foto = contenuti.foto_del_reel(scheda)
    png = []
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get("ELETTROFONI_CHROMIUM"),
                              args=["--no-sandbox", "--force-color-profile=srgb"])
        pg = b.new_page(viewport={"width": gr.L, "height": gr.H})
        for i, sc in enumerate(scene):
            tmp = lavoro / f"t{i}.html"
            tmp.write_text(gr._pagina(f"<style>.tag{{left:{TAG_LEFT}px}}</style>" + sc["html"]),
                           encoding="utf-8")
            pg.goto(tmp.as_uri())
            pg.wait_for_selector("body[data-pronto='1']", timeout=20000)
            if pg.evaluate("document.body.dataset.troppo") == "1":
                raise RuntimeError(f"battuta {i + 1} troppo lunga anche a 44px: accorciarla")
            f = lavoro / f"t{i}.png"
            pg.screenshot(path=str(f), omit_background=True)
            png.append(f)
        b.close()

    clip = []
    for i, sc in enumerate(scene):
        n = round(sec_scene[i] * FPS)
        f = foto[sc["foto"] % len(foto)]
        c = lavoro / f"c{i}.mp4"
        gr._esegui([ff, "-y", "-loglevel", "error",
                    "-noautorotate", "-i", str(RADICE / f["file"]),
                    "-loop", "1", "-framerate", str(FPS), "-i", str(png[i]),
                    "-filter_complex", gr._filtro(f, sc["moto"], n)
                    + f";[v1]scale={gr.LARG}:{gr.ALT},setsar=1,format=yuv420p[o]",
                    "-map", "[o]", "-frames:v", str(n), "-r", str(FPS),
                    "-c:v", "libx264", "-profile:v", "main", "-pix_fmt", "yuv420p",
                    "-g", str(FPS * 2), "-sc_threshold", "0", "-bf", "0",
                    "-preset", "medium", "-crf", "20", str(c)])
        clip.append(c)
    elenco = lavoro / "elenco.txt"
    elenco.write_text("".join(f"file '{c.name}'\n" for c in clip))
    muto = lavoro / "muto.mp4"
    gr._esegui([ff, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                "-i", str(elenco), "-c", "copy", str(muto)])
    n_tot = sum(round(s * FPS) for s in sec_scene)

    # 5. Dinamo sopra, con la bocca sulla voce. Misure portate dalla
    #    scala del disegno (1080) a quella del file (720).
    k = gr.LARG / gr.L
    dpx = int(round(DINAMO_PX * k / 2)) * 2
    dx = int(round(DINAMO_X * k))
    dy = int(round((gr.H - DINAMO_BOTTOM - DINAMO_PX) * k))
    pattern = dinamo.sequenza(voce_wav, FPS, n_tot / FPS, SEC_INTRO, lavoro / "dinamo")
    con_dinamo = lavoro / "con_dinamo.mp4"
    gr._esegui([ff, "-y", "-loglevel", "error", "-i", str(muto),
                "-framerate", str(FPS), "-i", str(pattern),
                "-filter_complex",
                f"[1:v]scale={dpx}:{dpx}[d];"
                f"[0:v][d]overlay={dx}:'{dy}+4*sin(2*PI*t/2.6)':eof_action=pass,format=yuv420p[v]",
                "-map", "[v]", "-frames:v", str(n_tot), "-r", str(FPS),
                "-c:v", "libx264", "-profile:v", "main", "-pix_fmt", "yuv420p",
                "-g", str(FPS * 2), "-sc_threshold", "0", "-bf", "0",
                "-preset", "medium", "-crf", "20", str(con_dinamo)])

    # 6. L'audio: la macchina vera per tutta la durata, piena nell'intro
    #    e nell'outro, sotto la voce in mezzo; la voce sopra.
    a = scheda.get("reel_audio")
    if not a:
        raise RuntimeError(f"{scheda['slug']} non ha reel_audio: il reel parlato vuole la macchina vera")
    A, B = SEC_INTRO, fine_voce
    vol = (f"if(lt(t,{A - 0.3:.2f}),1,"
           f"if(lt(t,{A:.2f}),1-{1 - VOLUME_SOTTO}*(t-{A - 0.3:.2f})/0.3,"
           f"if(lt(t,{B:.2f}),{VOLUME_SOTTO},"
           f"if(lt(t,{B + 0.8:.2f}),{VOLUME_SOTTO}+{1 - VOLUME_SOTTO}*(t-{B:.2f})/0.8,1))))")
    mix = lavoro / "mix.wav"
    gr._esegui([ff, "-y", "-loglevel", "error",
                "-stream_loop", "-1", "-ss", str(a.get("inizio", 0)), "-i", str(RADICE / a["file"]),
                "-i", str(voce_wav),
                "-filter_complex",
                f"[0:a]atrim=0:{durata:.2f},afade=t=in:d=0.01,afade=t=out:st={durata - 0.25:.2f}:d=0.25,"
                f"loudnorm=I=-16:TP=-1.5:LRA=11,volume='{vol}':eval=frame,aformat=sample_rates=44100:channel_layouts=stereo[m];"
                f"[1:a]loudnorm=I=-15:TP=-1.5:LRA=9,aformat=sample_rates=44100:channel_layouts=stereo[v];"
                f"[m][v]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[a]",
                "-map", "[a]", "-ar", "44100", "-ac", "2", "-c:a", "pcm_s16le", str(mix)])

    grezzo = lavoro / "grezzo.mp4"
    gr._esegui([ff, "-y", "-loglevel", "error", "-i", str(con_dinamo), "-i", str(mix),
                "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2",
                "-shortest", str(grezzo)])
    finale = cartella / NOME_FILE
    gr._esegui([ff, "-y", "-loglevel", "error", "-i", str(grezzo), "-c", "copy",
                "-movflags", "+faststart", "-use_editlist", "0", str(finale)])
    print(f"[reel3] scene: " + " + ".join(f"{s:.1f}" for s in sec_scene) + f" = {durata:.1f} s")
    return finale


if __name__ == "__main__":
    argv = sys.argv[1:]
    file_testo = None
    if "--testo" in argv:
        i = argv.index("--testo")
        file_testo = argv[i + 1]
        del argv[i:i + 2]
    slug = argv[0] if argv else "cz101"
    cartella = argv[1] if len(argv) > 1 else RADICE / "docs" / "tavole" / slug
    scheda = next((s for s in contenuti.SCHEDE if s["slug"] == slug), None)
    if scheda is None:
        print(f"nessuna scheda '{slug}'"); raise SystemExit(1)
    out = costruisci(scheda, cartella, file_testo)
    d, problemi = gr.verifica(out)
    print(f"[reel3] {slug}: {out.stat().st_size / 1e6:.1f} MB — "
          + ("OK" if not problemi else "PROBLEMI: " + ", ".join(problemi)))
    if problemi:
        print(d)
        raise SystemExit(1)
