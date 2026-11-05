# ISAB — LLM Wiki

Grafo di conoscenza per agenti che lavorano su Intelleo PDF Splitter (rilevamento e divisione allegati PDF per codice ODC).

Hub: [`../INDEX.md`](../INDEX.md). Ops: [`../../docs/GEMINI.md`](../../docs/GEMINI.md).

## Grafo

```
                     wiki/isab/INDEX.md
                             |
     +-----------------------+------------------------+
     |                       |                        |
architecture/overview   modules/overview        workflows/pre_commit_wiki_protocol
     |                       |                        |
glossario              elaborazione            docs_vs_wiki
                       classificazione         cursor_rules
                       gui
                       licenza_aggiornamenti
```

## Architettura

- [`architecture/overview.md`](architecture/overview.md) — processi, thread, dati, confini.
- [`architecture/glossario.md`](architecture/glossario.md) — ODC, ROI, ORIGINALI, sessione, HWID.

## Moduli

- [`modules/overview.md`](modules/overview.md) — tabella area, file, test.
- [`modules/elaborazione.md`](modules/elaborazione.md) — dal PDF in ingresso ai file divisi.
- [`modules/classificazione.md`](modules/classificazione.md) — regole, ROI, tre stadi, nomi file.
- [`modules/gui.md`](modules/gui.md) — finestra PySide6, tab, dialoghi, utility ROI.
- [`modules/licenza_aggiornamenti.md`](modules/licenza_aggiornamenti.md) — licenza locale, update, launcher, log.

## Workflow agente

- [`workflows/pre_commit_wiki_protocol.md`](workflows/pre_commit_wiki_protocol.md)
- [`workflows/docs_vs_wiki.md`](workflows/docs_vs_wiki.md)
- [`workflows/cursor_rules.md`](workflows/cursor_rules.md)
