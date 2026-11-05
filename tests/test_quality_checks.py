"""Gate di qualità: i check bloccanti decidono l'esito, gli avvisi restano nel report."""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def _load(name: str):
    path = SCRIPTS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _commands(calls: list[list[str]]) -> list[str]:
    return [" ".join(command) for command in calls]


def _run(monkeypatch, tmp_path, argv: list[str], responses: dict[str, tuple[int, str]]):
    runner = _load("run_quality_checks")
    monkeypatch.setattr(runner, "REPORT_FILE", tmp_path / "quality_report.log")
    calls: list[list[str]] = []

    def fake(command, **_kwargs):
        calls.append(list(command))
        text = " ".join(command)
        for needle, result in responses.items():
            if needle in text:
                return result
        return 0, ""

    monkeypatch.setattr(runner, "run_cmd", fake)
    code = runner.main(argv)
    report = (tmp_path / "quality_report.log").read_text(encoding="utf-8")
    return code, report, _commands(calls)


def test_fallimento_bloccante_esce_con_1(monkeypatch, tmp_path):
    code, report, commands = _run(
        monkeypatch,
        tmp_path,
        ["--skip-tests", "--skip-coverage"],
        {"ruff check": (1, "F401 unused")},
    )
    assert code == 1
    assert "ESITO: FAIL" in report
    assert "[FAIL] Ruff" in report
    assert not any("--cov" in command for command in commands)


def test_avviso_non_blocca(monkeypatch, tmp_path):
    code, report, _commands_run = _run(
        monkeypatch,
        tmp_path,
        ["--skip-tests", "--skip-coverage"],
        {"mypy": (1, "error: tipi mancanti")},
    )
    assert code == 0
    assert "ESITO: PASS" in report
    assert "[FAIL] Mypy" in report
    assert "ADVISORY failed:" in report


def test_tool_avviso_mancante_e_non_disponibile(monkeypatch, tmp_path):
    code, report, _commands_run = _run(
        monkeypatch,
        tmp_path,
        ["--skip-tests", "--skip-coverage"],
        {"deptry": (1, "No module named deptry")},
    )
    assert code == 0
    assert "[UNAVAILABLE] Deptry" in report
    assert "ESITO: PASS" in report


def test_tool_bloccante_mancante_fa_fallire(monkeypatch, tmp_path):
    code, report, _commands_run = _run(
        monkeypatch,
        tmp_path,
        ["--skip-tests", "--skip-coverage"],
        {"ruff check": (1, "No module named ruff")},
    )
    assert code == 1
    assert "[UNAVAILABLE] Ruff" in report
    assert "ESITO: FAIL" in report


def test_skip_tests_esclude_pytest_e_coverage(monkeypatch, tmp_path):
    code, report, commands = _run(monkeypatch, tmp_path, ["--skip-tests"], {})
    assert code == 0
    assert not any("pytest" in command for command in commands)
    assert "test saltati" in report
    assert "coverage saltata" in report


def test_coverage_parte_solo_se_i_bloccanti_passano(monkeypatch, tmp_path):
    code, _report, commands = _run(monkeypatch, tmp_path, [], {})
    assert code == 0
    assert any("pytest" in command and "--cov" not in command for command in commands)
    assert any("--cov" in command for command in commands)

    code, report, commands = _run(
        monkeypatch,
        tmp_path,
        [],
        {"ruff check": (1, "F401 unused")},
    )
    assert code == 1
    assert not any("--cov" in command for command in commands)
    assert "ESITO: FAIL" in report


def test_skip_coverage_lascia_i_test(monkeypatch, tmp_path):
    code, report, commands = _run(monkeypatch, tmp_path, ["--skip-coverage"], {})
    assert code == 0
    assert any("pytest" in command and "--cov" not in command for command in commands)
    assert not any("--cov" in command for command in commands)
    assert "coverage saltata" in report


def test_fix_lancia_ruff_prima_dei_check(monkeypatch, tmp_path):
    _code, _report, commands = _run(monkeypatch, tmp_path, ["--fix", "--skip-tests", "--skip-coverage"], {})
    assert "ruff format" in commands[0]
    assert "--fix" in commands[1]
    assert commands[1].index("--fix") < commands[1].index("src")


def test_avviso_wiki_resta_nel_report_anche_se_passa(monkeypatch, tmp_path):
    _code, report, _commands_run = _run(
        monkeypatch,
        tmp_path,
        ["--skip-tests", "--skip-coverage"],
        {"check_wiki_sync.py": (0, "AVVISO: src cambiato senza wiki")},
    )
    assert "[PASS] Wiki" in report
    assert "AVVISO: src cambiato senza wiki" in report


def test_comandi_usano_il_python_del_venv_e_gli_scope():
    config = _load("quality_config")
    ruff = " ".join(config.ruff_check_cmd())
    assert ruff.startswith(str(ROOT / ".venv" / "Scripts" / "python.exe"))
    assert " -m ruff check " in ruff
    for path in ("src", "tests", "scripts/quality_config.py", "scripts/run_quality_checks.py"):
        assert path in ruff
    pytest_cmd = " ".join(config.pytest_cmd())
    coverage = " ".join(config.coverage_cmd())
    assert "pytest" in pytest_cmd and "--cov" not in pytest_cmd
    assert "--cov" in coverage
    assert "check_wiki_sync.py" in " ".join(config.wiki_sync_cmd())
    assert str(ROOT / ".venv" / "Scripts" / "codespell.exe") in " ".join(config.codespell_cmd())


def test_bat_e_gruppo_dev_uv_e_documento_ops():
    assert not (ROOT / "requirements-dev.txt").exists()
    bat = (SCRIPTS / "run_quality_checks.bat").read_text(encoding="utf-8")
    assert "run_quality_checks.py" in bat
    assert r".venv\Scripts\python.exe" in bat
    assert "%~dp0\\.." in bat
    assert "uv sync --group dev --inexact" in bat
    assert "requirements-dev.txt" not in bat
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert "[dependency-groups]" in pyproject
    dev = pyproject.split("dev = [", 1)[1].split("]", 1)[0]
    for tool in ("ruff", "mypy", "bandit", "deptry", "vulture", "codespell", "refurb", "interrogate", "xenon", "radon"):
        assert tool in dev
    assert "pytest" not in dev
    docs = (ROOT / "docs" / "GEMINI.md").read_text(encoding="utf-8")
    assert "run_quality_checks.bat" in docs
    assert "uv sync --group dev --inexact" in docs
    assert "requirements-dev.txt" not in docs
