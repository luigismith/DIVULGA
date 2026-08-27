"""ELETTROFONI — la sentinella del silenzio.

PERCHÉ ESISTE (27/08/2026). Quel giorno alle 18:00 non è uscito niente e
in GitHub Actions non c'era nessun run fallito da guardare: non c'era
proprio nessun run. Il cron di GitHub è "best effort" e nei momenti di
carico un evento schedulato può essere scartato del tutto, in silenzio.

Tutti gli allarmi che avevamo si accorgevano di una PUBBLICAZIONE ANDATA
MALE. Nessuno si accorgeva di una PUBBLICAZIONE MAI TENTATA — che è
esattamente il modo in cui è morta la pagina precedente: nove giorni di
niente, senza un solo errore da nessuna parte.

Questo controllo è rovesciato rispetto agli altri: non guarda i run,
guarda il risultato. Se stasera in `stato.json` non c'è un post con la
data di oggi, apre una issue. Non gli interessa il perché.

Da solo non basta e va detto: anche questo gira su un cron, quindi anche
lui può essere scartato. Per questo la difesa vera restano le tre passate
di `pubblica.yml` (17:50, 18:35, 21:40): perché la giornata salti davvero
devono essere scartate tutte e tre, che è molto meno probabile di una.
La sentinella serve a non farcelo scoprire dal proprietario.
"""
import datetime as dt
import json
import os
import pathlib
import zoneinfo

import requests

RADICE = pathlib.Path(__file__).resolve().parent
FILE_STATO = RADICE / "stato.json"
ROMA = zoneinfo.ZoneInfo("Europe/Rome")


def data_italiana(iso):
    """La data del post nel fuso in cui vive la pagina, non in UTC.
    Un post delle 00:30 italiane è del giorno prima in UTC: contarlo nel
    giorno sbagliato farebbe scattare un falso allarme."""
    return dt.datetime.fromisoformat(iso).astimezone(ROMA).date()


def apri_issue(titolo, corpo):
    tok = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not (tok and repo):
        print("[warn] niente token o repo: issue non aperta")
        return
    r = requests.post(
        f"https://api.github.com/repos/{repo}/issues",
        headers={"Authorization": f"Bearer {tok}"},
        json={"title": titolo, "body": corpo, "labels": ["pubblicazione"]},
        timeout=30,
    )
    print(f"[issue] HTTP {r.status_code}")


def main():
    oggi = dt.datetime.now(ROMA).date()
    stato = json.loads(FILE_STATO.read_text()) if FILE_STATO.exists() else {"pubblicati": []}
    pubblicati = stato.get("pubblicati", [])

    di_oggi = [p for p in pubblicati if p.get("quando") and data_italiana(p["quando"]) == oggi]
    if di_oggi:
        print(f"[ok] oggi {oggi} è uscito: {', '.join(p['slug'] for p in di_oggi)}")
        return

    ultimo = pubblicati[-1] if pubblicati else None
    if ultimo:
        giorni = (oggi - data_italiana(ultimo["quando"])).days
        coda = (f"L'ultimo post è «{ultimo['slug']}» di {giorni} giorn"
                f"{'o' if giorni == 1 else 'i'} fa: {ultimo.get('permalink', '(senza permalink)')}")
    else:
        coda = "Non risulta nessun post pubblicato, mai."

    apri_issue(
        f"🔴 ELETTROFONI: oggi {oggi} non è uscito niente",
        "La sentinella serale non trova nessun post con la data di oggi "
        f"in `stato.json`.\n\n{coda}\n\n"
        "Da guardare **in quest'ordine**:\n"
        "1. In Actions **esiste** un run di «Pubblica scheda» di oggi? "
        "Se non esiste, il cron è stato scartato da GitHub: non c'è niente "
        "da riparare, si rilancia a mano con «Run workflow».\n"
        "2. Se esiste ed è fallito, leggere i log del passo che ha ceduto.\n"
        "3. Se esiste ed è riuscito ma il post non c'è, il problema è "
        "sull'API di Instagram: NON rilanciare in loop, fermarsi e capire.\n",
    )
    raise SystemExit(1)


if __name__ == "__main__":
    main()
