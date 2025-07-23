# Kiro Integration for EchoGuard

This directory contains Kiro configuration files for enhancing the development of the EchoGuard voice-to-text compliance logger.

## Directory Structure

```
.kiro/
├── hooks/              # Automation hooks for common tasks
├── specs/              # Specifications for feature development
├── steering/           # Coding standards and best practices
└── settings/           # Configuration for external tools
```

## Using Kiro with EchoGuard

### Specs

Specs provide structured development for complex features:

- **Audio Processing Pipeline** - `specs/audio-processing-pipeline.md`
- **Frontend Implementation** - `specs/frontend-implementation.md`
- **Compliance Analysis Engine** - `specs/compliance-analysis-engine.md`
- **Deployment Workflow** - `specs/deployment-workflow.md`

To use a spec with Kiro:

```
#Spec: audio-processing-pipeline
Help me implement the Lambda function for transcript analysis.
```

### Hooks

Hooks automate common development tasks:

- **Run Tests** - Automatically runs tests when Python files are modified
- **Validate CloudFormation** - Validates CloudFormation templates on save
- **Analyze Transcript** - Analyzes selected text for compliance issues
- **Test Frontend** - Runs frontend tests when React files are modified
- **Update Documentation** - Helps update documentation when code changes

To manually trigger a hook:

1. Open the Command Palette
2. Search for "Kiro: Run Hook"
3. Select the hook you want to run

### Steering

Steering files provide consistent standards:

- **AWS Best Practices** - Guidelines for AWS services
- **Python Standards** - Coding standards for Python Lambda functions
- **React Standards** - Best practices for React frontend development

These are automatically applied when working with relevant files.

### MCP Integration

External tools are configured via MCP:

- **AWS Documentation** - Quick access to AWS documentation
- **CloudFormation Validator** - Validates CloudFormation templates

## Common Kiro Commands for EchoGuard

### Development

```
Help me implement the S3 event notification for audio file uploads.
```

```
Review this Lambda function for compliance with our Python standards.
```

```
How can I optimize this React component for better performance?
```

### Architecture

```
What's the best way to structure the DynamoDB table for compliance data?
```

```
Help me design a more efficient event-driven workflow for audio processing.
```

### Troubleshooting

```
I'm getting this error when deploying the CloudFormation template: [error]. How do I fix it?
```

```
The Lambda function is timing out. How can I optimize it?
```

## Adding New Kiro Features

### Adding a New Spec

1. Create a new markdown file in `.kiro/specs/`
2. Define requirements, design, and implementation tasks
3. Add references to relevant files with `#[[file:path/to/file]]`

### Adding a New Hook

1. Create a new JSON file in `.kiro/hooks/`
2. Define the trigger events, file patterns, and command
3. Provide a prompt for Kiro to use when processing the hook

### Adding a New Steering File

1. Create a new markdown file in `.kiro/steering/`
2. Add front matter with inclusion rules
3. Define standards and best practices for the specific domain