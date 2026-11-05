"""Avviso wiki-sync: src/*.py cambiato senza un markdown in wiki/isab/."""

import importlib.util
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_wiki_sync.py"


def _load():
    spec = importlib.util.spec_from_file_location("check_wiki_sync", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_warning_when_src_python_changes_without_wiki():
    module = _load()
    status, message = module.classify(["src/core/pdf_processor.py"])
    assert status == "warning"
    assert "src/core/pdf_processor.py" in message
    assert "wiki/isab" in message


def test_passed_when_wiki_page_changes_with_code():
    module = _load()
    status, message = module.classify(
        ["src/gui/tabs/dashboard_tab.py", "wiki/isab/modules/gui.md"],
    )
    assert status == "passed"
    assert message == ""


def test_passed_for_tests_docs_and_gemini_only():
    module = _load()
    status, _message = module.classify(
        [
            "tests/test_pdf_processor.py",
            "docs/GEMINI.md",
            "src/core/GEMINI.md",
            "README.md",
        ],
    )
    assert status == "passed"


def test_parse_porcelain_rename_and_backslash():
    module = _load()
    text = "\n".join(
        [
            " M src\\core\\ocr_engine.py",
            'R  "src/old.py" -> "src/new.py"',
            "?? wiki/isab/modules/elaborazione.md",
        ],
    )
    assert module.parse_porcelain(text) == [
        "src/core/ocr_engine.py",
        "src/new.py",
        "wiki/isab/modules/elaborazione.md",
    ]


def _git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )


def _repo_with_src_change(tmp_path: Path, wiki_file: str) -> Path:
    repo = tmp_path / "repo"
    (repo / "src").mkdir(parents=True)
    (repo / "src" / "app.py").write_text("x = 1\n", encoding="utf-8")
    page = repo / wiki_file
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text("# nota\n", encoding="utf-8")
    _git(repo, "init")
    _git(repo, "add", "src/app.py")
    _git(
        repo,
        "-c",
        "user.email=dev@example.com",
        "-c",
        "user.name=dev",
        "commit",
        "-m",
        "init",
    )
    (repo / "src" / "app.py").write_text("x = 2\n", encoding="utf-8")
    return repo


def test_untracked_wiki_directory_counts_as_markdown(tmp_path):
    module = _load()
    repo = _repo_with_src_change(tmp_path, "wiki/isab/modules/note.md")
    status, message = module.classify(module.collect_changed(repo))
    assert status == "passed", message


def test_untracked_markdown_outside_isab_still_warns(tmp_path):
    module = _load()
    repo = _repo_with_src_change(tmp_path, "wiki/INDEX.md")
    status, message = module.classify(module.collect_changed(repo))
    assert status == "warning"
    assert "src/app.py" in message


def test_script_exits_zero_on_this_repo():
    module = _load()
    assert module.main() == 0
