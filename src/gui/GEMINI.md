# `src/gui`

Wiki: [`../../wiki/isab/modules/gui.md`](../../wiki/isab/modules/gui.md).

## Note agente

- I tab non possiedono la pipeline. Emettono azioni verso `MainApp` / `AppController`.
- `theme.py` va importato solo dopo `QApplication`. Il conftest dei test lo garantisce.
- Colori e QSS stanno in `theme.py`. Un dialogo nuovo usa `COLORS`, non una palette parallela.
- `unknown_review.py` può toccare `SessionManager`. Il resto dei dialoghi no, salvo richiesta esplicita.
- L’utility di disegno non è in questo package: è `src/roi_utility.py`.

## File

| Path | Ruolo |
|------|--------|
| `tabs/dashboard_tab.py` | Elaborazione e contatori |
| `tabs/config_tab.py` | Tesseract e regole |
| `tabs/help_tab.py` | Tab «Guida» |
| `dialogs/rule_editor.py` | Campi della regola |
| `dialogs/unknown_review.py` | Revisione non classificati |
| `dialogs/roi_selector_dialog.py` | Scelta categoria e coordinate |
| `widgets/drop_frame.py` | Drag and drop |
| `widgets/roi_renderer.py` | Disegno ROI su `QGraphicsScene` per `roi_utility.py`. Scala `(150 * zoom) / 72`. Coordinate diverse da 4 numeri non disegnano nulla |
| `widgets/preview_view.py` | Anteprima |
| `widgets/pdf_graphics_view.py` | Vista pagina |
| `widgets/page_thumbnail.py` | Miniature |
| `widgets/splash_screen.py` | Avvio |
| `ui_factory.py` | Bottoni e widget condivisi |
| `animations.py` | Animazioni UI |
| `theme.py` | Token visivi |

## Test

`tests/test_dashboard_tab.py`, `test_config_tab.py`, `test_ui_factory.py`, `test_unknown_review.py`, `test_pdf_graphics_view.py`, `test_splash_screen.py`.
