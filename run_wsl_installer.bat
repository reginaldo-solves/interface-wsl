@echo off
setlocal
 
:rem --- Verificação inicial do Python: se não existir, tenta instalar via winget ou baixar instalador ---
where py >nul 2>&1
if %errorlevel% equ 0 goto :python_check_done
where python >nul 2>&1
if %errorlevel% equ 0 goto :python_check_done

echo Python nao encontrado.

rem Primeiro tenta instalar via winget (se disponível)
where winget >nul 2>&1
if %errorlevel% equ 0 (
  echo Tentando instalar Python via winget (aceitando acordos)...
  winget install --id Python.Python.3 -e --accept-source-agreements --accept-package-agreements
  if %errorlevel% equ 0 (
    echo Python instalado via winget.
    goto :after_install_attempt
  ) else (
    echo winget falhou ao instalar Python. Tentando instalador direto...
  )
) else (
  echo winget nao encontrado. Tentando baixar instalador do Python via PowerShell...
)

rem Se winget nao instalou, tenta baixar instalador do python.org e executar silenciosamente
set "PYVER=3.11.5"
set "PYEXEC=python-%PYVER%-amd64.exe"
set "PYURL=https://www.python.org/ftp/python/%PYVER%/%PYEXEC%"
set "PYTMP=%TEMP%\%PYEXEC%"

echo Baixando %PYURL% para %PYTMP% ...
powershell -NoProfile -Command "try { Invoke-WebRequest -Uri '%PYURL%' -OutFile '%PYTMP%' } catch { exit 2 }"
if %errorlevel% neq 0 (
  echo Falha ao baixar o instalador do Python. Verifique sua conexao ou instale Python manualmente.
  goto :python_check_done
)

echo Executando instalador do Python (silencioso)...
start /wait "" "%PYTMP%" /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
if %errorlevel% neq 0 (
  echo Aviso: instalador retornou codigo %errorlevel%.
)

:after_install_attempt
rem Aguarda alguns segundos para o instalador ajustar PATH (se aplicavel)
timeout /t 3 /nobreak >nul 2>&1

where py >nul 2>&1
if %errorlevel% equ 0 goto :python_check_done
where python >nul 2>&1
if %errorlevel% equ 0 goto :python_check_done

echo Nao foi possivel instalar o Python automaticamente.
echo Por favor instale o Python manualmente e execute este instalador novamente.
pause
exit /b 1

:python_check_done

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
