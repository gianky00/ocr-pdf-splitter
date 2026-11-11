# OCR PDF Splitter & Document Classifier

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![OCR](https://img.shields.io/badge/OCR-Tesseract%20%7C%20PyMuPDF-0284C7?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows%20Desktop-0F172A?style=flat-square)
![Quality](https://img.shields.io/badge/Quality-Ruff%20%7C%20MyPy%20%7C%20Pytest-16A34A?style=flat-square)

Applicazione desktop di **Document Intelligence** progettata per analizzare, classificare e dividere automaticamente fascicoli **PDF multipagina** non strutturati (consuntivi, rapportini tecnici, allegati di commessa, certificazioni) tramite **Optical Character Recognition (OCR)** su **Regioni di Interesse (ROI)** configurabili visivamente.

---

## Architettura & Funzionalità Principali

- **Motore OCR Basato su ROI (`ocr_engine.py` & `roi_manager.py`):** Invece di processare l'intera pagina, l'applicazione estrae e sottopone a **Tesseract OCR** esclusivamente le coordinate rettangolari (ROI) definite dall'utente, massimizzando la precisione di lettura e riducendo drasticamente i tempi di elaborazione.
- **Editor Visuale delle Zone di Ricerca (`roi_controller.py`):** Interfaccia grafica interattiva con zoom e anteprima ad alta risoluzione (`PyMuPDF` + `Pillow`) per disegnare i riquadri di lettura direttamente su un documento PDF campione.
- **Classificazione Deterministica a Regole (`classifier.py` & `rule_service.py`):** Smistamento automatico delle singole pagine in base a parole chiave, codici documento e pattern associati a ciascuna categoria, con raggruppamento e generazione automatica dei file di output.
- **Elaborazione Multi-Thread & Drag-and-Drop (`processing_worker.py`):** Coda di lavorazione asincrona per processare interi lotti di documenti PDF senza bloccare l'interfaccia utente.
- **Interfaccia di Revisione Assistita:** Visualizzatore integrato con scorciatoie da tastiera per ispezionare rapidamente ed assegnare eventuali pagine non riconosciute.

---

## Stack Tecnologico

| Componente | Libreria / Tecnologia |
| :--- | :--- |
| **Rendering & Split PDF** | `PyMuPDF` (`fitz`) |
| **Computer Vision & OCR** | `pytesseract` (Tesseract OCR Engine), `Pillow` (Image Preprocessing) |
| **Interfaccia Desktop** | Python GUI con supporto Drag & Drop nativo (`tkinterdnd2`) |
| **Qualità & Test** | `Ruff`, `MyPy`, `Pytest` |

---

## Struttura del Progetto

```text
rilevamento-allegati-isab/
├── src/
│   ├── core/
│   │   ├── app_controller.py       # Coordinamento logica applicativa
│   │   ├── ocr_engine.py           # Pipeline di pre-processing immagine ed estrazione testo OCR
│   │   ├── pdf_processor.py        # Analisi pagine e orchestrazione del flusso
│   │   ├── pdf_splitter.py         # Costruzione e salvataggio dei PDF suddivisi per categoria
│   │   ├── classifier.py           # Valutazione regole di matching su testo estratto
│   │   ├── roi_manager.py          # Gestione coordinate normalizzate delle Regioni di Interesse
│   │   └── processing_worker.py    # Worker asincrono per elaborazione batch
│   ├── gui/                        # Finestre, dialoghi, animazioni e utility di disegno ROI
│   ├── app_launcher.py             # Entry point dell'applicazione
│   └── config_manager.py           # Persistenza configurazioni e regole di smistamento
└── pyproject.toml                  # Configurazione progetto, Ruff e MyPy
```

---

## Installazione e Utilizzo

### Prerequisiti
- **Python 3.10+**
- **Tesseract OCR** installato sul sistema (es. `C:\Program Files\Tesseract-OCR\tesseract.exe`)

### Avvio Rapido

```powershell
# Clona il repository
git clone https://github.com/gianky00/rilevamento-allegati-isab.git
cd rilevamento-allegati-isab

# Avvia lo script di setup ed esecuzione automatica
launch.bat
```

### Flusso Operativo
1. **Configurazione Regole:** Definisci le categorie documentali, il suffisso di output e le parole chiave da ricercare.
2. **Definizione ROI:** Apri un PDF di riferimento nell'editor ROI e traccia le aree rettangolari in cui compaiono le intestazioni o i codici identificativi.
3. **Elaborazione Batch:** Trascina i fascicoli PDF nell'area di lavoro; il sistema dividerà automaticamente gli allegati rinominandoli secondo la commessa/ODC impostata e archiviando gli originali.

---

## Autore
Progettato e sviluppato da **Giancarlo Allegretti** — *Industrial Automation, Instrumentation & AI Software Engineering*.
