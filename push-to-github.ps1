# PowerShell script to push EchoGuard to GitHub

# Set the path to Git executable (default installation path)
$gitPath = "C:\Program Files\Git\bin\git.exe"

# Check if Git exists at the default path
if (-not (Test-Path $gitPath)) {
    # Try another common path
    $gitPath = "C:\Program Files (x86)\Git\bin\git.exe"
    if (-not (Test-Path $gitPath)) {
        Write-Host "Git executable not found. Please install Git and try again."
        exit 1
    }
}

Write-Host "Git found at: $gitPath"

# Initialize Git repository
Write-Host "Initializing Git repository..."
& $gitPath init

# Configure Git user (replace with your info)
Write-Host "Please enter your Git username:"
$username = Read-Host
Write-Host "Please enter your Git email:"
$email = Read-Host

& $gitPath config user.name $username
& $gitPath config user.email $email

# Add all files
Write-Host "Adding files to Git..."
& $gitPath add .

# Commit changes
Write-Host "Committing changes..."
& $gitPath commit -m "Initial EchoGuard deployment"

# Add remote repository
Write-Host "Adding remote repository..."
& $gitPath remote add origin https://github.com/JosephHonpah/Echo-Guard.git

# Push to GitHub
Write-Host "Pushing to GitHub..."
Write-Host "You will be prompted for your GitHub username and personal access token."
& $gitPath push -u origin main

Write-Host "Done! EchoGuard has been pushed to GitHub."