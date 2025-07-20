import boto3
import os
import json
import logging
from urllib.parse import unquote_plus

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    
    try:
        # Get the object details from the event
        s3_obj = unquote_plus(event['Records'][0]['s3']['object']['key'])
        bucket = event['Records'][0]['s3']['bucket']['name']
        
        # Create a unique job name
        job_name = f"transcribe_{s3_obj.replace('/', '_').replace('.', '_')}_{context.aws_request_id}"
        job_name = job_name[:128]  # Ensure job name doesn't exceed AWS limits
        
        # Determine media format from file extension
        file_ext = s3_obj.split('.')[-1].lower()
        media_format = file_ext if file_ext in ['mp3', 'mp4', 'wav', 'flac'] else 'mp3'
        
        logger.info(f"Starting transcription job: {job_name} for s3://{bucket}/{s3_obj}")
        
        # Start transcription job
        transcribe = boto3.client('transcribe')
        response = transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': f's3://{bucket}/{s3_obj}'},
            MediaFormat=media_format,
            LanguageCode='en-US',
            OutputBucketName=os.environ['TRANSCRIBE_OUTPUT_BUCKET'],
            Settings={
                'ShowSpeakerLabels': True,
                'MaxSpeakerLabels': 10
            }
        )
        
        logger.info(f"Transcription job started: {response['TranscriptionJob']['TranscriptionJobStatus']}")
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "jobName": job_name,
                "status": response['TranscriptionJob']['TranscriptionJobStatus'],
                "file": s3_obj
            })
        }
        
    except Exception as e:
        logger.error(f"Error starting transcription job: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }