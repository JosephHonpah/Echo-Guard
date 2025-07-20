@echo off
REM EchoGuard Deployment Script for Windows

echo === EchoGuard Deployment ===

REM Configuration
set REGION=us-east-1
for /f "tokens=2 delims=\\\"'" %%a in ('aws sts get-caller-identity --query "Account"') do set ACCOUNT_ID=%%a
set LAMBDA_BUCKET=echoguard-lambda-%ACCOUNT_ID%
set FRONTEND_BUCKET=echoguard-frontend-%ACCOUNT_ID%
set BACKEND_STACK_NAME=echoguard-backend
set API_STACK_NAME=echoguard-api

echo AWS Account: %ACCOUNT_ID%
echo Region: %REGION%

REM Check AWS CLI configuration
echo Checking AWS CLI configuration...
aws sts get-caller-identity >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: AWS CLI not configured properly
    exit /b 1
)

REM Create S3 buckets if they don't exist
echo Creating S3 buckets...
aws s3 mb s3://%LAMBDA_BUCKET% --region %REGION% 2>nul || echo Lambda bucket already exists
aws s3 mb s3://%FRONTEND_BUCKET% --region %REGION% 2>nul || echo Frontend bucket already exists

REM Configure frontend bucket for static website hosting
echo Configuring frontend bucket for static website hosting...
aws s3 website s3://%FRONTEND_BUCKET% --index-document index.html --error-document index.html

REM Set bucket policy for frontend
echo Setting bucket policy for frontend...
echo {> bucket-policy.json
echo   "Version": "2012-10-17",>> bucket-policy.json
echo   "Statement": [>> bucket-policy.json
echo     {>> bucket-policy.json
echo       "Sid": "PublicReadGetObject",>> bucket-policy.json
echo       "Effect": "Allow",>> bucket-policy.json
echo       "Principal": "*",>> bucket-policy.json
echo       "Action": "s3:GetObject",>> bucket-policy.json
echo       "Resource": "arn:aws:s3:::%FRONTEND_BUCKET%/*">> bucket-policy.json
echo     }>> bucket-policy.json
echo   ]>> bucket-policy.json
echo }>> bucket-policy.json

aws s3api put-public-access-block --bucket %FRONTEND_BUCKET% --public-access-block-configuration "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false"
aws s3api put-bucket-policy --bucket %FRONTEND_BUCKET% --policy file://bucket-policy.json

REM Package Lambda functions
echo Packaging Lambda functions...
cd backend\lambda
powershell Compress-Archive -Path start_transcribe.py -DestinationPath start_transcribe.zip -Force
powershell Compress-Archive -Path analyze_transcript.py -DestinationPath analyze_transcript.zip -Force
aws s3 cp start_transcribe.zip s3://%LAMBDA_BUCKET%/
aws s3 cp analyze_transcript.zip s3://%LAMBDA_BUCKET%/
cd ..\..

REM Deploy backend infrastructure
echo Deploying backend infrastructure...
cd backend
aws cloudformation deploy --template-file infrastructure.yaml --stack-name %BACKEND_STACK_NAME% --capabilities CAPABILITY_NAMED_IAM --parameter-overrides LambdaCodeBucket=%LAMBDA_BUCKET%
cd ..

REM Package and deploy API
echo Packaging and deploying API...
cd backend\api
powershell Compress-Archive -Path src\* -DestinationPath api-function.zip -Force
aws s3 cp api-function.zip s3://%LAMBDA_BUCKET%/
aws cloudformation deploy --template-file api-template.yaml --stack-name %API_STACK_NAME% --capabilities CAPABILITY_IAM --parameter-overrides LambdaCodeBucket=%LAMBDA_BUCKET%
cd ..\..

REM Get API endpoint
for /f "tokens=2 delims='" %%a in ('aws cloudformation describe-stacks --stack-name %API_STACK_NAME% --query "Stacks[0].Outputs[?OutputKey=='ApiEndpoint'].OutputValue | [0]"') do set API_ENDPOINT=%%a
echo API Endpoint: %API_ENDPOINT%

REM Set up Cognito
echo Setting up Cognito...
for /f "tokens=2 delims=\\\"'" %%a in ('aws cognito-idp create-user-pool --pool-name EchoGuardUserPool --auto-verified-attributes email --username-attributes email --query "UserPool.Id"') do set USER_POOL_ID=%%a
for /f "tokens=2 delims=\\\"'" %%a in ('aws cognito-idp create-user-pool-client --user-pool-id %USER_POOL_ID% --client-name EchoGuardWebClient --no-generate-secret --explicit-auth-flows ALLOW_USER_PASSWORD_AUTH ALLOW_REFRESH_TOKEN_AUTH --query "UserPoolClient.ClientId"') do set CLIENT_ID=%%a
for /f "tokens=2 delims=\\\"'" %%a in ('aws cognito-identity create-identity-pool --identity-pool-name EchoGuardIdentityPool --allow-unauthenticated-identities false --cognito-identity-providers ProviderName="cognito-idp.%REGION%.amazonaws.com/%USER_POOL_ID%",ClientId="%CLIENT_ID%" --query "IdentityPoolId"') do set IDENTITY_POOL_ID=%%a

echo User Pool ID: %USER_POOL_ID%
echo Client ID: %CLIENT_ID%
echo Identity Pool ID: %IDENTITY_POOL_ID%

REM Create IAM roles for Cognito
echo Creating IAM roles for Cognito...
echo {> auth-role-trust-policy.json
echo   "Version": "2012-10-17",>> auth-role-trust-policy.json
echo   "Statement": [>> auth-role-trust-policy.json
echo     {>> auth-role-trust-policy.json
echo       "Effect": "Allow",>> auth-role-trust-policy.json
echo       "Principal": {>> auth-role-trust-policy.json
echo         "Federated": "cognito-identity.amazonaws.com">> auth-role-trust-policy.json
echo       },>> auth-role-trust-policy.json
echo       "Action": "sts:AssumeRoleWithWebIdentity",>> auth-role-trust-policy.json
echo       "Condition": {>> auth-role-trust-policy.json
echo         "StringEquals": {>> auth-role-trust-policy.json
echo           "cognito-identity.amazonaws.com:aud": "%IDENTITY_POOL_ID%">> auth-role-trust-policy.json
echo         },>> auth-role-trust-policy.json
echo         "ForAnyValue:StringLike": {>> auth-role-trust-policy.json
echo           "cognito-identity.amazonaws.com:amr": "authenticated">> auth-role-trust-policy.json
echo         }>> auth-role-trust-policy.json
echo       }>> auth-role-trust-policy.json
echo     }>> auth-role-trust-policy.json
echo   ]>> auth-role-trust-policy.json
echo }>> auth-role-trust-policy.json

for /f "tokens=2 delims=\\\"'" %%a in ('aws iam create-role --role-name EchoGuardAuthRole --assume-role-policy-document file://auth-role-trust-policy.json --query "Role.Arn"') do set AUTH_ROLE_ARN=%%a

echo {> auth-role-policy.json
echo   "Version": "2012-10-17",>> auth-role-policy.json
echo   "Statement": [>> auth-role-policy.json
echo     {>> auth-role-policy.json
echo       "Effect": "Allow",>> auth-role-policy.json
echo       "Action": [>> auth-role-policy.json
echo         "execute-api:Invoke">> auth-role-policy.json
echo       ],>> auth-role-policy.json
echo       "Resource": [>> auth-role-policy.json
echo         "arn:aws:execute-api:%REGION%:%ACCOUNT_ID%:*/*">> auth-role-policy.json
echo       ]>> auth-role-policy.json
echo     }>> auth-role-policy.json
echo   ]>> auth-role-policy.json
echo }>> auth-role-policy.json

aws iam put-role-policy --role-name EchoGuardAuthRole --policy-name EchoGuardAuthPolicy --policy-document file://auth-role-policy.json
aws cognito-identity set-identity-pool-roles --identity-pool-id %IDENTITY_POOL_ID% --roles authenticated=%AUTH_ROLE_ARN%

REM Update frontend configuration
echo Updating frontend configuration...
echo // AWS Amplify configuration> frontend\src\aws-exports.js
echo const awsmobile = {>> frontend\src\aws-exports.js
echo     "aws_project_region": "%REGION%",>> frontend\src\aws-exports.js
echo     "aws_cognito_identity_pool_id": "%IDENTITY_POOL_ID%",>> frontend\src\aws-exports.js
echo     "aws_cognito_region": "%REGION%",>> frontend\src\aws-exports.js
echo     "aws_user_pools_id": "%USER_POOL_ID%",>> frontend\src\aws-exports.js
echo     "aws_user_pools_web_client_id": "%CLIENT_ID%",>> frontend\src\aws-exports.js
echo     "oauth": {},>> frontend\src\aws-exports.js
echo     "aws_cloud_logic_custom": [>> frontend\src\aws-exports.js
echo         {>> frontend\src\aws-exports.js
echo             "name": "echoguardApi",>> frontend\src\aws-exports.js
echo             "endpoint": "%API_ENDPOINT%",>> frontend\src\aws-exports.js
echo             "region": "%REGION%">> frontend\src\aws-exports.js
echo         }>> frontend\src\aws-exports.js
echo     ]>> frontend\src\aws-exports.js
echo };>> frontend\src\aws-exports.js
echo.>> frontend\src\aws-exports.js
echo export default awsmobile;>> frontend\src\aws-exports.js

REM Build and deploy frontend
echo Building and deploying frontend...
cd frontend
call npm ci
call npm run build
aws s3 sync build/ s3://%FRONTEND_BUCKET% --delete
cd ..

REM Output deployment information
set FRONTEND_URL=http://%FRONTEND_BUCKET%.s3-website-%REGION%.amazonaws.com
echo.
echo === Deployment Complete ===
echo Frontend URL: %FRONTEND_URL%
echo API Endpoint: %API_ENDPOINT%
echo User Pool ID: %USER_POOL_ID%
echo Client ID: %CLIENT_ID%
echo.
echo Next steps:
echo 1. Access the application at: %FRONTEND_URL%
echo 2. Sign up for an account and verify your email
echo 3. Upload audio files for compliance analysis
echo 4. View compliance logs and statistics in the dashboard