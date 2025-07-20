# EchoGuard Deployment Guide

This guide provides detailed instructions for deploying EchoGuard to your AWS account.

## Prerequisites

- AWS Account
- AWS CLI installed and configured
- Node.js and npm
- Python 3.11
- Kiro IDE

## Step 1: Clone the Repository

```bash
git clone https://github.com/JosephHonpah/Echo-Guard.git
cd echoguard
```

## Step 2: Deploy Backend Resources

### Create S3 Bucket for Lambda Code

```bash
aws s3 mb s3://echoguard-lambda-YOUR_ACCOUNT_ID --region YOUR_REGION
```

Replace `YOUR_ACCOUNT_ID` with your AWS account ID and `YOUR_REGION` with your preferred AWS region.

### Deploy Lambda Functions

```bash
cd backend/lambda
zip -r start_transcribe.zip start_transcribe.py
zip -r analyze_transcript.zip analyze_transcript.py
aws s3 cp start_transcribe.zip s3://echoguard-lambda-YOUR_ACCOUNT_ID/
aws s3 cp analyze_transcript.zip s3://echoguard-lambda-YOUR_ACCOUNT_ID/
```

### Deploy CloudFormation Stack

```bash
cd backend
aws cloudformation deploy --template-file infrastructure.yaml --stack-name echoguard-backend --capabilities CAPABILITY_NAMED_IAM --parameter-overrides LambdaCodeBucket=echoguard-lambda-YOUR_ACCOUNT_ID
```

### Deploy API

```bash
cd backend/api
zip -r api-function.zip src/
aws s3 cp api-function.zip s3://echoguard-lambda-YOUR_ACCOUNT_ID/
aws cloudformation deploy --template-file api-template.yaml --stack-name echoguard-api --capabilities CAPABILITY_IAM
```

## Step 3: Set Up Authentication

### Create Cognito User Pool

```bash
aws cognito-idp create-user-pool --cli-input-json file://cognito-config.json
```

Save the User Pool ID from the output.

### Create User Pool Client

```bash
aws cognito-idp create-user-pool-client --user-pool-id YOUR_USER_POOL_ID --client-name EchoGuardWebClient --no-generate-secret --explicit-auth-flows ALLOW_USER_PASSWORD_AUTH ALLOW_REFRESH_TOKEN_AUTH
```

Save the Client ID from the output.

### Create Identity Pool

```bash
aws cognito-identity create-identity-pool --cli-input-json file://identity-pool-config.json
```

Save the Identity Pool ID from the output.

### Set Up IAM Roles

```bash
aws iam create-role --role-name EchoGuardAuthRole --assume-role-policy-document file://auth-role-trust-policy.json
aws iam put-role-policy --role-name EchoGuardAuthRole --policy-name EchoGuardAuthPolicy --policy-document file://auth-role-policy.json
aws cognito-identity set-identity-pool-roles --identity-pool-id YOUR_IDENTITY_POOL_ID --roles authenticated=arn:aws:iam::YOUR_ACCOUNT_ID:role/EchoGuardAuthRole
```

## Step 4: Deploy Frontend

### Create S3 Bucket for Frontend

```bash
aws s3 mb s3://echoguard-frontend-YOUR_ACCOUNT_ID --region YOUR_REGION
```

### Configure S3 for Website Hosting

```bash
aws s3 website s3://echoguard-frontend-YOUR_ACCOUNT_ID --index-document index.html --error-document index.html
```

### Set Bucket Policy

Create a file named `bucket-policy.json` with the following content:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::echoguard-frontend-YOUR_ACCOUNT_ID/*"
    }
  ]
}
```

Apply the policy:

```bash
aws s3api put-bucket-policy --bucket echoguard-frontend-YOUR_ACCOUNT_ID --policy file://bucket-policy.json
```

### Update Configuration

Edit `frontend/public/auth.html` and `frontend/public/dashboard.html` to update the Cognito configuration:

```javascript
const poolData = {
    UserPoolId: 'YOUR_USER_POOL_ID',
    ClientId: 'YOUR_CLIENT_ID'
};
```

### Upload Frontend Files

```bash
aws s3 cp frontend/public/ s3://echoguard-frontend-YOUR_ACCOUNT_ID/ --recursive
```

## Step 5: Set Up CloudFront (Optional but Recommended)

### Create Origin Access Identity

```bash
aws cloudfront create-cloud-front-origin-access-identity --cloud-front-origin-access-identity-config CallerReference=echoguard-frontend-oai,Comment="OAI for EchoGuard Frontend"
```

Save the ID from the output.

### Update Bucket Policy for CloudFront

Create a file named `bucket-policy-cloudfront.json` with the following content:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowCloudFrontServicePrincipal",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity YOUR_OAI_ID"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::echoguard-frontend-YOUR_ACCOUNT_ID/*"
    }
  ]
}
```

Apply the policy:

```bash
aws s3api put-bucket-policy --bucket echoguard-frontend-YOUR_ACCOUNT_ID --policy file://bucket-policy-cloudfront.json
```

### Create CloudFront Distribution

Create a CloudFront distribution pointing to your S3 bucket using the AWS Management Console or CLI.

## Step 6: Create Test User

```bash
aws cognito-idp admin-create-user --user-pool-id YOUR_USER_POOL_ID --username test@example.com --temporary-password Test1234! --message-action SUPPRESS
aws cognito-idp admin-set-user-password --user-pool-id YOUR_USER_POOL_ID --username test@example.com --password Test1234! --permanent
```

## Step 7: Test the Application

1. Access your S3 website URL or CloudFront distribution URL
2. Log in with the test user credentials
3. Try uploading audio files and check the dashboard

## Troubleshooting

- **CloudFront Access Denied**: Check your bucket policy and OAI configuration
- **Cognito Authentication Issues**: Verify user pool and app client settings
- **CORS Errors**: Add appropriate CORS headers to your S3 bucket and API Gateway
- **Lambda Execution Errors**: Check CloudWatch Logs for detailed error messages
