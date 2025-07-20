# EchoGuard Deployment Guide

This guide provides step-by-step instructions for deploying the EchoGuard Voice-to-Text Compliance Logger to production.

## Prerequisites

- AWS Account with Administrator Access
- AWS CLI installed & configured
- Node.js & NPM
- Python 3.11
- Amplify CLI: `npm install -g @aws-amplify/cli`

## Step 1: Deploy Backend Infrastructure

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create an S3 bucket for Lambda code:
   ```
   aws s3 mb s3://echoguard-lambda-YOUR_ACCOUNT_ID --region YOUR_REGION
   ```

3. Create Lambda deployment packages:
   ```
   cd lambda
   powershell Compress-Archive -Path start_transcribe.py -DestinationPath start_transcribe.zip -Force
   powershell Compress-Archive -Path analyze_transcript.py -DestinationPath analyze_transcript.zip -Force
   ```

4. Upload Lambda packages to S3:
   ```
   aws s3 cp start_transcribe.zip s3://echoguard-lambda-YOUR_ACCOUNT_ID/
   aws s3 cp analyze_transcript.zip s3://echoguard-lambda-YOUR_ACCOUNT_ID/
   ```

5. Update the CloudFormation template with your S3 bucket name:
   - Edit `infrastructure.yaml` and update the `LambdaCodeBucket` parameter default value

6. Deploy the CloudFormation stack:
   ```
   aws cloudformation deploy --template-file infrastructure.yaml --stack-name echoguard-backend --capabilities CAPABILITY_NAMED_IAM --parameter-overrides LambdaCodeBucket=echoguard-lambda-YOUR_ACCOUNT_ID
   ```

7. Get the CloudFormation stack outputs:
   ```
   aws cloudformation describe-stacks --stack-name echoguard-backend --query "Stacks[0].Outputs" --output table
   ```

8. Configure S3 bucket notifications:
   ```
   # Create notification configuration files
   # audio-notification.json and transcript-notification.json
   
   # Set up notifications
   aws s3api put-bucket-notification-configuration --bucket AUDIO_BUCKET_NAME --notification-configuration file://audio-notification.json
   aws s3api put-bucket-notification-configuration --bucket TRANSCRIPT_BUCKET_NAME --notification-configuration file://transcript-notification.json
   ```

## Step 2: Deploy API

1. Navigate to the API directory:
   ```
   cd backend/api
   ```

2. Update the API template with your bucket names:
   - Edit `api-template.yaml` and update the `LambdaCodeBucket` parameter default value
   - Update the `AUDIO_BUCKET` environment variable

3. Create the API deployment package:
   ```
   powershell Compress-Archive -Path src\* -DestinationPath api-function.zip -Force
   ```

4. Upload the API package to S3:
   ```
   aws s3 cp api-function.zip s3://echoguard-lambda-YOUR_ACCOUNT_ID/
   ```

5. Deploy the API CloudFormation stack:
   ```
   aws cloudformation deploy --template-file api-template.yaml --stack-name echoguard-api --capabilities CAPABILITY_IAM
   ```

6. Get the API endpoint URL:
   ```
   aws cloudformation describe-stacks --stack-name echoguard-api --query "Stacks[0].Outputs[?OutputKey=='ApiEndpoint'].OutputValue" --output text
   ```

## Step 3: Deploy Frontend

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Create a `.env` file with your API endpoint:
   ```
   REACT_APP_API_ENDPOINT=YOUR_API_ENDPOINT
   ```

3. Initialize Amplify:
   ```
   # Run the amplify-init.bat script
   amplify-init.bat
   ```

4. Deploy the frontend:
   ```
   # Run the amplify-deploy.bat script
   amplify-deploy.bat
   ```

## Step 4: Testing

1. Open the deployed application URL
2. Sign up for a new account and verify your email
3. Upload an audio file for testing
4. Check the CloudWatch Logs for Lambda functions to verify processing
5. View the compliance logs in the application

## Troubleshooting

### S3 Bucket Notifications

If S3 bucket notifications aren't working:

1. Check Lambda permissions:
   ```
   aws lambda get-policy --function-name StartTranscribe
   aws lambda get-policy --function-name AnalyzeTranscript
   ```

2. Verify bucket notification configuration:
   ```
   aws s3api get-bucket-notification-configuration --bucket AUDIO_BUCKET_NAME
   aws s3api get-bucket-notification-configuration --bucket TRANSCRIPT_BUCKET_NAME
   ```

### API Issues

If the API isn't working:

1. Check API Gateway logs in CloudWatch
2. Verify Lambda function permissions
3. Test the API endpoint directly:
   ```
   curl YOUR_API_ENDPOINT/audit-logs
   ```

### Frontend Issues

If the frontend isn't working:

1. Check browser console for errors
2. Verify Amplify configuration in `src/App.js`
3. Check Cognito User Pool settings in AWS Console

## Monitoring

Monitor your deployment with:

1. CloudWatch Logs for Lambda functions
2. CloudWatch Metrics for API Gateway
3. S3 bucket metrics
4. DynamoDB metrics

## Cleanup

To remove all resources:

1. Delete the Amplify project:
   ```
   amplify delete
   ```

2. Delete the CloudFormation stacks:
   ```
   aws cloudformation delete-stack --stack-name echoguard-api
   aws cloudformation delete-stack --stack-name echoguard-backend
   ```

3. Delete the S3 bucket for Lambda code:
   ```
   aws s3 rb s3://echoguard-lambda-YOUR_ACCOUNT_ID --force
   ```