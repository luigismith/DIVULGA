"""ELETTROFONI — prova della sentinella.

Esiste per la regola 10 di CLAUDE.md: «se una verifica non può dire di
no, non è una verifica». Qui i casi sono gli ORARI VERI delle cinque
passate schedulate fra il 27/08 e il 01/09/2026, presi da Actions, con
lo stato che la pagina aveva davvero in quel momento. Su quattro di essi
la vecchia regola apriva una issue: `prova_vecchia_regola_sbagliava` lo
rimette in scena, così la correzione non si può disfare per sbaglio.

    python prova_sentinella.py
"""
import datetime as dt
import re
import pathlib
import sys

import sentinella as S

ROMA = S.ROMA
RADICE = pathlib.Path(__file__).resolve().parent
errori = []


def roma(testo):
    return dt.datetime.fromisoformat(testo).replace(tzinfo=ROMA)


def stato(*iso):
    return [{"slug": f"s{i}", "quando": q, "permalink": "x"} for i, q in enumerate(iso)]


def esito(adesso_roma, pubblicati):
    """(suona, giorno_giudicato) — la decisione della sentinella."""
    giorno = S.giorno_da_controllare(roma(adesso_roma))
    silenzio, _ = S.verdetto(pubblicati, giorno)
    return (silenzio is None or silenzio > 0), giorno


def prova(nome, atteso, ottenuto):
    if atteso != ottenuto:
        errori.append(f"  {nome}\n     atteso {atteso}, ottenuto {ottenuto}")


# Le date sono in UTC come le scrive pubblica.py in stato.json.
DX7 = "2026-08-28T19:51:38+00:00"        # 21:51 italiane del 28
FAIRLIGHT = "2026-08-29T16:18:23+00:00"  # 18:18 italiane del 29
HAMMOND = "2026-08-30T16:01:52+00:00"    # 18:01 italiane del 30
ONDES = "2026-08-31T16:02:51+00:00"      # 18:02 italiane del 31
MELLOTRON = "2026-08-28T01:04:46+00:00"  # 03:04 italiane del 28, di notte

# ---------------------------------------------------------------- 1
# I QUATTRO FALSI ALLARMI VERI. Passata in ritardo, oltre la mezzanotte,
# con la pagina che aveva pubblicato regolarmente. Non deve suonare.
prova("29/08 05:11 (passata del 28 in ritardo di 8h)",
      (False, dt.date(2026, 8, 28)), esito("2026-08-29T05:11", stato(MELLOTRON, DX7)))
prova("30/08 01:24 (passata del 29 in ritardo di 2h)",
      (False, dt.date(2026, 8, 29)), esito("2026-08-30T01:24", stato(DX7, FAIRLIGHT)))
prova("31/08 01:35 (passata del 30 in ritardo di 2h)",
      (False, dt.date(2026, 8, 30)), esito("2026-08-31T01:35", stato(FAIRLIGHT, HAMMOND)))
prova("01/09 02:40 (passata del 31 in ritardo di 3h)",
      (False, dt.date(2026, 9, 1) - dt.timedelta(days=1)),
      esito("2026-09-01T02:40", stato(HAMMOND, ONDES)))

# ---------------------------------------------------------------- 2
# Passata puntuale: stesso verdetto della passata in ritardo.
prova("31/08 23:25 (puntuale, tutto a posto)",
      (False, dt.date(2026, 8, 31)), esito("2026-08-31T23:25", stato(HAMMOND, ONDES)))

# ---------------------------------------------------------------- 3
# IL SILENZIO VERO DEVE ANCORA SUONARE, altrimenti ho spento l'allarme
# invece di ripararlo.
prova("01/09 23:25, ultimo post del 31 → allarme",
      (True, dt.date(2026, 9, 1)), esito("2026-09-01T23:25", stato(HAMMOND, ONDES)))
prova("02/09 03:00, ultimo post del 31 → allarme (recupera la notte saltata)",
      (True, dt.date(2026, 9, 1)), esito("2026-09-02T03:00", stato(HAMMOND, ONDES)))
prova("04/09 23:30, ultimo post del 31 → allarme",
      (True, dt.date(2026, 9, 4)), esito("2026-09-04T23:30", stato(HAMMOND, ONDES)))
prova("stato vuoto → allarme",
      (True, dt.date(2026, 8, 31)), esito("2026-09-01T02:40", []))

# ---------------------------------------------------------------- 4
# Un post pubblicato nel cuore della notte (Mellotron, 03:04 italiane del
# 28) è del 28, non del 27: conta per la sua giornata italiana.
prova("28/08 23:25, post delle 03:04 dello stesso giorno",
      (False, dt.date(2026, 8, 28)), esito("2026-08-28T23:25", stato(MELLOTRON)))

# ---------------------------------------------------------------- 5
# La vecchia regola, rimessa in scena: `oggi = adesso.date()`.
def prova_vecchia_regola_sbagliava():
    casi = [("2026-08-29T05:11", stato(MELLOTRON, DX7)),
            ("2026-08-30T01:24", stato(DX7, FAIRLIGHT)),
            ("2026-08-31T01:35", stato(FAIRLIGHT, HAMMOND)),
            ("2026-09-01T02:40", stato(HAMMOND, ONDES))]
    for quando, pubblicati in casi:
        oggi = roma(quando).date()
        di_oggi = [p for p in pubblicati if S.data_italiana(p["quando"]) == oggi]
        if di_oggi:
            errori.append(f"  la vecchia regola NON sbagliava su {quando}: "
                          "la prova non dimostra più niente")
        if esito(quando, pubblicati)[0]:
            errori.append(f"  la regola nuova sbaglia come la vecchia su {quando}")


prova_vecchia_regola_sbagliava()

# ---------------------------------------------------------------- 6
# FINE_FINESTRA è una copia a mano di pubblica.FINESTRA_ORE[1]: se una
# delle due cambia e l'altra no, la sentinella giudica il giorno
# sbagliato. Si legge dal SORGENTE perché importare `pubblica` qui
# tirerebbe dentro `cryptography`, che nel workflow non c'è.
sorgente = (RADICE / "pubblica.py").read_text(encoding="utf-8")
m = re.search(r"^FINESTRA_ORE\s*=\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)", sorgente, re.M)
if not m:
    errori.append("  non trovo FINESTRA_ORE in pubblica.py: la prova è cieca")
elif int(m.group(2)) != S.FINE_FINESTRA:
    errori.append(f"  FINE_FINESTRA={S.FINE_FINESTRA} ma pubblica.FINESTRA_ORE "
                  f"finisce alle {m.group(2)}: allineare le due")

if errori:
    print("PROVA FALLITA:")
    print("\n".join(errori))
    sys.exit(1)
print("prova sentinella: tutto a posto")
