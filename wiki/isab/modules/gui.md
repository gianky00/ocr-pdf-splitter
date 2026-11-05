# GUI

`MainApp` in `src/main.py` è la view. Costruisce tre tab e riceve i `Signal` di `AppController`.

| Superficie | File | Cosa fa |
|------------|------|---------|
| Dashboard | `gui/tabs/dashboard_tab.py` | ODC, drop PDF, avvio, progresso, contatori |
| Configurazione | `gui/tabs/config_tab.py` | Tesseract, elenco regole, apre l’editor |
| Guida | `gui/tabs/help_tab.py` | Tab con etichetta «Guida» |
| Editor regola | `gui/dialogs/rule_editor.py` | Categoria, suffisso, keyword, colore, conteggio ROI |
| Revisione sconosciuti | `gui/dialogs/unknown_review.py` | Assegna a mano i file non classificati, poi elimina il PDF locale. Usa `SessionManager` |
| Selezione ROI | `gui/dialogs/roi_selector_dialog.py` | Dialogo categorie e coordinate |
| Utility ROI | `src/roi_utility.py` | Finestra standalone di disegno. Persiste via `RoiManager`. Il disegno degli item è `gui/widgets/roi_renderer.py` (`ROIRenderer`) |
| Tema | `gui/theme.py` | `COLORS`, `FONTS`, `GLOBAL_QSS`. Importarlo crea oggetti Qt: nei test ci pensa `conftest.py` |
| Widget | `gui/widgets/` | `drop_frame`, `roi_renderer`, `preview_view`, `pdf_graphics_view`, `page_thumbnail`, `splash_screen` |
| Factory | `gui/ui_factory.py` | `AnimatedButton` e costruzione widget condivisa |
| Toast | `core/notification_manager.py` | Notifiche sopra la finestra |

## Segnali del controller

`log_received`, `progress_updated`, `license_status_updated`, `processing_state_changed`, `rules_updated`, `session_status_changed`, `unknown_files_found`, `stats_updated`.

`log_received` porta messaggio, livello e un bool. `MainApp.add_log_message` e `NotificationManager.on_controller_log` leggono solo messaggio e livello.

Aggiungere uno stato visibile significa estendere un segnale esistente o uno nuovo, poi collegarlo in `MainApp`. Non leggere la config dal widget se il controller la possiede già.

## Drop e anteprima

`DropFrame` accetta file e cartelle. L’anteprima pagina sta nei widget grafici PyMuPDF, non nella pipeline di split.
