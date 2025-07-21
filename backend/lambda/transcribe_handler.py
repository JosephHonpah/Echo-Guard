import json
import boto3
import os
import uuid
import time
from datetime import datetime

# Initialize AWS clients
s3 = boto3.client('s3')
transcribe = boto3.client('transcribe')
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

# Environment variables
AUDIO_BUCKET = os.environ.get('AUDIO_BUCKET', 'echoguard-audio-656570226565')
TRANSCRIPT_BUCKET = os.environ.get('TRANSCRIPT_BUCKET', 'echoguard-transcripts-656570226565')
RECORDINGS_TABLE = os.environ.get('RECORDINGS_TABLE', 'echoguard-recordings')
ANALYSIS_TOPIC_ARN = os.environ.get('ANALYSIS_TOPIC_ARN', 'arn:aws:sns:us-east-1:656570226565:echoguard-analysis')

def lambda_handler(event, context):
    """
    Handles transcription of audio files using Amazon Transcribe.
    
    Expected SNS event format:
    {
        "recordingId": "abc-123",
        "s3Key": "user123/abc-123/recording.mp3",
        "bucket": "echoguard-audio-656570226565"
    }
    """
    try:
        # Extract message from SNS event
        message = json.loads(event['Records'][0]['Sns']['Message'])
        
        recording_id = message.get('recordingId')
        s3_key = message.get('s3Key')
        bucket = message.get('bucket', AUDIO_BUCKET)
        
        # Update recording status in DynamoDB
        update_recording_status(recording_id, 'TRANSCRIBING')
        
        # Start transcription job
        job_name = f"echoguard-{recording_id}-{int(time.time())}"
        media_uri = f"s3://{bucket}/{s3_key}"
        
        response = transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': media_uri},
            MediaFormat=get_media_format(s3_key),
            LanguageCode='en-US',
            OutputBucketName=TRANSCRIPT_BUCKET,
            OutputKey=f"{recording_id}/transcript.json"
        )
        
        # Store transcription job details in DynamoDB
        recordings_table = dynamodb.Table(RECORDINGS_TABLE)
        recordings_table.update_item(
            Key={'recordingId': recording_id},
            UpdateExpression="set transcriptionJobId = :jobId, transcriptionJobName = :jobName, updatedAt = :timestamp",
            ExpressionAttributeValues={
                ':jobId': response['TranscriptionJob']['TranscriptionJobName'],
                ':jobName': job_name,
                ':timestamp': int(time.time())
            }
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Transcription job started successfully',
                'recordingId': recording_id,
                'transcriptionJobName': job_name
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        
        # Update recording status to error if we have a recording ID
        if 'recording_id' in locals():
            update_recording_status(recording_id, 'TRANSCRIPTION_ERROR')
        
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error starting transcription job',
                'error': str(e)
            })
        }

def get_media_format(s3_key):
    """
    Determines the media format based on the file extension
    """
    extension = s3_key.split('.')[-1].lower()
    
    format_mapping = {
        'mp3': 'mp3',
        'mp4': 'mp4',
        'wav': 'wav',
        'flac': 'flac',
        'm4a': 'mp4',
        'ogg': 'ogg'
    }
    
    return format_mapping.get(extension, 'mp3')

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