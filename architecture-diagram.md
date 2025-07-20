# EchoGuard Voice-to-Text Compliance Logger - Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                    USER INTERFACE                                       │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                            React.js Frontend                                    │   │
│  │                         (AWS Amplify Hosted)                                   │   │
│  │                                                                                 │   │
│  │  • Audio Upload Interface    • Compliance Dashboard                            │   │
│  │  • Authentication UI         • Audit Log Viewer                               │   │
│  │  • Real-time Notifications   • Analytics & Reports                            │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                         │                                               │
└─────────────────────────────────────────┼───────────────────────────────────────────────┘
                                          │
                                          │ HTTPS/REST API
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                  AUTHENTICATION                                         │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────────────┐ │
│  │   Amazon Cognito    │    │   Identity Pool     │    │      IAM Roles             │ │
│  │    User Pool        │◄──►│                     │◄──►│                             │ │
│  │                     │    │  • Authenticated    │    │  • API Access              │ │
│  │  • User Management  │    │  • Unauthenticated  │    │  • S3 Upload Permissions   │ │
│  │  • Email Verification│   │                     │    │                             │ │
│  └─────────────────────┘    └─────────────────────┘    └─────────────────────────────┘ │
│                                         │                                               │
└─────────────────────────────────────────┼───────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                    API LAYER                                           │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                          Amazon API Gateway                                     │   │
│  │                              (REST API)                                        │   │
│  │                                                                                 │   │
│  │  Endpoints:                                                                     │   │
│  │  • GET  /audit-logs          • POST /upload-url                               │   │
│  │  • GET  /compliance-stats     • GET  /audio-files                             │   │
│  │  • POST /manual-analysis      • DELETE /audio-files/{id}                      │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                         │                                               │
└─────────────────────────────────────────┼───────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                 COMPUTE LAYER                                          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐   │
│  │                            AWS Lambda Functions                                 │   │
│  │                                                                                 │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────────────┐ │   │
│  │  │   API Function  │  │ StartTranscribe │  │    AnalyzeTranscript           │ │   │
│  │  │   (Node.js)     │  │   (Python)      │  │      (Python)                  │ │   │
│  │  │                 │  │                 │  │                                 │ │   │
│  │  │ • Handle API    │  │ • Trigger on    │  │ • Trigger on transcript        │ │   │
│  │  │   requests      │  │   audio upload  │  │   completion                   │ │   │
│  │  │ • CRUD operations│ │ • Start Amazon  │  │ • Analyze with Bedrock         │ │   │
│  │  │ • Generate      │  │   Transcribe    │  │ • Store compliance results     │ │   │
│  │  │   presigned URLs│  │   job           │  │ • Send SNS notifications       │ │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────────────────────┘   │
│                                         │                                               │
└─────────────────────────────────────────┼───────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                                 STORAGE LAYER                                          │
├─────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                         │
│  ┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────────────┐ │
│  │    Amazon S3        │    │     Amazon S3       │    │      Amazon DynamoDB       │ │
│  │   Audio Bucket      │    │  Transcript Bucket  │    │     Audit Log Table        │ │
│  │                     │    │                     │    │                             │ │
│  │ • Raw audio files   │    │ • Transcription     │    │ • Compliance analysis      │ │
│  │ • Secure upload     │    │   results           │    │   results                   │ │
│  │ • Event triggers    │    │ • JSON format       │    │ • Audit trails             │ │
│  │ • Lifecycle policies│    │ • Event triggers    │    │ • Query capabilities       │ │
│  └─────────────────────┘    └─────────────────────┘    └─────────────────────────────┘ │
│           │                            │                            ▲                  │
└───────────┼────────────────────────────┼────────────────────────────┼──────────────────┘
            │                            │                            │
            ▼                            ▼                            │
┌─────────────────────────────────────────────────────────────────────┼─────────────────┐
│                                AI/ML SERVICES                       │                 │
├─────────────────────────────────────────────────────────────────────┼─────────────────┤
│                                                                     │                 │
│  ┌─────────────────────┐    ┌─────────────────────────────────────┐ │                 │
│  │  Amazon Transcribe  │    │         Amazon Bedrock              │ │                 │
│  │                     │    │                                     │ │                 │
│  │ • Speech-to-text    │    │ • AI compliance analysis           │ │                 │
│  │ • Multiple formats  │    │ • Natural language processing      │ │                 │
│  │ • Custom vocabulary │    │ • Sentiment analysis               │ │                 │
│  │ • Speaker detection │    │ • Risk assessment                  │ │                 │
│  └─────────────────────┘    └─────────────────────────────────────┘ │                 │
│           │                                      │                   │                 │
└───────────┼──────────────────────────────────────┼───────────────────┼─────────────────┘
            │                                      │                   │
            └──────────────────────────────────────┘                   │
                                                                       │
┌─────────────────────────────────────────────────────────────────────┼─────────────────┐
│                              NOTIFICATION LAYER                     │                 │
├─────────────────────────────────────────────────────────────────────┼─────────────────┤
│                                                                     │                 │
│  ┌─────────────────────────────────────────────────────────────────┐│                 │
│  │                        Amazon SNS                               ││                 │
│  │                  Compliance Alert Topic                        ││                 │
│  │                                                                 ││                 │
│  │ • Real-time compliance violation alerts                        ││                 │
│  │ • Email notifications                                           ││                 │
│  │ • SMS notifications                                             ││                 │
│  │ • Integration with external systems                            ││                 │
│  └─────────────────────────────────────────────────────────────────┘│                 │
│                                                                     │                 │
└─────────────────────────────────────────────────────────────────────┼─────────────────┘
                                                                      │
                                                                      │
┌─────────────────────────────────────────────────────────────────────┼─────────────────┐
│                              MONITORING & LOGGING                   │                 │
├─────────────────────────────────────────────────────────────────────┼─────────────────┤
│                                                                     │                 │
│  ┌─────────────────────┐    ┌─────────────────────┐    ┌───────────┼───────────────┐ │
│  │   CloudWatch Logs   │    │  CloudWatch Metrics │    │   CloudWatch Alarms      │ │
│  │                     │    │                     │    │                           │ │
│  │ • Lambda function   │    │ • API Gateway       │    │ • Error rate monitoring  │ │
│  │   logs              │    │   metrics           │    │ • Performance alerts     │ │
│  │ • API access logs   │    │ • Lambda metrics    │    │ • Cost monitoring        │ │
│  │ • Error tracking    │    │ • S3 metrics        │    │                           │ │
│  └─────────────────────┘    └─────────────────────┘    └───────────────────────────┘ │
│                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────┘

                                    DATA FLOW
                                    ─────────

1. User uploads audio file through React frontend
2. Frontend authenticates with Cognito and gets temporary AWS credentials
3. Audio file uploaded directly to S3 Audio Bucket
4. S3 upload event triggers StartTranscribe Lambda function
5. StartTranscribe initiates Amazon Transcribe job
6. Transcribe saves results to S3 Transcript Bucket
7. Transcript upload triggers AnalyzeTranscript Lambda function
8. AnalyzeTranscript uses Amazon Bedrock for compliance analysis
9. Analysis results stored in DynamoDB Audit Log Table
10. SNS notifications sent for compliance violations
11. Frontend queries API Gateway for audit logs and statistics
12. API Lambda function retrieves data from DynamoDB
13. Real-time updates displayed in compliance dashboard

                                 SECURITY FEATURES
                                 ─────────────────

• End-to-end encryption for audio files and transcripts
• IAM roles with least privilege access
• Cognito-based authentication and authorization
• API Gateway with CORS and throttling
• VPC endpoints for private communication (optional)
• CloudTrail for audit logging
• S3 bucket policies and access controls
```