---
name: isab-ui
description: >-
  Interfaccia PySide6 di Intelleo PDF Splitter: tab, dialoghi, tema, segnali
  del controller, utility ROI. Usarla per modifiche visibili o ai widget.
---

# ISAB — UI PySide6

## Quando usarla

Modifiche a `src/main.py`, `src/gui/` (incluso `widgets/roi_renderer.py`), `src/roi_utility.py`, `src/core/app_controller.py` (segnali), `src/core/notification_manager.py`, `src/core/roi_controller.py`, `src/core/pdf_manager.py`.

## Leggere

1. `wiki/isab/modules/gui.md`
2. `src/gui/GEMINI.md`
3. `gui/theme.py` prima di introdurre colori o QSS nuovi

## Invarianti

- La view non chiama `process_pdf`.
- Stato nuovo verso la finestra: segnale di `AppController`, collegato in `MainApp`.
- Token visivi: `COLORS`, `FONTS`, `GLOBAL_QSS`. Niente palette parallela.
- `theme.py` si importa dopo `QApplication`. I test passano da `tests/conftest.py`.
- Il disegno ROI vive in `roi_utility.py` e `ROIController`, non nella dashboard.

## Verifica

Eseguire il test GUI del file toccato. Un test verde non sostituisce il controllo della finestra se il task cambia ciò che l’utente vede: dichiarare se la GUI non è stata aperta.
