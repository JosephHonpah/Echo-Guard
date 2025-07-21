import json
import boto3
import os
import time
import requests
from botocore.exceptions import ClientError

# Initialize AWS clients
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')
bedrock = boto3.client('bedrock-runtime')

# Environment variables
TRANSCRIPT_BUCKET = os.environ.get('TRANSCRIPT_BUCKET', 'echoguard-transcripts-656570226565')
RECORDINGS_TABLE = os.environ.get('RECORDINGS_TABLE', 'echoguard-recordings')
RESULTS_TABLE = os.environ.get('RESULTS_TABLE', 'echoguard-results')
NOTIFICATION_TOPIC_ARN = os.environ.get('NOTIFICATION_TOPIC_ARN', 'arn:aws:sns:us-east-1:656570226565:echoguard-notifications')
KIRO_API_ENDPOINT = os.environ.get('KIRO_API_ENDPOINT', 'https://api.kiro.ai/compliance/analyze')
KIRO_API_KEY = os.environ.get('KIRO_API_KEY', 'kiro-api-key')

def lambda_handler(event, context):
    """
    Handles analysis of transcripts using Amazon Bedrock and Kiro AI.
    
    Expected SNS event format:
    {
        "recordingId": "abc-123",
        "transcriptKey": "abc-123/transcript.json",
        "bucket": "echoguard-transcripts-656570226565"
    }
    """
    try:
        # Extract message from SNS event
        message = json.loads(event['Records'][0]['Sns']['Message'])
        
        recording_id = message.get('recordingId')
        transcript_key = message.get('transcriptKey')
        bucket = message.get('bucket', TRANSCRIPT_BUCKET)
        
        # Update recording status in DynamoDB
        update_recording_status(recording_id, 'ANALYZING')
        
        # Get transcript from S3
        transcript_obj = s3.get_object(Bucket=bucket, Key=transcript_key)
        transcript_data = json.loads(transcript_obj['Body'].read().decode('utf-8'))
        
        # Extract transcript text
        transcript_text = transcript_data['results']['transcripts'][0]['transcript']
        
        # Get recording metadata
        recordings_table = dynamodb.Table(RECORDINGS_TABLE)
        recording = recordings_table.get_item(Key={'recordingId': recording_id})['Item']
        
        # Analyze with Amazon Bedrock
        bedrock_results = analyze_with_bedrock(transcript_text, recording.get('description', ''))
        
        # Analyze with Kiro AI
        kiro_results = analyze_with_kiro(transcript_text, recording.get('description', ''))
        
        # Calculate compliance score
        compliance_score = calculate_compliance_score(bedrock_results, kiro_results)
        
        # Store analysis results in DynamoDB
        store_analysis_results(recording_id, transcript_text, bedrock_results, kiro_results, compliance_score)
        
        # Update recording status and score
        update_recording_completed(recording_id, compliance_score)
        
        # Send notification
        send_completion_notification(recording_id, compliance_score, recording.get('userId'))
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Analysis completed successfully',
                'recordingId': recording_id,
                'complianceScore': compliance_score
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        
        # Update recording status to error if we have a recording ID
        if 'recording_id' in locals():
            update_recording_status(recording_id, 'ANALYSIS_ERROR')
        
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error analyzing transcript',
                'error': str(e)
            })
        }

def analyze_with_bedrock(transcript_text, description):
    """
    Analyzes transcript using Amazon Bedrock
    """
    try:
        prompt = f"""
        You are a compliance expert analyzing a transcript of a conversation. 
        Identify any potential compliance issues in the following transcript.
        
        Context: {description}
        
        Transcript:
        {transcript_text}
        
        Please provide:
        1. A list of potential compliance issues
        2. A risk level for each issue (Low, Medium, High)
        3. Recommendations to address each issue
        4. An overall compliance risk score from 0-100 (where 0 is high risk and 100 is fully compliant)
        
        Format your response as JSON with the following structure:
        {{
            "issues": [
                {{
                    "description": "Issue description",
                    "risk_level": "Low|Medium|High",
                    "recommendation": "How to address this issue"
                }}
            ],
            "overall_score": 85,
            "summary": "Brief summary of compliance analysis"
        }}
        """
        
        # Call Amazon Bedrock
        response = bedrock.invoke_model(
            modelId='anthropic.claude-v2',
            body=json.dumps({
                "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
                "max_tokens_to_sample": 4000,
                "temperature": 0.1
            })
        )
        
        response_body = json.loads(response['body'].read())
        result_text = response_body['completion']
        
        # Extract JSON from the response
        json_start = result_text.find('{')
        json_end = result_text.rfind('}') + 1
        json_str = result_text[json_start:json_end]
        
        return json.loads(json_str)
        
    except Exception as e:
        print(f"Bedrock analysis error: {str(e)}")
        # Return a default response in case of error
        return {
            "issues": [],
            "overall_score": 50,
            "summary": "Error analyzing transcript with Bedrock"
        }

def analyze_with_kiro(transcript_text, description):
    """
    Analyzes transcript using Kiro AI
    """
    try:
        # Prepare request to Kiro AI API
        headers = {
            'Authorization': f'Bearer {KIRO_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'transcript': transcript_text,
            'context': description,
            'domain': 'financial',
            'detailed': True
        }
        
        # Call Kiro AI API
        response = requests.post(KIRO_API_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        
        return response.json()
        
    except Exception as e:
        print(f"Kiro analysis error: {str(e)}")
        # Return a default response in case of error
        return {
            "financial_compliance_score": 50,
            "issues": [],
            "summary": "Error analyzing transcript with Kiro AI"
        }

def calculate_compliance_score(bedrock_results, kiro_results):
    """
    Calculates overall compliance score based on both analysis results
    """
    bedrock_score = bedrock_results.get('overall_score', 50)
    kiro_score = kiro_results.get('financial_compliance_score', 50)
    
    # Weight Kiro AI higher for financial compliance
    weighted_score = (bedrock_score * 0.4) + (kiro_score * 0.6)
    
    return round(weighted_score)

def store_analysis_results(recording_id, transcript_text, bedrock_results, kiro_results, compliance_score):
    """
    Stores analysis results in DynamoDB
    """
    results_table = dynamodb.Table(RESULTS_TABLE)
    
    # Combine issues from both analyses
    all_issues = []
    
    # Add Bedrock issues
    for issue in bedrock_results.get('issues', []):
        all_issues.append({
            'source': 'Bedrock',
            'description': issue.get('description', ''),
            'risk_level': issue.get('risk_level', 'Medium'),
            'recommendation': issue.get('recommendation', '')
        })
    
    # Add Kiro issues
    for issue in kiro_results.get('issues', []):
        all_issues.append({
            'source': 'Kiro AI',
            'description': issue.get('description', ''),
            'risk_level': issue.get('severity', 'Medium'),
            'recommendation': issue.get('recommendation', '')
        })
    
    # Store results
    results_table.put_item(
        Item={
            'recordingId': recording_id,
            'transcript': transcript_text,
            'bedrockResults': bedrock_results,
            'kiroResults': kiro_results,
            'issues': all_issues,
            'complianceScore': compliance_score,
            'bedrockSummary': bedrock_results.get('summary', ''),
            'kiroSummary': kiro_results.get('summary', ''),
            'timestamp': int(time.time())
        }
    )

def update_recording_status(recording_id, status):
    """
    Updates the status of a recording in DynamoDB
    """
    recordings_table = dynamodb.Table(RECORDINGS_TABLE)
    recordings_table.update_item(
        Key={'recordingId': recording_id},
        UpdateExpression="set #status = :status, updatedAt = :timestamp",
        ExpressionAttributeNames={
            '#status': 'status'
        },
        ExpressionAttributeValues={
            ':status': status,
            ':timestamp': int(time.time())
        }
    )

def update_recording_completed(recording_id, compliance_score):
    """
    Updates the recording with completed status and compliance score
    """
    recordings_table = dynamodb.Table(RECORDINGS_TABLE)
    recordings_table.update_item(
        Key={'recordingId': recording_id},
        UpdateExpression="set #status = :status, complianceScore = :score, updatedAt = :timestamp",
        ExpressionAttributeNames={
            '#status': 'status'
        },
        ExpressionAttributeValues={
            ':status': 'COMPLETED',
            ':score': compliance_score,
            ':timestamp': int(time.time())
        }
    )

def send_completion_notification(recording_id, compliance_score, user_id):
    """
    Sends an SNS notification about completed analysis
    """
    message = {
        'recordingId': recording_id,
        'userId': user_id,
        'complianceScore': compliance_score,
        'timestamp': int(time.time())
    }
    
    sns.publish(
        TopicArn=NOTIFICATION_TOPIC_ARN,
        Message=json.dumps(message),
        Subject='Compliance Analysis Completed'
    )