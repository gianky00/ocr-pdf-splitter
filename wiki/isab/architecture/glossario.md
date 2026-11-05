# Glossario

| Termine | Significato nel codice |
|---------|------------------------|
| ODC | Codice commessa inserito in GUI. Prefisso dei PDF generati |
| ROI | Rettangolo `[x0, y0, x1, y1]` in punti PDF, salvato in `classification_rules[].rois` |
| Regola | `category_name`, `keywords`, `filename_suffix`, `color`, `rois` |
| Categoria `sconosciuto` | Nessuna keyword trovata nelle ROI. File `{odc}_SCONOSCIUTO_{nome_originale}.pdf` |
| ORIGINALI | Sottocartella in cui `ArchiveService` sposta il PDF sorgente dopo lo split. `FileService` non rilegge i PDF che stanno già lì |
| Sessione | `session.json` con task e ODC, per riprendere un’elaborazione interrotta |
| HWID | Identificativo macchina usato dal validatore licenza. Non va copiato in wiki, log o test committati |
| Utility ROI | Finestra separata `src/roi_utility.py` per disegnare le aree e salvarle sulla regola |
