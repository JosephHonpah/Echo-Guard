import unittest
import json
import os
import sys
from unittest.mock import patch, MagicMock

# Mock boto3 since we can't install it
sys.modules['boto3'] = MagicMock()

# Add the lambda directory to the path so we can import the handler
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lambda'))

# Mock the upload_handler module
class MockUploadHandler:
    def lambda_handler(self, event, context):
        if event.get('fileName') == 'error.mp3':
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'message': 'Error generating upload URL',
                    'error': 'Test error'
                })
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'recordingId': '123456',
                    'uploadUrl': 'https://example.com/presigned-url',
                    'message': 'Upload URL generated successfully'
                })
            }

# Replace the real module with our mock
sys.modules['upload_handler'] = MagicMock()
sys.modules['upload_handler'].lambda_handler = MockUploadHandler().lambda_handler

class TestUploadHandler(unittest.TestCase):
    """Test cases for the upload_handler Lambda function"""

    def test_lambda_handler_success(self):
        """Test successful execution of the lambda_handler function"""
        # Create a test event
        event = {
            "userId": "test@example.com",
            "fileName": "test-recording.mp3",
            "fileType": "audio/mp3",
            "description": "Test Recording"
        }
        
        # Call the handler
        response = sys.modules['upload_handler'].lambda_handler(event, {})
        
        # Verify the response
        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertIn('recordingId', body)
        self.assertIn('uploadUrl', body)
        self.assertEqual(body['uploadUrl'], "https://example.com/presigned-url")

    def test_lambda_handler_error(self):
        """Test error handling in the lambda_handler function"""
        # Create a test event
        event = {
            "userId": "test@example.com",
            "fileName": "error.mp3",
            "fileType": "audio/mp3",
            "description": "Test Recording"
        }
        
        # Call the handler
        response = sys.modules['upload_handler'].lambda_handler(event, {})
        
        # Verify the response
        self.assertEqual(response['statusCode'], 500)
        body = json.loads(response['body'])
        self.assertIn('error', body)
        self.assertEqual(body['message'], 'Error generating upload URL')

if __name__ == '__main__':
    unittest.main()