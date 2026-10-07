# -*- coding: utf-8 -*-
"""
ELETTROFONI — i numeri, per decidere invece di indovinare.

Solo letture. Per ogni contenuto pubblicato raccoglie le metriche che
l'API espone (copertura, visualizzazioni, like, commenti, condivisioni,
salvataggi, follow generati, e per i reel il tempo di visione), poi i
numeri dell'account: follower oggi, follower guadagnati giorno per giorno,
copertura divisa per tipo di contenuto, da dove viene il pubblico.
Scrive metriche/AAAA-MM-GG.json e stampa un riassunto.

LEZIONE GIA' SCRITTA in diagnostica_api.py: i nomi delle metriche cambiano
da una versione dell'API all'altra. Qui si chiede il gruppo intero e, se
viene rifiutato, si richiede una metrica alla volta: una metrica sparita
non deve buttare via tutte le altre. Quelle rifiutate finiscono nel file
sotto "rifiutate", cosi' il buco si vede invece di sembrare uno zero.
"""
import datetime as dt
import json
import pathlib
import sys

import requests

import token_ig

GRAPH = token_ig.GRAPH
RADICE = pathlib.Path(__file__).resolve().parent
CARTELLA = RADICE / "metriche"

# reels_skip_rate (07/10/2026): la quota di visualizzazioni abbandonate
# nei primi 3 secondi. È la cosa che il formato 2 dei reel deve abbassare,
# e la stessa che Instagram usa per decidere se mostrarlo ad altri: senza
# questo numero il cambio di formato non si potrebbe giudicare.
# follows e profile_visits NON ci sono: secondo il riferimento delle
# insights esistono solo per FEED e STORY, e sui 45 reel l'API li ha
# rifiutati tutte le volte (07/10/2026). Chiederli ogni settimana
# produceva solo una riga di «rifiutate» da ignorare.
# reels_skip_rate è «in development»: sui reel del formato 1 non ha dato
# valori. Si tiene perché è il numero che il formato 2 deve abbassare; se
# continua a non rispondere, il riassunto lo dice («None»), non lo nasconde.
METRICHE_REEL = ["reach", "views", "likes", "comments", "shares", "saved",
                 "total_interactions", "ig_reels_avg_watch_time",
                 "ig_reels_video_view_total_time", "reels_skip_rate"]
METRICHE_FEED = ["reach", "views", "likes", "comments", "shares", "saved",
                 "total_interactions", "follows", "profile_visits"]


def _get(percorso, token, **params):
    params["access_token"] = token
    r = requests.get(f"{GRAPH}/{percorso}", params=params, timeout=40)
    try:
        corpo = r.json()
    except ValueError:
        corpo = {"testo": r.text[:300]}
    return r.status_code, corpo


def tutti_i_media(token):
    """Tutti i contenuti dell'account, pagina per pagina."""
    campi = ("id,caption,media_type,media_product_type,permalink,timestamp,"
             "like_count,comments_count")
    media, dopo = [], None
    while True:
        params = {"fields": campi, "limit": 50}
        if dopo:
            params["after"] = dopo
        stato, corpo = _get("me/media", token, **params)
        if stato != 200:
            raise SystemExit(f"me/media: HTTP {stato} — {str(corpo)[:300]}")
        media += corpo.get("data", [])
        dopo = (corpo.get("paging", {}).get("cursors") or {}).get("after")
        if not corpo.get("paging", {}).get("next"):
            return media


def _valori(corpo):
    out = {}
    for d in corpo.get("data", []):
        if d.get("values"):
            out[d["name"]] = d["values"][0].get("value")
        elif "total_value" in d:
            out[d["name"]] = d["total_value"].get("value")
    return out


def insights_media(token, media_id, metriche):
    stato, corpo = _get(f"{media_id}/insights", token, metric=",".join(metriche))
    if stato == 200:
        return _valori(corpo), []
    valori, rifiutate = {}, []
    for m in metriche:
        s1, c1 = _get(f"{media_id}/insights", token, metric=m)
        if s1 == 200:
            valori.update(_valori(c1))
        else:
            rifiutate.append(m)
    return valori, rifiutate


def insights_account(token):
    """Numeri dell'account. Ogni richiesta e' indipendente: se una metrica
    non esiste piu', le altre arrivano lo stesso e il buco resta scritto."""
    oggi = dt.datetime.now(dt.timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    da = int((oggi - dt.timedelta(days=29)).timestamp())
    a = int(oggi.timestamp())
    out, rifiutate = {}, {}

    s, c = _get("me", token, fields="username,followers_count,follows_count,media_count")
    out["profilo"] = c if s == 200 else None

    # follower guadagnati al giorno (l'API li da' solo per gli ultimi 30)
    s, c = _get("me/insights", token, metric="follower_count", period="day", since=da, until=a)
    if s == 200:
        serie = []
        for d in c.get("data", []):
            for v in d.get("values", []):
                serie.append({"giorno": v.get("end_time", "")[:10], "nuovi": v.get("value")})
        out["follower_al_giorno"] = serie
    else:
        rifiutate["follower_count"] = str(c)[:200]

    # copertura e interazioni del periodo, divise per tipo di contenuto
    for metrica, rottura in (("reach", "media_product_type"),
                             ("views", "media_product_type"),
                             ("total_interactions", "media_product_type"),
                             ("accounts_engaged", None),
                             ("profile_links_taps", None)):
        params = {"metric": metrica, "period": "day", "metric_type": "total_value",
                  "since": da, "until": a}
        if rottura:
            params["breakdown"] = rottura
        s, c = _get("me/insights", token, **params)
        if s == 200:
            out[metrica] = c.get("data", [])
        else:
            rifiutate[metrica] = str(c)[:200]

    # da dove vengono i follower (l'API risponde solo sopra i 100 follower)
    for rottura in ("country", "city", "age", "gender"):
        s, c = _get("me/insights", token, metric="follower_demographics",
                    period="lifetime", metric_type="total_value", breakdown=rottura)
        if s == 200:
            out[f"demografia_{rottura}"] = c.get("data", [])
        else:
            rifiutate[f"demografia_{rottura}"] = str(c)[:200]

    out["rifiutate"] = rifiutate
    return out


def slug_per_media():
    """media_id -> (slug, 'carosello'|'reel'|'reel2') da stato.json.
    'reel2' è il formato 2 (dal 07/10/2026): tenerli separati è tutto il
    punto, perché il confronto fra i due formati decide se il cambio ha
    funzionato."""
    stato = json.loads((RADICE / "stato.json").read_text())
    mappa = {}
    for p in stato.get("pubblicati", []):
        if p.get("media_id"):
            mappa[p["media_id"]] = (p["slug"], "carosello")
    for r in stato.get("reel", []):
        ruolo = "reel2" if r.get("formato", 1) == 2 else "reel"
        if r.get("media_id"):
            mappa[r["media_id"]] = (r["slug"], ruolo)
        elif r.get("permalink"):
            # Voce aggiunta a mano senza media_id (07/10/2026, Novachord):
            # la si riconosce dal permalink.
            mappa[r["permalink"]] = (r["slug"], ruolo)
    return mappa


def riassunto(dati):
    acc = dati["account"]
    prof = acc.get("profilo") or {}
    print("=" * 72)
    print(f"follower oggi: {prof.get('followers_count')}   contenuti: {prof.get('media_count')}")
    serie = acc.get("follower_al_giorno") or []
    if serie:
        tot = sum(x["nuovi"] or 0 for x in serie)
        print(f"follower guadagnati negli ultimi {len(serie)} giorni: {tot}")
        print("  " + " ".join(f"{x['giorno'][5:]}:{x['nuovi']}" for x in serie[-14:]))
    print("=" * 72)
    for tipo in ("REELS", "FEED"):
        righe = [m for m in dati["media"] if m.get("media_product_type") == tipo]
        if not righe:
            continue
        righe.sort(key=lambda m: m["insights"].get("reach") or 0, reverse=True)
        n = len(righe)
        def media_di(k):
            vals = [m["insights"].get(k) for m in righe if m["insights"].get(k) is not None]
            return sum(vals) / len(vals) if vals else None
        print(f"\n{tipo}: {n} contenuti — copertura media {media_di('reach')}, "
              f"condivisioni medie {media_di('shares')}, salvataggi medi {media_di('saved')}, "
              f"follow medi {media_di('follows')}")
        if tipo == "REELS":
            print(f"  tempo medio di visione (ms): {media_di('ig_reels_avg_watch_time')}")
        print("  i migliori per copertura:")
        for m in righe[:10]:
            i = m["insights"]
            print(f"    {str(m.get('slug')):16} reach={i.get('reach')} views={i.get('views')} "
                  f"cond={i.get('shares')} salv={i.get('saved')} like={i.get('likes')} "
                  f"comm={i.get('comments')} follow={i.get('follows')} "
                  f"visione_ms={i.get('ig_reels_avg_watch_time')}")
        print("  i peggiori:")
        for m in righe[-5:]:
            i = m["insights"]
            print(f"    {str(m.get('slug')):16} reach={i.get('reach')} views={i.get('views')} "
                  f"cond={i.get('shares')} salv={i.get('saved')}")
    # Il confronto che conta: formato 1 contro formato 2, stesse metriche.
    print("\nREEL PER FORMATO (mediane):")
    for ruolo, nome in (("reel", "formato 1"), ("reel2", "formato 2")):
        g = [m["insights"] for m in dati["media"] if m.get("ruolo") == ruolo]
        if not g:
            print(f"  {nome}: nessun reel"); continue
        def med(k):
            v = sorted(x[k] for x in g if x.get(k) is not None)
            return v[len(v) // 2] if v else None
        cond = [x["shares"] / x["reach"] for x in g if x.get("reach") and x.get("shares") is not None]
        per100 = f"{100 * sum(cond) / len(cond):.2f}" if cond else "n.d."
        print(f"  {nome}: {len(g)} reel — copertura {med('reach')}, "
              f"visione_ms {med('ig_reels_avg_watch_time')}, "
              f"abbandono<3s {med('reels_skip_rate')}, condivisioni {med('shares')}, "
              f"condivisioni per 100 raggiunti {per100}")
    if acc.get("rifiutate"):
        print("\nmetriche dell'account rifiutate dall'API:", ", ".join(acc["rifiutate"]))


def main():
    token, rinnovato = token_ig.token_corrente()
    print(f"[metriche] token {token_ig.redigi(token)}{' (rinnovato)' if rinnovato else ''}")
    mappa = slug_per_media()
    media = tutti_i_media(token)
    print(f"[metriche] {len(media)} contenuti sull'account")
    righe = []
    for m in media:
        tipo = m.get("media_product_type")
        if tipo not in ("REELS", "FEED"):
            continue
        metriche = METRICHE_REEL if tipo == "REELS" else METRICHE_FEED
        valori, rifiutate = insights_media(token, m["id"], metriche)
        slug, ruolo = mappa.get(m["id"]) or mappa.get(m.get("permalink"), (None, None))
        righe.append({
            "id": m["id"], "slug": slug, "ruolo": ruolo,
            "media_type": m.get("media_type"), "media_product_type": tipo,
            "timestamp": m.get("timestamp"), "permalink": m.get("permalink"),
            "like_count": m.get("like_count"), "comments_count": m.get("comments_count"),
            "insights": valori, "rifiutate": rifiutate,
        })
    dati = {
        "raccolta": dt.datetime.now(dt.timezone.utc).isoformat(),
        "account": insights_account(token),
        "media": righe,
    }
    CARTELLA.mkdir(exist_ok=True)
    nome = CARTELLA / f"{dt.date.today().isoformat()}.json"
    nome.write_text(json.dumps(dati, indent=1, ensure_ascii=False) + "\n")
    print(f"[metriche] scritto {nome.relative_to(RADICE)}")
    riassunto(dati)


if __name__ == "__main__":
    sys.exit(main())
