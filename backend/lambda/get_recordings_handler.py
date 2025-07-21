import json
import boto3
import os
from boto3.dynamodb.conditions import Key

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')

# Environment variables
RECORDINGS_TABLE = os.environ.get('RECORDINGS_TABLE', 'echoguard-recordings')
RESULTS_TABLE = os.environ.get('RESULTS_TABLE', 'echoguard-results')

def lambda_handler(event, context):
    """
    Retrieves recordings for a user.
    
    Expected API Gateway event format:
    {
        "pathParameters": {
            "userId": "user123"
        },
        "queryStringParameters": {
            "limit": "10",
            "nextToken": "abc123"
        }
    }
    """
    try:
        # Extract user ID from path parameters
        user_id = event['pathParameters']['userId']
        
        # Extract pagination parameters
        query_params = event.get('queryStringParameters', {}) or {}
        limit = int(query_params.get('limit', '10'))
        next_token = query_params.get('nextToken')
        
        # Query DynamoDB for recordings
        recordings_table = dynamodb.Table(RECORDINGS_TABLE)
        
        query_params = {
            'IndexName': 'UserIdIndex',
            'KeyConditionExpression': Key('userId').eq(user_id),
            'Limit': limit,
            'ScanIndexForward': False  # Sort by most recent first
        }
        
        if next_token:
            query_params['ExclusiveStartKey'] = json.loads(next_token)
        
        response = recordings_table.query(**query_params)
        
        # Format response
        recordings = response.get('Items', [])
        
        # Generate next token for pagination
        pagination = {}
        if 'LastEvaluatedKey' in response:
            pagination['nextToken'] = json.dumps(response['LastEvaluatedKey'])
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'GET,OPTIONS'
            },
            'body': json.dumps({
                'recordings': recordings,
                'pagination': pagination
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'GET,OPTIONS'
            },
            'body': json.dumps({
                'message': 'Error retrieving recordings',
                'error': str(e)
            })
        }

def get_recording_details(event, context):
    """
    Retrieves detailed information about a specific recording.
    
    Expected API Gateway event format:
    {
        "pathParameters": {
            "recordingId": "abc-123"
        }
    }
    """
    try:
        # Extract recording ID from path parameters
        recording_id = event['pathParameters']['recordingId']
        
        # Get recording metadata
        recordings_table = dynamodb.Table(RECORDINGS_TABLE)
        recording = recordings_table.get_item(Key={'recordingId': recording_id})
        
        if 'Item' not in recording:
            return {
                'statusCode': 404,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                    'Access-Control-Allow-Methods': 'GET,OPTIONS'
                },
                'body': json.dumps({
                    'message': 'Recording not found'
                })
            }
        
        # Get analysis results if available
        results_table = dynamodb.Table(RESULTS_TABLE)
        results = results_table.get_item(Key={'recordingId': recording_id})
        
        response_data = {
            'recording': recording['Item']
        }
        
        if 'Item' in results:
            response_data['analysis'] = {
                'complianceScore': results['Item'].get('complianceScore'),
                'issues': results['Item'].get('issues', []),
                'bedrockSummary': results['Item'].get('bedrockSummary', ''),
                'kiroSummary': results['Item'].get('kiroSummary', '')
            }
            
            # Include transcript if available
            if 'transcript' in results['Item']:
                response_data['transcript'] = results['Item']['transcript']
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'GET,OPTIONS'
            },
            'body': json.dumps(response_data)
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'GET,OPTIONS'
            },
            'body': json.dumps({
                'message': 'Error retrieving recording details',
                'error': str(e)
            })
        }