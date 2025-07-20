# EchoGuard Deployment URL Guide

## Frontend URL Configuration

After deploying the EchoGuard frontend, you'll need to provide users with the correct URL to access the application.

### S3 Website Hosting URL

If you've deployed the frontend to S3 with website hosting enabled, the URL will follow this format:
```
http://{bucket-name}.s3-website-{region}.amazonaws.com
```

For example:
```
http://echoguard-frontend-123456789012.s3-website-us-east-1.amazonaws.com
```

### CloudFront Distribution URL

If you've set up CloudFront for HTTPS and better performance, the URL will be:
```
https://{distribution-id}.cloudfront.net
```

### Custom Domain

If you've configured a custom domain, users will access EchoGuard at:
```
https://echoguard.yourdomain.com
```

## Finding Your Deployment URL

After deployment, you can find your URL using one of these methods:

### For S3 Website Hosting:
```bash
aws s3 website s3://echoguard-frontend-YOUR_ACCOUNT_ID --get
```

### For CloudFront:
```bash
aws cloudfront list-distributions --query "DistributionList.Items[?contains(Origins.Items[0].DomainName, 'echoguard')].DomainName" --output text
```

## Updating User Guides

Once you have your deployment URL, update the following files with the correct URL:
- USER_GUIDE.md
- QUICK_START.md
- frontend/public/upload-guide.html

## Testing Access

After deployment, verify that your URL is accessible by:
1. Opening the URL in a web browser
2. Confirming the login page loads correctly
3. Testing user registration and login
4. Verifying that audio uploads work properly