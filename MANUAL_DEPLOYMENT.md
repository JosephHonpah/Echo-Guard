# EchoGuard Manual Deployment Guide

If you're unable to use the automated deployment scripts, follow these manual steps to deploy EchoGuard.

## Backend Deployment

### 1. Create S3 Bucket for Lambda Code

1. Go to the AWS Management Console
2. Navigate to S3
3. Click "Create bucket"
4. Enter a bucket name (e.g., `echoguard-lambda-YOUR_ACCOUNT_ID`)
5. Select your preferred region
6. Keep default settings and click "Create bucket"

### 2. Upload Lambda Functions

1. Zip the Lambda function files:
   - `start_transcribe.py` → `start_transcribe.zip`
   - `analyze_transcript.py` → `analyze_transcript.zip`
2. Upload these zip files to your S3 bucket

### 3. Deploy CloudFormation Stack for Backend

1. Go to the AWS Management Console
2. Navigate to CloudFormation
3. Click "Create stack" → "With new resources"
4. Select "Upload a template file"
5. Upload the `infrastructure.yaml` file
6. Enter stack name: `echoguard-backend`
7. Enter parameters:
   - LambdaCodeBucket: Your S3 bucket name
8. Click "Next" through the options
9. Check the box acknowledging IAM resource creation
10. Click "Create stack"

### 4. Configure S3 Bucket Notifications

1. Go to the AWS Management Console
2. Navigate to Lambda
3. For each Lambda function (`StartTranscribe` and `AnalyzeTranscript`):
   - Add permission for S3 to invoke the function
4. Go to S3 and configure event notifications:
   - For the audio bucket: Configure to trigger `StartTranscribe` on object creation
   - For the transcript bucket: Configure to trigger `AnalyzeTranscript` on object creation

### 5. Deploy API

1. Zip the API files in the `src` directory to `api-function.zip`
2. Upload to your S3 bucket
3. Go to CloudFormation
4. Create a new stack using the `api-template.yaml` file
5. Enter stack name: `echoguard-api`
6. Enter parameters:
   - LambdaCodeBucket: Your S3 bucket name
7. Complete the stack creation

## Frontend Deployment

### 1. Create Amplify App

1. Go to the AWS Management Console
2. Navigate to AWS Amplify
3. Click "New app" → "Host web app"
4. Choose your deployment method:
   - If using GitHub: Connect to your GitHub repository
   - If manual deploy: Choose "Deploy without Git provider"
5. Configure build settings:
   - App name: `EchoGuard`
   - Environment variables:
     - Key: `REACT_APP_API_ENDPOINT`
     - Value: Your API Gateway endpoint URL
6. Click "Save and deploy"

### 2. Manual Deployment (if not using Git)

1. Install Node.js and npm
2. Navigate to the frontend directory
3. Run:
   ```
   npm install
   npm run build
   ```
4. In the Amplify Console, click "Manual deploy"
5. Upload the contents of the `build` directory
6. Click "Save and deploy"

## Testing the Deployment

1. Access the Amplify app URL
2. Sign up for a new account
3. Verify your email address
4. Sign in to the application
5. Upload an audio file
6. Check CloudWatch Logs to verify processing
7. View the compliance logs in the application

## Troubleshooting

### Lambda Functions

If Lambda functions aren't working:
1. Check CloudWatch Logs for errors
2. Verify IAM permissions
3. Test the functions directly in the Lambda console

### API Gateway

If API Gateway isn't working:
1. Test the API in the API Gateway console
2. Check CORS configuration
3. Verify Lambda integration

### Amplify Frontend

If the frontend isn't working:
1. Check browser console for errors
2. Verify environment variables
3. Check Cognito User Pool settings