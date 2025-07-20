@echo off
echo ===================================
echo EchoGuard Frontend Deployment
echo ===================================

REM Check if AWS CLI is installed
where aws >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: AWS CLI is not installed or not in PATH.
    echo Please install AWS CLI and configure it with your credentials.
    echo Visit: https://aws.amazon.com/cli/
    exit /b 1
)

REM Check if AWS CLI is configured
aws sts get-caller-identity >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: AWS CLI is not configured properly.
    echo Please run 'aws configure' to set up your credentials.
    exit /b 1
)

REM Get API endpoint from CloudFormation stack
echo Getting API endpoint from CloudFormation stack...
for /f "tokens=2 delims='" %%a in ('aws cloudformation describe-stacks --stack-name echoguard-api --query "Stacks[0].Outputs[?OutputKey=='ApiEndpoint'].OutputValue | [0]"') do set API_ENDPOINT=%%a

if "%API_ENDPOINT%"=="" (
    echo Error: Could not get API endpoint from CloudFormation stack.
    exit /b 1
)

echo Using API endpoint: %API_ENDPOINT%

REM Create S3 bucket for frontend deployment
echo Creating S3 bucket for frontend deployment...
for /f "tokens=2 delims=\\\"'" %%a in ('aws sts get-caller-identity --query "Account"') do set AWS_ACCOUNT=%%a
set BUCKET_NAME=echoguard-frontend-%AWS_ACCOUNT%

aws s3 mb s3://%BUCKET_NAME% --region us-east-1
if %ERRORLEVEL% NEQ 0 (
    echo Error creating S3 bucket. Checking if it already exists...
    aws s3 ls s3://%BUCKET_NAME% >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo Error: Could not create or access S3 bucket.
        exit /b 1
    )
)

REM Upload frontend package to S3
echo Uploading frontend package to S3...
aws s3 cp frontend-package.zip s3://%BUCKET_NAME%/
if %ERRORLEVEL% NEQ 0 (
    echo Error uploading frontend package to S3.
    exit /b 1
)

REM Create CloudFormation stack for Amplify deployment
echo Deploying frontend with CloudFormation...
aws cloudformation deploy --template-file frontend-template.yaml --stack-name echoguard-frontend --capabilities CAPABILITY_IAM --parameter-overrides ApiEndpoint=%API_ENDPOINT%
if %ERRORLEVEL% NEQ 0 (
    echo Error deploying CloudFormation stack.
    exit /b 1
)

REM Get Amplify app URL
echo Getting Amplify app URL...
for /f "tokens=2 delims='" %%a in ('aws cloudformation describe-stacks --stack-name echoguard-frontend --query "Stacks[0].Outputs[?OutputKey=='MainBranchURL'].OutputValue | [0]"') do set APP_URL=%%a

echo ===================================
echo Frontend deployment complete!
echo ===================================
echo.
echo Frontend URL: %APP_URL%
echo.
echo Next steps:
echo 1. Access the application at the URL above
echo 2. Sign up for an account and verify your email
echo 3. Upload audio files for compliance analysis
echo 4. View compliance logs and statistics in the dashboard
echo.