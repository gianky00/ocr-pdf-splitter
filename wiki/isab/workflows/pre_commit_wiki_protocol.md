# Protocollo wiki-sync

## Boot

1. `AGENTS.md`
2. `wiki/INDEX.md`
3. `wiki/isab/INDEX.md` e il nodo del task
4. Solo dopo: codice, test, consegna

Env e comandi stanno in `docs/GEMINI.md`, non nelle pagine di architettura.

## Quando aggiornare

Prima di considerare chiuso un task, aggiornare `wiki/isab/` se è cambiato almeno uno di questi:

1. Ordine della pipeline PDF, thread, o punto di ingresso (`app_launcher`, `process_pdf`, worker).
2. Contratto di `classification_rules` (campi, match, nomi file, cartella `ORIGINALI`).
3. Segnali di `AppController` o tab e dialoghi che l’utente vede.
4. Dove vive config, sessione o licenza.
5. `AGENTS.md`, `.cursor/rules/`, skill di progetto, hook di sessione.

Aggiornare `wiki/isab/INDEX.md` se nasce un nodo. Aggiornare `wiki/INDEX.md` solo se cambia il layout delle sezioni. Aggiornare il `GEMINI.md` dell’area se cambia l’entrypoint o il file da leggere per primo.

## Checklist

- [ ] Boot letto.
- [ ] Modifica limitata al comportamento chiesto.
- [ ] Test già presente sul codice toccato eseguito. Se è rosso, correzione nel codice appena toccato o nel test.
- [ ] Wiki e `GEMINI.md` allineati al codice.
- [ ] `.venv\Scripts\python.exe scripts\check_wiki_sync.py` letto. Esce sempre con 0. Se avvisa e il cambiamento è in questo elenco, la wiki manca ancora. Un avviso su un ritocco interno che non è in elenco si può lasciare.
- [ ] Nessun segreto, HWID, UNC o IP nuovo nei file aggiunti.
