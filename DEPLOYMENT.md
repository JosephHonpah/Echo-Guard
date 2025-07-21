# EchoGuard Deployment Guide

This guide provides detailed instructions for deploying EchoGuard to your AWS account.

## Prerequisites

Before you begin, ensure you have the following:

- AWS Account with appropriate permissions
- AWS CLI installed and configured
- Node.js and npm installed
- Python 3.11 installed
- Git installed

## Quick Deployment

### 1. Clone the Repository

```bash
git clone https://github.com/JosephHonpah/Echo-Guard.git
cd Echo-Guard
```

### 2. Deploy the Backend

#### Windows

```bash
.\deploy.bat
```

#### Linux/Mac

```bash
./deploy.sh
```

### 3. Deploy the Frontend

#### Windows

```bash
.\deploy-frontend.bat
```

#### Linux/Mac

```bash
./deploy-frontend.sh
```

## Manual Deployment

If you prefer to deploy each component manually, follow these steps:

### 1. Create S3 Buckets

```bash
# Create bucket for Lambda code
aws s3 mb s3://echoguard-lambda-code-$AWS_ACCOUNT_ID-$AWS_REGION

# Create bucket for audio files
aws s3 mb s3://echoguard-audio-$AWS_ACCOUNT_ID-$AWS_REGION

# Create bucket for transcripts
aws s3 mb s3://echoguard-transcripts-$AWS_ACCOUNT_ID-$AWS_REGION

# Create bucket for frontend
aws s3 mb s3://echoguard-frontend-$AWS_ACCOUNT_ID
```

### 2. Create DynamoDB Tables

```bash
# Create recordings table
aws dynamodb create-table \
  --table-name echoguard-recordings \
  --attribute-definitions \
    AttributeName=userId,AttributeType=S \
    AttributeName=recordingId,AttributeType=S \
  --key-schema \
    AttributeName=userId,KeyType=HASH \
    AttributeName=recordingId,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST

# Create results table
aws dynamodb create-table \
  --table-name echoguard-results \
  --attribute-definitions \
    AttributeName=recordingId,AttributeType=S \
  --key-schema \
    AttributeName=recordingId,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
```

### 3. Create SNS Topics

```bash
# Create transcribe topic
aws sns create-topic --name echoguard-transcribe

# Create analysis topic
aws sns create-topic --name echoguard-analysis

# Create notifications topic
aws sns create-topic --name echoguard-notifications
```

### 4. Create IAM Role for Lambda Functions

```bash
# Create role
aws iam create-role \
  --role-name echoguard-lambda-role \
  --assume-role-policy-document file://backend/iam/lambda-trust-policy.json

# Attach policies
aws iam attach-role-policy \
  --role-name echoguard-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam attach-role-policy \
  --role-name echoguard-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

aws iam attach-role-policy \
  --role-name echoguard-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess

aws iam attach-role-policy \
  --role-name echoguard-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonTranscribeFullAccess

aws iam attach-role-policy \
  --role-name echoguard-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonSNSFullAccess

aws iam attach-role-policy \
  --role-name echoguard-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess
```

### 5. Deploy Lambda Functions

```bash
# Package Lambda functions
cd backend/lambda
zip -r upload_handler.zip upload_handler.py
zip -r transcribe_handler.zip transcribe_handler.py
zip -r analysis_handler.zip analysis_handler.py
zip -r get_recordings_handler.zip get_recordings_handler.py

# Upload to S3
aws s3 cp upload_handler.zip s3://echoguard-lambda-code-$AWS_ACCOUNT_ID-$AWS_REGION/lambda/
aws s3 cp transcribe_handler.zip s3://echoguard-lambda-code-$AWS_ACCOUNT_ID-$AWS_REGION/lambda/
aws s3 cp analysis_handler.zip s3://echoguard-lambda-code-$AWS_ACCOUNT_ID-$AWS_REGION/lambda/
aws s3 cp get_recordings_handler.zip s3://echoguard-lambda-code-$AWS_ACCOUNT_ID-$AWS_REGION/lambda/

# Create Lambda functions
aws lambda create-function \
  --function-name echoguard-upload-handler \
  --runtime python3.11 \
  --role arn:aws:iam::$AWS_ACCOUNT_ID:role/echoguard-lambda-role \
  --handler upload_handler.lambda_handler \
  --code S3Bucket=echoguard-lambda-code-$AWS_ACCOUNT_ID-$AWS_REGION,S3Key=lambda/upload_handler.zip \
  --environment Variables="{AUDIO_BUCKET=echoguard-audio-$AWS_ACCOUNT_ID-$AWS_REGION,RECORDINGS_TABLE=echoguard-recordings,TRANSCRIBE_TOPIC_ARN=arn:aws:sns:$AWS_REGION:$AWS_ACCOUNT_ID:echoguard-transcribe}"

# Create remaining Lambda functions (similar pattern)
```

### 6. Create API Gateway

```bash
# Create REST API
aws apigateway create-rest-api --name echoguard-api

# Create resources and methods
# Configure integrations with Lambda functions
# Deploy API
aws apigateway create-deployment \
  --rest-api-id $API_ID \
  --stage-name dev
```

### 7. Create Cognito User Pool

```bash
# Create user pool
aws cognito-idp create-user-pool \
  --pool-name EchoGuard \
  --auto-verified-attributes email

# Create app client
aws cognito-idp create-user-pool-client \
  --user-pool-id $USER_POOL_ID \
  --client-name EchoGuardWebClient \
  --no-generate-secret \
  --explicit-auth-flows ALLOW_USER_SRP_AUTH ALLOW_REFRESH_TOKEN_AUTH ALLOW_USER_PASSWORD_AUTH
```

### 8. Deploy Frontend

```bash
# Build frontend
cd frontend
npm install
npm run build

# Upload to S3
aws s3 sync ./public/ s3://echoguard-frontend-$AWS_ACCOUNT_ID/

# Create CloudFront distribution
aws cloudfront create-distribution \
  --origin-domain-name echoguard-frontend-$AWS_ACCOUNT_ID.s3.amazonaws.com \
  --default-root-object index.html
```

## Environment Configuration

Update the following files with your specific AWS resource identifiers:

### Frontend Configuration

Update `frontend/public/js/api.js` with your API Gateway URL:

```javascript
const API_CONFIG = {
  apiUrl: 'https://YOUR_API_GATEWAY_ID.execute-api.YOUR_REGION.amazonaws.com/dev',
  demoMode: false
};
```

Update `frontend/public/auth.html` and `frontend/public/dashboard.html` with your Cognito User Pool details:

```javascript
const poolData = {
  UserPoolId: 'YOUR_USER_POOL_ID',
  ClientId: 'YOUR_CLIENT_ID'
};
```

## Testing the Deployment

1. Access your CloudFront URL
2. Sign up for a new account
3. Verify your email
4. Log in to the dashboard
5. Upload a test audio file
6. Verify that the file appears in your dashboard

## Troubleshooting

### CORS Issues

If you encounter CORS errors:

1. Enable CORS on your API Gateway
2. Add the CloudFront domain to the allowed origins
3. Deploy the API again

### Authentication Issues

If authentication fails:

1. Verify that the Cognito User Pool and Client IDs are correct
2. Ensure the authentication flows are properly configured
3. Check browser console for specific error messages

### Upload Issues

If file uploads fail:

1. Verify S3 bucket permissions
2. Check CORS configuration on the S3 bucket
3. Ensure the pre-signed URL is generated correctly

## Cleanup

To remove all deployed resources:

```bash
# Delete CloudFront distribution
aws cloudfront delete-distribution --id $DISTRIBUTION_ID

# Delete S3 buckets
aws s3 rb s3://echoguard-frontend-$AWS_ACCOUNT_ID --force
aws s3 rb s3://echoguard-audio-$AWS_ACCOUNT_ID-$AWS_REGION --force
aws s3 rb s3://echoguard-transcripts-$AWS_ACCOUNT_ID-$AWS_REGION --force
aws s3 rb s3://echoguard-lambda-code-$AWS_ACCOUNT_ID-$AWS_REGION --force

# Delete Lambda functions
aws lambda delete-function --function-name echoguard-upload-handler
# Delete remaining Lambda functions

# Delete API Gateway
aws apigateway delete-rest-api --rest-api-id $API_ID

# Delete DynamoDB tables
aws dynamodb delete-table --table-name echoguard-recordings
aws dynamodb delete-table --table-name echoguard-results

# Delete SNS topics
aws sns delete-topic --topic-arn arn:aws:sns:$AWS_REGION:$AWS_ACCOUNT_ID:echoguard-transcribe
aws sns delete-topic --topic-arn arn:aws:sns:$AWS_REGION:$AWS_ACCOUNT_ID:echoguard-analysis
aws sns delete-topic --topic-arn arn:aws:sns:$AWS_REGION:$AWS_ACCOUNT_ID:echoguard-notifications

# Delete Cognito User Pool
aws cognito-idp delete-user-pool --user-pool-id $USER_POOL_ID

# Delete IAM role
aws iam detach-role-policy --role-name echoguard-lambda-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
# Detach remaining policies
aws iam delete-role --role-name echoguard-lambda-role
```