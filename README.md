# ELETTROFONI

Pagina Instagram divulgativa italiana sugli **strumenti musicali
elettronici**: origini, storia, tecnologia, chi li ha inventati e chi li
ha suonati. Ogni scheda è un carosello di 6 tavole in stile «catalogo
anni '70», con la **foto reale dello strumento sempre in vista** e le
fonti in calce.

- Instagram: [@elettrofoni](https://www.instagram.com/elettrofoni/)
- Archivio pubblico: https://luigismith.github.io/DIVULGA/
- Personaggio: **Dinamo**, l'automa che chiude ogni scheda con una battuta.
- Firma fissa: **«LE MACCHINE NON SUONANO DA SOLE. QUASI MAI.»**

## Come funziona

| File | Ruolo |
|---|---|
| `contenuti.py` | **Unico** database dei contenuti: una lista di dizionari, un campo per sezione, la funzione che compone la didascalia e i controlli automatici (2200 unità UTF-16, max 5 hashtag, max 10 slide, limiti dei campi in tavola). |
| `genera_tavole.py` | HTML+CSS → JPEG 1080×1350 con Playwright/Chromium headless. Autofit del testo; `flex:none` sui titoli. Output in `docs/tavole/<slug>/`. |
| `genera_archivio.py` | Il sito-archivio su GitHub Pages. Elenca **solo** i post usciti: la coda non si mostra. |
| `pubblica.py` | Publisher: guardie anti-doppione e anti-soft-block, HEAD sulle immagini prima dell'API, stato salvato subito dopo il publish, primo commento con le menzioni, verifica finale contro l'API. |
| `token_ig.py` | Token cifrato in `token.enc` (AES-GCM, chiave dal secret `STATE_KEY`), rinnovo automatico, redazione nei log. |
| `stato.json` | Cosa è uscito, quando, con quale id: **l'idempotenza vive qui**, non nell'API. |
| `.github/workflows/` | `pubblica.yml` (cron lun/mer/ven), `verifica-setup.yml` (manuale), `rinnova-token.yml` (rete di sicurezza), `controlli.yml` (validazione a ogni push). |

## Regole editoriali (fisse)

1. **Niente esce senza verifica su almeno 2 fonti indipendenti**, con data.
   Se una storia non regge, si butta e si dice che si è buttata.
2. Si tagga sempre l'autore o il soggetto in didascalia **e nel primo
   commento** (in didascalia lunga il tag resta dietro «… altro»).
   Handle verificati prima di taggare; **mai taggare il bersaglio** di
   una battuta.
3. La foto dello strumento è obbligatoria, con credito (autore + licenza)
   sulla tavola e in didascalia. Fonte: Wikimedia Commons o equivalenti
   con licenza libera.
4. Massimo 2 post al giorno, mai ravvicinati. Cross-post Facebook: spento.
5. Su errori API: fermarsi e segnalare (issue), **mai** retry in loop.
6. La coda non scende mai sotto le 2 settimane di pubblicazioni.

## Setup (una tantum)

Vedi la conversazione di avvio: account IG professionale, app Meta con
«Instagram API with Instagram Login» (`graph.instagram.com`), token di
lunga durata nei GitHub secrets (`IG_ACCESS_TOKEN` + `STATE_KEY`), poi
workflow **Verifica setup**.
