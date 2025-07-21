import json
import boto3
import os
import time

# Initialize AWS clients
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

# Environment variables
TRANSCRIPT_BUCKET = os.environ.get('TRANSCRIPT_BUCKET', 'echoguard-transcripts-656570226565')
RECORDINGS_TABLE = os.environ.get('RECORDINGS_TABLE', 'echoguard-recordings')
ANALYSIS_TOPIC_ARN = os.environ.get('ANALYSIS_TOPIC_ARN', 'arn:aws:sns:us-east-1:656570226565:echoguard-analysis')

def lambda_handler(event, context):
    """
    Handles completion of transcription jobs and triggers analysis.
    
    Expected CloudWatch Event format:
    {
        "detail": {
            "TranscriptionJobName": "echoguard-abc-123-1626123456",
            "TranscriptionJobStatus": "COMPLETED"
        }
    }
    """
    try:
        # Extract job details from event
        job_name = event['detail']['TranscriptionJobName']
        job_status = event['detail']['TranscriptionJobStatus']
        
        # Get recording ID from job name
        recording_id = job_name.split('-')[1]
        
        if job_status == 'COMPLETED':
            # Update recording status in DynamoDB
            update_recording_status(recording_id, 'TRANSCRIBED')
            
            # Get transcript file path
            transcript_key = f"{recording_id}/transcript.json"
            
            # Trigger analysis
            notify_analysis_service(recording_id, transcript_key)
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Transcription completed successfully',
                    'recordingId': recording_id
                })
            }
        else:
            # Handle failed transcription
            update_recording_status(recording_id, 'TRANSCRIPTION_FAILED')
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Transcription failed',
                    'recordingId': recording_id,
                    'status': job_status
                })
            }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Error handling transcription completion',
                'error': str(e)
            })
        }

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

def notify_analysis_service(recording_id, transcript_key):
    """
    Sends an SNS notification to trigger the analysis process
    """
    message = {
        'recordingId': recording_id,
        'transcriptKey': transcript_key,
        'bucket': TRANSCRIPT_BUCKET
    }
    
    sns.publish(
        TopicArn=ANALYSIS_TOPIC_ARN,
        Message=json.dumps(message),
        Subject='Transcript Ready for Analysis'
    )