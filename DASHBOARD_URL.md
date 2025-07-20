# EchoGuard Dashboard and Authentication

I've created a complete authentication flow with a dashboard for EchoGuard.

## URLs

- **Authentication Page**: https://d4t0hj4peur25.cloudfront.net/auth.html
- **Dashboard Page**: https://d4t0hj4peur25.cloudfront.net/dashboard.html

## Authentication Flow

1. Visit the auth page
2. Login with existing credentials or sign up for a new account
3. After successful authentication, you'll be automatically redirected to the dashboard

## Test User Credentials

- **Email**: test@example.com
- **Password**: Test1234!

## Dashboard Features

The dashboard includes:

- **Recent Recordings**: View your uploaded recordings with compliance scores
- **Upload Tab**: Upload new audio recordings with drag-and-drop support
- **Settings Tab**: Manage your account and notification preferences
- **User Info**: Shows your email address and logout option
- **Compliance Overview**: Summary of your compliance metrics

## Notes

- The dashboard is a fully functional frontend demo
- Authentication is handled by Amazon Cognito
- File uploads are simulated (no actual processing occurs)
- Session management is implemented (login state is preserved)
