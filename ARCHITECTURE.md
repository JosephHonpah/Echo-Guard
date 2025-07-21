# EchoGuard Architecture

## Overview

EchoGuard uses a serverless architecture built on AWS services to provide a scalable, cost-effective solution for voice compliance monitoring.

## Architecture Diagram

```
+------------------+     +----------------+     +-------------------+
|                  |     |                |     |                   |
|  CloudFront      +---->+  S3 Frontend   |     |  Cognito          |
|  Distribution    |     |  Bucket        |     |  User Pool        |
|                  |     |                |     |                   |
+--------+---------+     +----------------+     +--------+----------+
         |                                               |
         |                                               |
         v                                               v
+--------+---------+                           +---------+----------+
|                  |                           |                    |
|  API Gateway     +<--------------------------+  Authentication    |
|                  |                           |                    |
+--------+---------+                           +--------------------+
         |
         |
         v
+--------+---------+     +----------------+     +-------------------+
|                  |     |                |     |                   |
|  Upload Handler  +---->+  S3 Audio      +---->+  SNS Transcribe   |
|  Lambda          |     |  Bucket        |     |  Topic            |
|                  |     |                |     |                   |
+------------------+     +----------------+     +--------+----------+
                                                         |
                                                         |
                                                         v
+------------------+     +----------------+     +---------+----------+
|                  |     |                |     |                    |
|  S3 Transcript   +<----+  Transcribe    +<----+  Transcribe       |
|  Bucket          |     |  Service       |     |  Handler Lambda   |
|                  |     |                |     |                    |
+--------+---------+     +----------------+     +--------------------+
         |
         |
         v
+--------+---------+                           +-------------------+
|                  |                           |                   |
|  SNS Analysis    +-------------------------->+  Analysis         |
|  Topic           |                           |  Handler Lambda   |
|                  |                           |                   |
+------------------+                           +--------+----------+
                                                        |
                                                        |
                    +-----------------------------------|
                    |                                   |
                    v                                   v
          +---------+---------+              +----------+---------+
          |                   |              |                    |
          |  Amazon Bedrock   |              |  Kiro AI           |
          |  Analysis         |              |  Analysis          |
          |                   |              |                    |
          +--------+----------+              +---------+----------+
                   |                                   |
                   |                                   |
                   v                                   v
          +--------+-----------------------------------+----------+
          |                                                       |
          |  DynamoDB Tables                                      |
          |  (Recordings & Results)                               |
          |                                                       |
          +-----------------------+-------------------------------+
                                  |
                                  |
                                  v
          +-----------------------+-------------------------------+
          |                                                       |
          |  SNS Notifications Topic                              |
          |  (High-risk alerts)                                   |
          |                                                       |
          +-------------------------------------------------------+
```

## Component Details

### Frontend Components
- **CloudFront Distribution**: Serves the web application with low latency
- **S3 Frontend Bucket**: Hosts static website assets
- **Cognito User Pool**: Manages user authentication and authorization

### API Layer
- **API Gateway**: Provides RESTful API endpoints for the frontend
- **Lambda Functions**: Handle API requests and business logic

### Storage Layer
- **S3 Audio Bucket**: Stores uploaded audio recordings
- **S3 Transcript Bucket**: Stores transcription results
- **DynamoDB Tables**: Store metadata, user data, and analysis results

### Processing Pipeline
- **Upload Handler Lambda**: Processes new audio uploads
- **Transcribe Handler Lambda**: Manages transcription jobs
- **Analysis Handler Lambda**: Coordinates AI analysis

### AI/ML Components
- **Amazon Transcribe**: Converts speech to text
- **Amazon Bedrock**: Performs general compliance analysis
- **Kiro AI**: Performs specialized financial compliance checks

### Notification System
- **SNS Topics**: Coordinate asynchronous processing and alerts
- **Email Notifications**: Alert users to high-risk compliance issues

## Data Flow

1. **User Authentication**:
   - User logs in via the web interface
   - Cognito authenticates the user and provides JWT tokens
   - Frontend stores tokens for API authorization

2. **Upload Process**:
   - User uploads an audio file through the web interface
   - Frontend gets a pre-signed URL from the API
   - File is uploaded directly to S3
   - S3 event triggers the Upload Handler Lambda

3. **Transcription Process**:
   - Upload Handler publishes to the Transcribe SNS Topic
   - Transcribe Handler Lambda starts an Amazon Transcribe job
   - When complete, transcription results are stored in S3
   - S3 event triggers the next step in the pipeline

4. **Analysis Process**:
   - Transcript triggers publication to Analysis SNS Topic
   - Analysis Handler Lambda coordinates dual AI analysis:
     - Amazon Bedrock analyzes for general compliance
     - Kiro AI analyzes for financial-specific compliance
   - Results are combined and stored in DynamoDB

5. **Notification Process**:
   - High-risk compliance issues trigger SNS notifications
   - Users can view all results in the dashboard

## Security Considerations

- **Authentication**: JWT-based authentication with Cognito
- **Authorization**: IAM roles with least privilege principle
- **Data Encryption**: S3 buckets use server-side encryption
- **API Security**: API Gateway with Cognito authorizers
- **Network Security**: VPC for sensitive components

## Scalability

The serverless architecture allows EchoGuard to scale automatically:

- Lambda functions scale with request volume
- S3 provides virtually unlimited storage
- DynamoDB auto-scaling handles varying database loads
- CloudFront handles global distribution and caching

## Cost Optimization

- Pay-per-use model for all serverless components
- S3 lifecycle policies for cost-effective storage
- Lambda concurrency limits to prevent unexpected costs
- CloudFront caching to reduce API calls
