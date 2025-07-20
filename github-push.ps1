# PowerShell script to push EchoGuard to GitHub for JosephHonpah

# Repository information
$repoOwner = "JosephHonpah"
$repoName = "Echo-Guard"
$repoUrl = "https://github.com/$repoOwner/$repoName.git"

# Check for GitHub CLI
$useGhCli = $false
try {
    $ghVersion = Invoke-Expression "gh --version" -ErrorAction SilentlyContinue
    if ($ghVersion) {
        $useGhCli = $true
        Write-Host "GitHub CLI found, will use it for authentication."
    }
} catch {
    Write-Host "GitHub CLI not found, will use Git directly."
}

# Find Git executable
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
        break
    }
}

if (-not $gitExe) {
    Write-Host "Git executable not found. Please install Git and try again."
    exit 1
}

# Initialize Git repository
Write-Host "Initializing Git repository..."
& $gitExe init

# Configure Git user for JosephHonpah
& $gitExe config user.name "JosephHonpah"
Write-Host "Enter your email address:"
$email = Read-Host
& $gitExe config user.email $email

# Add all files
Write-Host "Adding files to Git..."
& $gitExe add .

# Commit changes
Write-Host "Committing changes..."
& $gitExe commit -m "Initial EchoGuard deployment - Now Live!"

# Add remote repository
Write-Host "Adding remote repository..."
& $gitExe remote add origin $repoUrl

# Push to GitHub
Write-Host "Pushing to GitHub..."
if ($useGhCli) {
    # Use GitHub CLI for authentication
    Write-Host "Using GitHub CLI for authentication..."
    & gh auth login
    & $gitExe push -u origin main
} else {
    # Use Git credential helper
    Write-Host "You will be prompted for your GitHub username and personal access token."
    Write-Host "Username: JosephHonpah"
    Write-Host "Password: Use your GitHub personal access token (not your regular password)"
    & $gitExe push -u origin main
}

Write-Host "Done! EchoGuard has been pushed to GitHub."