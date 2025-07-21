# EchoGuard Architecture

## Overview

EchoGuard uses a serverless architecture built on AWS services to provide a scalable, cost-effective solution for voice compliance monitoring.
https://viewer.diagrams.net/?tags=%7B%7D&lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=Echoguard.drawio&dark=auto#R%3Cmxfile%3E%3Cdiagram%20name%3D%22Page-1%22%20id%3D%22-zu22PK1w80f7_6dTbhX%22%3E7V1bc6O4Ev41qZp5iIs7%2BNGX9czUbPbkTGbr7D6lZJBtbTDygpzE8%2BuPZC4GSY6Jw8UJ7GbX0IAQ%2Br5utVqNuNIn6%2BcvIdisbrAH%2FStN8Z6v9OmVpqm2YtEfJtnFEt1RYsEyRF5y0kFwh37BRJietkUejAonEox9gjZFoYuDALqkIANhiJ%2BKpy2wX7zrBiyhILhzgS9K%2F4c8soqljqkc5F8hWq7SO6tKcmQN0pMTQbQCHn7KifTfrvRJiDGJt9bPE%2BizxkvbJb5uduRoVrEQBqTMBTeP0%2B9D6P1HfTIe%2F0u%2B6Yuv14trXY%2BLeQT%2BNnnipLZklzZBiLeBB1kpypU%2BflohAu82wGVHnyjoVLYia5%2FuqXQzKQ6GBD4fraiaPT7lDcRrSMIdPSW5wE4pklLGMOL9pwMAanrOKtf4dsI1kGC%2BzIo%2BNAvdSFrmFa2knm6kXBOwh0eUQb%2BDOfRvcYQIwgE9NseE4DU9AfhoyQQubRAYUoHPzhwD92G5b%2BsJ9nG4L1Zf7P%2FJFTpKriWYNXxEQvyQEVPLJLkSFMVRZgy4jH9sxwPRKoOUHtmwx1g%2FL5kSDxCO7AGiGhUNttG%2Bgm9BNUEx0%2BgciroExFRWOYglmB49QOKuklbBW%2BKjgDZlaliYcIEDkmtc%2Bu%2BMVWFMG85D8HAswAGUoZHhuUC%2BLyuoAMwxJq2R57E6C6w4TrEcP2UazJ4rMb5q%2Bpx3ScOwayJ6OgqWdE%2BXEAY8RcZgE2Jv65JvLqvieBPGG8VzIr0aE5FZ2YRchsgtS8Itpy5uGa%2Fk1gajgOwrYY7pH63WJP7PpKdOmGSgmRKhTGaLQlU8jf6osjvwQpnMFoWqeBrbS2tdFMpktinWmL9alVytclfTv1eqKqd5zsSYzWYv6mopncxUT26pX1LIvPJpnPKxW4JoEz%2FWAj2zesj1L4QR3oYuTBSQ7so00PXx1luEmOlZHZqoKXvEOGU0hqIyprLKldHqlfG9KuN0Sp29SXeUES8DRHA1mqjZZ%2FWJVl19ot2r4XtVw99s1bTHnVFDsEH3S0DgE9hVpIrcCFYdWpJO0ZRoo1mXNjqntVHKmLpxlsCmD3ywnnvgfrEN3PgOPEFnpmPqxvFxVwUYGhqPYTl7ag5TqCvHcNiPYD%2FMCNZQzYsawabRmb677rvrC%2B%2BuoyCqRgdNSzlHB2vzmNUScea%2Bk34JQU1Ry3XSWl0Qar0Zfa9mVFFHjjPtjBklIQgiN0TzinTRGp7WxUaHPGo%2F4%2FNx%2FGWeXa37y%2F2Uz7s19L2%2FfJ4OOvpZOlifv2z2%2FvLbEGzfX%2B4n696tGe2YvzyHXojdh4oUUdEKiqins%2BH5SXNHVMRUVr0i9tN171YRJ0PNjPudTiiitwvAGnvzigYW3DyPLNvUlGiiWZsmlpiq6zXxMjWxH1mcORum80qotzy0KDHXCgNvxN4wYED4IIqQW0SimDcPnxH5K7f9N9umfIz3ps%2B5Q9NdbucWhog%2BE4N5L4urAT3htQWurWlV9wiW6PMJCJeQnDRJInolI3sh9AFBj8UKyyBL7nDLDFouyK9y5LA51OMHTa46AC8WxM0W6BpXUNwQQkF7BmWPfT6p0kevnlTqQLHsArGMbL88tSiBwt1f%2BZ0cSdnuoaj93i6%2FVydPS9LUaJWl3Mj6XJIKCbVNk7RE1PyVJG2HVifpYrdJF5WfuUyb%2BbV80Tj%2FVVMa5kuJINyZRu2NPeWlmrOyvW6rna5ucLTiZ1LK8lPnpwX5F7zq5meJCOOZnlzGyb%2FzlGzDk2uVKgZHFfXcrs%2Fg%2BlC1aVNWIgb2OqqUhbg16LhE5bM96zQacqScuoErETKpQsfVNnU8HQWdHq21SinTLlJBPbfjsDSuoKY7jtpCAB%2FVsVHLet5xllxbDOWJJXgkpRl6iuo1MzStdx1DtYGp60V22brT8oAtTuhqizZ22rrHBlplaWNzL%2BqpRsO0qT4MVaVBkltJ3W43VKqX5WirQSibiyqo6pkcdbiYKx9or5uiWl197yU5dEZZTpltcsoxuF7u3EGCM%2BQKajiyqZdI2fxYwzuHDzKeDR0%2Fc9J0l1V5kPHSoeOdBJ1f3Kq0k8qvpsUXVDd0rwuqJLmO72oatd1ALT91znfV5SeeOJ7ozfKk8hjOpat4VdPaXDnCCzV1A3dunCSiFSMXHHdvTaO5GeBs5YFXT73wBSk6vzZBzdwwzh1qXjo3SnQLrQ4EVS1bhuKtLFI1rqCGZ2UM2VjQ8tn6ZR56pJvLeCkzC6xZblwwj9jP3R939Jo%2FMEEL5AKWVhfR%2FZ94Q3nEnZqWRmtXLFByj70o2oCgwGHr3y1bxXU8z5bwvHbj1L8RG9%2BxFy1TBtFClNwxnyF%2F7YHw4VO4nH9i6YxX%2B8DS%2Fudz%2FMuOaKYZ7%2BQ3Pn%2BOa5XcPq3np6%2B01OsQRQ8MJR%2BGJPqce8i4%2BsVH4p%2Bd01ECn0lR%2FYQURD5TMXtjMYQR%2BgXmWQJiMV2VZVyCLcFRkrJ4xedOJg5hPtGyuvdhdIdfhSMhW36pWZma8uOf6laSlKXfnGT7dJ8SPWXk%2BsmaOvp4nP4BXRx6KFgyPc6eP%2F4%2FlfyA0dbveX6E56ZtXBrPxWDMaA1%2B4eCYdb50go6T14OO8a8jTBMW75Ysm5VFpRtZ99kQY0ejAPi7CEU8176CgLZwSE%2F%2Bff%2ByZndQ45O0DNmCdaosBb8%2B3MTErdipO6CX%2BnOdQYnzxB0RokaXVDfE2N6dzmBJlhbZsGHEeOs%2BQNIZkCyTHy61DZIYWHu5p805SD8Pa8R024Gy7CKqcgMp%2ByhFfR6UGHcrwCXv2U5CnvZ8nYbb1Hi4h7L%2BUKbHteGduudCf3gcdZlGJxGQTqOrF9GVICvzUOtDVoyS7rvR0dZDWIJh2qN2GkRDOQWi3SiGYpTyz42PgUdlB%2BPbG1tZEG5Ypm9tWCXFMNxoS1b0iZJocmfQ4acXs04vj43SpENrSgb0t9%2Bo4EuyhntnoOHTe6SKM2wUG3HQPkk%2BcqEpf0ZSI3iLsd9xE6iZpzozGYr1Wb8j4%2FoZ%2B24QDLwUrXnIuyQdwcu5LLiOj%2FCVyeF7T10Bx%2BSnvo84FI1GYUxxtB6bw46Acs1nKUncCNkEVG2AWOJwWgCjX2apIKt0maW%2BOftVq1r8BOIToJp9r1Vj3NT0fZUXJj0bXfrcKpF31xu3y9TGjn0DEXksqEJ29yDw7oHrwii6X4MALOE6zd14%2B%2FCKz5Efai3rpxgtnGRWqTM%2Bocr5hIZkQfFGoxeWGPX7NrrpDB4aNy8iw8NoFI8yH1lITA9aA5a0Pd7%2FjlIDJbVWZ1rM5A7TFSGbaJ9JNqN%2FcI3%2FQYPIB%2B7DNcsbH7i0CG32U1E1W%2FlhfBlRTs0eUIhZaAtCYJlDZ6FYrgLm1mDDPrBRSUCCS%2BBpfT1pSwzSft83Qkd0SQBE4hI2q0v9Svu9S%2Fg%2BXMIHuMu5gPcRDB%2BRW1dwsP2xmhhs%2F35z1xlDyX%2BDUeJzVBQXpLshZjnb2bEvjHM32IPsjP8D%3C%2Fdiagram%3E%3C%2Fmxfile%3E

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
