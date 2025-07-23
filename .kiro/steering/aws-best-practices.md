---
inclusion: always
---

# AWS Best Practices for EchoGuard

When working with AWS services in EchoGuard, follow these guidelines:

## Security
- Use IAM roles with least privilege
- Enable encryption at rest for all storage
- Use HTTPS/TLS for all communications
- Implement proper secrets management (no hardcoded credentials)
- Use Origin Access Control for CloudFront to S3 access
- Implement WAF for API Gateway protection
- Enable CloudTrail for auditing all API calls

## Cost Optimization
- Use pay-per-use serverless services where possible
- Implement lifecycle policies for S3
- Use DynamoDB on-demand capacity for variable workloads
- Set up CloudWatch alarms for cost anomalies
- Configure appropriate Lambda memory settings
- Use CloudFront caching to reduce origin requests
- Implement S3 Intelligent-Tiering for audio storage

## Performance
- Use CloudFront for content delivery
- Implement caching strategies
- Optimize Lambda memory settings
- Use parallel processing for independent tasks
- Configure appropriate provisioned concurrency for critical Lambdas
- Use DynamoDB DAX for high-read scenarios
- Implement pagination for large dataset queries

## Compliance
- Ensure 7-year retention of compliance data
- Implement proper audit logging
- Use versioning for compliance-related resources
- Follow regulatory requirements for data handling
- Implement appropriate tagging for compliance tracking
- Set up automated compliance reporting
- Configure data lifecycle management for regulatory requirements

## Resilience
- Design for multi-AZ resilience
- Implement retry logic with exponential backoff
- Use DynamoDB global tables for multi-region resilience
- Configure appropriate timeouts and error handling
- Implement dead-letter queues for failed processing
- Set up CloudWatch alarms for critical service metrics
- Create automated recovery procedures