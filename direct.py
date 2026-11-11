# -*- coding: utf-8 -*-
"""ELETTROFONI — conta i messaggi diretti nuovi (sola lettura).

I DIRECT NON SI STAMPANO (11/11/2026, il proprietario: «si vedono i
direct sulla repo. non va bene»). Il repo è pubblico, e i log di GitHub
Actions di un repo pubblico li legge chiunque: dal 16/10 ogni lettura
scriveva nel log chi ci aveva scritto e cosa. Un messaggio privato
mandato a noi non deve finire in una pagina pubblica, e nemmeno il nome
di chi l'ha mandato. I log di quelle letture sono stati cancellati.

Ora questo script stampa solo DUE NUMERI: quante conversazioni hanno
messaggi arrivati da altri nelle ultime N ore, e quanti messaggi sono.
Niente nomi, niente testo, niente id. I direct si leggono dall'app; la
sessione di presidio dice al proprietario quanti ne sono arrivati.

Regola per chiunque tocchi questo file: nel log di un repo pubblico va
solo quello che si potrebbe mettere in un post. Se serve leggere il
contenuto, NON si stampa: si chiede al proprietario.

Serve il permesso instagram_business_manage_messages sul token; se
manca, l'API lo dice nell'errore e si stampa solo il codice, non il
corpo (che potrebbe contenere dati della conversazione).
"""
import sys
from datetime import datetime, timedelta, timezone

import token_ig
from pubblica import api


def main():
    ore = int(sys.argv[1]) if len(sys.argv) > 1 else 26
    token, _ = token_ig.token_corrente()
    io = api("GET", "me", token, fields="username").get("username")
    try:
        conv = api("GET", "me/conversations", token, platform="instagram",
                   fields="updated_time,messages.limit(20){from,created_time}",
                   limit=25).get("data", [])
    except Exception as e:
        print(f"[direct] l'API non li dà ({type(e).__name__})")
        sys.exit(1)
    da = datetime.now(timezone.utc) - timedelta(hours=ore)
    conversazioni = messaggi = 0
    for c in conv:
        nuovi = 0
        for m in (c.get("messages") or {}).get("data", []):
            chi = (m.get("from") or {}).get("username")
            quando = datetime.strptime(m["created_time"], "%Y-%m-%dT%H:%M:%S%z")
            if chi != io and quando >= da:
                nuovi += 1
        if nuovi:
            conversazioni += 1
            messaggi += nuovi
    print(f"[direct] ultime {ore} ore: {messaggi} messaggi nuovi "
          f"in {conversazioni} conversazioni (il contenuto si legge dall'app)")


if __name__ == "__main__":
    main()
