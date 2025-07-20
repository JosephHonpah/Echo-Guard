import json
import os
import unittest
from unittest.mock import patch, MagicMock

import boto3
import pytest
from moto import mock_s3, mock_transcribe

# Import the Lambda function
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lambda'))
import start_transcribe

@mock_s3
@mock_transcribe
class TestStartTranscribe(unittest.TestCase):
    def setUp(self):
        # Set up mock S3 bucket and file
        self.s3 = boto3.client('s3', region_name='us-east-1')
        self.s3.create_bucket(Bucket='echoguard-audio')
        self.s3.put_object(
            Bucket='echoguard-audio',
            Key='test-audio.mp3',
            Body=b'test audio content'
        )
        
        # Mock event
        self.event = {
            'Records': [{
                's3': {
                    'bucket': {'name': 'echoguard-audio'},
                    'object': {'key': 'test-audio.mp3'}
                }
            }]
        }
        
        # Set environment variables
        os.environ['TRANSCRIPT_BUCKET'] = 'echoguard-transcripts'
        os.environ['AWS_REGION'] = 'us-east-1'
    
    @patch('start_transcribe.transcribe_client')
    def test_lambda_handler(self, mock_transcribe_client):
        # Mock the start_transcription_job method
        mock_start_job = MagicMock()
        mock_transcribe_client.start_transcription_job = mock_start_job
        
        # Call the Lambda handler
        response = start_transcribe.lambda_handler(self.event, {})
        
        # Assert that start_transcription_job was called with correct parameters
        mock_start_job.assert_called_once()
        call_args = mock_start_job.call_args[1]
        
        self.assertEqual(call_args['TranscriptionJobName'].startswith('echoguard-'), True)
        self.assertEqual(call_args['LanguageCode'], 'en-US')
        self.assertEqual(call_args['Media']['MediaFileUri'].startswith('s3://echoguard-audio/test-audio.mp3'), True)
        self.assertEqual(call_args['OutputBucketName'], 'echoguard-transcripts')
        
        # Assert the response
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Started transcription job', response['body'])

if __name__ == '__main__':
    unittest.main()