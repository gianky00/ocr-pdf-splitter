"""Avviso: codice in src/ cambiato senza un aggiornamento di wiki/isab/.

Esce sempre con codice 0. Il testo di avviso non blocca i test né il rilascio.
Il protocollo in wiki/isab/workflows/pre_commit_wiki_protocol.md dice quando l'aggiornamento è obbligatorio.
"""

import subprocess
from pathlib import Path


def parse_porcelain(text: str) -> list[str]:
    """Estrae i path da `git status --porcelain`, con slash normalizzati."""
    paths: list[str] = []
    for line in text.splitlines():
        if len(line) < 4:
            continue
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1].strip()
        path = path.strip().strip('"').replace("\\", "/")
        if path:
            paths.append(path)
    return paths


def expand_wiki_directories(paths: list[str], root: Path) -> list[str]:
    """Sostituisce una cartella wiki non tracciata con i markdown che contiene.

    `git status --porcelain` compatta un albero nuovo in `?? wiki/`.
    Senza questa espansione i file `wiki/isab/**/*.md` non entrano nel confronto.
    """
    expanded: list[str] = []
    root_resolved = root.resolve()
    for path in paths:
        normalized = path.replace("\\", "/").strip("/")
        candidate = root_resolved / normalized
        if (normalized == "wiki" or normalized.startswith("wiki/")) and candidate.is_dir():
            for file in sorted(candidate.rglob("*.md")):
                if file.is_file():
                    expanded.append(file.relative_to(root_resolved).as_posix())
            continue
        expanded.append(path)
    return expanded


def classify(paths: list[str]) -> tuple[str, str]:
    """Ritorna ('warning', messaggio) se cambia un .py in src/ e nessun .md in wiki/isab/."""
    normalized = [path.replace("\\", "/").lstrip("./") for path in paths]
    code = [path for path in normalized if path.startswith("src/") and path.endswith(".py")]
    wiki = [path for path in normalized if path.startswith("wiki/isab/") and path.endswith(".md")]
    if code and not wiki:
        listed = ", ".join(code)
        return (
            "warning",
            "src/ è cambiato e wiki/isab/ no. "
            f"File: {listed}. "
            "Aggiornare wiki/isab/ se il protocollo lo richiede "
            "(wiki/isab/workflows/pre_commit_wiki_protocol.md).",
        )
    return "passed", ""


def collect_changed(root: Path) -> list[str]:
    """Legge i path modificati nel working tree. Lista vuota se git non risponde."""
    try:
        proc = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except OSError:
        return []
    if proc.returncode != 0:
        return []
    return expand_wiki_directories(parse_porcelain(proc.stdout), root)


def main() -> int:
    """Stampa l'avviso, se c'è, e termina con 0."""
    status, message = classify(collect_changed(Path(__file__).resolve().parents[1]))
    if status == "warning":
        print(message)
    else:
        print("wiki-sync: nessun avviso")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
