# -*- coding: utf-8 -*-
"""ELETTROFONI — che cosa esce oggi: il post o il reel.

Decisioni del proprietario, 15/11/2026:
  «Uno strumento al giorno è troppo» → le schede nuove escono lunedì,
  mercoledì e venerdì alle 18;
  «Facciamo che nei giorni in cui non esce il post esce il reel» → martedì,
  giovedì e sabato alle 18 esce il reel della scheda uscita il giorno
  prima, la domenica alle 18 il reel HeyGen sulla scheda andata meglio
  (uno a settimana, non più due). I rifacimenti delle 12:30 si fermano.
Un'uscita al giorno, sempre alle 18: chi ci segue sa quando guardare.

Gli inneschi restano quotidiani (cron-job.org alle 18 chiama
pubblica.yml, più i cron di GitHub): è questo file che dice a pubblica.yml
se oggi tocca al post o al reel, e a reel.yml quale reel. Un solo posto
per la regola, così pubblica.py, sentinella.py e pubblica_reel.py non
possono andare in disaccordo (prima della sentinella c'era una copia a
mano dei giorni, controllata da una prova: ora non serve).

Qui niente import pesanti: la sentinella gira con il solo `requests`.

    python calendario.py        # stampa «post» o «reel» per oggi
"""
import datetime as dt
import json
import pathlib
import zoneinfo

ROMA = zoneinfo.ZoneInfo("Europe/Rome")
RADICE = pathlib.Path(__file__).resolve().parent

GIORNI_USCITA = (0, 2, 4)   # lunedì, mercoledì, venerdì (0 = lunedì)
GIORNO_HEYGEN = 6           # domenica


def data_italiana(iso):
    return dt.datetime.fromisoformat(iso).astimezone(ROMA).date()


def ultimo_giorno_uscita(giorno, giorni=GIORNI_USCITA):
    """Il giorno d'uscita più recente, `giorno` compreso."""
    while giorno.weekday() not in giorni:
        giorno -= dt.timedelta(days=1)
    return giorno


def oggi_si_pubblica(pubblicati, oggi):
    """Vero nei giorni d'uscita, e nei giorni da reel SOLO per recuperare
    un giorno d'uscita rimasto senza post (un lunedì saltato esce martedì,
    non mercoledì insieme alla scheda del mercoledì). Quel giorno il reel
    slitta: un'uscita al giorno."""
    if oggi.weekday() in GIORNI_USCITA:
        return True
    previsto = ultimo_giorno_uscita(oggi)
    return not any(data_italiana(x["quando"]) >= previsto for x in pubblicati)


def reel_di_oggi(stato, oggi):
    """Gli slug dei reel già usciti oggi (fuso di Roma)."""
    return [r["slug"] for r in stato.get("reel", [])
            if r.get("quando") and data_italiana(r["quando"]) == oggi]


def cosa_oggi(stato, oggi=None):
    oggi = oggi or dt.datetime.now(ROMA).date()
    return "post" if oggi_si_pubblica(stato.get("pubblicati", []), oggi) else "reel"


def leggi_stato():
    f = RADICE / "stato.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {"pubblicati": []}


if __name__ == "__main__":
    print(cosa_oggi(leggi_stato()))
