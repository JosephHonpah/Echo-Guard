# EchoGuard Testing Guide

Use this guide to verify that your EchoGuard deployment is working correctly.

## Prerequisites

- Deployed backend infrastructure
- Deployed API
- Deployed frontend
- Test audio files (MP3 format recommended)

## Test Cases

### 1. User Authentication

#### 1.1 User Registration
1. Access the EchoGuard application URL
2. Click "Create account"
3. Enter email, password, and other required information
4. Submit the form
5. Check your email for verification code
6. Enter verification code

**Expected Result**: Account created successfully and redirected to sign-in page

#### 1.2 User Sign-in
1. Enter your email and password
2. Click "Sign in"

**Expected Result**: Successfully signed in and redirected to the dashboard

### 2. Audio Upload

#### 2.1 Basic Upload
1. Navigate to the upload section
2. Select an MP3 audio file
3. Click "Upload Audio"

**Expected Result**: File uploads successfully with progress indicator

#### 2.2 Processing Verification
1. After upload completes, check AWS services:
   - S3: Verify file exists in audio bucket
   - CloudWatch: Check StartTranscribe Lambda logs
   - Amazon Transcribe: Verify job was created
   - CloudWatch: Check AnalyzeTranscript Lambda logs
   - DynamoDB: Verify record was created in EchoGuardAuditLogs table

**Expected Result**: Complete processing chain works without errors

### 3. Compliance Logs

#### 3.1 View Logs
1. Navigate to the Compliance Logs tab
2. Wait for your uploaded file to appear in the list

**Expected Result**: Processed file appears with compliance score, tone, and flags

#### 3.2 Filtering
1. Use the filters to search for specific compliance scores
2. Apply date filters

**Expected Result**: Filters work correctly and display matching results

### 4. Statistics

#### 4.1 View Statistics
1. Navigate to the Statistics tab
2. Check the overview metrics

**Expected Result**: Statistics display correctly with data from your uploads

### 5. Error Handling

#### 5.1 Invalid File Type
1. Try to upload a non-audio file (e.g., PDF)

**Expected Result**: Application shows appropriate error message

#### 5.2 Network Issues
1. Disable network connection
2. Try to upload a file

**Expected Result**: Application shows appropriate error message

## Monitoring During Testing

While testing, monitor these AWS services:

1. **CloudWatch Logs**:
   - `/aws/lambda/StartTranscribe`
   - `/aws/lambda/AnalyzeTranscript`
   - API Gateway logs

2. **S3 Buckets**:
   - Audio bucket
   - Transcript bucket

3. **DynamoDB**:
   - EchoGuardAuditLogs table

4. **Amazon Transcribe**:
   - Transcription jobs

## Performance Testing

For production readiness, consider these additional tests:

1. **Concurrent Uploads**:
   - Upload multiple files simultaneously
   - Verify all are processed correctly

2. **Large Files**:
   - Test with audio files of various sizes
   - Verify processing of longer recordings (30+ minutes)

3. **Load Testing**:
   - Simulate multiple users accessing the application
   - Monitor API response times

## Security Testing

1. **Authentication**:
   - Verify unauthenticated users cannot access protected resources
   - Test password reset functionality

2. **API Security**:
   - Verify API endpoints require authentication
   - Check for proper error handling of invalid requests

## Reporting Issues

If you encounter any issues during testing:

1. Capture the exact steps to reproduce
2. Note any error messages (frontend and CloudWatch logs)
3. Record the time of the error
4. Document the expected vs. actual behavior