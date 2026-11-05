# `src/` — entrypoint fuori dai package

Leggere prima [`../wiki/isab/INDEX.md`](../wiki/isab/INDEX.md) e [`../docs/GEMINI.md`](../docs/GEMINI.md). I package hanno la propria nota: `core/GEMINI.md`, `gui/GEMINI.md`, `shared/GEMINI.md`.

## File

| File | Ruolo |
|------|--------|
| `app_launcher.py` | Entrypoint. Path, licenza, scelta GUI o utility ROI |
| `main.py` | `MainApp`, view Qt |
| `app_logger.py` | Log su file. Importarlo prima del resto in fase di avvio |
| `config_manager.py` | Load/save JSON atomico. APPDATA, fallback al `config.json` di root se mancano le regole |
| `license_validator.py` | Licenza locale Fernet + HWID |
| `license_updater.py` | Aggiornamento licenza online |
| `app_updater.py` | Setup applicazione, web e rete. Citare `version.UPDATE_URL` e `version.NETWORK_UPDATE_PATH`, non ricopiare gli indirizzi |
| `version.py` | `__version__` e i due canali di update |
| `roi_utility.py` | Finestra di disegno ROI |
| `generate_icon.py` | Utility icona, esclusa dalla coverage |

## Freeze

- Non spostare l’entrypoint da `app_launcher.py` senza aggiornare `launch.bat` e `wiki/isab/modules/licenza_aggiornamenti.md`.
- Non loggare payload di licenza o HWID.
- `config.json` di root è template. Il file vivo è in APPDATA.
