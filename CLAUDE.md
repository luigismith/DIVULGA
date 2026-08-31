# CLAUDE.md — memoria operativa del progetto ELETTROFONI

Sei l'operatore autonomo di una pagina Instagram divulgativa italiana
sugli strumenti musicali elettronici. Il proprietario NON deve fare
niente: se una cosa si può fare da sola, si fa da sola. Tutta
l'automazione vive su GitHub Actions, i segreti nei GitHub secrets.

## Identità (decisa in fase 0 — NON cambiarla)

- Nome: **ELETTROFONI** (@elettrofoni) · «Catalogo delle macchine sonore»
- Stile tavole: catalogo anni '70 — crema `#f4e9d2`, bruno `#38291d`,
  arancio `#d9702e`; font Oswald (titoli) + IBM Plex Mono (dati).
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
- CTA fissa: «quale macchina vuoi vedere nella prossima scheda».
- Cadenza: OGNI GIORNO alle 18 italiane (dal 26/08/2026).
- **La foto reale dello strumento è obbligatoria in ogni scheda** (regola
  del proprietario), con credito autore+licenza; fonti foto: Wikimedia
  Commons (API: `commons.wikimedia.org/w/api.php`, campi extmetadata).

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
6. Max 2 post/giorno, distanziati ≥6h, e **solo fra le 16 e le 23 italiane**
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
  run, guarda `stato.json`. Se oggi non c'è un post, apre una issue senza
  chiedersi il perché. Serve contro il modo in cui è morta la pagina
  precedente — non un errore, ma il nulla.
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
  sonora è **sintetizzata** da `suoni.py` (un motivo fisso col timbro
  della famiglia di quella macchina) e deve stare DENTRO il file:
  l'API non permette di agganciare la musica del catalogo Instagram.
  Se il reel manca si ripiega sul `story.jpg` muto.
  La storia resta facoltativa per scelta — se fallisce si annota nel log
  e non si blocca niente (il post è la missione, la story il megafono).
- Audio: si normalizza sull'**RMS** (≈ −15 dBFS), non sul picco. Con la
  normalizzazione a picco la voce «acido» usciva a −2,4 dB contro i −11
  delle altre: stesso picco, volume percepito triplo.
- Un controllo troppo stretto mente invece di proteggere: il HEAD prima
  dell'API accettava solo `image/`, e con la storia video avrebbe
  ripiegato in silenzio sul JPEG per sempre. Ora accetta anche `video/`.
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
- **I reel sono l'unica cosa che esce dal recinto.** Misurato il
  31/08/2026: copertura del reel 46 contro una media di 6,6 dei
  caroselli, sette volte tanto, e i follower da 2 a 7 in due giorni. I
  caroselli li vedono quasi solo i follower: servono per la griglia,
  l'archivio e Google. Se un giorno bisogna scegliere cosa salvare, il
  reel viene prima.
- Reel: `genera_reel.py` costruisce e VERIFICA il file (`--prossima` per
  la scheda del giorno, generata dentro `pubblica.yml` insieme alle
  tavole, cosi' e' gia' online su Pages); `pubblica_reel.py` ne pubblica
  UNO, a comando, e senza slug sceglie la scheda piu' vecchia che non ha
  ancora avuto il suo reel. Il publisher quotidiano non pubblica reel. Sei scene proprie (non le
  tavole del carosello, che sono 4:5 e troppo piene), 4 s l'una, 24 s in
  tutto, sigla di `suoni.py` sopra. Provato il 28/08/2026: 720×1280,
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
  in ~12 container: UN tentativo, poi un'ora di attesa. Musica solo
  sintetizzata.
- GitHub Pages: `docs/` su main, deploy via Actions (`configure-pages`
  con `enablement: true`). HEAD sulle immagini prima di chiamare l'API.
- Download da Wikimedia/Flickr DAL CONTAINER: spesso rate-limitati
  (429 robot-policy / 502). I thumbnail di Commons accettano solo
  larghezze standard (1920px sì, 1600 no) e serve uno User-Agent con
  contatto. Se il container è bloccato NON insistere: si usa il
  workflow `scarica-foto.yml` (dispatch con url+dest), che scarica da
  un runner GitHub con IP pulito e committa.

## Sessione di rifornimento schede (ricorrente)

1. `python contenuti.py` per lo stato della coda.
2. Scegliere strumenti nuovi (varietà: synth, drum machine, organi,
   campionatori, effetti; includere il filone italiano: Farfisa, Elka
   Synthex, Crumar, Synket di Paolo Ketoff, Studio di Fonologia RAI…).
3. Per ciascuno: verificare i fatti (≥2 fonti), trovare foto libera su
   Commons (salvare autore/licenza), verificare handle da taggare,
   scrivere i campi rispettando i limiti, `verificata: True`, validare,
   generare le tavole e GUARDARLE, committare.
4. Aggiornare la coda finché le schede verificate non pubblicate sono ≥14.
