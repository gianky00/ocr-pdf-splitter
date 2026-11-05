# Regole Cursor e skill

Le `.mdc` iniettano vincoli. La conoscenza sta in `wiki/isab/` e nei `GEMINI.md`. Se divergono, vince il codice, poi la wiki.

## Always-on

| Regola | Solo questo |
|--------|-------------|
| `agents-wiki-boot` | Ordine di lettura e quando fare wiki-sync |
| `isab-agent-guidance` | Diff, test, comandi Windows, segreti, thread GUI |
| `lingua-italiano` | Risposte in italiano |
| `superpowers-invoke` | Skill Superpowers del plugin, lette dal file corrente |
| `isab-rules-index` | Questa mappa |

## Glob

| Regola | Trigger |
|--------|---------|
| `python-pyside` | `src/**/*.py` |

## Skill di progetto

Catalogo: `.agents/isab-skills.json`.

| Skill | Quando |
|-------|--------|
| `isab-rules` | Qualsiasi task sul repository |
| `isab-elaborazione` | Pipeline PDF, OCR, regole, ROI, nomi file |
| `isab-ui` | Tab, dialoghi, tema, segnali Qt |

La copia canonica è `.agents/skills/<nome>/`. `.cursor/skills/<nome>/` è il mirror. Vanno tenute uguali.

Le skill generiche (debug, TDD, verifica, review) stanno nel plugin Superpowers, non in questo repo.

## Hook

`.cursor/hooks.json` avvia `.cursor/hooks/session_start.cjs` su `sessionStart`. Il hook ricorda il boot. Non duplica la wiki.
