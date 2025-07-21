# EchoGuard CloudFront Deployment Guide

## Architecture Overview

This deployment creates the complete EchoGuard architecture as shown in the visual diagram:

```
User → CloudFront (HTTPS) → S3 Frontend → Cognito → API Gateway → Lambda Functions
                                                           ↓
Audio Processing: S3 Audio → Transcribe → S3 Transcripts → AI Analysis → DynamoDB
                                                           ↓
Notifications: SNS Topics (Transcribe, Analysis, General)
```

## Prerequisites

- AWS CLI configured with appropriate permissions
- Node.js and npm installed
- PowerShell (for Windows deployment scripts)

## Quick Deployment

### Option 1: Complete Infrastructure Deployment

```cmd
aws cloudformation deploy \
  --template-file infrastructure/echoguard-complete.yaml \
  --stack-name echoguard-prod \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides Environment=prod ProjectName=echoguard
```

### Option 2: Automated Script Deployment

```cmd
deploy-with-cloudfront.bat
```

## Architecture Components Deployed

### 🌐 Frontend Layer
- **CloudFront Distribution**: HTTPS CDN with global edge locations
- **S3 Frontend Bucket**: Private bucket for React static files
- **Origin Access Control**: Secure S3 access via CloudFront only

### 🔐 Authentication Layer
- **Cognito User Pool**: User authentication and management
- **Cognito Identity Pool**: AWS resource access for authenticated users
- **IAM Roles**: Service-to-service authentication

### 🚀 API Layer
- **API Gateway**: RESTful endpoints with authentication
- **Lambda Functions**: Serverless compute for API handling

### 📁 Storage Layer
- **S3 Audio Bucket**: Encrypted storage for audio files
- **S3 Transcript Bucket**: Storage for transcription results
- **DynamoDB Table**: NoSQL database for compliance data

### 🤖 AI/ML Layer
- **Amazon Transcribe**: Speech-to-text conversion
- **Amazon Bedrock**: General compliance analysis
- **Kiro AI**: Custom financial compliance analysis

### 📢 Notification Layer
- **SNS Transcribe Topic**: Transcription progress notifications
- **SNS Analysis Topic**: High-risk compliance alerts
- **SNS General Topic**: System-wide notifications

### 📊 Monitoring Layer
- **CloudWatch**: Logging and monitoring
- **IAM**: Security and access control

## Deployment Outputs

After successful deployment, you'll receive:

```
✅ Application URL (HTTPS): https://d1234567890.cloudfront.net
📡 CloudFront Distribution ID: E1234567890ABC
🔗 API Endpoint: https://abc123.execute-api.us-east-1.amazonaws.com/prod
👥 User Pool ID: us-east-1_ABC123DEF
📱 Client ID: 1234567890abcdef
```

## Security Features

### HTTPS Everywhere
- CloudFront enforces HTTPS redirects
- SSL/TLS termination at edge locations
- Secure communication throughout the pipeline

### Origin Access Control
- S3 buckets are private (no public access)
- CloudFront uses OAC for secure S3 access
- No direct S3 website hosting

### Authentication & Authorization
- Cognito handles user authentication
- IAM roles for service-to-service communication
- Least privilege access policies

### Data Encryption
- S3 server-side encryption (AES-256)
- DynamoDB encryption at rest
- HTTPS/TLS for data in transit

## Performance Optimizations

### Global CDN
- CloudFront edge locations worldwide
- Cached static assets for faster loading
- HTTP/2 support for improved performance

### Serverless Scaling
- Lambda auto-scaling (up to 1000 concurrent executions)
- DynamoDB on-demand scaling
- API Gateway built-in scaling

### Parallel Processing
- Bedrock and Kiro AI analysis run simultaneously
- Event-driven architecture for efficient processing
- Optimized Lambda memory allocation

## Cost Optimization

### Pay-per-Use Model
- Lambda: Execution time and memory
- Transcribe: Audio processing minutes
- Bedrock: API calls and tokens
- DynamoDB: Read/write capacity units
- CloudFront: Data transfer and requests

### Storage Optimization
- S3 Intelligent Tiering for cost savings
- 7-year lifecycle policy for compliance
- Efficient data compression

## Monitoring & Alerting

### CloudWatch Integration
- Lambda function metrics and logs
- API Gateway request/response monitoring
- DynamoDB performance metrics
- S3 request and error metrics

### SNS Notifications
- Real-time compliance alerts
- Processing status updates
- System health notifications

## Testing the Deployment

### 1. Access the Application
```
https://your-cloudfront-domain.cloudfront.net
```

### 2. Create User Account
- Sign up with email address
- Verify email confirmation
- Log in to the dashboard

### 3. Upload Audio File
- Select audio file (WAV or MP3)
- Monitor processing status
- View compliance analysis results

### 4. Check Notifications
- Monitor SNS topics for alerts
- Review CloudWatch logs
- Verify DynamoDB entries

## Troubleshooting

### CloudFront Issues
```cmd
# Check distribution status
aws cloudfront get-distribution --id YOUR_DISTRIBUTION_ID

# Invalidate cache
aws cloudfront create-invalidation --distribution-id YOUR_DISTRIBUTION_ID --paths "/*"
```

### Lambda Function Issues
```cmd
# Check function logs
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/echoguard"

# View recent logs
aws logs filter-log-events --log-group-name "/aws/lambda/echoguard-prod-upload-processor"
```

### API Gateway Issues
```cmd
# Test API endpoint
curl -X GET "https://your-api-id.execute-api.us-east-1.amazonaws.com/prod/compliance-logs"
```

## Cleanup

To remove all resources:

```cmd
# Delete CloudFormation stack
aws cloudformation delete-stack --stack-name echoguard-prod

# Empty S3 buckets (if needed)
aws s3 rm s3://echoguard-prod-frontend-ACCOUNT_ID --recursive
aws s3 rm s3://echoguard-prod-audio-ACCOUNT_ID --recursive
aws s3 rm s3://echoguard-prod-transcripts-ACCOUNT_ID --recursive
```

## Next Steps

1. **Custom Domain**: Configure Route 53 for custom domain
2. **SSL Certificate**: Add ACM certificate for custom domain
3. **Monitoring**: Set up CloudWatch dashboards
4. **Backup**: Configure cross-region replication
5. **CI/CD**: Implement automated deployment pipeline

## Support

For issues or questions:
- Check CloudWatch logs for error details
- Review AWS service quotas and limits
- Consult AWS documentation for service-specific issues
- Monitor SNS topics for system notifications

This deployment provides a production-ready, secure, and scalable voice-to-text compliance logging system with global HTTPS distribution via CloudFront.