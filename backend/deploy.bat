@echo off
echo ===================================
echo EchoGuard Backend Deployment Script
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

REM Get or create S3 bucket for Lambda code
set /p BUCKET_NAME=Enter S3 bucket name for Lambda code (or press Enter to create a new one): 

if "%BUCKET_NAME%"=="" (
    REM Generate a unique bucket name
    for /f "tokens=2 delims=\"'" %%a in ('aws sts get-caller-identity --query "Account"') do set AWS_ACCOUNT=%%a
    set BUCKET_NAME=echoguard-lambda-%AWS_ACCOUNT%-%RANDOM%
    
    echo Creating new S3 bucket: %BUCKET_NAME%
    aws s3 mb s3://%BUCKET_NAME% --region us-east-1
    if %ERRORLEVEL% NEQ 0 (
        echo Error creating S3 bucket. Please try again with a different name.
        exit /b 1
    )
) else (
    REM Check if bucket exists
    aws s3 ls s3://%BUCKET_NAME% >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo Bucket does not exist. Creating bucket: %BUCKET_NAME%
        aws s3 mb s3://%BUCKET_NAME% --region us-east-1
        if %ERRORLEVEL% NEQ 0 (
            echo Error creating S3 bucket. Please try again with a different name.
            exit /b 1
        )
    )
)

echo Using S3 bucket: %BUCKET_NAME%

REM Create zip files for Lambda functions
echo Creating Lambda function zip files...
cd lambda
powershell Compress-Archive -Path start_transcribe.py -DestinationPath start_transcribe.zip -Force
if %ERRORLEVEL% NEQ 0 (
    echo Error creating start_transcribe.zip
    cd ..
    exit /b 1
)

powershell Compress-Archive -Path analyze_transcript.py -DestinationPath analyze_transcript.zip -Force
if %ERRORLEVEL% NEQ 0 (
    echo Error creating analyze_transcript.zip
    cd ..
    exit /b 1
)
cd ..

REM Upload Lambda code to S3
echo Uploading Lambda code to S3...
aws s3 cp lambda\start_transcribe.zip s3://%BUCKET_NAME%/
if %ERRORLEVEL% NEQ 0 (
    echo Error uploading start_transcribe.zip to S3
    exit /b 1
)

aws s3 cp lambda\analyze_transcript.zip s3://%BUCKET_NAME%/
if %ERRORLEVEL% NEQ 0 (
    echo Error uploading analyze_transcript.zip to S3
    exit /b 1
)

REM Deploy CloudFormation stack
echo Deploying CloudFormation stack...
aws cloudformation deploy --template-file infrastructure.yaml --stack-name echoguard-backend --capabilities CAPABILITY_NAMED_IAM --parameter-overrides LambdaCodeBucket=%BUCKET_NAME%
if %ERRORLEVEL% NEQ 0 (
    echo Error deploying CloudFormation stack
    exit /b 1
)

REM Get stack outputs
echo Getting deployment outputs...
aws cloudformation describe-stacks --stack-name echoguard-backend --query "Stacks[0].Outputs" --output table

echo ===================================
echo Deployment complete!
echo ===================================
echo.
echo Next steps:
echo 1. Note the output values above for configuring the frontend
echo 2. Deploy the API Lambda function
echo 3. Set up the Amplify frontend
echo.