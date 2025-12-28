Set objShell = CreateObject("Shell.Application")
Set fso = CreateObject("Scripting.FileSystemObject")

scriptPath = WScript.ScriptFullName
scriptFolder = fso.GetParentFolderName(scriptPath)
batPath = scriptFolder & "\run_wsl_installer.bat"

' ShellExecute(file, parameters, directory, verb, windowStyle)
' verb "runas" solicita elevação (UAC)
' windowStyle 0 = oculto
objShell.ShellExecute "cmd.exe", "/c """ & batPath & """", scriptFolder, "runas", 0
