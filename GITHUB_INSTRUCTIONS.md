# GitHub Repository Instructions

## Pushing EchoGuard to GitHub

To push the EchoGuard project to your GitHub repository, follow these steps:

### Prerequisites

1. Make sure Git is installed on your system
   - If not installed, download and install from [git-scm.com](https://git-scm.com/downloads)
   - Or use Windows Package Manager: `winget install --id Git.Git`

2. Have a GitHub account with a personal access token
   - Create a token at GitHub: Settings → Developer settings → Personal access tokens
   - Token needs `repo` permissions

### Using the PowerShell Script

1. Right-click on `push-to-github.ps1` and select "Run with PowerShell"
2. When prompted, enter your GitHub username and email
3. When prompted for credentials during the push:
   - Username: your GitHub username
   - Password: use your personal access token (not your GitHub password)

### Manual Steps (Alternative)

If the script doesn't work, you can run these commands manually:

```powershell
# Open PowerShell as Administrator
cd c:\EchoGuard

# Initialize Git repository
git init

# Configure Git user
git config user.name "YOUR_USERNAME"
git config user.email "YOUR_EMAIL"

# Add all files
git add .

# Commit changes
git commit -m "Initial EchoGuard deployment"

# Add remote repository
git remote add origin https://github.com/JosephHonpah/Echo-Guard.git

# Push to GitHub
git push -u origin main
```

## Updating the Repository

After making changes to the project:

```powershell
git add .
git commit -m "Description of changes"
git push origin main
```

## Cloning the Repository

To clone the repository on another machine:

```powershell
git clone https://github.com/JosephHonpah/Echo-Guard.git
cd Echo-Guard
```