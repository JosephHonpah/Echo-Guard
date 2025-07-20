@echo off
echo Updating Lambda function with Kiro integration...

echo Please enter your AWS account ID:
set /p AWS_ACCOUNT_ID=

echo Please enter your AWS region (e.g., us-east-1):
set /p AWS_REGION=

echo.
echo Uploading Lambda package to S3...
aws s3 cp backend\lambda\analyze_transcript.zip s3://echoguard-lambda-%AWS_ACCOUNT_ID%/

echo.
echo Updating Lambda function...
aws lambda update-function-code ^
  --function-name AnalyzeTranscript ^
  --s3-bucket echoguard-lambda-%AWS_ACCOUNT_ID% ^
  --s3-key analyze_transcript.zip ^
  --region %AWS_REGION%

echo.
echo Lambda function updated. You can now use Kiro integration.
echo.
pause