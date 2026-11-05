---
name: isab-rules
description: >-
  Bootstrap operativo per lavorare sul repository rilevamento-allegati-isab.
  Impone il boot verso wiki e AGENTS.md e il wiki-sync. Non duplica la pipeline PDF.
---

# ISAB — skill agente (bootstrap)

Questa skill non è la knowledge base. Architettura, regole di classificazione e protocolli stanno in `/wiki` e in `AGENTS.md`.

## Quando usarla

Qualsiasi task su questo repository.

## Boot

1. `AGENTS.md`
2. `wiki/INDEX.md`
3. `wiki/isab/INDEX.md`
4. Nodo wiki del dominio
5. `docs/GEMINI.md` solo per comandi e percorsi
6. `src/core/GEMINI.md`, `src/gui/GEMINI.md`, `src/shared/GEMINI.md` o `src/GEMINI.md`

Protocollo: `wiki/isab/workflows/pre_commit_wiki_protocol.md`.

Se wiki e skill divergono, vince il codice.

## Comportamento

- Rispondi in italiano.
- Diff minimo. Leggi il codice attorno al punto prima di modificarlo.
- Commit e push solo se l’utente lo chiede.
- Pipeline, OCR, ROI: carica `isab-elaborazione`.
- Tab, dialoghi, tema: carica `isab-ui`.
- Prima di dichiarare un test verde, esegui il pytest del file toccato.
- Se hai modificato un `.py` in `src/`, esegui `scripts/check_wiki_sync.py`. L’avviso non fallisce il processo: il protocollo wiki dice se la pagina va aggiornata.
