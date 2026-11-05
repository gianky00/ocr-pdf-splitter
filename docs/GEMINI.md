# Intelleo PDF Splitter — guida operativa agenti

Non è il grafo architetturale. Quello è [`../wiki/isab/INDEX.md`](../wiki/isab/INDEX.md).

Boot: [`../AGENTS.md`](../AGENTS.md) → [`../wiki/INDEX.md`](../wiki/INDEX.md) → wiki/isab.

## Dove trovare cosa

| Bisogno | Dove |
|---------|------|
| Flussi, moduli, protocolli | [`../wiki/isab/INDEX.md`](../wiki/isab/INDEX.md) |
| Pipeline e OCR | [`../wiki/isab/modules/elaborazione.md`](../wiki/isab/modules/elaborazione.md) |
| Regole e ROI | [`../wiki/isab/modules/classificazione.md`](../wiki/isab/modules/classificazione.md) |
| Note codice | `src/GEMINI.md`, `src/core/GEMINI.md`, `src/gui/GEMINI.md`, `src/shared/GEMINI.md` |
| Presentazione utente | [`../README.md`](../README.md) |
| Rilascio | `release_patch.bat` e `admin/Crea Setup/build_dist.py`, sotto |

## Comandi

PowerShell, dalla root del repository.

| Azione | Comando |
|--------|---------|
| Avvio | `.\launch.bat` |
| Test di un file | `.venv\Scripts\python.exe -m pytest tests\<file>.py -q` |
| Test del corredo agente | `.venv\Scripts\python.exe -m pytest tests\test_agent_kit.py -q` |
| Ruff | `.venv\Scripts\ruff.exe check <file>` |
| Avviso wiki | `.venv\Scripts\python.exe scripts\check_wiki_sync.py` |
| Suite qualità | `.\scripts\run_quality_checks.bat` |
| Suite senza coverage | `.\scripts\run_quality_checks.bat --skip-coverage` |
| Auto-fix Ruff | `.\scripts\run_quality_checks.bat --fix` |

`pyproject.toml` punta i test a `tests/` e la coverage a `src/` con soglia 50. `launch.bat` installa `src/requirements.txt` nel `.venv`.

`scripts/run_quality_checks.bat` lancia `scripts/run_quality_checks.py`. I bloccanti sono Ruff e pytest; `pytest --cov` parte dopo, con la soglia già in `pyproject.toml`, e si esclude con `--skip-coverage`. `--skip-tests` esclude pytest e coverage. Mypy, Bandit, `scripts/check_wiki_sync.py` e gli altri strumenti del gruppo `dev` in `pyproject.toml` sono avvisi: se il modulo manca, il report lo segna non disponibile. L'esito del processo è quello dei bloccanti. Il report sta in `logs/quality_report.log`. I tool di sviluppo si installano con `uv sync --group dev --inexact`: il flag lascia nel `.venv` i pacchetti già installati da `launch.bat`.

Python del progetto: `.venv\Scripts\python.exe`. Il `python` di sistema non vede le dipendenze.

`scripts/check_wiki_sync.py` legge `git status` e termina sempre con 0. Se un `.py` sotto `src/` è cambiato e nessun `.md` sotto `wiki/isab/` lo è, stampa un avviso. Una cartella `wiki/` non tracciata conta come i markdown che contiene: git la riporta come directory e lo script la espande. L’avviso si chiude nello stesso task, aggiornando la pagina del modulo. Un `GEMINI.md` aggiornato da solo non spegne l’avviso. Protocollo: [`../wiki/isab/workflows/pre_commit_wiki_protocol.md`](../wiki/isab/workflows/pre_commit_wiki_protocol.md).

## Rilascio

Non lanciare questi script durante una modifica ordinaria: fanno bump di versione, build e copia del setup.

| Comando | Effetto |
|---------|---------|
| `release_patch.bat` | Esegue `pytest`, poi `bump_version.py` patch, poi `build_dist.py`. Lo script di build, senza `--no-bump`, incrementa la versione una seconda volta |
| `release_patch_no_Deploy.bat` | Stesso percorso, con `build_dist.py --no-deploy` |

`build_dist.py` offusca con PyArmor, impacchetta con PyInstaller e prepara il setup Inno. Flag:

| Flag | Effetto |
|------|---------|
| `--no-deploy` | Salta Netlify. La copia in rete resta |
| `--no-network` | Salta la copia in rete |
| `--no-bump` | Non incrementa la versione dentro lo script di build |
| `--minor` / `--major` | Tipo di bump, se il bump non è disattivato |

Il percorso di rete è la costante `NETWORK_DEPLOY_PATH` in quello script. Non va ricopiato in wiki o log. I vecchi setup sulla share finiscono in una cartella `Archivio` accanto alla destinazione. Il nome del sito Netlify usato dallo script è `intelleo-pdf-splitter`.

## Dati di runtime

| Voce | Posizione |
|------|-----------|
| Config | `%APPDATA%\Intelleo PDF Splitter\config.json` |
| Sessione | stessa cartella, `session.json` |
| Tesseract | chiave `tesseract_path` nella config. Eseguibile esterno, di solito sotto `C:\Program Files\Tesseract-OCR\` |
| Licenza | `Licenza/` accanto all’eseguibile o alla root di sviluppo. Non in git |
| Versione | `src/version.py` (`__version__`) |

## Checklist prima di chiudere

- [ ] Test esistente sul perimetro eseguito.
- [ ] `.venv\Scripts\python.exe scripts\check_wiki_sync.py` eseguito. Se avvisa, la pagina del modulo è aggiornata nello stesso task.
- [ ] Nessun file di config utente, licenza o log aggiunto al commit.
- [ ] OCR e split non spostati sul thread della UI.
