@echo off
setlocal

rem Run from this .bat location
set "SCRIPT_DIR=%~dp0"
set "PY_SCRIPT=%SCRIPT_DIR%wsl_installer.py"

if not exist "%PY_SCRIPT%" (
  echo ERROR: Could not find "%PY_SCRIPT%".
  echo Make sure this .bat is in the same folder as wsl_installer.py
  pause
  exit /b 1
)

rem Relaunch as Administrator if needed
net session >nul 2>&1
if %errorlevel% neq 0 (
  echo Requesting Administrator privileges...
  powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '%COMSPEC%' -ArgumentList '/c','""%~f0""' -WorkingDirectory '""%SCRIPT_DIR%""' -Verb RunAs"
  exit /b
)

pushd "%SCRIPT_DIR%"

rem Prefer Python Launcher if available
where py >nul 2>&1
if %errorlevel% equ 0 (
  py -3 "%PY_SCRIPT%"
) else (
  where python >nul 2>&1
  if %errorlevel% equ 0 (
    python "%PY_SCRIPT%"
  ) else (
    echo ERROR: Python was not found.
    echo Install Python 3 and ensure it is on PATH, or install the Python Launcher.
    popd
    pause
    exit /b 1
  )
)

set "EXIT_CODE=%errorlevel%"
popd

if not "%EXIT_CODE%"=="0" (
  echo.
  echo The installer exited with code %EXIT_CODE%.
  pause
)

endlocal
