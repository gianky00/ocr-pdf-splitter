"""Quality checks ISAB: i bloccanti decidono l'esito, gli avvisi finiscono nel report.

Flag:
  --fix            applica ruff format e ruff check --fix prima del report
  --skip-tests     salta pytest e la coverage
  --skip-coverage  salta pytest --cov (parte solo se i bloccanti precedenti passano)
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import quality_config as qc

REPORT_FILE = qc.ROOT / "logs" / "quality_report.log"

GUARDRAILS = """
=== GUARDRAILS — leggere prima di correggere ===
Il report descrive una esecuzione. Il boot resta AGENTS.md, wiki/INDEX.md, wiki/isab/INDEX.md.
PASS: controllo eseguito e riuscito. FAIL: controllo eseguito e fallito.
UNAVAILABLE: strumento non avviabile. SKIPPED: esclusione richiesta.
L'esito del processo dipende dai soli BLOCKING. Un avviso non è un successo del controllo.
Non alzare soglie, non ignorare regole e non spegnere test per ottenere PASS.
--fix modifica i file: leggere git diff prima di tenere il risultato.
OCR e split restano nel ProcessingWorker. Nessun segreto nel report.
""".strip()


@dataclass
class CheckResult:
    name: str
    tier: str
    ok: bool
    command: str
    output: str = ""
    hint: str = ""
    unavailable: bool = False
    keep_output: bool = False

    @property
    def status(self) -> str:
        if self.unavailable:
            return "UNAVAILABLE"
        return "PASS" if self.ok else "FAIL"


@dataclass
class Report:
    results: list[CheckResult] = field(default_factory=list)
    skipped_checks: list[str] = field(default_factory=list)

    def add(self, result: CheckResult) -> None:
        self.results.append(result)

    @property
    def blocking_failed(self) -> list[CheckResult]:
        return [item for item in self.results if item.tier == "BLOCKING" and not item.ok]

    @property
    def advisory_failed(self) -> list[CheckResult]:
        return [item for item in self.results if item.tier == "ADVISORY" and not item.ok and not item.unavailable]

    @property
    def unavailable(self) -> list[CheckResult]:
        return [item for item in self.results if item.unavailable]


def run_cmd(
    command: list[str],
    *,
    cwd: Path | None = None,
    timeout: int = 300,
    extra_env: dict[str, str] | None = None,
) -> tuple[int, str]:
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("QT_QPA_PLATFORM", "offscreen")
    if extra_env:
        env.update(extra_env)
    completed = subprocess.run(
        command,
        cwd=str(cwd or qc.ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        timeout=timeout,
        check=False,
    )
    output = "\n".join(part for part in (completed.stdout, completed.stderr) if part).strip()
    return completed.returncode, output


def _tool_missing(output: str) -> bool:
    lowered = output.lower()
    return "no module named" in lowered or "not recognized" in lowered


def _clip(text: str, max_lines: int = 80) -> str:
    lines = text.splitlines()
    if len(lines) <= max_lines:
        return text
    hidden = len(lines) - max_lines
    return "\n".join([*lines[:max_lines], f"... ({hidden} righe omesse)"])


def run_check(report: Report, result: CheckResult, command: list[str], *, timeout: int) -> None:
    print(f"  -> {result.name}...", flush=True)
    try:
        code, output = run_cmd(command, timeout=timeout)
    except subprocess.TimeoutExpired:
        result.ok = False
        result.output = f"Timeout dopo {timeout}s"
        report.add(result)
        return
    except FileNotFoundError as exc:
        result.ok = False
        result.unavailable = True
        result.output = f"Tool non disponibile: {exc}"
        report.add(result)
        return
    result.output = output
    if code != 0 and _tool_missing(output):
        result.ok = False
        result.unavailable = True
    else:
        result.ok = code == 0
    report.add(result)


def _blocking(*, skip_tests: bool) -> list[tuple[CheckResult, list[str], int]]:
    checks = [
        (
            CheckResult(
                name="Ruff (src, tests, script di qualità)",
                tier="BLOCKING",
                ok=False,
                command=" ".join(qc.ruff_check_cmd()),
                hint="Correggere il lint nello scope di quality_config.RUFF_PATHS.",
            ),
            qc.ruff_check_cmd(),
            120,
        )
    ]
    if not skip_tests:
        checks.append(
            (
                CheckResult(
                    name="Pytest",
                    tier="BLOCKING",
                    ok=False,
                    command=" ".join(qc.pytest_cmd()),
                    hint="Correggere il test o il codice che lo fa fallire.",
                ),
                qc.pytest_cmd(),
                qc.PYTEST_TIMEOUT_SEC,
            )
        )
    return checks


def _advisory() -> list[tuple[CheckResult, list[str], int]]:
    specs: list[tuple[str, list[str], str, int, bool]] = [
        (
            "Ruff format (src, tests, script di qualità)",
            qc.ruff_format_check_cmd(),
            "scripts\\run_quality_checks.bat --fix formatta e riprova.",
            120,
            False,
        ),
        ("Mypy (src/)", qc.mypy_cmd(), "Allineare i tipi nello scope già configurato.", 300, False),
        ("Bandit (src/)", qc.bandit_cmd(), "Valutare il rilievo. La configurazione è in pyproject.toml.", 180, False),
        (
            "Wiki sync",
            qc.wiki_sync_cmd(),
            "Lo script esce con 0. Il protocollo wiki dice se la pagina va aggiornata.",
            60,
            True,
        ),
        ("Deptry", qc.deptry_cmd(), "Dipendenze: avviso.", 120, False),
        ("Vulture (src/, confidence 80)", qc.vulture_cmd(), "Non cancellare codice in blocco.", 120, False),
        ("Codespell", qc.codespell_cmd(), "Correggere il refuso, non la parola di dominio.", 120, False),
        ("Refurb (src/)", qc.refurb_cmd(), "Suggerimenti di sintassi. Applicarli sul punto toccato.", 180, False),
        ("Interrogate (src/)", qc.interrogate_cmd(), "Report docstring. Soglia 0: non aggiunge obbligo.", 120, False),
        ("Xenon (src/)", qc.xenon_cmd(), "Complessità sopra la soglia. Valutare il punto, non un rewrite.", 120, False),
        ("Radon CC (src/)", qc.radon_cc_cmd(), "Report di complessità.", 120, False),
        ("Radon MI (src/)", qc.radon_mi_cmd(), "Report di manutenibilità.", 120, False),
    ]
    checks = []
    for name, command, hint, timeout, keep_output in specs:
        checks.append(
            (
                CheckResult(
                    name=name,
                    tier="ADVISORY",
                    ok=False,
                    command=" ".join(command),
                    hint=hint,
                    keep_output=keep_output,
                ),
                command,
                timeout,
            )
        )
    return checks


def _coverage_check() -> tuple[CheckResult, list[str], int]:
    command = qc.coverage_cmd()
    return (
        CheckResult(
            name="Coverage (pytest --cov)",
            tier="BLOCKING",
            ok=False,
            command=" ".join(command),
            hint="Soglia fail_under in pyproject.toml. Saltabile con --skip-coverage.",
        ),
        command,
        qc.COVERAGE_TIMEOUT_SEC,
    )


def apply_autofix() -> None:
    """Applica i fix automatici di Ruff prima di misurare."""
    fixers = (
        ("Ruff format", qc.ruff_format_cmd()),
        ("Ruff --fix", qc.ruff_fix_cmd()),
    )
    print("Applicazione auto-fix Ruff...")
    for name, command in fixers:
        print(f"  -> {name}...", flush=True)
        try:
            _code, output = run_cmd(command, timeout=300)
        except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
            print(f"     saltato: {exc}")
            continue
        if output:
            print(_clip(output, 15))
    print("Auto-fix completati. Rivedere git diff prima di tenere le modifiche.\n")


def _format_section(title: str, results: list[CheckResult]) -> list[str]:
    lines = [f"--- {title} ---", ""]
    for result in results:
        lines.append(f"[{result.status}] {result.name}")
        lines.append(f"  cmd: {result.command}")
        if result.hint:
            lines.append(f"  hint: {result.hint}")
        if result.output and (not result.ok or result.keep_output):
            lines.append(_clip(result.output))
        lines.append("")
    return lines


def write_report(report: Report) -> str:
    blocking = [item for item in report.results if item.tier == "BLOCKING"]
    advisory = [item for item in report.results if item.tier == "ADVISORY"]
    lines = [
        "=" * 64,
        f"QUALITY CHECK REPORT — {datetime.now():%Y-%m-%d %H:%M:%S}",
        "=" * 64,
        GUARDRAILS,
        "",
        f"BLOCKING failed: {len(report.blocking_failed)} / {len(blocking)}",
        f"ADVISORY failed: {len(report.advisory_failed)} / {len(advisory)} (non bloccano l'esito)",
        f"UNAVAILABLE: {len(report.unavailable)}",
        f"Esclusioni: {', '.join(report.skipped_checks) or 'nessuna'}",
        "",
        *_format_section("BLOCKING CHECKS", blocking),
        *_format_section("ADVISORY", advisory),
        "=" * 64,
    ]
    if report.blocking_failed:
        lines.append("ESITO: FAIL — i check bloccanti falliti o non disponibili vanno risolti.")
    else:
        lines.append("ESITO: PASS — check bloccanti ok.")
        if report.advisory_failed:
            lines.append(f"Nota: {len(report.advisory_failed)} avvisi da leggere nel report.")
    lines.append("=" * 64)
    text = "\n".join(lines) + "\n"
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(text, encoding="utf-8")
    print(text)
    return text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Quality checks ISAB. L'esito dipende dai check bloccanti.",
        epilog="Report: logs/quality_report.log. Tool di sviluppo: uv sync --group dev --inexact.",
    )
    parser.add_argument("--fix", action="store_true", help="Applica ruff format e ruff check --fix.")
    parser.add_argument("--skip-tests", action="store_true", help="Salta pytest e la coverage.")
    parser.add_argument(
        "--skip-coverage",
        action="store_true",
        help="Salta pytest --cov. La coverage parte solo se gli altri bloccanti passano.",
    )
    args = parser.parse_args(argv)
    if args.fix:
        apply_autofix()

    skip_coverage = args.skip_coverage or args.skip_tests
    report = Report()
    if args.skip_tests:
        report.skipped_checks.append("test saltati")
    if skip_coverage:
        report.skipped_checks.append("coverage saltata")

    print("Esecuzione check BLOCKING...")
    for result, command, timeout in _blocking(skip_tests=args.skip_tests):
        run_check(report, result, command, timeout=timeout)

    print("Esecuzione check ADVISORY...")
    for result, command, timeout in _advisory():
        run_check(report, result, command, timeout=timeout)

    if not report.blocking_failed and not skip_coverage:
        print("Check bloccanti ok. Avvio coverage...")
        result, command, timeout = _coverage_check()
        run_check(report, result, command, timeout=timeout)

    write_report(report)
    return 1 if report.blocking_failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
