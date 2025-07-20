# EchoGuard Architecture Diagram

```mermaid
flowchart TD
    %% Layers
    subgraph UI["User Interface"]
        Frontend["React.js Frontend<br>(AWS Amplify)"]
    end
    
    subgraph Auth["Authentication"]
        Cognito["Amazon Cognito"]
        IAM["IAM Roles"]
    end
    
    subgraph API["API Layer"]
        APIGateway["Amazon API Gateway"]
    end
    
    subgraph Compute["Compute Layer"]
        APILambda["API Lambda<br>(Node.js)"]
        StartLambda["StartTranscribe<br>Lambda (Python)"]
        AnalyzeLambda["AnalyzeTranscript<br>Lambda (Python)"]
    end
    
    subgraph Storage["Storage Layer"]
        AudioS3["S3 Audio Bucket"]
        TranscriptS3["S3 Transcript Bucket"]
        DynamoDB["DynamoDB<br>Audit Log Table"]
    end
    
    subgraph AIML["AI/ML Services"]
        Transcribe["Amazon Transcribe"]
        Bedrock["Amazon Bedrock"]
    end
    
    %% Connections
    Frontend --> Cognito
    Cognito --> IAM
    Frontend --> APIGateway
    APIGateway --> APILambda
    APILambda --> DynamoDB
    Frontend --> AudioS3
    AudioS3 --> StartLambda
    StartLambda --> Transcribe
    Transcribe --> TranscriptS3
    TranscriptS3 --> AnalyzeLambda
    AnalyzeLambda --> Bedrock
    AnalyzeLambda --> DynamoDB
    
    %% Styling
    classDef aws fill:#FF9900,stroke:#232F3E,color:#232F3E
    class Cognito,IAM,APIGateway,APILambda,StartLambda,AnalyzeLambda,AudioS3,TranscriptS3,DynamoDB,Transcribe,Bedrock aws
```

To view this diagram:
1. Copy the Mermaid code above
2. Paste it into a Mermaid live editor (https://mermaid.live/)
3. Export as PNG
4. Save the PNG to the docs/images folder as "architecture.png"