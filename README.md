# EchoGuard: Voice-to-Text Compliance Logger 🚀 NOW LIVE!

EchoGuard is a serverless application that transcribes audio recordings, analyzes them for compliance issues using AI, and provides a dashboard for monitoring compliance metrics.

![EchoGuard Dashboard](docs/images/dashboard.png)

## Features

- **Audio Transcription**: Automatically transcribe audio recordings using Amazon Transcribe
- **Dual AI Compliance Analysis**: Analyze transcripts using both Amazon Bedrock and Kiro AI
- **Real-time Alerts**: Get notified of potential compliance violations
- **Compliance Dashboard**: Monitor compliance metrics and trends
- **Secure Authentication**: User management with Amazon Cognito
- **Enhanced Compliance**: Specialized financial compliance checks with Kiro AI

## Architecture

![Architecture Diagram](docs/images/architecture.png)

Detailed architecture diagrams are available in the following formats:
- [ASCII Diagram](docs/images/architecture.md)
- [Mermaid Diagram](docs/images/architecture-mermaid.md)
- [HTML Interactive Diagram](docs/images/architecture.html)

EchoGuard uses a serverless architecture built on AWS:

- **Frontend**: React.js with AWS Amplify
- **Authentication**: Amazon Cognito
- **API**: Amazon API Gateway + Lambda
- **Processing**: AWS Lambda functions
- **Storage**: Amazon S3 + DynamoDB
- **AI/ML**: Amazon Transcribe + Amazon Bedrock + Kiro AI

## Deployment Guide

### Prerequisites

- AWS Account
- AWS CLI installed and configured
- Node.js and npm
- Python 3.11

### Backend Deployment

1. Create S3 bucket for Lambda code:
   ```
   aws s3 mb s3://echoguard-lambda-YOUR_ACCOUNT_ID --region YOUR_REGION
   ```

2. Deploy Lambda functions:
   ```
   cd backend/lambda
   zip -r start_transcribe.zip start_transcribe.py
   zip -r analyze_transcript.zip analyze_transcript.py
   aws s3 cp start_transcribe.zip s3://echoguard-lambda-YOUR_ACCOUNT_ID/
   aws s3 cp analyze_transcript.zip s3://echoguard-lambda-YOUR_ACCOUNT_ID/
   ```

3. Deploy CloudFormation stack:
   ```
   cd backend
   aws cloudformation deploy --template-file infrastructure.yaml --stack-name echoguard-backend --capabilities CAPABILITY_NAMED_IAM --parameter-overrides LambdaCodeBucket=echoguard-lambda-YOUR_ACCOUNT_ID
   ```

4. Deploy API:
   ```
   cd backend/api
   zip -r api-function.zip src/
   aws s3 cp api-function.zip s3://echoguard-lambda-YOUR_ACCOUNT_ID/
   aws cloudformation deploy --template-file api-template.yaml --stack-name echoguard-api --capabilities CAPABILITY_IAM
   ```

### Authentication Setup

1. Create Cognito User Pool:
   ```
   aws cognito-idp create-user-pool --cli-input-json file://cognito-config.json
   ```

2. Create User Pool Client:
   ```
   aws cognito-idp create-user-pool-client --user-pool-id YOUR_USER_POOL_ID --client-name EchoGuardWebClient --no-generate-secret --explicit-auth-flows ALLOW_USER_PASSWORD_AUTH ALLOW_REFRESH_TOKEN_AUTH
   ```

3. Create Identity Pool:
   ```
   aws cognito-identity create-identity-pool --cli-input-json file://identity-pool-config.json
   ```

4. Set up IAM roles:
   ```
   aws iam create-role --role-name EchoGuardAuthRole --assume-role-policy-document file://auth-role-trust-policy.json
   aws iam put-role-policy --role-name EchoGuardAuthRole --policy-name EchoGuardAuthPolicy --policy-document file://auth-role-policy.json
   aws cognito-identity set-identity-pool-roles --identity-pool-id YOUR_IDENTITY_POOL_ID --roles authenticated=arn:aws:iam::YOUR_ACCOUNT_ID:role/EchoGuardAuthRole
   ```

### Frontend Deployment

1. Update configuration:
   ```
   cd frontend
   # Update src/aws-exports.js with your Cognito and API details
   ```

2. Build and deploy:
   ```
   npm install
   npm run build
   aws s3 mb s3://echoguard-frontend-YOUR_ACCOUNT_ID
   aws s3 website s3://echoguard-frontend-YOUR_ACCOUNT_ID --index-document index.html --error-document index.html
   aws s3api put-bucket-policy --bucket echoguard-frontend-YOUR_ACCOUNT_ID --policy file://bucket-policy.json
   aws s3 sync build/ s3://echoguard-frontend-YOUR_ACCOUNT_ID
   ```

## Usage

1. Access the application at your S3 website URL or our live deployment
2. Sign up for an account and verify your email
3. Upload audio files for compliance analysis
4. View compliance logs and statistics in the dashboard

## Live Deployment

EchoGuard is now live! The application has been fully deployed and is ready for use. The deployment includes all AWS resources described in the architecture diagram.

## Development

### Backend Development

```
cd backend
# Edit Lambda functions in the lambda/ directory
# Edit API code in the api/src/ directory
```

### Frontend Development

```
cd frontend
npm install
npm start
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.