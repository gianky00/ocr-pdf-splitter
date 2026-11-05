# Classificazione

## Contratto regola

Campi usati dal codice:

| Campo | Uso |
|-------|-----|
| `category_name` | Chiave della categoria. Duplicato rifiutato da `RuleService.add_rule` |
| `keywords` | Sottostringhe, confronto in minuscolo |
| `rois` | Lista di quattro numeri. Una ROI è valida se rientra nel rettangolo pagina |
| `filename_suffix` | Nome file. Se assente si usa `category_name` |
| `color` | Solo UI (`RuleEditorDialog`, default `#0D6EFD`) |

`RuleService` modifica la dict di config in memoria. `save` / `save_rules` chiamano `config_manager.save_config`. `add_roi_to_rule` appende le coordinate e non sostituisce le ROI già presenti, salvo il flusso che passa una lista nuova.

## Tre stadi per pagina

Funzione: `_analyze_single_page_standalone` in `src/core/analysis_service.py`.

La prima regola, nella prima ROI, che contiene una keyword vince. Poi la pagina non viene più analizzata.

1. Testo nativo PyMuPDF dentro la ROI (`page.get_text("text", clip=...)`).
2. OCR a 300 DPI, scala `300/72`, `--psm 6` di default, una chiamata per ROI.
3. OCR robusto (`OcrEngine.robust_scan`: contrasto, binarizzazione, rotazioni) solo se i due stadi precedenti non hanno match.

Senza match la categoria è `sconosciuto`.

Una regola senza ROI non partecipa: i tre cicli iterano solo `rois` valide. `DocumentClassifier.classify_text` farebbe un match sull’intero testo, ma `AnalysisService` non lo chiama. Cambiare il classificatore non cambia lo split.

## Timeout OCR

`OcrEngine._DEFAULT_TIMEOUT` è 8 secondi. Il motore imposta `pytesseract.pytesseract.tesseract_cmd` e `OMP_THREAD_LIMIT=1`.
