# Intelleo PDF Splitter

<div align="center">

![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

**Applicazione professionale per la divisione automatica di PDF basata su OCR**

</div>

---

## 📋 Descrizione

Intelleo PDF Splitter è un'applicazione desktop Windows che permette di dividere automaticamente documenti PDF multipagina in base al contenuto riconosciuto tramite OCR (Optical Character Recognition).

### Funzionalità Principali

- 🔍 **Riconoscimento OCR** - Analisi automatica del contenuto delle pagine
- 📂 **Classificazione Intelligente** - Smistamento pagine in base a regole configurabili
- 🎯 **Aree ROI Personalizzabili** - Definizione visuale delle zone di ricerca
- 📊 **Dashboard Integrata** - Monitoraggio stato, statistiche e attività
- 🔄 **Drag & Drop** - Trascinamento diretto di file e cartelle
- 📝 **Revisione Manuale** - Interfaccia per gestire file non riconosciuti

---

## 🚀 Installazione

### Requisiti

- **Windows 10/11**
- **Python 3.10+**
- **Tesseract OCR** - [Download](https://github.com/UB-Mannheim/tesseract/wiki)

### Setup Rapido

1. **Clona il repository**
   ```bash
   git clone <repository-url>
   cd rilevamento-allegati-isab
   ```

2. **Avvia l'applicazione**
   ```bash
   launch.bat
   ```
   Questo script creerà automaticamente l'ambiente virtuale e installerà le dipendenze.

### Configurazione Tesseract

Al primo avvio, configura il percorso di Tesseract:
1. Vai nella tab **Configurazione**
2. Clicca su **Auto-Rileva** o **Sfoglia**
3. Seleziona `tesseract.exe` (di solito in `C:\Program Files\Tesseract-OCR\`)

---

## 📖 Guida all'Uso

### 1️⃣ Configurazione Regole

Ogni regola di classificazione definisce:
- **Nome Categoria** - Es. "consuntivo", "rapportini"
- **Suffisso File** - Aggiunto al nome del file generato
- **Keywords** - Parole chiave da cercare via OCR
- **Colore** - Per identificazione visiva
- **Aree ROI** - Zone della pagina dove cercare

### 2️⃣ Definizione ROI

1. Clicca su **Utility ROI** nella tab Configurazione
2. Apri un PDF di esempio
3. **Disegna un rettangolo** sull'area di interesse
4. Associa la ROI a una categoria
5. Le modifiche vengono salvate automaticamente

### 3️⃣ Elaborazione PDF

1. Vai nella tab **Dashboard**
2. Inserisci il **Codice ODC**
3. **Trascina** i file PDF oppure clicca su **Seleziona PDF**
4. L'elaborazione parte automaticamente

### 4️⃣ Output

- I PDF vengono divisi nella **stessa cartella** del file originale
- I file originali vengono spostati in una sottocartella `ORIGINALI`
- I file non riconosciuti possono essere rinominati manualmente

---

## ⌨️ Scorciatoie

| Tasto | Azione |
|-------|--------|
| `←` `→` | Navigazione pagine |
| `↑` `↓` | Navigazione file (revisione) |
| `Rotella mouse` | Zoom anteprima |
| `Ctrl + Rotella` | Zoom ROI Utility |

---

## 📁 Struttura Progetto

```
rilevamento-allegati-isab/
├── launch.bat                 # Crea .venv, installa src/requirements.txt, avvia l'app
├── src/
│   ├── app_launcher.py        # Entrypoint
│   ├── main.py                # Finestra principale
│   ├── version.py             # Versione applicativa
│   ├── core/                  # Pipeline PDF, OCR, regole, sessione
│   ├── gui/                   # Tab, dialoghi, tema PySide6
│   └── requirements.txt
├── tests/
├── wiki/                      # Mappa per gli agenti
├── docs/GEMINI.md             # Comandi e rilascio
└── Licenza/                   # File licenza (non in git)
```

La config di lavoro non è il `config.json` della root: sta in `%APPDATA%\Intelleo PDF Splitter\`. La versione numerica è `src/version.py`. L'avvio è `src/app_launcher.py`.

---

## 🔧 Dipendenze

| Pacchetto | Descrizione |
|-----------|-------------|
| `PySide6` | Interfaccia |
| `PyMuPDF` | Elaborazione PDF |
| `Pillow` | Manipolazione immagini |
| `pytesseract` | Wrapper Tesseract OCR |
| `cryptography` | Gestione licenze |
| `requests` | Comunicazione HTTP |
| `packaging` | Gestione versioni |

---

## 🔐 Licenza

Questo software richiede una licenza valida per funzionare.
La licenza è vincolata all'Hardware ID della macchina.

Per richiedere una licenza, contattare il supporto tecnico Intelleo.

---

## Agenti IA

Boot: [`AGENTS.md`](AGENTS.md) → [`wiki/INDEX.md`](wiki/INDEX.md) → [`wiki/isab/INDEX.md`](wiki/isab/INDEX.md). Comandi e rilascio: [`docs/GEMINI.md`](docs/GEMINI.md).

## 📞 Supporto

Per assistenza tecnica o segnalazione bug:
- Email: supporto@intelleo.it
- Telefono: [Inserire numero]

---

<div align="center">
<sub>© 2024 Intelleo - Tutti i diritti riservati</sub>
</div>
