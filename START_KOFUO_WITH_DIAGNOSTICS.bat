@echo off
setlocal

set "KOFUO_LAUNCHER=%~dp0KOFUO_LAUNCHER_ULTIMATE.py"
if not exist "%KOFUO_LAUNCHER%" (
  echo KOFUO launcher not found: "%KOFUO_LAUNCHER%"
  pause
  exit /b 2
)

if not defined KOFUO_GAME_DIR set "KOFUO_GAME_DIR=%~dp0"
if not defined KOFUO_DIAGNOSTICS_LOCAL_DIR set "KOFUO_DIAGNOSTICS_LOCAL_DIR=%LOCALAPPDATA%\KOFUO\diagnostics"

if not defined KOFUO_DIAGNOSTICS_OUTBOX if exist "\\VBOXSVR\KOFUOReports\" (
  set "KOFUO_DIAGNOSTICS_OUTBOX=\\VBOXSVR\KOFUOReports"
  echo Supa shared-folder outbox detected.
) else (
  echo Shared-folder outbox unavailable. Reports will remain local.
)

where py >nul 2>nul
if errorlevel 1 goto use_python
py -3 "%KOFUO_LAUNCHER%"
goto finished

:use_python
where python >nul 2>nul
if errorlevel 1 goto no_python
python "%KOFUO_LAUNCHER%"
goto finished

:no_python
echo Python was not found. Install Python 3 with Tkinter or start the launcher manually.
pause
exit /b 9009

:finished
if errorlevel 1 (
  echo Launcher exited with code %ERRORLEVEL%.
  pause
)
exit /b %ERRORLEVEL%
