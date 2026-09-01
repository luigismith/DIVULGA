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
guarda il risultato in `stato.json`. Non gli interessa il perché.

------------------------------------------------------------------------
LEZIONE IMPARATA (01/09/2026) — LA SENTINELLA HA GRIDATO AL LUPO PER
QUATTRO NOTTI DI FILA, E OGNI VOLTA SI SBAGLIAVA.

Issue #1, #2, #3, #4: tutte false. La pagina aveva pubblicato
regolarmente ogni giorno. Cinque passate schedulate, cinque partite in
ritardo, NESSUNA all'ora prevista:

    schedulata 21:25 UTC   partita          ora italiana    esito
    27/08                  28/08 05:28 UTC  07:28 del 28    passata per caso
    28/08                  29/08 03:11 UTC  05:11 del 29    FALSO ALLARME
    29/08                  29/08 23:24 UTC  01:24 del 30    FALSO ALLARME
    30/08                  30/08 23:35 UTC  01:35 del 31    FALSO ALLARME
    31/08                  01/09 00:40 UTC  02:40 del  1    FALSO ALLARME

La causa è una riga sola: `oggi = datetime.now(ROMA).date()`. La
sentinella chiedeva «è uscito qualcosa OGGI?» usando l'orologio del
momento in cui gira. Ma girava dopo mezzanotte, quando «oggi» era un
giorno appena cominciato in cui ovviamente non era ancora uscito niente.
Non poteva che dare allarme: era una domanda a cui esisteva una sola
risposta.

L'errore vero è più profondo del fuso. È aver dato per buono che una
cosa parta quando è schedulata — nel progetto che ha già scritto, in
CLAUDE.md e nella finestra oraria di `pubblica.py`, che il cron di GitHub
arriva ore dopo o non arriva. La lezione era già stata imparata per chi
pubblica e non l'ho applicata a chi controlla.

REGOLA: un allarme non deve MAI dedurre di che giorno parla dall'ora in
cui si sveglia. Deve dedurlo dal calendario del lavoro che sorveglia —
qui: l'ultima giornata la cui finestra di pubblicazione è già chiusa.
Così la stessa passata dà lo stesso verdetto che parta alle 23:25, alle
2 di notte o alle 7 del mattino.

COROLLARIO: un allarme che si sbaglia è peggio di nessun allarme. Dopo
quattro notti di rosso ingiustificato il proprietario smette di aprire
le issue — e la sentinella esiste proprio per bucare il silenzio.
------------------------------------------------------------------------
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

# Copia dichiarata di pubblica.FINESTRA_ORE[1]: dopo quest'ora italiana
# la giornata editoriale è chiusa e o è uscito qualcosa o non uscirà più.
# NON si importa `pubblica` perché si tira dietro `cryptography`, che in
# questo workflow non è installato (qui si fa solo `pip install requests`).
# Che le due restino allineate lo verifica `prova_sentinella.py`, che
# legge il numero dal sorgente di pubblica.py senza importarlo.
FINE_FINESTRA = 23


def data_italiana(iso):
    """La data del post nel fuso in cui vive la pagina, non in UTC.
    Un post delle 00:30 italiane è del giorno prima in UTC: contarlo nel
    giorno sbagliato farebbe scattare un falso allarme."""
    return dt.datetime.fromisoformat(iso).astimezone(ROMA).date()


def giorno_da_controllare(adesso=None):
    """L'ultima giornata la cui finestra di pubblicazione è già chiusa.

    Questa funzione è il cuore della correzione del 01/09/2026: NON
    risponde «oggi», risponde «l'ultimo giorno su cui ha senso avere un
    giudizio». Prima delle 23 italiane la giornata in corso può ancora
    pubblicare, quindi il giorno da giudicare è quello prima; dalle 23 in
    poi la finestra di oggi è chiusa e oggi è giudicabile.

    Conseguenza voluta: il ritardo del cron diventa innocuo. Una passata
    delle 02:40 e una delle 23:25 parlano della stessa giornata.
    """
    adesso = adesso or dt.datetime.now(ROMA)
    if adesso.hour >= FINE_FINESTRA:
        return adesso.date()
    return adesso.date() - dt.timedelta(days=1)


def issue_gia_aperta(titolo):
    """Non ripetere lo stesso allarme: se la issue di quel giorno c'è già
    (passata rilanciata a mano, doppione del cron), si tace."""
    tok = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not (tok and repo):
        return False
    try:
        r = requests.get(
            f"https://api.github.com/repos/{repo}/issues",
            headers={"Authorization": f"Bearer {tok}"},
            params={"state": "open", "labels": "pubblicazione", "per_page": 100},
            timeout=30,
        )
        r.raise_for_status()
        return any(i.get("title") == titolo for i in r.json())
    except Exception as e:
        # Se non riesco a controllare, preferisco un doppione al silenzio.
        print(f"[warn] non ho potuto cercare doppioni: {e}")
        return False


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


def verdetto(pubblicati, giorno):
    """(silenzio_da_giorni, ultimo_post). 0 giorni = tutto a posto.

    Si confronta la data dell'ULTIMO post con il giorno da controllare,
    invece di chiedere «esiste un post con questa data esatta». Così la
    sentinella recupera anche i propri buchi: se una notte la sua passata
    viene scartata e riparte la notte dopo, vede comunque che l'ultimo
    post è di due giorni fa e suona.
    """
    datati = [p for p in pubblicati if p.get("quando")]
    if not datati:
        return (None, None)
    ultimo = max(datati, key=lambda p: p["quando"])
    return ((giorno - data_italiana(ultimo["quando"])).days, ultimo)


def main():
    adesso = dt.datetime.now(ROMA)
    giorno = giorno_da_controllare(adesso)
    stato = json.loads(FILE_STATO.read_text()) if FILE_STATO.exists() else {"pubblicati": []}
    pubblicati = stato.get("pubblicati", [])

    silenzio, ultimo = verdetto(pubblicati, giorno)
    print(f"[sentinella] ora italiana {adesso:%Y-%m-%d %H:%M}, giudico il giorno {giorno}")

    if silenzio is not None and silenzio <= 0:
        print(f"[ok] il {giorno} è uscito «{ultimo['slug']}»: nessun allarme")
        return

    if ultimo:
        coda = (f"L'ultimo post è «{ultimo['slug']}» del "
                f"{data_italiana(ultimo['quando'])}, cioè {silenzio} giorn"
                f"{'o' if silenzio == 1 else 'i'} prima del {giorno}: "
                f"{ultimo.get('permalink', '(senza permalink)')}")
    else:
        coda = "Non risulta nessun post pubblicato, mai."

    titolo = f"🔴 ELETTROFONI: il {giorno} non è uscito niente"
    if issue_gia_aperta(titolo):
        print("[ok] allarme già aperto per questo giorno: non ne apro un altro")
        raise SystemExit(1)

    apri_issue(
        titolo,
        f"La sentinella non trova nessun post del **{giorno}** in `stato.json`.\n\n"
        f"{coda}\n\n"
        f"(Passata delle {adesso:%H:%M} italiane. Il giorno giudicato è "
        "l'ultimo con la finestra di pubblicazione già chiusa, non «oggi»: "
        "il cron può arrivare in piena notte e il verdetto non deve "
        "cambiare per questo.)\n\n"
        "Da guardare **in quest'ordine**:\n"
        f"1. In Actions **esiste** un run di «Pubblica scheda» del {giorno}? "
        "Se non esiste, l'innesco è saltato: non c'è niente da riparare, "
        "si rilancia a mano con «Run workflow».\n"
        "2. Se esiste ed è fallito, leggere i log del passo che ha ceduto.\n"
        "3. Se esiste ed è riuscito ma il post non c'è, il problema è "
        "sull'API di Instagram: NON rilanciare in loop, fermarsi e capire.\n",
    )
    raise SystemExit(1)


if __name__ == "__main__":
    main()
