@echo off
echo ===================================
echo EchoGuard Frontend Deployment
echo ===================================

REM Check if Amplify CLI is installed
where amplify >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Amplify CLI is not installed or not in PATH.
    echo Please install Amplify CLI with: npm install -g @aws-amplify/cli
    exit /b 1
)

REM Add hosting
echo Adding hosting...
amplify add hosting --headless ^
  --serviceName "amplifyhosting" ^
  --type "manual"

REM Publish the app
echo Publishing the app...
amplify publish --yes

echo ===================================
echo Frontend deployment complete!
echo ===================================