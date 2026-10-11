@echo off
setlocal
set "ARGOS_QA_ROOT=%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\localqa\start_argos_qa.ps1"
set "ARGOS_QA_EXIT=%ERRORLEVEL%"
if not "%ARGOS_QA_EXIT%"=="0" (
  echo.
  echo O ARGOS QA terminou com erro. Consulte a mensagem acima.
  pause
)
exit /b %ARGOS_QA_EXIT%
