# Elaborazione

Entrypoint della pipeline: `core.pdf_processor.process_pdf(pdf_path, odc, config, progress_callback, cancel_check)`.

Ritorno: `(ok, messaggio, generated, moved_path)`. `generated` è la lista dei file scritti. `moved_path` è il PDF spostato in `ORIGINALI`.

## Ordine

1. Se `cancel_check` è vero: `(False, "Annullato", [], None)`.
2. `config["tesseract_path"]` deve essere un file. Altrimenti esce senza aprire il PDF. Il pulsante Auto-Rileva della GUI usa `TesseractManager.auto_detect` (`src/core/tesseract_manager.py`): cerca `tesseract.exe` sotto Program Files, Program Files (x86) e LocalAppData. Non sostituisce il controllo di `process_pdf`.
3. `OcrEngine` + `AnalysisService(classification_rules, ocr_engine)`.
4. `analyze_pdf` raggruppa gli indici di pagina per categoria. Le pagine sono analizzate in parallelo (`ThreadPoolExecutor`).
5. Il documento si riapre una volta con PyMuPDF. `PdfSplitter.split_and_save` accoda le pagine al PDF di categoria, anche se il file esiste già.
6. `ArchiveService.archive_original` sposta il sorgente in `ORIGINALI`. Se il file è già in quella cartella, non lo sposta.

Il worker (`ProcessingWorker`) gira su un thread e pubblica log e progresso su una coda. Il controller la svuota con un `QTimer` da 50 ms. Non chiamare `process_pdf` dal thread Qt.

## Output

Nella cartella del PDF originale:

- categoria nota: `{odc}_{filename_suffix oppure category_name}.pdf`
- sconosciuto: `{odc}_SCONOSCIUTO_{stem_originale}.pdf`

Salvataggio: file `.tmp`, `deflate=True`, `garbage=3`, poi replace. I retry su `PermissionError` usano `time.sleep` nel worker di produzione, non nei test.

## Ingresso file

`FileService.find_pdfs_in_path` accetta un file o una cartella, cerca `*.pdf` in ricorsione e salta ogni path che contiene il segmento `ORIGINALI`.
