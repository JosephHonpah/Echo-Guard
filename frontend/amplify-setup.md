# EchoGuard Amplify Setup Guide

This guide provides step-by-step instructions for setting up AWS Amplify for the EchoGuard frontend.

## Prerequisites

- Node.js and npm installed
- AWS account with appropriate permissions
- AWS CLI configured with your credentials
- Amplify CLI installed: `npm install -g @aws-amplify/cli`
- Backend infrastructure deployed (CloudFormation stack)

## Step 1: Initialize the Project

First, make sure you're in the frontend directory:

```bash
cd frontend
```

Install the required dependencies:

```bash
npm install
```

## Step 2: Initialize Amplify

```bash
amplify init
```

When prompted:
- Enter a name for the project: `echoguard`
- Choose your default editor
- Choose the type of app: `javascript`
- Choose the JavaScript framework: `react`
- Source directory path: `src`
- Distribution directory path: `build`
- Build command: `npm run build`
- Start command: `npm start`
- Select the authentication method: `AWS profile`
- Choose the AWS profile to use

## Step 3: Add Authentication

```bash
amplify add auth
```

When prompted:
- Choose default configuration or manual settings based on your requirements
- How do you want users to sign in: `Username`
- Do you want to configure advanced settings: `No`

## Step 4: Add Storage for Audio Files

```bash
amplify add storage
```

When prompted:
- Select `Content`
- Provide a resource name: `echoguardaudio`
- Provide a bucket name: `echoguard-audio-frontend`
- Who should have access: `Auth users only`
- What kind of access: `create/update, read`
- Do you want to add a Lambda Trigger: `No`

## Step 5: Add API Connection

Instead of adding an API through Amplify, we'll connect to our existing API Gateway endpoint.

Create a `.env` file in the frontend directory:

```
REACT_APP_API_ENDPOINT=https://your-api-endpoint.execute-api.region.amazonaws.com/prod
```

Replace the URL with the actual API Gateway endpoint from your backend deployment.

## Step 6: Push Amplify Resources

```bash
amplify push
```

Confirm all the changes when prompted.

## Step 7: Update API Configuration

After pushing Amplify resources, you need to update the API configuration in `src/App.js`.

Make sure the API endpoint is correctly set:

```javascript
const apiConfig = {
  API: {
    endpoints: [
      {
        name: "echoguardApi",
        endpoint: process.env.REACT_APP_API_ENDPOINT
      }
    ]
  }
};
```

## Step 8: Add Hosting

```bash
amplify add hosting
```

When prompted:
- Select the plugin module: `Hosting with Amplify Console`
- Choose between manual or CI/CD deployment: Choose based on your preference
- Follow the remaining prompts to complete the setup

## Step 9: Publish the App

```bash
amplify publish
```

This will build and deploy your application to AWS Amplify hosting.

## Step 10: Testing the Application

After deployment, you should be able to:

1. Sign up and sign in to the application
2. Upload audio files for analysis
3. View compliance logs and statistics

## Troubleshooting

### API Connection Issues

If you're having trouble connecting to the API:

1. Check that the API endpoint URL is correct in the `.env` file
2. Ensure CORS is properly configured on the API Gateway
3. Verify that the API Lambda function has the necessary permissions

### Authentication Issues

If users can't sign in:

1. Check the Cognito User Pool settings in the AWS Console
2. Verify that the Amplify configuration is correct

### Storage Issues

If file uploads aren't working:

1. Check the S3 bucket permissions
2. Verify that authenticated users have upload permissions
3. Check the browser console for any errors during upload