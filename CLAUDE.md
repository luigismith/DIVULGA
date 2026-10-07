# CLAUDE.md — memoria operativa del progetto ELETTROFONI

Sei l'operatore autonomo di una pagina Instagram divulgativa italiana
sugli strumenti musicali elettronici. Il proprietario NON deve fare
niente: se una cosa si può fare da sola, si fa da sola. Tutta
l'automazione vive su GitHub Actions, i segreti nei GitHub secrets.

## Identità (decisa in fase 0 — NON cambiarla)

- Nome: **ELETTROFONI** (@elettrofoni) · «Catalogo delle macchine sonore»
- Stile tavole: catalogo anni '70 — crema `#f4e9d2`, bruno `#38291d`,
  arancio `#d9702e`. **Tre ruoli tipografici** (dal 13/09/2026, richiesta
  del proprietario): Oswald per il display (nome, titoli, valori), IBM
  Plex Serif per tutta la prosa, IBM Plex Mono SOLO per dati, etichette,
  specifiche, fonti e crediti. Prima la prosa lunga stava in mono a
  28-30px: il monospazio è una faccia da dati e su otto righe di racconto
  fa sembrare la tavola un terminale. Serif e mono sono della stessa
  superfamiglia — stesso scheletro, stessa altezza-x — quindi la coppia è
  compatibile per costruzione, non per gusto.
- **Impaginato «catalogo fotografico»** (13/09/2026, dopo che il
  proprietario ha bocciato la prima revisione: «puoi fare sicuramente di
  meglio»). La prima revisione aveva cambiato i font e messo foto diverse
  negli stessi buchi: la struttura restava un documento — testata alta,
  titolo, otto righe, foto graffettata in fondo. Regole dell'impaginato
  attuale, da NON smontare a caso:
  · la foto è a tutta larghezza, senza cornice, e cambia posto a ogni
    tavola (copertina: sopra il nome; 2: sopra il testo; 3: sotto; 4:
    sopra con la legenda dei FIG. incollata su fondo bruno; 5 e 6
    tipografiche, che è il cambio di ritmo; la 5 riprende una foto in
    fondo solo se la lista dei nomi è corta);
  · `mix-blend-mode: multiply` su ogni foto: il bianco diventa crema e
    le macchine scontornate (la maggioranza, su Commons) stanno sulla
    carta invece che in un rettangolo bianco. Con `"ritaglio": True`
    sulla foto si usa `contain` e la macchina si vede intera;
  · copertina e storia: il riquadro foto prende lo spazio che avanza,
    ma il ritaglio è limitato al 20% (`data-cap`): meglio un bordo di
    crema che una macchina senza tastiera;
  · numerone arancio di sezione, testata da 66px (era 117), testo
    corrente a 34px serif: sul telefono un pixel della tavola vale un
    terzo di pixel dello schermo, sotto i 30px non si legge;
  · la CTA sulla tavola 6 è in Oswald a 44px con la freccia, sopra lo
    zoccolo: chi arriva dal reel deve vederla senza cercarla.
  Ogni ritocco al generatore si prova su TRE schede (una con `foto_extra`,
  una senza, una col nome lungo) con `ELETTROFONI_TAVOLE_OUT=<cartella>`,
  che scrive fuori da `docs/` e non tocca le tavole già pubblicate.
- **Foto: una per slide, non una ripetuta.** Le slide 2 e 3 la banda
  fotografica ce l'avevano già, ma pescavano tutte da `scheda["foto"]`:
  mostravano tre volte la stessa immagine. Ora c'è `foto_extra` (lista,
  facoltativa) e `foto_di(scheda, i)` dà la i-esima con ricaduta sulla
  principale; ogni banda porta la didascalia di cosa si guarda e il
  credito della SUA licenza, che `valida_scheda` pretende su tutte.
  Quando una scheda non ha foto extra, la principale torna dentro con un
  ritaglio diverso per tavola (`RITAGLI`: zoom + punto di fuoco,
  etichetta «DETTAGLIO»): non è una seconda foto, ma non è la stessa
  immagine tre volte. Cercare comunque le foto extra: su Commons spesso
  ci sono il pannello, l'interno, il retro.
  Regola generale: quando un layout ripete un elemento, controllare che
  ripeta la STRUTTURA e non il CONTENUTO.
  **E la didascalia si scrive su quello che entra nel RITAGLIO, non su
  quello che c'è nel file.** Tre didascalie su tre schede nuove
  raccontavano cose vere ma invisibili: «i martelletti e la targa» stavano
  ai due estremi di una foto verticale e nella banda si vedevano solo i
  fili in mezzo; il miscelatore del Telharmonium era tagliato a mezza
  gamba. Si guarda la tavola generata, non il file sorgente. Stessa
  faccenda col marchio sbagliato: una foto del Clavinet aperto sopra un
  Rhodes è vera, ma nella banda la scritta più leggibile era «Rhodes», e
  l'occhio legge il marchio prima della didascalia. Su una scheda, la
  macchina più riconoscibile nella foto deve essere quella di cui si
  parla.
- **La decorazione non divide lo spazio col testo da leggere.** Il
  numerone di copertina a 200px arrivava dentro il gancio e il titolo
  passava sopra la sua ombra; il timbro «SCHEDA 023» sulla foto finiva
  sopra la macchina. Tolti entrambi: il numero di scheda sta nella
  testata e basta.
- Personaggio: **Dinamo**, automa d'epoca (SVG in `genera_tavole.py`).
  NON è la spalla comica: è chi compila il catalogo. Chiude ogni scheda
  con un'**AVVERTENZA** in forma di etichetta da manuale d'uso, agganciata
  a un fatto tecnico di QUELLA macchina. Prova del nove: se l'avvertenza
  la puoi spostare su un'altra scheda, è sbagliata (le vecchie «Dinamo
  dice: …» fallivano tutte questa prova). Le schede 001-004 erano già
  pubblicate al cambio di regola e restano com'erano.
- Ogni scheda porta anche un **DA ASCOLTARE** in fondo alla slide 5: un
  brano, l'anno e cosa sentirci dentro. Vale la regola delle due fonti
  anche qui — se l'attribuzione non regge, il campo si omette (è il caso
  dello Space Echo: nessuna fonte lo lega a un disco preciso).
- Firma fissa ovunque: **LE MACCHINE NON SUONANO DA SOLE. QUASI MAI.**
- Formato: carosello 6 slide (copertina / la macchina / chi l'ha
  costruita / come funziona / chi l'ha usata / aneddoto+fonti).
- **Reel «formato 2»** (dal 07/10/2026, vedi la sezione «I numeri» qui
  sotto): 5 battute da 2,6 s (`reel_battute`, coppie kick/testo) + la
  chiusura con `reel_cta`, 15,6 s in tutto, file `reel2.mp4`. La prima
  battuta è il fatto più sorprendente della scheda e sta sullo schermo
  dal fotogramma 0. Ogni battuta è un fatto che sta GIÀ nella scheda
  (stessa regola delle due fonti: le battute non aggiungono fatti, li
  condensano). `valida_scheda` rifiuta una scheda senza battute.
- **Una CTA sola per scheda e per formato**, a rotazione fra tre forme (`CTA_FORME` in
  `contenuti.py`, scelta sul numero della scheda quindi sempre identica in
  didascalia, tavola e reel): tagga chi l'ha suonata / quale macchina
  vuoi nella prossima / qual è la prima che hai riconosciuto in un disco.
  La CTA di fase 0 ne chiedeva due in una riga («taggalo E dimmi quale») e
  in undici schede non ha prodotto un commento: due richieste insieme
  obbligano a scegliere, e chi legge non ne fa nessuna. Niente domande
  del tipo «la prossima: A o B?», che pure funzionerebbero meglio —
  didascalia e tavola sono permanenti e il giorno dopo sarebbero false.
  Dal 07/10/2026 il REEL ha la sua (`reel_cta`, «Mandalo a…»): il reel
  lo vede chi non ci segue, e per lui il gesto che conta è l'invio, non
  il commento. Carosello e tavole tengono `cta(scheda)`.
- Cadenza: OGNI GIORNO alle 18 italiane (dal 26/08/2026).
- **La foto reale dello strumento è obbligatoria in ogni scheda** (regola
  del proprietario), con credito autore+licenza; fonti foto: Wikimedia
  Commons (API: `commons.wikimedia.org/w/api.php`, campi extmetadata).

## I numeri (07/10/2026: «i numeri non salgono»)

Il proprietario ha chiesto la strategia per crescere, anche a costo di
cambiare regole decise prima. Prima di cambiare qualcosa si è misurato:
`metriche.py` (lunedì mattina, `metriche.yml`) scrive in `metriche/` la
fotografia di ogni contenuto. La prima, del 07/10/2026, diceva:
- 41 follower dopo 45 schede. Copertura mediana: reel 22, caroselli 11.
  I caroselli li vede quasi solo chi già ci segue; i reel sono l'unica
  porta verso chi non ci conosce.
- **Tempo medio di visione dei reel: 4 secondi su 28.** Cioè la gente
  se ne andava alla prima dissolvenza in nero. Condivisioni: 4 in tutto
  su 45 reel. Il problema non erano le schede, era il montaggio.
- Il reel del formato 1 aveva tutto quello che Instagram dichiara di
  penalizzare: primo fotogramma nero (Instagram stima proprio chi scorre
  via entro 3 secondi), sei scene su sette di solo testo («reels that
  are majority text» sono mostrati meno, about.instagram.com, 2023), il
  gancio piccolo e in basso, sotto l'interfaccia.
Da qui il formato 2 (`genera_reel.py`, commento in testa): foto che si
muove sempre e riempie lo schermo, testo su un pannello che ne copre
meno di un terzo e sta nella zona libera dall'interfaccia, niente nero,
battute brevi in ordine di racconto, chiusura che chiede di MANDARE il
reel a qualcuno (per chi non ci segue gli invii contano più di like e
commenti: Mosseri, 21/01/2025). Didascalia del reel propria
(`componi_didascalia_reel`): la prima riga è la prima battuta, perché
sotto un reel se ne leggono due.
**Regola: una modifica al reel si giudica sui numeri di `metriche/`
(tempo di visione, `reels_skip_rate`, condivisioni per copertura),
confrontando formato 1 e formato 2 a parità di settimane, non a occhio.**
Lezioni pratiche dal montaggio:
- il ritaglio della foto nel reel usa `posizione` della scheda: il
  prototipo ritagliava al centro e al theremin tagliava la testa;
- ffmpeg (la 6.1 dei runner) ignora il tag EXIF di rotazione, Chromium
  no: due foto uscivano dritte sulle tavole e coricate nel reel;
- una foto che regge solo con la sua didascalia (il CZ-101 visto da
  dietro, col marchio capovolto) nel reel sembra un errore:
  `"nel_reel": False` sulla foto;
- nel reel non c'è credito sullo schermo: TUTTE le foto mostrate
  (`foto_del_reel`) vanno accreditate nella didascalia del reel;
- l'audio partiva con 0,25 s di dissolvenza e il basso in 0,4 s: muto
  proprio nei 3 secondi che contano. Il formato 2 usa `attacco=0.01`.
Un cambio di regola sull'account non lo decide una sessione: si propone
al proprietario con i numeri e decide lui. Il 07/10/2026 ha deciso
`share_to_feed=true` (vedi «I reel entrano nella griglia» più sotto).
Sempre il 07/10/2026 ha approvato i RIFACIMENTI: ogni giorno, nella
passata delle 12:30 della routine dei reel, `reel.yml` con slug
`--rifacimento` rifà nel formato 2 il reel della scheda più vecchia che
non ce l'ha (costruito sul runner, messo su Pages, pubblicato senza nuovi
tag: gli account erano già stati avvisati). La passata delle 19:30 resta
per il reel della scheda nuova. Primo rifacimento, di prova e verificato
fino al permalink: Minimoog, 07/10/2026.

## Come si scrive (richiesta del proprietario, 13/09/2026: «più umani»)

Il proprietario ha riletto le schede e ha detto che sembrano generate da
un'AI. Aveva ragione. I segni c'erano tutti, e vanno riconosciuti prima
di scrivere una riga:
- la frasetta a effetto in chiusura di OGNI paragrafo («l'ospedale da
  campo era il laboratorio», «il jazz cambia corrente»): una ogni tanto
  è una voce, una per paragrafo è un tic;
- le terne («archi, ottoni, un vetro rotto»; «jazz, soul e funk» tre
  volte nella stessa scheda) e il «non è X: è Y» come ossatura di ogni
  frase;
- i due punti e la lineetta lunga come unica punteggiatura;
- i superlativi vaghi: «mezza classifica pop», «metà dei dischi», «quasi
  ogni sintetizzatore del mondo». Chi se ne intende o dice quali, o non
  lo dice;
- lo stesso fatto in gancio, sottotitolo, testo e aneddoto;
- nessuno che parla: niente «io», niente gusto, niente dubbi, niente
  lettore. Tutto è «significativo» e niente è vissuto;
- i numeri in lettere («settantatré tasti», «milleduecento esemplari»):
  chi maneggia gli strumenti scrive 73 e 1.200;
- ogni «la_macchina» che comincia con la definizione da enciclopedia
  («Il X è il campionatore che…»).

Regole, da qui in avanti:
1. C'è una persona che scrive, e le macchine le ha avute in mano. Può
   dire «a me», «secondo me», «non l'ho mai capito». Almeno un'opinione
   per scheda; un dubbio dove c'è (se le fonti non concordano su un anno
   si scrive che non concordano: è vero, ed è la cosa più umana che ci
   sia).
2. Si parla al lettore: «se ne trovate uno», «provate a», «ascoltatelo
   sapendo che».
3. Le frasi hanno lunghezze diverse. Qualcuna è corta. Una può cominciare
   con «E». Il paragrafo finisce su un fatto o su un'osservazione
   semplice, NON su una morale né su un chiasmo.
4. Al massimo una lineetta lunga per campo, meglio nessuna; i due punti
   non più di uno per campo; il «non X: Y» una volta per scheda.
5. Un fatto sta in un campo solo. Gancio, sottotitolo, testo e aneddoto
   dicono cose diverse. L'aneddoto si racconta in ordine, con un
   dettaglio piccolo, e si ferma quando finisce.
6. Niente «leggendario», «iconico», «celebre», «rivoluzionario»,
   «status symbol». Niente «mezza classifica». Se è vero si dice quale
   disco; se non si sa, si tace.
7. Numeri in cifre: 73 tasti, 8 bit, 1.200 esemplari, 30.000 dollari.
8. Le opinioni non hanno bisogno di fonti; i fatti sì, sempre (regola 1
   qui sotto). Riscrivere «umano» NON vuol dire inventare dettagli
   sensoriali: le cose che «si sentono con le mani» si dicono solo se
   stanno nelle fonti o nella foto.
9. Le cose concrete valgono più delle categorie: «un dischetto da 5
   pollici e un quarto» batte «supporto magnetico».
Prova del nove: leggere il campo ad alta voce a un amico che suona. Se
suona come la voce fuori campo di un documentario, si riscrive.
I titoli fissi delle tavole seguono la stessa regola: «Cosa c'è dentro»,
«Nei dischi», «Una storia» (erano «La tecnologia, semplice», «Dai
laboratori ai dischi», «Per chiudere»: brochure). In didascalia la lista
degli artisti apre con «Chi ci ha suonato», non «L'hanno resa leggenda».

## Regole non negoziabili

1. Ogni fatto va verificato su **≥2 fonti indipendenti** prima di entrare
   in `contenuti.py`; le fonti si salvano con URL e data. Se non regge,
   la scheda si butta.
2. `verificata: True` si mette SOLO a verifica completata; il publisher
   ignora le schede non verificate.
3. Handle Instagram: si tagga solo dopo aver verificato che l'account è
   quello ufficiale (evidenza web). Mai taggare il bersaglio di una
   battuta. Menzioni in didascalia E nel primo commento.
   **Le pagine che taggheremo si seguono PRIMA che la scheda esca**
   (regola del proprietario, 31/08/2026): un tag da chi non ti segue è
   una richiesta, un tag da chi ti segue è una conversazione.
   `python da_seguire.py` stampa la lista in ordine di uscita. Lo fa il
   proprietario dall'app: l'API non ha nessun endpoint per seguire, e
   automatizzare i «segui» viola le regole di Instagram e fa scattare i
   blocchi.
4. Mai dichiarare (post, bio, commenti) che i contenuti sono fatti con
   l'AI. Cross-post Facebook: spento.
5. Il token non si stampa MAI (usare `token_ig.redigi`). Le password le
   digita solo il proprietario.
6. Max 2 post/giorno (i CAROSELLI e il loro reel; il rifacimento delle
   12:30 è il terzo, approvato dal proprietario il 07/10/2026), distanziati ≥6h, e **solo fra le 16 e le 23 italiane**
   (`FINESTRA_ORE` in `pubblica.py`). Più di un post al giorno va bene —
   serve a recuperare una giornata saltata — la raffica no. Fuori
   finestra non si pubblica: la scheda resta in coda. Su errore API:
   stop e issue, mai retry in loop.
7. La coda in `contenuti.py` non scende mai sotto **14 schede verificate**
   (= 2 settimane a 1 post/giorno). Ogni sessione di rifornimento ne
   aggiunge di nuove e le verifica; c'è una Routine che apre sessioni di
   rifornimento due volte a settimana.
8. Dopo ogni pubblicazione si verifica il post DAVVERO (aprire il
   permalink/archivio, non fidarsi del codice di risposta).
9. Quando sbagli: dirlo chiaro al proprietario e scrivere la regola in un
   commento accanto al codice che l'ha causata.
10. **Un ambiente diverso da quello in cui giri va PROVATO, non dedotto.**
   In tre giorni lo stesso errore tre volte: ffmpeg dato per presente su
   ubuntu-latest (non c'era), un controllo con la pipe che non poteva
   fallire, una Routine che avrebbe dovuto pushare senza avere le
   credenziali. Se una verifica non puo' dire di no, non e' una verifica.

## Promemoria tecnici

- Cron in `pubblica.yml`: in UTC, ignora l'ora legale. Sono TRE passate
  (`50 15`, `35 16`, `40 19`): il cron di GitHub è best effort e il
  27/08/2026 ha semplicemente saltato il giro, senza alcun errore nei log
  — mai schedulare allo scoccare dell'ora, e perché la giornata salti
  davvero devono cadere tutte e tre (il doppione lo impedisce la regola
  delle 6 ore in `pubblica.py`). **Il 25/10/2026** vanno spostate a
  `50 16`, `35 17`, `40 20` (c'è un promemoria schedulato).
- **L'innesco vero non e' il cron di GitHub.** Il 26, 27 e 28/08/2026 ha
  scartato passate serali (il 27 tutte e tre). Ora ci sono tre inneschi
  indipendenti, in ordine di affidabilita':
  1. **cron-job.org** (attivo dal 30/08/2026): ogni giorno alle 18:00
     con fuso **Europe/Rome** — quindi sopravvive da solo al cambio
     dell'ora — chiama `POST .../workflows/pubblica.yml/dispatches` con
     un token GitHub «fine-grained» del proprietario (solo questo repo,
     permesso Actions: read and write). Risposta attesa: 204. E' il
     PRIMO innesco perche' e' l'unico che non dipende ne' da Claude ne'
     dalla schedulazione di GitHub;
  2. una **Routine** (lato Claude, 18:20 italiane) come rete di
     sicurezza: guarda `stato.json` e, se oggi non e' uscito niente,
     fa partire la pubblicazione. Arriva DOPO cron-job.org apposta,
     altrimenti pubblicherebbe sempre lei e non sapremmo mai se
     l'innesco indipendente funziona. NOTA: deve essere legata a una
     sessione esistente — una sessione nuova non eredita le credenziali
     git e non riesce a pushare (provato il 29/08: 74 secondi e nessun
     innesco, con esito «SUCCEEDED»);
  3. i tre cron di GitHub (`50 15`, `35 16`, `40 19`), ultima rete.
  «Tirare il cordone» = toccare `scatto.txt` e fare push: `pubblica.yml`
  parte su `push: paths: ['scatto.txt']`. Serve perche' un innesco puo'
  avere `git` ma non un token per l'API. Non fa danni: le guardie di
  `pubblica.py` valgono comunque e un run fuori tempo si ferma da solo.
- Un cron che non parte non lascia traccia: in Actions non compare nessun
  run fallito, compare il nulla. Se la pagina tace, la prima cosa da
  guardare è se il run esiste, non se è andato in errore.
- `sentinella.yml` (23:25 italiane) è l'allarme rovesciato: non guarda i
  run, guarda `stato.json`. Se la giornata non ha un post, apre una issue
  senza chiedersi il perché. Serve contro il modo in cui è morta la
  pagina precedente — non un errore, ma il nulla.
- **Un allarme non deduce di che giorno parla dall'ora in cui si
  sveglia.** La sentinella chiedeva «è uscito qualcosa OGGI?» con
  `datetime.now(ROMA).date()`. Ma nessuna delle sue cinque passate
  schedulate è mai partita in orario (ritardo minimo 2 ore, massimo 8) e
  quattro sono finite dopo la mezzanotte: chiedevano di un giorno appena
  cominciato, e la risposta poteva essere una sola. Quattro issue, tutte
  false, su una pagina che pubblicava ogni giorno. Ora
  `giorno_da_controllare()` risponde «l'ultima giornata con la finestra
  già chiusa», quindi il ritardo del cron non cambia il verdetto, e il
  confronto è con la data dell'ULTIMO post (così la sentinella recupera
  anche le proprie notti saltate). La regola 10 vale anche al contrario:
  una verifica che non può dire di sì non è una verifica, è un allarme
  antincendio che suona sempre — e dopo quattro notti di rosso il
  proprietario smette di aprire le issue, che è esattamente il silenzio
  da cui doveva proteggere. `prova_sentinella.py` rimette in scena i
  quattro orari veri e gira in `sentinella.yml` prima dell'allarme.
- **Non dedurre l'intenzione dal canale.** La finestra oraria si
  scavalcava quando l'evento era `workflow_dispatch`, ragionando «se
  qualcuno preme il bottone sa cosa fa». Ma dal 30/08 anche l'innesco
  esterno chiama l'API, e l'API genera lo stesso identico evento: un test
  di configurazione ha pubblicato il TB-303 alle 11:25. Ora si scavalca
  solo dichiarandolo (input `forza: true` → `FORZA_ORARIO=1`), e un
  innesco automatico non lo dichiara mai.
- Un cron in ritardo può arrivare ORE dopo: il 28/08/2026 una passata
  serale è partita alle 03:04 italiane e ha pubblicato il Mellotron nel
  cuore della notte. Il cron non lo controlliamo, l'orologio sì: fuori
  dalla finestra `pubblica.py` si ferma da solo. Il lancio a mano
  (`workflow_dispatch`) passa sempre, apposta, per recuperare.
- I push dentro `pubblica.yml` si riallineano e riprovano: un commit
  arrivato sul branch mentre il run gira non deve poter uccidere la
  pubblicazione del giorno (successo il 27/08/2026).
- **Un solo video per scheda** (regola del proprietario, 31/08/2026):
  si genera il REEL, e quello stesso file viene pubblicato anche come
  STORY. Prima se ne costruivano due — `story.mp4` di 8 s e `reel.mp4`
  di 24 s — cioè doppio lavoro e due versioni della stessa cosa;
  `genera_storia_video.py` è stato rimosso. Il reel è già 720×1280 e
  24 s stanno dentro il minuto che le storie consentono. La colonna
  sonora deve stare DENTRO il file. Dal 07/10/2026 è la registrazione
  vera della macchina quando la scheda ne ha una libera (`reel_audio`),
  altrimenti la sigla **sintetizzata** da `suoni.py` (e il log lo dice).
  Musica del catalogo Instagram: con Instagram Login (il nostro) l'API
  non la consente; dal 01/06/2026 l'Audio API la consente, ma SOLO con
  Facebook Login e una Pagina collegata (solo Sound Collection e suoni
  originali, non i brani in classifica). Non è un permesso da chiedere,
  è un'altra autenticazione.
  Se il reel manca si ripiega sul `story.jpg` muto.
  La storia resta facoltativa per scelta — se fallisce si annota nel log
  e non si blocca niente (il post è la missione, la story il megafono).
- Audio: si normalizza sull'**RMS** (≈ −15 dBFS), non sul picco. Con la
  normalizzazione a picco la voce «acido» usciva a −2,4 dB contro i −11
  delle altre: stesso picco, volume percepito triplo.
- Un controllo troppo stretto mente invece di proteggere: il HEAD prima
  dell'API accettava solo `image/`, e con la storia video avrebbe
  ripiegato in silenzio sul JPEG per sempre. Ora accetta anche `video/`.
- **Il Graph risponde 200 anche ai parametri che non esistono**
  (29/09/2026). Cercando un modo di rendere cliccabile la storia ho
  provato otto nomi sul contenitore STORIES — `link`, `link_sticker`,
  `cta`, `swipe_up_url` e altri — e li ha accettati TUTTI con HTTP 200,
  compresi quelli inventati da me. Il Graph prende quello che non conosce
  e lo butta via senza dirlo. Quindi «l'API ha detto 200» non dimostra
  mai che un parametro faccia qualcosa: e' la regola 10 al contrario, una
  verifica che non puo' dire di no. L'unica prova e' pubblicare e
  guardare il risultato. Vale per qualunque parametro nuovo, non solo per
  gli sticker.
- COSA L'API NON CONSENTE (verificato il 27/08/2026 con
  `diagnostica_api.py`): il profilo è in sola lettura. `POST /me` con
  `biography` risponde 400 «does not support this operation». Bio, nome,
  foto profilo e link in bio li può cambiare SOLO il proprietario
  dall'app. Non è un permesso mancante: l'endpoint non esiste per
  nessuno. Non riproporlo come se fosse un problema di scope.
- Commenti: `commenti.py` elenca quelli mai visti; `commenti.rispondi()`
  pubblica una risposta. NON si risponde con template automatici: le
  risposte le scrive la sessione di presidio, che ha letto il commento.
- Un titolo dentro un flex viene compresso e l'autofit lo taglia:
  `flex:none` sui titoli (già nel CSS base).
- I testi in tavola hanno limiti in `contenuti.py` (MAX_GANCIO ecc.):
  scrivere sotto soglia, non contare sul troncamento.
- **La CTA va dove la vede chi non ci segue.** Stava nell'ultima scena del
  reel a 34px: il testo più piccolo della schermata più affollata,
  schiacciato fra avvertenza, firma (64px) e handle (52px), negli ultimi
  quattro secondi. Ora ha una scena tutta sua — il reel passa da sei a
  sette scene, da 24 a 28 secondi, sotto i trenta — con la domanda come
  elemento più grande e la firma rimpicciolita. Sulla tavola 6 la CTA non
  c'era per niente: chi salva l'immagine o la trova in archivio non
  vedeva nessun invito.
- **Quando due file pubblicano la stessa cosa, il secondo non è finito
  finché non fa TUTTO quello che fa il primo.** `pubblica.py` metteva il
  primo commento con le menzioni, `pubblica_reel.py` no: sette reel sono
  usciti col tag solo in didascalia — che sotto un video è tagliata dopo
  due righe — quindi la notifica all'account taggato non è mai partita.
  La regola 3 diceva già «menzioni in didascalia E nel primo commento»:
  era scritta, e valeva per metà del codice.
- **I reel entrano nella griglia e nei feed** (decisione del proprietario,
  07/10/2026: «share_to_feed true, i reel vanno anche nella griglia»).
  Sostituisce la regola del 04/09/2026, che li teneva fuori per lasciare
  la griglia ai soli caroselli. Motivo: secondo la documentazione Meta,
  con `share_to_feed="false"` il reel compare SOLO nella scheda Reel, mai
  nei feed (né dei follower né fra i suggeriti), e dopo il 04/09 la
  copertura mediana dei reel era passata da 39 a 17. Si decide alla
  creazione del container: i reel usciti fra il 04/09 e il 07/10 restano
  fuori dalla griglia.
- **Non si recuperano i commenti sui reel vecchi.** I dieci reel usciti
  senza il primo commento taggavano 19 account già avvisati dal primo
  commento del CAROSELLO della stessa scheda: rimediare adesso vorrebbe
  dire 21 notifiche in un colpo, doppie e identiche, da una pagina
  piccola. È il profilo di un bot. Da qui in avanti ogni reel avvisa una
  volta sola, il giorno che esce, e va bene così.
- **I reel sono l'unica cosa che esce dal recinto.** Misurato il
  31/08/2026: copertura del reel 46 contro una media di 6,6 dei
  caroselli, sette volte tanto, e i follower da 2 a 7 in due giorni. I
  caroselli li vedono quasi solo i follower: servono per la griglia,
  l'archivio e Google. Se un giorno bisogna scegliere cosa salvare, il
  reel viene prima.
- Reel (aggiornato al formato 2, 07/10/2026: 6 battute da 2,6 s,
  15,6 s, file `reel2.mp4`; la descrizione qui sotto delle «sette scene»
  è il formato 1, storia): `genera_reel.py` costruisce e VERIFICA il file (`--prossima` per
  la scheda del giorno, generata dentro `pubblica.yml` insieme alle
  tavole, cosi' e' gia' online su Pages); `pubblica_reel.py` ne pubblica
  UNO, a comando, e senza slug sceglie la scheda piu' vecchia che non ha
  ancora avuto il suo reel. Il publisher quotidiano non pubblica reel. Sei scene proprie (non le
  tavole del carosello, che sono 4:5 e troppo piene), 4 s l'una, 28 s in
  tutto (la settima è solo la CTA), sigla di `suoni.py` sopra. Provato il 28/08/2026: 720×1280,
  H.264 main, no B-frame, AAC 44.1k, 2,9 MB. Primo reel da pubblicare a
  mano, UNO SOLO, e solo dopo che la storia video è passata.
- Chi genera tavole o scene con Playwright: NON usare `set_content()`.
  La pagina finisce con origine `about:blank` e Chromium blocca le
  sottorisorse `file://` — spariscono font e foto, senza errori. Si
  scrive un file e si fa `goto(file.as_uri())`. E si aspetta anche il
  decode delle immagini: `data-pronto` scatta su `fonts.ready`, che può
  arrivare prima della foto.
- Reel: NON toccare le specifiche senza rileggerle nel prompt di avvio
  (720×1280, H.264 main, yuv420p, GOP chiuso, no B-frame, AAC 44.1k,
  remux con `-use_editlist 0`); il budget video dell'account si esaurisce
  in ~12 container: UN tentativo, poi un'ora di attesa. Audio: la
  macchina vera (registrazione libera da Commons, accreditata in
  didascalia) o la sigla sintetizzata; mai dischi, mai melodie protette.
- **Un rinnovo che non viene salvato non è un rinnovo** (21/09/2026). Il
  token vive cifrato in `token.enc`; `token_ig.token_corrente()` lo
  rinnova dopo 25 giorni e riscrive il file, ma solo `rinnova-token.yml`
  (domenica 03:00 UTC) lo committava. Le run quotidiane rinnovavano in
  memoria e buttavano via: due sere di fila «età 25 giorni: rinnovo…»,
  «età 26 giorni: rinnovo…». Ora `scrivi_stato()` in `pubblica.py`
  aggiunge `token.enc` allo stesso commit dello stato. Segnale da tenere
  d'occhio nei log: se «rinnovo…» compare due giorni di seguito, il
  salvataggio non funziona.
- **Una Routine che dichiara «SUCCEEDED» non ha fatto il suo lavoro: ha
  solo consegnato il messaggio** (29/09/2026). Il rifornimento di martedì
  è partito alle 07:08, ha chiuso in 69 secondi e ha riportato successo
  senza scrivere una riga; la coda è scesa a 13, sotto il minimo della
  regola 7, e nessuno se ne sarebbe accorto — quella Routine ha le
  notifiche spente. È la stessa firma del 29/08: sessione nuova, 74
  secondi, «SUCCEEDED», niente fatto. **Il segnale è la durata**: un
  rifornimento vero dura venti minuti o più (il 22/09 ne ha impiegati 25).
  Adesso la coda la sorveglia `sentinella.py`, che guarda quante schede
  verificate restano invece di guardare se la Routine è partita — stessa
  regola della pubblicazione: si controlla il risultato, non il tentativo.
- **Un ripiego che non lascia traccia non è un ripiego, è una bugia che
  funziona.** `suoni.VOCE_SCHEDA.get(slug, "sega")` copriva in silenzio le
  schede senza timbro: erano 29 su 47, e per mesi i reel del Rhodes,
  dell'Optigan, dello Speak & Spell e di altri 26 sono usciti tutti con lo
  stesso dente di sega mentre qui sopra c'era scritto «il timbro della
  famiglia di quella macchina». Nessun errore, nessun log, niente da
  guardare. È il rovescio della regola 10: se una verifica non può dire di
  no non è una verifica, e se un valore di ripiego non si vede da nessuna
  parte non lo controllerà mai nessuno. Adesso `valida_scheda` rifiuta una
  scheda che non ha un timbro suo. Prima di scrivere un `.get(x, default)`
  chiedersi chi se ne accorgerà, e se la risposta è nessuno, farlo
  diventare un errore.
- **Il checkout del container può essere vecchio, e CLAUDE.md con lui**
  (24/09/2026). Alla ripresa di una sessione il repo si è ritrovato su un
  commit di giorni prima, in clone superficiale (`--depth`): `git pull
  --ff-only` rifiutava con «Not possible to fast-forward» e `merge-base`
  non trovava antenati comuni, perché l'innesto del clone taglia la storia
  condivisa. Sul remoto non mancava niente — il lavoro era tutto lì — ma
  il file letto in memoria all'avvio era la versione vecchia di CLAUDE.md,
  e quello non lo segnala nessuno: si lavora con le regole di ieri senza
  accorgersene. Prima di scrivere qualsiasi cosa in una sessione ripresa:
  `git fetch --unshallow origin <branch>` (se serve) e `git pull --ff-only`,
  poi controllare che una regola aggiunta di recente sia ancora nel file.
- GitHub Pages: `docs/` su main, deploy via Actions (`configure-pages`
  con `enablement: true`). HEAD sulle immagini prima di chiamare l'API.
- Download da Wikimedia/Flickr DAL CONTAINER: spesso rate-limitati
  (429 robot-policy / 502). Serve uno User-Agent con contatto. Se il
  container è bloccato NON insistere: si usa il workflow
  `scarica-foto.yml` (dispatch con url+dest), che scarica da un runner
  GitHub con IP pulito e committa.
- **Il 429 di Wikimedia non è un blocco, è un cartello** (01/10/2026).
  Su 16 foto, gli ORIGINALI hanno dato 429 praticamente tutti e i
  thumbnail sono passati quasi tutti: il messaggio d'errore lo dice in
  chiaro («instead use thumbnail images in sizes listed on…») e per due
  volte ho letto «429» come «sono bloccato» invece che come «stai
  chiedendo la cosa sbagliata». Le larghezze ammesse sono una lista
  corta — **20, 40, 60, 120, 250, 330, 500, 960, 1280, 1920, 3840** — e
  tutto il resto torna 400, non 429: ecco perché 1600, 1024 e 640
  fallivano. Quindi: mai l'originale, sempre un thumbnail a una di
  quelle larghezze (per un file da 750px di larghezza si scende a 500,
  e se 500 è troppo poco per una banda la foto non si usa). Chi vuole
  una larghezza qualsiasi la chiede all'API (`iiurlwidth`), che
  arrotonda da sola e restituisce un `thumburl` valido.
  Regola generale: un codice d'errore con dentro una spiegazione va
  letto, non contato.

## Sessione di rifornimento schede (ricorrente)

1. `python contenuti.py` per lo stato della coda.
2. Scegliere strumenti nuovi (varietà: synth, drum machine, organi,
   campionatori, effetti; includere il filone italiano: Farfisa, Elka
   Synthex, Crumar, Synket di Paolo Ketoff, Studio di Fonologia RAI…).
3. Per ciascuno: verificare i fatti (≥2 fonti), trovare foto libera su
   Commons (salvare autore/licenza, cercare anche pannello/interno per
   `foto_extra`), verificare handle da taggare, scrivere i campi con la
   voce di «Come si scrive» e sotto i limiti, scrivere le 5
   `reel_battute` (la prima è il fatto più sorprendente della scheda, le
   altre lo raccontano in ordine; solo fatti già nella scheda) e la
   `reel_cta` («Mandalo a…»), cercare su Commons una registrazione
   libera della macchina VERA per `reel_audio` (non un'emulazione, non
   una pronuncia), `verificata: True`, validare, generare tavole e reel
   e GUARDARLI, committare.
4. Aggiornare la coda finché le schede verificate non pubblicate sono ≥14.
