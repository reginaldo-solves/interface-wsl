; Inno Setup Script (compatible com Inno Setup 6.4.3)
[Setup]
AppName=Interface WSL Installer
AppVersion=1.0
DefaultDirName={pf}\Interface WSL Installer
DefaultGroupName=Interface WSL Installer
OutputBaseFilename=interface-wsl-setup
Compression=lzma2
SolidCompression=yes
PrivilegesRequired=admin

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na &área de trabalho"; GroupDescription: "Ícones:";

[Files]
Source: "wsl_installer.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "run_wsl_installer.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: isreadme

[Icons]
Name: "{group}\Interface WSL Installer"; Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; Parameters: "-NoProfile -ExecutionPolicy Bypass -Command ""Start-Process -FilePath '{app}\run_wsl_installer.bat' -Verb RunAs"""
Name: "{userdesktop}\Interface WSL Installer"; Filename: "{sys}\WindowsPowerShell\v1.0\powershell.exe"; Parameters: "-NoProfile -ExecutionPolicy Bypass -Command ""Start-Process -FilePath '{app}\run_wsl_installer.bat' -Verb RunAs"""; Tasks: desktopicon

[Run]
Filename: "{app}\run_wsl_installer.bat"; Description: "Executar Interface WSL Installer"; Flags: shellexec postinstall skipifsilent
