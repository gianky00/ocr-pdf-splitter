@echo off
setlocal
chcp 65001 > nul
set PYTHONUTF8=1
cd /d "%~dp0\.."
if errorlevel 1 (
    echo ERRORE: impossibile accedere alla cartella del progetto.
    exit /b 1
)

set "SHOW_HELP="
for %%A in (%*) do (
    if /I "%%~A"=="--help" set "SHOW_HELP=1"
    if /I "%%~A"=="-h" set "SHOW_HELP=1"
)

if not exist ".venv\Scripts\python.exe" (
    echo ERRORE: .venv\Scripts\python.exe assente.
    echo Eseguire launch.bat, poi uv sync --group dev --inexact
    exit /b 1
)

if defined SHOW_HELP goto :run_kernel

echo.
echo ============================================================
echo  ISAB — Quality Checks
echo  Report: logs\quality_report.log
echo  Kernel: scripts\run_quality_checks.py
echo  Tool dev: uv sync --group dev --inexact
echo.
echo  Bloccanti: Ruff, pytest, poi coverage se i precedenti passano.
echo  Avvisi: formato, Mypy, Bandit, wiki-sync e gli altri tool dev.
echo  --skip-coverage salta la coverage. --skip-tests salta pytest e coverage.
echo  --fix applica ruff format e ruff check --fix prima del report.
echo ============================================================
echo.

:run_kernel
".venv\Scripts\python.exe" scripts\run_quality_checks.py %*
set "EXIT_CODE=%ERRORLEVEL%"
if defined SHOW_HELP exit /b %EXIT_CODE%

if %EXIT_CODE% EQU 0 (
    echo.
    echo OK: check bloccanti passati. Dettaglio in logs\quality_report.log
) else (
    echo.
    echo ATTENZIONE: esecuzione non riuscita ^(codice %EXIT_CODE%^).
    echo Leggere logs\quality_report.log.
    echo Provare scripts\run_quality_checks.bat --fix per gli errori auto-correggibili di Ruff.
)

exit /b %EXIT_CODE%
