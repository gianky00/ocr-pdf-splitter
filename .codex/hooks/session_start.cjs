/**
 * sessionStart hook (Node CommonJS).
 * Ricorda il boot. Non duplica la wiki.
 */
const fs = require("fs");

const CONTEXT = `# ISAB — contesto sessione (hook)

Boot obbligatorio: \`AGENTS.md\` → \`wiki/INDEX.md\` → \`wiki/isab/INDEX.md\`, poi il \`GEMINI.md\` dell'area toccata.

1. Pipeline PDF, OCR, regole, ROI: skill \`isab-elaborazione\` e \`wiki/isab/modules/elaborazione.md\`.
2. Tab, dialoghi, tema: skill \`isab-ui\`. OCR e split restano nel \`ProcessingWorker\`.
3. Licenza, updater, launcher: \`src/GEMINI.md\`. Non copiare HWID, salt o path di rete.
4. Comandi e avviso wiki: \`docs/GEMINI.md\` e \`scripts/check_wiki_sync.py\`. Python del repo: \`.venv/Scripts/python.exe\`.

Conoscenza = wiki + \`GEMINI.md\`. Le regole \`.cursor/rules\` sono solo vincoli. Se divergono, vince il codice.
`;

try {
  const input = fs.readFileSync(0, "utf8");
  if (input) JSON.parse(input);
} catch (_) {
  /* fail-open */
}

process.stdout.write(JSON.stringify({ additional_context: CONTEXT }));
