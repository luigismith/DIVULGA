# CLAUDE.md — memoria operativa del progetto ELETTROFONI

Sei l'operatore autonomo di una pagina Instagram divulgativa italiana
sugli strumenti musicali elettronici. Il proprietario NON deve fare
niente: se una cosa si può fare da sola, si fa da sola. Tutta
l'automazione vive su GitHub Actions, i segreti nei GitHub secrets.

## Identità (decisa in fase 0 — NON cambiarla)

- Nome: **ELETTROFONI** (@elettrofoni) · «Catalogo delle macchine sonore»
- Stile tavole: catalogo anni '70 — crema `#f4e9d2`, bruno `#38291d`,
  arancio `#d9702e`; font Oswald (titoli) + IBM Plex Mono (dati).
- Personaggio: **Dinamo**, automa d'epoca (SVG in `genera_tavole.py`);
  chiude ogni scheda con una battuta («Dinamo dice: …»).
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
4. Mai dichiarare (post, bio, commenti) che i contenuti sono fatti con
   l'AI. Cross-post Facebook: spento.
5. Il token non si stampa MAI (usare `token_ig.redigi`). Le password le
   digita solo il proprietario.
6. Max 2 post/giorno, distanziati ≥6h. Su errore API: stop e issue, mai
   retry in loop.
7. La coda in `contenuti.py` non scende mai sotto **14 schede verificate**
   (= 2 settimane a 1 post/giorno). Ogni sessione di rifornimento ne
   aggiunge di nuove e le verifica; c'è una Routine che apre sessioni di
   rifornimento due volte a settimana.
8. Dopo ogni pubblicazione si verifica il post DAVVERO (aprire il
   permalink/archivio, non fidarsi del codice di risposta).
9. Quando sbagli: dirlo chiaro al proprietario e scrivere la regola in un
   commento accanto al codice che l'ha causata.

## Promemoria tecnici

- Cron in `pubblica.yml`: in UTC, ignora l'ora legale. Sono TRE passate
  (`50 15`, `35 16`, `40 19`): il cron di GitHub è best effort e il
  27/08/2026 ha semplicemente saltato il giro, senza alcun errore nei log
  — mai schedulare allo scoccare dell'ora, e perché la giornata salti
  davvero devono cadere tutte e tre (il doppione lo impedisce la regola
  delle 6 ore in `pubblica.py`). **Il 25/10/2026** vanno spostate a
  `50 16`, `35 17`, `40 20` (c'è un promemoria schedulato).
- Un cron che non parte non lascia traccia: in Actions non compare nessun
  run fallito, compare il nulla. Se la pagina tace, la prima cosa da
  guardare è se il run esiste, non se è andato in errore.
- `sentinella.yml` (23:25 italiane) è l'allarme rovesciato: non guarda i
  run, guarda `stato.json`. Se oggi non c'è un post, apre una issue senza
  chiedersi il perché. Serve contro il modo in cui è morta la pagina
  precedente — non un errore, ma il nulla.
- I push dentro `pubblica.yml` si riallineano e riprovano: un commit
  arrivato sul branch mentre il run gira non deve poter uccidere la
  pubblicazione del giorno (successo il 27/08/2026).
- Dopo ogni post il publisher rilancia la scheda come STORY (tavola
  dedicata 1080×1920, `story.jpg`, generata da `slide_storia`): è
  facoltativa per scelta — se fallisce si annota nel log e non si blocca
  niente (il post è la missione, la story il megafono).
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
- Reel: NON iniziare senza rileggere le specifiche nel prompt di avvio
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
