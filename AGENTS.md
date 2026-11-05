# AGENTS.md — Rilevamento allegati ISAB

Guida corta per qualsiasi agente IA. Non sostituisce la documentazione: punta alle mappe operative di Intelleo PDF Splitter.

## Boot obbligatorio (ogni prompt)

Prima di agire, leggere questo file e poi seguire l’ordine sotto. L’entrypoint di contesto è `wiki/INDEX.md` (hub) e poi `wiki/isab/INDEX.md` (grafo codice). Senza quel grafo l’agente non ha l’architettura corretta.

Regole Cursor: `.cursor/rules/` (indice `isab-rules-index.mdc`).
Hook sessione: `.cursor/hooks.json`.
Skill di progetto: `.agents/skills/` (mirror in `.cursor/skills/`). Catalogo: `.agents/isab-skills.json`.

Superpowers (Cursor e Codex): all’inizio di ogni prompt, dopo il boot wiki e prima di chiarimenti, esplorazione o edit, leggere `using-superpowers` dal plugin installato e applicare `.cursor/rules/superpowers-invoke.mdc`. Le skill generiche restano nel plugin: non sono vendute in questo repository. Istruzioni utente, wiki e vincoli di questo repo prevalgono sulle skill. Worktree, branch, commit, push e PR restano solo su richiesta.

## Leggere nell’ordine

1. [`wiki/INDEX.md`](wiki/INDEX.md) — hub
2. [`wiki/isab/INDEX.md`](wiki/isab/INDEX.md) — grafo codice
3. [`docs/GEMINI.md`](docs/GEMINI.md) — ops: comandi, percorsi dati, checklist
4. Note del codice toccato: [`src/core/GEMINI.md`](src/core/GEMINI.md), [`src/gui/GEMINI.md`](src/gui/GEMINI.md), [`src/shared/GEMINI.md`](src/shared/GEMINI.md), oppure [`src/GEMINI.md`](src/GEMINI.md) per launcher, licenza, config e updater
5. Nodo wiki del dominio in `wiki/isab/modules/` o `wiki/isab/architecture/`

## Vincoli rapidi

| Regola | Dettaglio |
|--------|-----------|
| Lingua | Sempre italiano |
| Diff minimo | Solo ciò che serve al task |
| Wiki-sync | Obbligatorio se cambi architettura, contratto regole/ROI, nomi file di output, flussi GUI o protocolli agente. Protocollo: [`wiki/isab/workflows/pre_commit_wiki_protocol.md`](wiki/isab/workflows/pre_commit_wiki_protocol.md) |
| GUI | PySide6. OCR e split stanno nel `ProcessingWorker`, non nel thread della UI |
| Config | `config.json` di lavoro vive in APPDATA (`Intelleo PDF Splitter`), non va committato |
| Licenza | Cartella `Licenza/` fuori da git. Non loggare payload, chiavi o HWID reali |
| Segreti | Non introdurre credenziali, UNC o IP interni in codice nuovo, wiki o log. I percorsi di rete già nel sorgente si citano per simbolo (`version.NETWORK_UPDATE_PATH`, `version.UPDATE_URL`) |
| Test | Se il codice toccato ha già un test, eseguirlo. `tests/conftest.py` crea `QApplication` prima degli import GUI |
| Wiki-sync | Se cambi un `.py` in `src/`, esegui `.venv\Scripts\python.exe scripts\check_wiki_sync.py`. Esce con 0. Se avvisa, aggiorna nello stesso task la pagina del modulo, senza chiedere. Protocollo: [`wiki/isab/workflows/pre_commit_wiki_protocol.md`](wiki/isab/workflows/pre_commit_wiki_protocol.md) |
| Commit | Solo se l’utente lo chiede |

## Stack

Python ≥ 3.10 · PySide6 · PyMuPDF · Tesseract tramite pytesseract · Pillow · config JSON · pytest

## Ambiente Windows

| Scenario | Comando |
|----------|---------|
| Avvio app | `launch.bat` (crea `.venv`, installa `src/requirements.txt`, esegue `src/app_launcher.py`) |
| Pytest mirato | `.venv\Scripts\python.exe -m pytest tests\<file>.py -q` |
| Ruff sul file toccato | `.venv\Scripts\ruff.exe check <file>` |
| Catena comandi | Una chiamata per comando. Niente `&&` in CMD legacy |

## Cosa non è stato portato da Vertex

Lens, vault manuali, bot Playwright, MCP di dominio, account di login web e briefing di campagna in `.agents/` non hanno un equivalente qui. La conoscenza vive in `wiki/isab/` e nei `GEMINI.md`.
