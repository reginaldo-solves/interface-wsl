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
; ----- Logo e imagens do assistente -----
; Coloque os arquivos de logo na subpasta 'logo' do projeto antes de compilar:
; - logo\setup.ico        -> ícone do instalador (recomendado .ico)
; - logo\wizard.bmp      -> imagem grande mostrada no assistente (BMP)
; - logo\wizardsmall.bmp -> imagem pequena do assistente (BMP)
; A seguir usamos diretivas do pré-processador para só definir as opções
; quando os arquivos existirem, evitando erro na compilação.
#if FileExists("logo\setup.ico")
SetupIconFile=logo\setup.ico
#endif
#if FileExists("logo\wizard.bmp")
WizardImageFile=logo\wizard.bmp
#endif
#if FileExists("logo\wizardsmall.bmp")
WizardSmallImageFile=logo\wizardsmall.bmp
#endif

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na &área de trabalho"; GroupDescription: "Ícones:";

[Files]
Source: "wsl_installer.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "run_wsl_installer.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: isreadme
Source: "run_wsl_installer.vbs"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Interface WSL Installer"; Filename: "{app}\run_wsl_installer.vbs"
Name: "{userdesktop}\Interface WSL Installer"; Filename: "{app}\run_wsl_installer.vbs"; Tasks: desktopicon

[Run]
Filename: "{app}\run_wsl_installer.vbs"; Description: "Executar Interface WSL Installer"; Flags: shellexec postinstall skipifsilent
