@echo off
echo Pushing EchoGuard to GitHub for JosephHonpah...
powershell -ExecutionPolicy Bypass -File "%~dp0github-push.ps1"
echo.
echo If you see any errors, please:
echo 1. Make sure Git is installed
echo 2. Create a personal access token on GitHub (Settings > Developer settings > Personal access tokens)
echo 3. Use your GitHub username (JosephHonpah) and the token as password when prompted
echo.
pause