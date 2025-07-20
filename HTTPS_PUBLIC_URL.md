# EchoGuard HTTPS Public URL

The EchoGuard application is now available with HTTPS and public signup at:

**URL**: https://d4t0hj4peur25.cloudfront.net

## Features

- **HTTPS Security**: All traffic is encrypted using CloudFront's SSL/TLS certificate
- **Public Signup**: Anyone can create an account and use the application
- **Email Verification**: New users must verify their email address
- **Secure Authentication**: Powered by Amazon Cognito

## How to Use

### For New Users:

1. Visit https://d4t0hj4peur25.cloudfront.net
2. Click "Login with Cognito"
3. Click "Sign up" to create a new account
4. Enter your email and create a password
5. Check your email for a verification code
6. Enter the verification code to complete registration
7. Log in with your new credentials

### For Existing Users:

- **Email**: test@example.com
- **Password**: Test1234!

## Technical Details

- **CloudFront Distribution**: E2B3ZARQ08OD5M
- **Cognito User Pool**: us-east-1_q03tLrCfS
- **App Client ID**: 4ks45uv9681eh9hnevrutksqru

## Notes

- The CloudFront distribution may take up to 15 minutes to fully deploy
- If you encounter "Distribution not ready" errors, please wait and try again
- Email verification is required for all new accounts