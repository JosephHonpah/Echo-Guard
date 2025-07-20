import boto3
import json
import os
import uuid
import logging
from datetime import datetime

# Import Kiro integration
import kiro_integration

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    
    try:
        # Initialize AWS clients
        s3 = boto3.client('s3')
        bedrock = boto3.client('bedrock-runtime')
        dynamodb = boto3.resource('dynamodb')
        sns = boto3.client('sns')
        
        # Get the transcript file details
        key = event['Records'][0]['s3']['object']['key']
        bucket = event['Records'][0]['s3']['bucket']['name']
        logger.info(f"Processing transcript from s3://{bucket}/{key}")
        
        # Get the transcript content
        obj = s3.get_object(Bucket=bucket, Key=key)
        transcript_data = json.loads(obj['Body'].read())
        transcript = transcript_data['results']['transcripts'][0]['transcript']
        
        # Extract job name from the key to link back to original audio
        job_name = key.replace('.json', '')
        
        # Prepare the prompt for Bedrock
        prompt = f"""Human: Analyze this customer call transcript for compliance issues. 
        Provide your analysis in JSON format with the following fields:
        - complianceScore: a number from 0-100 indicating overall compliance
        - tone: a single word describing the overall tone (e.g., 'professional', 'aggressive', 'confused')
        - violations: an array of potential compliance violations found
        - summary: a brief summary of the call
        
        Here is the transcript:
        {transcript}
        
        Assistant: """
        
        logger.info("Sending transcript to Bedrock for analysis")
        
        # Call Bedrock for analysis
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }),
            contentType='application/json'
        )
        
        # Parse the response
        response_body = json.loads(response.get('body').read())
        response_content = response_body.get('content', [{}])[0].get('text', '{}')
        
        # Try to extract JSON from the response
        try:
            # Find JSON in the response (it might be wrapped in markdown code blocks)
            if '```json' in response_content:
                json_str = response_content.split('```json')[1].split('```')[0].strip()
            elif '```' in response_content:
                json_str = response_content.split('```')[1].split('```')[0].strip()
            else:
                json_str = response_content.strip()
                
            analysis = json.loads(json_str)
        except Exception as e:
            logger.error(f"Error parsing Bedrock response: {str(e)}")
            # Create a default analysis if parsing fails
            analysis = {
                "complianceScore": 50,
                "tone": "unknown",
                "violations": ["Error analyzing transcript"],
                "summary": "Failed to analyze transcript properly"
            }
            
        # Call Kiro for enhanced compliance analysis
        try:
            logger.info("Sending transcript to Kiro for enhanced compliance analysis")
            metadata = {
                "job_name": job_name,
                "source": "amazon_transcribe"
            }
            kiro_results = kiro_integration.analyze_compliance(transcript, metadata)
            
            if kiro_results:
                # Enhance the analysis with Kiro results
                analysis["kiroScore"] = kiro_results.get("compliance_score")
                analysis["kiroFindings"] = kiro_results.get("findings")
                analysis["kiroRecommendations"] = kiro_results.get("recommendations")
                logger.info(f"Kiro analysis complete: {json.dumps(kiro_results)}")
            else:
                logger.warning("Kiro analysis failed or returned no results")
                
        except Exception as e:
            logger.error(f"Error during Kiro analysis: {str(e)}")
            # Continue with just the Bedrock analysis
        
        logger.info(f"Analysis results: {json.dumps(analysis)}")
        
        # Generate a unique ID for this analysis
        call_id = str(uuid.uuid4())
        
        # Store the results in DynamoDB
        table = dynamodb.Table(os.environ['AUDIT_TABLE'])
        item = {
            'callId': call_id,
            'jobName': job_name,
            'timestamp': datetime.utcnow().isoformat(),
            'score': analysis.get('complianceScore', 0),
            'tone': analysis.get('tone', 'neutral'),
            'flags': analysis.get('violations', []),
            'summary': analysis.get('summary', ''),
            'transcriptBucket': bucket,
            'transcriptKey': key,
            # Add Kiro-specific fields if available
            'kiroScore': analysis.get('kiroScore'),
            'kiroFindings': analysis.get('kiroFindings'),
            'kiroRecommendations': analysis.get('kiroRecommendations')
        }
        
        table.put_item(Item=item)
        logger.info(f"Stored analysis in DynamoDB with ID: {call_id}")
        
        # Send alert if compliance score is low
        if analysis.get('complianceScore', 0) < 70:
            alert_message = {
                'callId': call_id,
                'score': analysis.get('complianceScore', 0),
                'violations': analysis.get('violations', []),
                'summary': analysis.get('summary', ''),
                'timestamp': item['timestamp']
            }
            
            sns.publish(
                TopicArn=os.environ['SNS_TOPIC'],
                Subject=f"Compliance Alert: Score {analysis.get('complianceScore', 0)}",
                Message=json.dumps(alert_message)
            )
            logger.info(f"Sent compliance alert to SNS topic")
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "callId": call_id,
                "status": "analyzed",
                "score": analysis.get('complianceScore', 0)
            })
        }
        
    except Exception as e:
        logger.error(f"Error analyzing transcript: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }