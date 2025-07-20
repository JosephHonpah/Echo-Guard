@echo off
echo Deploying Kiro integration for EchoGuard...

echo Please enter your AWS account ID:
set /p AWS_ACCOUNT_ID=

echo Please enter your AWS region (e.g., us-east-1):
set /p AWS_REGION=

echo Please enter your Kiro API key:
set /p KIRO_API_KEY=

echo.
echo Uploading Lambda package to S3...
aws s3 cp backend\lambda\analyze_transcript.zip s3://echoguard-lambda-%AWS_ACCOUNT_ID%/

echo.
echo Updating CloudFormation stack...
cd backend
aws cloudformation update-stack --stack-name echoguard-backend ^
  --template-body file://infrastructure.yaml ^
  --capabilities CAPABILITY_NAMED_IAM ^
  --parameters ParameterKey=LambdaCodeBucket,ParameterValue=echoguard-lambda-%AWS_ACCOUNT_ID% ^
               ParameterKey=KiroApiKey,ParameterValue=%KIRO_API_KEY%

echo.
echo Deployment initiated. Check the AWS CloudFormation console for status.
echo.
pause