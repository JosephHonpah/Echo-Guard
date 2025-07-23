---
inclusion: fileMatch
fileMatchPattern: '*.py'
---

# Python Standards for EchoGuard

When writing Python code for EchoGuard Lambda functions:

## Code Style
- Follow PEP 8 guidelines
- Use type hints for function parameters and return values
- Use docstrings for all functions and classes
- Maximum line length of 100 characters

## Error Handling
- Use try/except blocks for AWS service calls
- Log errors with appropriate context
- Return meaningful error messages
- Implement proper status codes in responses

## AWS SDK Usage
- Use boto3 for AWS service interactions
- Reuse clients when possible
- Use pagination for listing operations
- Implement retries with exponential backoff

## Testing
- Write unit tests for all functions
- Mock AWS services in tests
- Test error handling paths
- Use pytest for test framework

## Lambda Best Practices
- Keep dependencies minimal
- Reuse connections outside handler
- Use environment variables for configuration
- Implement proper logging with context
- Handle timeouts gracefully
- Use appropriate memory settings
- Implement idempotent operations