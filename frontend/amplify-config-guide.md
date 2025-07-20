# Amplify Configuration Guide for EchoGuard

This guide provides step-by-step instructions for configuring AWS Amplify for the EchoGuard frontend.

## Prerequisites
- Node.js and npm installed
- AWS account with appropriate permissions
- AWS CLI configured with your credentials
- Amplify CLI installed: `npm install -g @aws-amplify/cli`

## Step 1: Initialize Amplify

```bash
cd frontend
amplify init
```

When prompted:
- Enter a name for the project: `echoguard-ui`
- Choose your default editor
- Choose the type of app: `javascript`
- Choose the JavaScript framework: `react`
- Source directory path: `src`
- Distribution directory path: `build`
- Build command: `npm run build`
- Start command: `npm start`
- Select the authentication method: `AWS profile`
- Choose the AWS profile to use

## Step 2: Add Authentication

```bash
amplify add auth
```

When prompted:
- Choose default configuration or manual settings based on your requirements
- How do you want users to sign in: `Username`
- Do you want to configure advanced settings: `No`

## Step 3: Add Storage for Audio Files

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

## Step 4: Add API for Accessing DynamoDB

```bash
amplify add api
```

When prompted:
- Select `REST`
- Provide a resource name: `echoguardApi`
- Provide a path: `/audit-logs`
- Choose to create a new Lambda function: `Yes`
- Provide a name for the function: `echoguardApiFunction`
- Choose the runtime: `NodeJS`
- Choose the function template: `Serverless ExpressJS`
- Do you want to configure advanced settings: `Yes`
- Do you want to access other resources: `Yes`
- Select the categories: `storage`
- Select the operations: `read`
- Do you want to invoke this API on a recurring schedule: `No`
- Do you want to edit the local lambda function now: `No`

## Step 5: Update Lambda Function

Edit the Lambda function code in `amplify/backend/function/echoguardApiFunction/src/app.js` to add the following route:

```javascript
app.get('/audit-logs', async function(req, res) {
  // Get identity ID for the authenticated user
  const identityId = req.apiGateway.event.requestContext.identity.cognitoIdentityId;
  
  const AWS = require('aws-sdk');
  const docClient = new AWS.DynamoDB.DocumentClient();
  
  try {
    // Query the DynamoDB table
    const params = {
      TableName: 'EchoGuardAuditLogs'
    };
    
    const data = await docClient.scan(params).promise();
    res.json(data.Items);
  } catch (err) {
    res.status(500).json({ error: 'Could not load audit logs', details: err });
  }
});
```

## Step 6: Deploy Amplify Resources

```bash
amplify push
```

Confirm all the changes when prompted.

## Step 7: Add Hosting

```bash
amplify add hosting
```

When prompted:
- Select the plugin module: `Hosting with Amplify Console`
- Choose between manual or CI/CD deployment: Choose based on your preference
- Follow the remaining prompts to complete the setup

## Step 8: Publish the App

```bash
amplify publish
```

This will build and deploy your application to AWS Amplify hosting.

## Step 9: Connect Backend and Frontend

After deploying both the CloudFormation backend and Amplify frontend, you'll need to:

1. Update the Lambda function in Amplify to use the DynamoDB table created by CloudFormation
2. Configure the S3 trigger in CloudFormation to work with the Amplify Storage S3 bucket

These connections can be made through the AWS Console or by updating the respective configuration files.