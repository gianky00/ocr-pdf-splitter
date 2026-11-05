"""Il corredo agente resta collegato: boot, wiki, GEMINI, regole, skill, hook."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "AGENTS.md",
    "wiki/INDEX.md",
    "wiki/README.md",
    "wiki/isab/INDEX.md",
    "wiki/isab/architecture/overview.md",
    "wiki/isab/architecture/glossario.md",
    "wiki/isab/modules/overview.md",
    "wiki/isab/modules/elaborazione.md",
    "wiki/isab/modules/classificazione.md",
    "wiki/isab/modules/gui.md",
    "wiki/isab/modules/licenza_aggiornamenti.md",
    "wiki/isab/workflows/docs_vs_wiki.md",
    "wiki/isab/workflows/pre_commit_wiki_protocol.md",
    "wiki/isab/workflows/cursor_rules.md",
    "docs/GEMINI.md",
    "src/GEMINI.md",
    "src/core/GEMINI.md",
    "src/gui/GEMINI.md",
    "src/shared/GEMINI.md",
    ".cursor/rules/agents-wiki-boot.mdc",
    ".cursor/rules/isab-agent-guidance.mdc",
    ".cursor/rules/isab-rules-index.mdc",
    ".cursor/rules/lingua-italiano.mdc",
    ".cursor/rules/superpowers-invoke.mdc",
    ".cursor/rules/python-pyside.mdc",
    ".cursor/hooks.json",
    ".cursor/hooks/session_start.cjs",
    "scripts/check_wiki_sync.py",
    ".agents/isab-skills.json",
    ".agents/skills/isab-rules/SKILL.md",
    ".agents/skills/isab-elaborazione/SKILL.md",
    ".agents/skills/isab-ui/SKILL.md",
    ".cursor/skills/isab-rules/SKILL.md",
    ".cursor/skills/isab-elaborazione/SKILL.md",
    ".cursor/skills/isab-ui/SKILL.md",
]

LINKS = {
    "AGENTS.md": [
        "wiki/INDEX.md",
        "wiki/isab/INDEX.md",
        "docs/GEMINI.md",
        "src/core/GEMINI.md",
        ".cursor/rules/",
        ".agents/skills/",
    ],
    "wiki/INDEX.md": ["isab/INDEX.md", "docs/GEMINI.md"],
    "wiki/isab/INDEX.md": [
        "architecture/overview.md",
        "modules/elaborazione.md",
        "workflows/pre_commit_wiki_protocol.md",
    ],
    "docs/GEMINI.md": ["wiki/isab/INDEX.md", "AGENTS.md", "check_wiki_sync.py", "release_patch.bat"],
    "src/core/GEMINI.md": ["tesseract_manager.py"],
    "src/gui/GEMINI.md": ["roi_renderer.py"],
    "prompt/README.md": ["AGENTS.md"],
    "README.md": ["src/app_launcher.py"],
    ".cursor/hooks.json": ["session_start.cjs"],
    ".cursor/rules/agents-wiki-boot.mdc": ["AGENTS.md", "wiki/isab/INDEX.md"],
}


def test_agent_kit_files_exist():
    missing = [rel for rel in REQUIRED if not (ROOT / rel).is_file()]
    assert missing == []


def test_agent_kit_links():
    for rel, needles in LINKS.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        absent = [needle for needle in needles if needle not in text]
        assert absent == [], f"{rel} senza {absent}"


def test_relative_markdown_links_resolve():
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    kit = [ROOT / "AGENTS.md", ROOT / "README.md", ROOT / "docs" / "GEMINI.md", ROOT / "prompt" / "README.md"]
    kit += list((ROOT / "wiki").rglob("*.md"))
    kit += list((ROOT / "src").rglob("GEMINI.md"))
    broken: list[str] = []
    for path in kit:
        text = path.read_text(encoding="utf-8")
        for target in link_re.findall(text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            clean = target.split("#", 1)[0].strip()
            if not clean:
                continue
            resolved = (path.parent / clean).resolve()
            if not resolved.exists():
                broken.append(f"{path.relative_to(ROOT)} -> {target}")
    assert broken == []


def test_skill_mirrors_match():
    for name in ("isab-rules", "isab-elaborazione", "isab-ui"):
        canonical = (ROOT / ".agents" / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
        mirror = (ROOT / ".cursor" / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
        assert canonical == mirror
