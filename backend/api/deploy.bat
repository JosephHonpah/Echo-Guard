@echo off
echo ===================================
echo EchoGuard API Deployment Script
echo ===================================

REM Check if AWS CLI is installed
where aws >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: AWS CLI is not installed or not in PATH.
    echo Please install AWS CLI and configure it with your credentials.
    echo Visit: https://aws.amazon.com/cli/
    exit /b 1
)

REM Check if AWS CLI is configured
aws sts get-caller-identity >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: AWS CLI is not configured properly.
    echo Please run 'aws configure' to set up your credentials.
    exit /b 1
)

REM Get backend stack outputs
echo Getting backend stack outputs...
aws cloudformation describe-stacks --stack-name echoguard-backend --query "Stacks[0].Outputs" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Backend stack not found. Please deploy the backend first.
    exit /b 1
)

REM Get S3 bucket name from previous deployment or prompt for it
set /p BUCKET_NAME=Enter S3 bucket name for Lambda code (same as backend deployment): 
if "%BUCKET_NAME%"=="" (
    echo Error: S3 bucket name is required.
    exit /b 1
)

REM Check if bucket exists
aws s3 ls s3://%BUCKET_NAME% >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: S3 bucket %BUCKET_NAME% does not exist.
    exit /b 1
)

REM Get DynamoDB table name and Audio bucket from stack outputs
for /f "tokens=2 delims=\"'" %%a in ('aws cloudformation describe-stacks --stack-name echoguard-backend --query "Stacks[0].Outputs[?OutputKey=='AuditTableName'].OutputValue | [0]"') do set AUDIT_TABLE=%%a
for /f "tokens=2 delims=\"'" %%a in ('aws cloudformation describe-stacks --stack-name echoguard-backend --query "Stacks[0].Outputs[?OutputKey=='AudioBucketName'].OutputValue | [0]"') do set AUDIO_BUCKET=%%a

echo Using DynamoDB table: %AUDIT_TABLE%
echo Using Audio bucket: %AUDIO_BUCKET%

REM Install dependencies
echo Installing dependencies...
npm install
if %ERRORLEVEL% NEQ 0 (
    echo Error installing dependencies.
    exit /b 1
)

REM Create API CloudFormation template
echo Creating API CloudFormation template...
(
echo Description: EchoGuard API Gateway and Lambda Function

echo Parameters:
  echo LambdaCodeBucket:
    echo Type: String
    echo Description: S3 bucket containing Lambda function code
    echo Default: %BUCKET_NAME%

echo Resources:
  echo ApiFunction:
    echo Type: AWS::Lambda::Function
    echo Properties:
      echo FunctionName: EchoGuardApiFunction
      echo Handler: index.handler
      echo Runtime: nodejs18.x
      echo Timeout: 30
      echo MemorySize: 256
      echo Code:
        echo S3Bucket: !Ref LambdaCodeBucket
        echo S3Key: api-function.zip
      echo Role: !GetAtt ApiFunctionRole.Arn
      echo Environment:
        echo Variables:
          echo AUDIT_TABLE: %AUDIT_TABLE%
          echo AUDIO_BUCKET: %AUDIO_BUCKET%

  echo ApiFunctionRole:
    echo Type: AWS::IAM::Role
    echo Properties:
      echo AssumeRolePolicyDocument:
        echo Version: '2012-10-17'
        echo Statement:
          echo - Effect: Allow
            echo Principal:
              echo Service: lambda.amazonaws.com
            echo Action: sts:AssumeRole
      echo ManagedPolicyArns:
        echo - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
        echo - arn:aws:iam::aws:policy/AmazonDynamoDBReadOnlyAccess
        echo - arn:aws:iam::aws:policy/AmazonS3FullAccess

  echo ApiGateway:
    echo Type: AWS::ApiGateway::RestApi
    echo Properties:
      echo Name: EchoGuardApi
      echo Description: API for EchoGuard Voice Compliance Logger
      echo EndpointConfiguration:
        echo Types:
          echo - REGIONAL

  echo ApiResource:
    echo Type: AWS::ApiGateway::Resource
    echo Properties:
      echo RestApiId: !Ref ApiGateway
      echo ParentId: !GetAtt ApiGateway.RootResourceId
      echo PathPart: '{proxy+}'

  echo ApiMethod:
    echo Type: AWS::ApiGateway::Method
    echo Properties:
      echo RestApiId: !Ref ApiGateway
      echo ResourceId: !Ref ApiResource
      echo HttpMethod: ANY
      echo AuthorizationType: NONE
      echo Integration:
        echo Type: AWS_PROXY
        echo IntegrationHttpMethod: POST
        echo Uri: !Sub arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${ApiFunction.Arn}/invocations

  echo ApiRootMethod:
    echo Type: AWS::ApiGateway::Method
    echo Properties:
      echo RestApiId: !Ref ApiGateway
      echo ResourceId: !GetAtt ApiGateway.RootResourceId
      echo HttpMethod: ANY
      echo AuthorizationType: NONE
      echo Integration:
        echo Type: AWS_PROXY
        echo IntegrationHttpMethod: POST
        echo Uri: !Sub arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${ApiFunction.Arn}/invocations

  echo ApiDeployment:
    echo Type: AWS::ApiGateway::Deployment
    echo DependsOn:
      echo - ApiMethod
      echo - ApiRootMethod
    echo Properties:
      echo RestApiId: !Ref ApiGateway
      echo StageName: prod

  echo LambdaApiGatewayPermission:
    echo Type: AWS::Lambda::Permission
    echo Properties:
      echo Action: lambda:InvokeFunction
      echo FunctionName: !Ref ApiFunction
      echo Principal: apigateway.amazonaws.com
      echo SourceArn: !Sub arn:aws:execute-api:${AWS::Region}:${AWS::AccountId}:${ApiGateway}/*

echo Outputs:
  echo ApiEndpoint:
    echo Description: URL of the API Gateway endpoint
    echo Value: !Sub https://${ApiGateway}.execute-api.${AWS::Region}.amazonaws.com/prod
) > api-template.yaml

REM Create zip file for Lambda function
echo Creating Lambda function zip file...
powershell Compress-Archive -Path src\*, package.json -DestinationPath api-function.zip -Force
if %ERRORLEVEL% NEQ 0 (
    echo Error creating Lambda function zip file.
    exit /b 1
)

REM Upload Lambda code to S3
echo Uploading Lambda code to S3...
aws s3 cp api-function.zip s3://%BUCKET_NAME%/
if %ERRORLEVEL% NEQ 0 (
    echo Error uploading Lambda code to S3.
    exit /b 1
)

REM Deploy API CloudFormation stack
echo Deploying API CloudFormation stack...
aws cloudformation deploy --template-file api-template.yaml --stack-name echoguard-api --capabilities CAPABILITY_IAM --parameter-overrides LambdaCodeBucket=%BUCKET_NAME%
if %ERRORLEVEL% NEQ 0 (
    echo Error deploying API CloudFormation stack.
    exit /b 1
)

REM Get API endpoint URL
echo Getting API endpoint URL...
for /f "tokens=2 delims=\"'" %%a in ('aws cloudformation describe-stacks --stack-name echoguard-api --query "Stacks[0].Outputs[?OutputKey=='ApiEndpoint'].OutputValue | [0]"') do set API_ENDPOINT=%%a

echo ===================================
echo API deployment complete!
echo ===================================
echo.
echo API Endpoint: %API_ENDPOINT%
echo.
echo Next steps:
echo 1. Use this API endpoint when configuring the Amplify frontend
echo 2. Test the API with: curl %API_ENDPOINT%/audit-logs
echo.