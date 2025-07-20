"""
Kiro Integration Module for EchoGuard
Provides enhanced compliance analysis capabilities
"""
import json
import os
import boto3
import requests
from botocore.exceptions import ClientError

# Kiro API configuration
KIRO_API_ENDPOINT = os.environ.get('KIRO_API_ENDPOINT', 'https://api.kiro.ai/v1')
KIRO_API_KEY = os.environ.get('KIRO_API_KEY')

def analyze_compliance(transcript_text, metadata=None):
    """
    Analyze transcript for compliance issues using Kiro AI
    
    Args:
        transcript_text (str): The transcript text to analyze
        metadata (dict): Additional metadata about the audio recording
        
    Returns:
        dict: Compliance analysis results from Kiro
    """
    if not KIRO_API_KEY:
        raise ValueError("KIRO_API_KEY environment variable not set")
    
    # Prepare request payload
    payload = {
        "text": transcript_text,
        "analysis_type": "compliance",
        "industry": os.environ.get('INDUSTRY_TYPE', 'financial'),
        "metadata": metadata or {}
    }
    
    # Set headers with API key
    headers = {
        "Authorization": f"Bearer {KIRO_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        # Make API request to Kiro
        response = requests.post(
            f"{KIRO_API_ENDPOINT}/analyze",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        
        # Parse and return results
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error calling Kiro API: {str(e)}")
        # Fallback to Bedrock if Kiro fails
        return None

def store_kiro_results(analysis_id, kiro_results):
    """
    Store Kiro analysis results in DynamoDB
    
    Args:
        analysis_id (str): Unique ID for the analysis
        kiro_results (dict): Results from Kiro analysis
        
    Returns:
        bool: Success status
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.environ.get('AUDIT_TABLE_NAME'))
    
    try:
        # Add Kiro-specific fields
        item = {
            'analysisId': analysis_id,
            'kiroTimestamp': kiro_results.get('timestamp'),
            'kiroComplianceScore': kiro_results.get('compliance_score'),
            'kiroFindings': kiro_results.get('findings'),
            'kiroRecommendations': kiro_results.get('recommendations')
        }
        
        # Update the existing record with Kiro results
        response = table.update_item(
            Key={'analysisId': analysis_id},
            UpdateExpression="set kiroTimestamp=:kt, kiroComplianceScore=:ks, kiroFindings=:kf, kiroRecommendations=:kr",
            ExpressionAttributeValues={
                ':kt': item['kiroTimestamp'],
                ':ks': item['kiroComplianceScore'],
                ':kf': item['kiroFindings'],
                ':kr': item['kiroRecommendations']
            },
            ReturnValues="UPDATED_NEW"
        )
        
        return True
        
    except ClientError as e:
        print(f"Error storing Kiro results: {str(e)}")
        return False