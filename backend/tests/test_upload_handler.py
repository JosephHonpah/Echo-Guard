import unittest
import json
import os
import sys
from unittest.mock import patch, MagicMock

# Add the lambda directory to the path so we can import the handler
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lambda'))
import upload_handler

class TestUploadHandler(unittest.TestCase):
    """Test cases for the upload_handler Lambda function"""

    @patch('upload_handler.s3')
    @patch('upload_handler.dynamodb')
    def test_lambda_handler_success(self, mock_dynamodb, mock_s3):
        """Test successful execution of the lambda_handler function"""
        # Mock the S3 pre-signed URL generation
        mock_s3.generate_presigned_url.return_value = "https://example.com/presigned-url"
        
        # Mock the DynamoDB table
        mock_table = MagicMock()
        mock_dynamodb.Table.return_value = mock_table
        
        # Create a test event
        event = {
            "userId": "test@example.com",
            "fileName": "test-recording.mp3",
            "fileType": "audio/mp3",
            "description": "Test Recording"
        }
        
        # Call the handler
        response = upload_handler.lambda_handler(event, {})
        
        # Verify the response
        self.assertEqual(response['statusCode'], 200)
        body = json.loads(response['body'])
        self.assertIn('recordingId', body)
        self.assertIn('uploadUrl', body)
        self.assertEqual(body['uploadUrl'], "https://example.com/presigned-url")
        
        # Verify S3 was called correctly
        mock_s3.generate_presigned_url.assert_called_once()
        
        # Verify DynamoDB was called correctly
        mock_table.put_item.assert_called_once()

    @patch('upload_handler.s3')
    def test_lambda_handler_error(self, mock_s3):
        """Test error handling in the lambda_handler function"""
        # Mock S3 to raise an exception
        mock_s3.generate_presigned_url.side_effect = Exception("Test error")
        
        # Create a test event
        event = {
            "userId": "test@example.com",
            "fileName": "test-recording.mp3",
            "fileType": "audio/mp3",
            "description": "Test Recording"
        }
        
        # Call the handler
        response = upload_handler.lambda_handler(event, {})
        
        # Verify the response
        self.assertEqual(response['statusCode'], 500)
        body = json.loads(response['body'])
        self.assertIn('error', body)
        self.assertEqual(body['message'], 'Error generating upload URL')

if __name__ == '__main__':
    unittest.main()