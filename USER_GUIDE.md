# EchoGuard User Guide

## Accessing EchoGuard

EchoGuard is available at: `https://echoguard-frontend-656570226565.s3-website-us-east-1.amazonaws.com`

## User Registration and Login

1. **Register a New Account**:
   - Visit the EchoGuard website
   - Click "Create Account"
   - Enter your email address, password, and other required information
   - Check your email for a verification code
   - Enter the verification code to complete registration

2. **Login**:
   - Enter your email and password
   - If you've forgotten your password, click "Forgot Password" to reset it

## Uploading Audio Recordings

1. **Navigate to Upload Page**:
   - After logging in, click on "Upload" in the navigation menu

2. **Select Audio Files**:
   - Click "Choose File" or drag and drop audio files onto the upload area
   - Supported formats: MP3, WAV, M4A, FLAC (up to 100MB per file)

3. **Add Metadata (Optional)**:
   - Enter a description for the recording
   - Select a category (e.g., "Customer Call", "Meeting", "Interview")
   - Add any relevant tags

4. **Upload**:
   - Click the "Upload" button
   - A progress bar will show the upload status
   - Wait for confirmation that the upload is complete

## Viewing Compliance Analysis

1. **Dashboard**:
   - The main dashboard shows recent uploads and their compliance status
   - Green: High compliance (80-100%)
   - Yellow: Moderate compliance (60-79%)
   - Red: Low compliance (0-59%)

2. **Detailed Analysis**:
   - Click on any recording to view detailed analysis
   - You'll see:
     - Transcript of the audio
     - Overall compliance score
     - Specific compliance issues detected
     - Recommendations for improvement
     - Dual analysis from both AI systems (Bedrock and Kiro)

3. **Filtering and Searching**:
   - Use the search bar to find specific recordings
   - Filter by date, compliance score, or category

## Receiving Alerts

1. **Email Alerts**:
   - You'll receive email notifications for low compliance scores
   - Configure alert thresholds in your profile settings

2. **Dashboard Notifications**:
   - The dashboard shows real-time alerts for new compliance issues

## Direct Upload API (For Developers)

For automated uploads or integration with other systems:

```
POST https://api.echoguard.example.com/upload
Authorization: Bearer YOUR_API_KEY
Content-Type: multipart/form-data

Form fields:
- file: The audio file
- description: (Optional) Description of the recording
- category: (Optional) Category of the recording
```

## Troubleshooting

- **Upload Issues**: Ensure your file is under 100MB and in a supported format
- **Playback Problems**: Try downloading the file and playing it locally
- **Missing Analysis**: Analysis typically takes 1-5 minutes to complete

## Support

For assistance, contact support at support@echoguard.example.com or use the in-app chat feature.