#!/usr/bin/env python3
"""
EchoGuard Backend Deployment Script

This script deploys the EchoGuard backend infrastructure and Lambda functions.
"""

import os
import sys
import json
import boto3
import argparse
import zipfile
import tempfile
import shutil
from botocore.exceptions import ClientError

# AWS clients
cloudformation = boto3.client('cloudformation')
s3 = boto3.client('s3')
ssm = boto3.client('ssm')
lambda_client = boto3.client('lambda')

# Constants
LAMBDA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lambda')
CLOUDFORMATION_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cloudformation')
STACK_NAME = 'echoguard-backend'
LAMBDA_BUCKET_NAME = 'echoguard-lambda-code'
LAMBDA_FUNCTIONS = [
    'upload_handler',
    'transcribe_handler',
    'transcribe_complete_handler',
    'analysis_handler',
    'get_recordings_handler'
]

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Deploy EchoGuard backend')
    parser.add_argument('--environment', '-e', default='dev',
                        choices=['dev', 'test', 'prod'],
                        help='Deployment environment')
    parser.add_argument('--region', '-r', default='us-east-1',
                        help='AWS region')
    parser.add_argument('--kiro-api-endpoint', default='https://api.kiro.ai/compliance/analyze',
                        help='Kiro AI API endpoint')
    parser.add_argument('--kiro-api-key', default='',
                        help='Kiro AI API key')
    parser.add_argument('--cognito-user-pool-arn', default='',
                        help='Cognito User Pool ARN')
    return parser.parse_args()

def create_lambda_bucket(bucket_name, region):
    """Create S3 bucket for Lambda code if it doesn't exist"""
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} already exists")
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            if region == 'us-east-1':
                s3.create_bucket(Bucket=bucket_name)
            else:
                s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': region}
                )
            print(f"Created bucket {bucket_name}")
        else:
            raise

def zip_lambda_function(function_name):
    """Create a ZIP file for a Lambda function"""
    zip_path = os.path.join(tempfile.gettempdir(), f"{function_name}.zip")
    source_path = os.path.join(LAMBDA_DIR, f"{function_name}.py")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(source_path, os.path.basename(source_path))
    
    return zip_path

def upload_lambda_code(bucket_name, function_name, zip_path):
    """Upload Lambda code to S3"""
    key = f"lambda/{function_name}.zip"
    s3.upload_file(zip_path, bucket_name, key)
    print(f"Uploaded {function_name}.zip to s3://{bucket_name}/{key}")
    return key

def store_ssm_parameters(environment, kiro_api_endpoint, kiro_api_key, cognito_user_pool_arn):
    """Store parameters in SSM Parameter Store"""
    ssm.put_parameter(
        Name=f"/echoguard/{environment}/kiro_api_endpoint",
        Value=kiro_api_endpoint,
        Type="String",
        Overwrite=True
    )
    
    ssm.put_parameter(
        Name=f"/echoguard/{environment}/kiro_api_key",
        Value=kiro_api_key,
        Type="SecureString",
        Overwrite=True
    )
    
    ssm.put_parameter(
        Name=f"/echoguard/{environment}/cognito_user_pool_arn",
        Value=cognito_user_pool_arn,
        Type="String",
        Overwrite=True
    )
    
    print(f"Stored SSM parameters for environment {environment}")

def update_lambda_code(function_name, environment, bucket_name, key):
    """Update Lambda function code"""
    function_name_with_env = f"echoguard-{function_name.replace('_', '-')}-{environment}"
    try:
        lambda_client.update_function_code(
            FunctionName=function_name_with_env,
            S3Bucket=bucket_name,
            S3Key=key,
            Publish=True
        )
        print(f"Updated Lambda function {function_name_with_env}")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"Lambda function {function_name_with_env} not found, will be created by CloudFormation")
        else:
            raise

def deploy_cloudformation(environment, region, lambda_bucket):
    """Deploy CloudFormation stack"""
    template_path = os.path.join(CLOUDFORMATION_DIR, 'infrastructure.yaml')
    
    with open(template_path, 'r') as f:
        template_body = f.read()
    
    stack_name = f"{STACK_NAME}-{environment}"
    
    try:
        cloudformation.describe_stacks(StackName=stack_name)
        update_stack = True
    except ClientError as e:
        if 'does not exist' in str(e):
            update_stack = False
        else:
            raise
    
    parameters = [
        {
            'ParameterKey': 'Environment',
            'ParameterValue': environment
        }
    ]
    
    capabilities = ['CAPABILITY_NAMED_IAM']
    
    if update_stack:
        try:
            cloudformation.update_stack(
                StackName=stack_name,
                TemplateBody=template_body,
                Parameters=parameters,
                Capabilities=capabilities
            )
            print(f"Updating CloudFormation stack {stack_name}")
        except ClientError as e:
            if 'No updates are to be performed' in str(e):
                print(f"No updates needed for CloudFormation stack {stack_name}")
            else:
                raise
    else:
        cloudformation.create_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Parameters=parameters,
            Capabilities=capabilities
        )
        print(f"Creating CloudFormation stack {stack_name}")
    
    # Wait for stack to complete
    print("Waiting for CloudFormation stack to complete...")
    waiter = cloudformation.get_waiter('stack_update_complete' if update_stack else 'stack_create_complete')
    waiter.wait(StackName=stack_name)
    
    # Get stack outputs
    response = cloudformation.describe_stacks(StackName=stack_name)
    outputs = {output['OutputKey']: output['OutputValue'] for output in response['Stacks'][0]['Outputs']}
    
    print("\nStack outputs:")
    for key, value in outputs.items():
        print(f"{key}: {value}")
    
    return outputs

def main():
    """Main function"""
    args = parse_args()
    
    # Create Lambda code bucket
    lambda_bucket = f"{LAMBDA_BUCKET_NAME}-{args.environment}"
    create_lambda_bucket(lambda_bucket, args.region)
    
    # Store SSM parameters
    store_ssm_parameters(
        args.environment,
        args.kiro_api_endpoint,
        args.kiro_api_key,
        args.cognito_user_pool_arn
    )
    
    # Deploy CloudFormation stack
    outputs = deploy_cloudformation(args.environment, args.region, lambda_bucket)
    
    # Package and upload Lambda functions
    for function_name in LAMBDA_FUNCTIONS:
        zip_path = zip_lambda_function(function_name)
        key = upload_lambda_code(lambda_bucket, function_name, zip_path)
        update_lambda_code(function_name, args.environment, lambda_bucket, key)
        os.remove(zip_path)
    
    print("\nDeployment complete!")
    print(f"API URL: {outputs.get('ApiUrl', 'N/A')}")

if __name__ == "__main__":
    main()