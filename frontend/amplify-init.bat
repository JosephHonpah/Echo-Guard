@echo off
echo ===================================
echo EchoGuard Amplify Initialization
echo ===================================

REM Check if Amplify CLI is installed
where amplify >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Amplify CLI is not installed or not in PATH.
    echo Please install Amplify CLI with: npm install -g @aws-amplify/cli
    exit /b 1
)

REM Initialize Amplify
echo Initializing Amplify project...
amplify init --yes ^
  --amplify "{\"projectName\":\"echoguard\",\"defaultEditor\":\"code\"}" ^
  --frontend "{\"frontend\":\"javascript\",\"framework\":\"react\",\"config\":{\"SourceDir\":\"src\",\"DistributionDir\":\"build\",\"BuildCommand\":\"npm run build\",\"StartCommand\":\"npm start\"}}" ^
  --providers "{\"awscloudformation\":{\"useProfile\":true,\"profileName\":\"default\"}}"

REM Add authentication
echo Adding authentication...
amplify add auth --headless ^
  --authSelections "identityPoolAndUserPool" ^
  --usernameAttributes "email" ^
  --requiredAttributes "email" ^
  --mfaConfiguration "OFF" ^
  --socialProviders "[]" ^
  --serviceName "Cognito" ^
  --userPoolName "echoguardUserPool" ^
  --userPoolGroups "false" ^
  --userpoolClientRefreshTokenValidity "30" ^
  --userpoolClientReadAttributes "email" ^
  --userpoolClientWriteAttributes "email" ^
  --emailVerificationMessage "Your verification code is {####}" ^
  --emailVerificationSubject "Your EchoGuard verification code" ^
  --smsVerificationMessage "Your verification code is {####}" ^
  --smsAuthenticationMessage "Your authentication code is {####}" ^
  --defaultPasswordPolicy "false" ^
  --passwordPolicyMinLength "8" ^
  --passwordPolicyCharacters "[]" ^
  --resourceName "echoguardauth" ^
  --useDefault "default" ^
  --usernameAttributes "email" ^
  --userPoolGroupList "[]" ^
  --adminQueries "false" ^
  --thirdPartyAuth "false" ^
  --authProviders "[]" ^
  --identityPoolName "echoguardIdentityPool"

REM Add storage
echo Adding storage...
amplify add storage --headless ^
  --resourceName "echoguardaudio" ^
  --bucketName "echoguard-audio-frontend" ^
  --storageAccess "auth" ^
  --guestAccess "[]" ^
  --authAccess "[\"CREATE_AND_UPDATE\",\"READ\"]" ^
  --triggerFunction "false" ^
  --serviceName "S3AndCloudFront"

REM Push changes
echo Pushing Amplify resources...
amplify push --yes

echo ===================================
echo Amplify initialization complete!
echo ===================================
echo.
echo Next steps:
echo 1. Update the API configuration in src/App.js
echo 2. Build and deploy the frontend
echo.