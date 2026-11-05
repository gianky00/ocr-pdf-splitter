---
name: isab-elaborazione
description: >-
  Pipeline di divisione PDF per allegati ISAB: OCR sulle ROI, tre stadi di match,
  split per categoria, archivio ORIGINALI. Usarla quando il task tocca core/pdf,
  analisi, regole, Tesseract o i nomi dei file generati.
---

# ISAB — elaborazione PDF

## Quando usarla

Modifiche a `src/core/pdf_processor.py`, `analysis_service.py`, `ocr_engine.py`, `tesseract_manager.py`, `pdf_splitter.py`, `archive_service.py`, `file_service.py`, `processing_worker.py`, `rule_service.py`, `roi_manager.py`, `classifier.py`.

## Leggere

1. `wiki/isab/modules/elaborazione.md`
2. `wiki/isab/modules/classificazione.md`
3. `src/core/GEMINI.md`

## Invarianti

- `process_pdf` orchestra. Il worker è l’unico chiamante di produzione.
- Il match è a tre stadi sulle ROI, in ordine di regola. La prima keyword vince.
- `DocumentClassifier.classify_text` non è sul percorso di split.
- Una regola senza ROI non classifica pagine.
- Output: `{odc}_{suffix}.pdf`, sconosciuto `{odc}_SCONOSCIUTO_{stem}.pdf`.
- I PDF sotto `ORIGINALI` non rientrano nell’ingresso.
- Senza `tesseract_path` valido la pipeline esce prima di aprire il documento.
- Non spostare OCR o split sul thread Qt.

## Verifica

Eseguire i test del file toccato tra `tests/test_pdf_processor.py`, `test_analysis_service.py`, `test_ocr_engine.py`, `test_pdf_splitter.py`, `test_processing_worker.py`, `test_rule_service.py`.
