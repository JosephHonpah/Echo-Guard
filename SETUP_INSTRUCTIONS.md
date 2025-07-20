# EchoGuard Frontend Setup Instructions

Since we need Node.js and npm to deploy the frontend, follow these steps on a machine with Node.js installed:

## Step 1: Install Node.js and NPM

1. Download Node.js from [https://nodejs.org/](https://nodejs.org/) (LTS version recommended)
2. Follow the installation instructions for your operating system
3. Verify installation by running:
   ```
   node --version
   npm --version
   ```

## Step 2: Install the Amplify CLI

```bash
npm install -g @aws-amplify/cli
```

## Step 3: Configure AWS Credentials

If you haven't already configured AWS credentials:

```bash
aws configure
```

Enter your AWS Access Key ID, Secret Access Key, default region, and output format.

## Step 4: Clone the Repository

Clone the EchoGuard repository to your local machine or copy the files.

## Step 5: Initialize Amplify

Navigate to the frontend directory:

```bash
cd frontend
```

Initialize Amplify:

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

## Step 6: Add Authentication

```bash
amplify add auth
```

When prompted:
- Choose default configuration
- How do you want users to sign in: `Email`
- Do you want to configure advanced settings: `No`

## Step 7: Add Storage

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

## Step 8: Install Frontend Dependencies

```bash
npm install
```

## Step 9: Deploy the Frontend

```bash
amplify add hosting
```

When prompted:
- Select `Hosting with Amplify Console`
- Choose `Manual deployment`

Then publish:

```bash
amplify publish
```

## Step 10: Update API Configuration

After deployment, you may need to update the API configuration in the Amplify Console:

1. Go to the AWS Amplify Console
2. Select your app
3. Go to Environment Variables
4. Add the environment variable:
   - Key: `REACT_APP_API_ENDPOINT`
   - Value: `https://j5pdd9cbul.execute-api.us-east-1.amazonaws.com/prod`
5. Save and redeploy

## Step 11: Test the Application

1. Open the deployed application URL
2. Sign up for a new account and verify your email
3. Upload an audio file for testing
4. Check the CloudWatch Logs for Lambda functions to verify processing
5. View the compliance logs in the application