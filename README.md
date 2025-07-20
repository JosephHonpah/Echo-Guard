# EchoGuard: Voice-to-Text Compliance Logger 🚀 NOW LIVE!

EchoGuard is a serverless application that transcribes audio recordings, analyzes them for compliance issues using AI, and provides a dashboard for monitoring compliance metrics.

## Live Demo

**URL**: [https://d4t0hj4peur25.cloudfront.net/auth.html](https://d4t0hj4peur25.cloudfront.net/auth.html)

**Test Credentials**:
- **Email**: test@example.com
- **Password**: Test1234!

## Features

- **Audio Transcription**: Automatically transcribe audio recordings using Amazon Transcribe
- **Dual AI Compliance Analysis**: Analyze transcripts using both Amazon Bedrock and Kiro AI
- **Real-time Alerts**: Get notified of potential compliance violations
- **Compliance Dashboard**: Monitor compliance metrics and trends
- **Secure Authentication**: User management with Amazon Cognito
- **Enhanced Compliance**: Specialized financial compliance checks with Kiro AI

## How It Works

EchoGuard follows a streamlined workflow for processing audio recordings:

1. **Upload Process**:
   - User uploads an audio file through the web interface
   - File is stored in an S3 bucket with appropriate metadata
   - Upload event triggers a Lambda function

2. **Transcription**:
   - Lambda function initiates an Amazon Transcribe job
   - Transcribe processes the audio and generates a text transcript
   - Completion notification is sent via SNS

3. **AI Analysis**:
   - Transcript is analyzed by two AI systems in parallel:
     - Amazon Bedrock for general compliance analysis
     - Kiro AI for specialized financial compliance checks
   - Both systems identify potential compliance issues and assign risk scores

4. **Results Processing**:
   - Analysis results are combined and stored in DynamoDB
   - Compliance score is calculated based on weighted factors
   - High-risk issues trigger alerts via SNS

5. **Dashboard Display**:
   - User views results in the dashboard
   - Recordings are listed with compliance scores
   - Detailed view shows specific issues and recommendations

This serverless architecture ensures scalability, cost-efficiency, and real-time processing of audio recordings.

## How to Use

1. **Authentication**:
   - Visit the [EchoGuard Auth Page](https://d4t0hj4peur25.cloudfront.net/auth.html)
   - Login with existing credentials or sign up for a new account
   - New users will need to verify their email address

2. **Dashboard**:
   - After login, you'll be redirected to the dashboard
   - View your recent recordings and compliance metrics
   - Navigate between Dashboard, Upload, and Settings tabs

3. **Upload Recordings**:
   - Click the "Upload" tab in the dashboard
   - Drag and drop audio files or use the file selector
   - Add an optional description
   - Click "Upload" to process the recording
   - Wait for the compliance analysis to complete

4. **View Compliance Results**:
   - Return to the Dashboard tab to see all recordings
   - Click on any recording to view detailed analysis
   - Check compliance scores and identified issues
   - Review recommendations for improvement

## Architecture

EchoGuard uses a serverless architecture built on AWS:

- **Frontend**: HTML/CSS/JS with AWS Amplify
- **Authentication**: Amazon Cognito
- **API**: Amazon API Gateway + Lambda
- **Processing**: AWS Lambda functions
- **Storage**: Amazon S3 + DynamoDB
- **AI/ML**: Amazon Transcribe + Amazon Bedrock + Kiro AI
- **Content Delivery**: Amazon CloudFront

## Kiro AI Integration

EchoGuard leverages Kiro AI for specialized financial compliance analysis:

### Installing Kiro IDE

1. **Download Kiro IDE**:
   - Visit [Kiro AI Developer Portal](https://developer.kiro.ai)
   - Register for a developer account
   - Download the Kiro IDE for your platform (Windows, macOS, Linux)

2. **Configure Kiro IDE**:
   - Install the IDE following the provided instructions
   - Launch the IDE and sign in with your developer credentials
   - Create a new project or open the EchoGuard project

3. **Set Up Kiro API Keys**:
   - Generate API keys from the Kiro Developer Portal
   - Add the keys to your project configuration
   - Test the connection to Kiro AI services

4. **Deploy Kiro Models**:
   ```
   cd backend
   ./deploy-kiro.bat
   ```
   Or on Linux/Mac:
   ```
   ./deploy-kiro.sh
   ```

### Using Kiro AI in EchoGuard

Kiro AI provides specialized compliance analysis for financial conversations:

- **Financial Regulations**: Checks for compliance with financial regulations
- **Disclosure Requirements**: Identifies missing required disclosures
- **Risk Assessment**: Evaluates risk levels in financial advice
- **Terminology Analysis**: Flags problematic financial terminology
- **Recommendation Compliance**: Ensures financial recommendations meet regulatory standards

## Deployment Guide

### Prerequisites

- AWS Account
- AWS CLI installed and configured
- Node.js and npm
- Python 3.11
- Kiro IDE (for Kiro AI integration)

### Quick Deployment

1. **Clone the repository**:
   ```
   git clone https://github.com/your-username/echoguard.git
   cd echoguard
   ```

2. **Deploy the backend**:
   ```
   ./deploy.bat
   ```
   Or on Linux/Mac:
   ```
   ./deploy.sh
   ```

3. **Deploy the frontend**:
   ```
   ./deploy-frontend.bat
   ```
   Or on Linux/Mac:
   ```
   ./deploy-frontend.sh
   ```

### Manual Deployment

For detailed step-by-step deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

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

## Documentation

- [User Guide](USER_GUIDE.md) - Complete guide for end users
- [Quick Start](QUICK_START.md) - Get started quickly with EchoGuard
- [Deployment Guide](DEPLOYMENT.md) - Detailed deployment instructions
- [Contributing Guide](CONTRIBUTING.md) - How to contribute to the project

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.