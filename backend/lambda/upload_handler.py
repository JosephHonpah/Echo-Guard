import json
import boto3
import os
import uuid
import time
from datetime import datetime

# Initialize AWS clients
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

# Environment variables
AUDIO_BUCKET = os.environ.get('AUDIO_BUCKET', 'echoguard-audio-656570226565')
RECORDINGS_TABLE = os.environ.get('RECORDINGS_TABLE', 'echoguard-recordings')
TRANSCRIBE_TOPIC_ARN = os.environ.get('TRANSCRIBE_TOPIC_ARN', 'arn:aws:sns:us-east-1:656570226565:echoguard-transcribe')

def lambda_handler(event, context):
    """
    Handles audio file uploads, stores metadata in DynamoDB, and initiates transcription.
    
    Expected event format:
    {
        "userId": "user123",
        "fileName": "recording.mp3",
        "fileType": "audio/mp3",
        "description": "Customer call about investment options"
    }
    """
    try:
        # Extract data from event
        user_id = event.get('userId')
        file_name = event.get('fileName')
        file_type = event.get('fileType')
        description = event.get('description', 'Audio Recording')
        
        # Generate unique recording ID
        recording_id = str(uuid.uuid4())
        timestamp = int(time.time())
        date_str = datetime.now().strftime('%Y-%m-%d')
        
        # Generate pre-signed URL for file upload
        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': AUDIO_BUCKET,
                'Key': f"{user_id}/{recording_id}/{file_name}",
                'ContentType': file_type
            },
            ExpiresIn=300  # URL valid for 5 minutes
        )
        
        # Store recording metadata in DynamoDB
        recordings_table = dynamodb.Table(RECORDINGS_TABLE)
        recordings_table.put_item(
            Item={
                'recordingId': recording_id,
                'userId': user_id,
                'fileName': file_name,
                'fileType': file_type,
                'description': description,
                's3Key': f"{user_id}/{recording_id}/{file_name}",
                'uploadDate': date_str,
                'timestamp': timestamp,
                'status': 'PENDING_UPLOAD',
                'createdAt': timestamp
            }
        )
        
        # Return pre-signed URL and recording ID
        return {
            'statusCode': 200,
            'body': json.dumps({
                'recordingId': recording_id,
                'uploadUrl': presigned_url,
                'message': 'Upload URL generated successfully'
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error generating upload URL',
                'error': str(e)
            })
        }

def notify_transcribe_service(recording_id, s3_key):
    """
    Sends an SNS notification to trigger the transcription process
    """
    message = {
        'recordingId': recording_id,
        's3Key': s3_key,
        'bucket': AUDIO_BUCKET
    }
    
    sns.publish(
        TopicArn=TRANSCRIBE_TOPIC_ARN,
        Message=json.dumps(message),
        Subject='New Audio Upload'
    )