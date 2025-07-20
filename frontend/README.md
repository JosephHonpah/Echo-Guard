# EchoGuard Frontend

This is the React frontend for the EchoGuard Voice-to-Text Compliance Logger.

## Setup Instructions

1. Install dependencies:
   ```
   npm install
   ```

2. Initialize Amplify:
   ```
   amplify init
   ```

3. Add authentication:
   ```
   amplify add auth
   ```

4. Add storage:
   ```
   amplify add storage
   ```

5. Add API:
   ```
   amplify add api
   ```

6. Push changes to AWS:
   ```
   amplify push
   ```

7. Start the development server:
   ```
   npm start
   ```

## Deployment

To deploy the application:
```
amplify add hosting
amplify publish
```