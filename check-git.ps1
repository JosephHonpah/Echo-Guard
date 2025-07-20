# Check Git version
$gitPaths = @(
    "C:\Program Files\Git\bin\git.exe",
    "C:\Program Files (x86)\Git\bin\git.exe",
    "C:\Program Files\Git\cmd\git.exe"
)

$gitExe = $null
foreach ($path in $gitPaths) {
    if (Test-Path $path) {
        $gitExe = $path
        Write-Host "Git found at: $gitExe"
        
        # Check version
        $version = & $gitExe --version
        Write-Host "Git version: $version"
        
        break
    }
}

if (-not $gitExe) {
    Write-Host "Git executable not found."
}

# Keep window open
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")