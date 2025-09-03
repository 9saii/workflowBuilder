$pythonScriptsPath = "$env:APPDATA\Python\Python312\Scripts"
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($currentPath -notlike "*$pythonScriptsPath*") {
    $newPath = "$currentPath;$pythonScriptsPath"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "Added $pythonScriptsPath to user PATH. Please restart your command prompt or PowerShell for changes to take effect."
} else {
    Write-Host "$pythonScriptsPath is already in PATH."
}
