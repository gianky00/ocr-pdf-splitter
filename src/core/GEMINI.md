# `src/core`

Mappa per chi modifica pipeline, regole, sessione o notifiche.

Wiki: [`../../wiki/isab/modules/elaborazione.md`](../../wiki/isab/modules/elaborazione.md), [`../../wiki/isab/modules/classificazione.md`](../../wiki/isab/modules/classificazione.md). Ops: [`../../docs/GEMINI.md`](../../docs/GEMINI.md).

## Note agente

- `process_pdf` è l’unica orchestrazione dello split. Non duplicarla nel controller.
- Il match di pagina è `_analyze_single_page_standalone` (tre stadi sulle ROI). `DocumentClassifier.classify_text` non è sul percorso.
- `ProcessingWorker` è un `threading.Thread`. La view consuma `log_queue` con il timer del controller.
- `PdfSplitter` accoda a un PDF di categoria già presente. Lo sconosciuto include lo stem del file originale per non collidere.
- `ArchiveService` e `FileService` trattano la cartella `ORIGINALI` come archivio, non come input.
- `OcrEngine` scrive `OMP_THREAD_LIMIT` nell’ambiente del processo.
- `SessionManager` legge e scrive `shared.constants.SESSION_FILE`.
- `RoiManager` è la persistenza usata dall’utility ROI. Il CRUD regole della GUI passa da `RuleService`.

## File

| File | Ruolo |
|------|--------|
| `pdf_processor.py` | `process_pdf` |
| `analysis_service.py` | Gruppi di pagine, parallelismo |
| `classifier.py` | Match su testo intero, oggi non chiamato dallo split |
| `ocr_engine.py` | Tesseract, scan e scan robusto |
| `tesseract_manager.py` | `auto_detect` e `is_valid` per il pulsante Auto-Rileva in `main.py`. Non apre il PDF: `process_pdf` esige comunque `tesseract_path` già valido |
| `pdf_splitter.py` | Scrittura PDF per categoria |
| `archive_service.py` | Spostamento in `ORIGINALI` |
| `file_service.py` | Ricerca PDF in ingresso |
| `processing_worker.py` | Thread di batch |
| `app_controller.py` | Stato applicativo e segnali |
| `rule_service.py` | CRUD regole sulla dict di config |
| `roi_manager.py` | Load/save ROI |
| `roi_controller.py` | Controller dell’utility ROI: navigazione, zoom, collega `RoiManager` e `PdfManager`. Il suo `SIGNAL_FILE` è `.update_signal` |
| `session_manager.py` | `session.json` |
| `path_manager.py` | Base dir, APPDATA, asset, bundle |
| `notification_manager.py` | Toast Qt |
| `pdf_manager.py` | Apertura e rendering pagine per la GUI (DPI default 150). Non è lo split |

## Test

`tests/test_pdf_processor.py`, `test_analysis_service.py`, `test_ocr_engine.py`, `test_pdf_splitter.py`, `test_processing_worker.py`, `test_rule_service.py`, `test_app_controller.py`, `test_session_manager_core.py`.
