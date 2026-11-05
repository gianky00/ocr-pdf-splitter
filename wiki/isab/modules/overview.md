# Moduli

| Area | Responsabilità | Note agente | Test già presenti |
|------|----------------|-------------|-------------------|
| Pipeline PDF | Analisi, split, archivio, worker | [`../../../src/core/GEMINI.md`](../../../src/core/GEMINI.md) | `test_pdf_processor.py`, `test_pdf_splitter.py`, `test_analysis_service.py`, `test_ocr_engine.py`, `test_processing_worker.py` |
| Regole e ROI | CRUD regole, coordinate | stessa nota `core` | `test_rule_service.py`, `test_roi_utility.py` |
| GUI | Tab, dialoghi, tema | [`../../../src/gui/GEMINI.md`](../../../src/gui/GEMINI.md) | `test_config_tab.py`, `test_dashboard_tab.py`, `test_ui_factory.py`, `test_unknown_review.py`, `test_pdf_graphics_view.py`, `test_splash_screen.py` |
| Avvio, licenza, update, config | Entrypoint e persistenza | [`../../../src/GEMINI.md`](../../../src/GEMINI.md) | `test_main.py`, `test_app_launcher.py`, `test_app_controller.py`, `test_license_validator.py`, `test_license_updater.py`, `test_app_updater.py`, `test_config_manager.py`, `test_app_logger.py`, `test_session_manager_core.py`, `test_session_management.py` |
| Condiviso | Path di sessione, sanitize HTML | [`../../../src/shared/GEMINI.md`](../../../src/shared/GEMINI.md) | coperto dai test di sessione |

Dettaglio flussi: [`elaborazione.md`](elaborazione.md), [`classificazione.md`](classificazione.md), [`gui.md`](gui.md), [`licenza_aggiornamenti.md`](licenza_aggiornamenti.md).
