"""Comandi della suite di qualità. Ogni percorso ha un solo strumento principale."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RUFF_PATHS = (
    "src",
    "tests",
    "scripts/quality_config.py",
    "scripts/run_quality_checks.py",
)

PYTEST_TIMEOUT_SEC = 900
COVERAGE_TIMEOUT_SEC = 900


def python() -> str:
    """Interprete del progetto. Il python di sistema non vede le dipendenze."""
    candidate = ROOT / ".venv" / "Scripts" / "python.exe"
    if candidate.is_file():
        return str(candidate)
    return sys.executable


def ruff_check_cmd() -> list[str]:
    return [python(), "-m", "ruff", "check", *RUFF_PATHS]


def ruff_format_check_cmd() -> list[str]:
    return [python(), "-m", "ruff", "format", "--check", *RUFF_PATHS]


def ruff_format_cmd() -> list[str]:
    return [python(), "-m", "ruff", "format", *RUFF_PATHS]


def ruff_fix_cmd() -> list[str]:
    return [python(), "-m", "ruff", "check", "--fix", *RUFF_PATHS]


def pytest_cmd() -> list[str]:
    return [python(), "-m", "pytest", "tests"]


def coverage_cmd() -> list[str]:
    return [python(), "-m", "pytest", "--cov", "--cov-report=term-missing"]


def mypy_cmd() -> list[str]:
    return [python(), "-m", "mypy", "src"]


def bandit_cmd() -> list[str]:
    return [python(), "-m", "bandit", "-r", "src", "-c", "pyproject.toml", "-ll"]


def wiki_sync_cmd() -> list[str]:
    return [python(), str(ROOT / "scripts" / "check_wiki_sync.py")]


def deptry_cmd() -> list[str]:
    return [python(), "-m", "deptry", "src", "tests", "scripts"]


def vulture_cmd() -> list[str]:
    return [python(), "-m", "vulture", "src", "--min-confidence", "80"]


def _tool_command(name: str) -> list[str]:
    """Eseguibile del venv. Alcuni tool, come codespell, non hanno `python -m`."""
    candidate = ROOT / ".venv" / "Scripts" / f"{name}.exe"
    if candidate.is_file():
        return [str(candidate)]
    return [python(), "-m", name]


def codespell_cmd() -> list[str]:
    ignore = ROOT / "scripts" / "codespell_ignore.txt"
    return [*_tool_command("codespell"), "--ignore-words", str(ignore), "src", "tests", "scripts", "docs", "wiki"]


def refurb_cmd() -> list[str]:
    return [python(), "-m", "refurb", "src", "--python-version", "3.10"]


def interrogate_cmd() -> list[str]:
    return [python(), "-m", "interrogate", "src", "--fail-under", "0"]


def xenon_cmd() -> list[str]:
    return [
        python(),
        "-m",
        "xenon",
        "--max-absolute",
        "C",
        "--max-modules",
        "C",
        "--max-average",
        "A",
        "src",
    ]


def radon_cc_cmd() -> list[str]:
    return [python(), "-m", "radon", "cc", "src", "-a"]


def radon_mi_cmd() -> list[str]:
    return [python(), "-m", "radon", "mi", "src"]
