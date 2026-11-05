# Wiki — Hub

Knowledge graph del repository, radicato su `wiki/`.

## Boot agenti

1. Leggere [`AGENTS.md`](../AGENTS.md)
2. Aprire questo hub, poi il grafo della sezione pertinente
3. Per lavoro sul codice: [`isab/INDEX.md`](isab/INDEX.md)

## Albero

```
wiki/
├── INDEX.md          questo hub
├── README.md         alias di navigazione
└── isab/             grafo codice (agenti)
    ├── architecture/
    ├── modules/
    └── workflows/
```

## Sezioni

| Sezione | Path | Contenuto |
|---------|------|-----------|
| Codice | [`isab/INDEX.md`](isab/INDEX.md) | Architettura, moduli, protocolli agente |
| Ops | [`../docs/GEMINI.md`](../docs/GEMINI.md) | Comandi, percorsi dati, checklist. Non è il grafo |

## Note

- Sync obbligatorio su modifiche di flusso, contratto regole/ROI o protocolli agente: [`isab/workflows/pre_commit_wiki_protocol.md`](isab/workflows/pre_commit_wiki_protocol.md).
- Split ops vs wiki: [`isab/workflows/docs_vs_wiki.md`](isab/workflows/docs_vs_wiki.md).
- Questo hub non è un corpus RAG e non contiene manuali di impianto.
