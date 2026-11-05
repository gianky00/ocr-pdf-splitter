# `src/shared`

Wiki: [`../../wiki/isab/architecture/overview.md`](../../wiki/isab/architecture/overview.md).

## Note agente

- `constants.py` importa `config_manager` e quindi risolve `CONFIG_DIR` all’import. `SESSION_FILE` è `session.json` in APPDATA. `SIGNAL_FILE` è `.update_signal` nella working directory.
- `security_utils.sanitize_html` toglie `script`, `iframe` e attributi `on*`. È un filtro regex, non un parser HTML. Usarlo sull’HTML mostrato, non come validatore di path o di licenza.

## File

| File | Ruolo |
|------|--------|
| `constants.py` | `SIGNAL_FILE`, `SESSION_FILE` |
| `security_utils.py` | `sanitize_html` |
