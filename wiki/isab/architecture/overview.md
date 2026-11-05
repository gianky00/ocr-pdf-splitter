# Architettura

Applicazione desktop Windows. Divide un PDF multipagina in PDF per categoria, usando keyword cercate dentro aree ROI. Il codice ODC entra nel nome dei file prodotti.

## Processi

| Pezzo | File | Ruolo |
|-------|------|--------|
| Avvio | `src/app_launcher.py` | Mette `src/` sul path, controlla la licenza, apre la GUI oppure l’utility ROI |
| View | `src/main.py` (`MainApp`) | Finestra, tab, coda log, non contiene la pipeline PDF |
| Controller | `src/core/app_controller.py` | Licenza, regole, sessione, avvio worker. Parla con la view solo via `Signal` |
| Worker | `src/core/processing_worker.py` | Thread separato. Chiama `core.pdf_processor.process_pdf` |
| Pipeline | `src/core/pdf_processor.py` | OCR → analisi → split → archivio `ORIGINALI` |

`launch.bat` esegue `.venv\Scripts\python.exe src/app_launcher.py`.

## Dati

| Dato | Dove |
|------|------|
| Config di lavoro | `%APPDATA%\Intelleo PDF Splitter\config.json` (`core.path_manager.PathManager.get_app_data_dir`) |
| Template regole | `config.json` nella root del repo, usato solo se l’APPDATA non ha `classification_rules` |
| Sessione interrotta | `session.json` nella stessa cartella APPDATA (`shared.constants.SESSION_FILE`) |
| Segnale ROI | file `.update_signal` (`shared.constants.SIGNAL_FILE`) |
| Log diagnostici | scritti da `src/app_logger.py`, da importare prima del resto in fase di avvio |
| Licenza | cartella `Licenza/`, non in git |

Salvataggio config: scrittura su file `.tmp` e poi replace (`ConfigManager.save_config`).

## Confini

- PyInstaller: `sys.frozen` e `_MEIPASS` cambiano base dir e asset (`PathManager`).
- Tesseract è un eseguibile esterno. Senza `tesseract_path` valido `process_pdf` si ferma prima dell’analisi.
- `OMP_THREAD_LIMIT=1` è impostato da `OcrEngine` perché le pagine girano già in parallelo.
- `DocumentClassifier` è istanziato da `AnalysisService` ma il match di pagina non chiama `classify_text`. Il percorso reale è in [`../modules/classificazione.md`](../modules/classificazione.md).

## Test

`tests/conftest.py` inserisce `src/` in `sys.path` e crea `QApplication` prima di ogni import che tocchi font o icone Qt.
