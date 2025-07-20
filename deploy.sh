#!/bin/bash
# EchoGuard Deployment Script

set -e

# Configuration
REGION="us-east-1"
ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
LAMBDA_BUCKET="echoguard-lambda-${ACCOUNT_ID}"
FRONTEND_BUCKET="echoguard-frontend-${ACCOUNT_ID}"
BACKEND_STACK_NAME="echoguard-backend"
API_STACK_NAME="echoguard-api"

echo "=== EchoGuard Deployment ==="
echo "AWS Account: ${ACCOUNT_ID}"
echo "Region: ${REGION}"

# Check AWS CLI configuration
echo "Checking AWS CLI configuration..."
aws sts get-caller-identity > /dev/null || { echo "Error: AWS CLI not configured properly"; exit 1; }

# Create S3 buckets if they don't exist
echo "Creating S3 buckets..."
aws s3 mb s3://${LAMBDA_BUCKET} --region ${REGION} || true
aws s3 mb s3://${FRONTEND_BUCKET} --region ${REGION} || true

# Configure frontend bucket for static website hosting
echo "Configuring frontend bucket for static website hosting..."
aws s3 website s3://${FRONTEND_BUCKET} --index-document index.html --error-document index.html

# Set bucket policy for frontend
echo "Setting bucket policy for frontend..."
cat > bucket-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::${FRONTEND_BUCKET}/*"
    }
  ]
}
EOF

aws s3api put-public-access-block --bucket ${FRONTEND_BUCKET} --public-access-block-configuration "BlockPublicAcls=false,IgnorePublicAcls=false,BlockPublicPolicy=false,RestrictPublicBuckets=false"
aws s3api put-bucket-policy --bucket ${FRONTEND_BUCKET} --policy file://bucket-policy.json

# Package Lambda functions
echo "Packaging Lambda functions..."
cd backend/lambda
zip -r start_transcribe.zip start_transcribe.py
zip -r analyze_transcript.zip analyze_transcript.py
aws s3 cp start_transcribe.zip s3://${LAMBDA_BUCKET}/
aws s3 cp analyze_transcript.zip s3://${LAMBDA_BUCKET}/
cd ../..

# Deploy backend infrastructure
echo "Deploying backend infrastructure..."
cd backend
aws cloudformation deploy \
  --template-file infrastructure.yaml \
  --stack-name ${BACKEND_STACK_NAME} \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides LambdaCodeBucket=${LAMBDA_BUCKET}
cd ..

# Package and deploy API
echo "Packaging and deploying API..."
cd backend/api
zip -r api-function.zip src/
aws s3 cp api-function.zip s3://${LAMBDA_BUCKET}/
aws cloudformation deploy \
  --template-file api-template.yaml \
  --stack-name ${API_STACK_NAME} \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides LambdaCodeBucket=${LAMBDA_BUCKET}
cd ../..

# Get API endpoint
API_ENDPOINT=$(aws cloudformation describe-stacks --stack-name ${API_STACK_NAME} --query "Stacks[0].Outputs[?OutputKey=='ApiEndpoint'].OutputValue" --output text)
echo "API Endpoint: ${API_ENDPOINT}"

# Set up Cognito
echo "Setting up Cognito..."
USER_POOL_ID=$(aws cognito-idp create-user-pool --pool-name EchoGuardUserPool --auto-verified-attributes email --username-attributes email --query "UserPool.Id" --output text)
CLIENT_ID=$(aws cognito-idp create-user-pool-client --user-pool-id ${USER_POOL_ID} --client-name EchoGuardWebClient --no-generate-secret --explicit-auth-flows ALLOW_USER_PASSWORD_AUTH ALLOW_REFRESH_TOKEN_AUTH --query "UserPoolClient.ClientId" --output text)
IDENTITY_POOL_ID=$(aws cognito-identity create-identity-pool --identity-pool-name EchoGuardIdentityPool --allow-unauthenticated-identities false --cognito-identity-providers ProviderName="cognito-idp.${REGION}.amazonaws.com/${USER_POOL_ID}",ClientId="${CLIENT_ID}" --query "IdentityPoolId" --output text)

echo "User Pool ID: ${USER_POOL_ID}"
echo "Client ID: ${CLIENT_ID}"
echo "Identity Pool ID: ${IDENTITY_POOL_ID}"

# Create IAM roles for Cognito
echo "Creating IAM roles for Cognito..."
cat > auth-role-trust-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "cognito-identity.amazonaws.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "cognito-identity.amazonaws.com:aud": "${IDENTITY_POOL_ID}"
        },
        "ForAnyValue:StringLike": {
          "cognito-identity.amazonaws.com:amr": "authenticated"
        }
      }
    }
  ]
}
EOF

AUTH_ROLE_ARN=$(aws iam create-role --role-name EchoGuardAuthRole --assume-role-policy-document file://auth-role-trust-policy.json --query "Role.Arn" --output text)

cat > auth-role-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "execute-api:Invoke"
      ],
      "Resource": [
        "arn:aws:execute-api:${REGION}:${ACCOUNT_ID}:*/*"
      ]
    }
  ]
}
EOF

aws iam put-role-policy --role-name EchoGuardAuthRole --policy-name EchoGuardAuthPolicy --policy-document file://auth-role-policy.json
aws cognito-identity set-identity-pool-roles --identity-pool-id ${IDENTITY_POOL_ID} --roles authenticated=${AUTH_ROLE_ARN}

# Update frontend configuration
echo "Updating frontend configuration..."
cat > frontend/src/aws-exports.js << EOF
// AWS Amplify configuration
const awsmobile = {
    "aws_project_region": "${REGION}",
    "aws_cognito_identity_pool_id": "${IDENTITY_POOL_ID}",
    "aws_cognito_region": "${REGION}",
    "aws_user_pools_id": "${USER_POOL_ID}",
    "aws_user_pools_web_client_id": "${CLIENT_ID}",
    "oauth": {},
    "aws_cloud_logic_custom": [
        {
            "name": "echoguardApi",
            "endpoint": "${API_ENDPOINT}",
            "region": "${REGION}"
        }
    ]
};

export default awsmobile;
EOF

# Build and deploy frontend
echo "Building and deploying frontend..."
cd frontend
npm ci
npm run build
aws s3 sync build/ s3://${FRONTEND_BUCKET} --delete
cd ..

# Output deployment information
FRONTEND_URL="http://${FRONTEND_BUCKET}.s3-website-${REGION}.amazonaws.com"
echo ""
echo "=== Deployment Complete ==="
echo "Frontend URL: ${FRONTEND_URL}"
echo "API Endpoint: ${API_ENDPOINT}"
echo "User Pool ID: ${USER_POOL_ID}"
echo "Client ID: ${CLIENT_ID}"
echo ""
echo "Next steps:"
echo "1. Access the application at: ${FRONTEND_URL}"
echo "2. Sign up for an account and verify your email"
echo "3. Upload audio files for compliance analysis"
echo "4. View compliance logs and statistics in the dashboard"