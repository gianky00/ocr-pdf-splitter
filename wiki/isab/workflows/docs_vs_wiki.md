# Docs ops vs wiki

| Path | Ruolo | Si aggiorna quando |
|------|--------|--------------------|
| [`../../INDEX.md`](../../INDEX.md) | Hub sezioni | Cambia il layout delle sezioni |
| [`../INDEX.md`](../INDEX.md) | Grafo codice | Nasce un nodo, cambia un flusso, un contratto o un protocollo |
| [`../../../docs/GEMINI.md`](../../../docs/GEMINI.md) | Comandi, percorsi, checklist | Cambiano comandi o dove stanno i dati |
| [`../../../src/GEMINI.md`](../../../src/GEMINI.md) e `src/<area>/GEMINI.md` | Note del codice toccato | Cambiano entrypoint, segnali, freeze o il file da aprire per primo |
| [`../../../docs/prompts/`](../../../docs/prompts/) | Prompt storici di analisi | Non sono la mappa corrente |
| [`../../../prompt/`](../../../prompt/) | Campagne di qualità storiche. Il boot resta `AGENTS.md` | Non sono la mappa corrente |
| [`../../../README.md`](../../../README.md) | Presentazione utente | Solo se cambia l’uso visibile |

## Boot

`AGENTS.md` → `wiki/INDEX.md` → `wiki/isab/INDEX.md` → `docs/GEMINI.md` se servono i comandi → `GEMINI.md` dell’area toccata.

Se wiki e `GEMINI.md` divergono, vince il codice e si aggiornano entrambi.
