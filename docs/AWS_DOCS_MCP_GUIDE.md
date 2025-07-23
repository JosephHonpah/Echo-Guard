# Using AWS Documentation MCP Server with Kiro

This guide explains how to use the AWS Documentation MCP server with Kiro for the EchoGuard project.

## What is the AWS Documentation MCP Server?

The AWS Documentation MCP server is a tool that allows Kiro to search and retrieve information from AWS documentation. This helps you get accurate and up-to-date information about AWS services directly within Kiro.

## Setup Status

✅ **AWS Documentation MCP Server**: Successfully installed and configured
❌ **CloudFormation Validator MCP Server**: Not available (package not found)

## Using AWS Documentation with Kiro

Now that the AWS Documentation MCP server is set up, you can use it to get information about AWS services directly in Kiro. Here are some examples:

### Example 1: Get Information About an AWS Service

```
Tell me about Amazon S3 bucket lifecycle policies.
```

### Example 2: Ask About AWS Best Practices

```
What are the best practices for securing Amazon DynamoDB tables?
```

### Example 3: Get Help with AWS CLI Commands

```
How do I use the AWS CLI to create an S3 event notification for Lambda?
```

### Example 4: Learn About AWS Service Limits

```
What are the limits for Lambda functions?
```

### Example 5: Get Information About AWS Pricing

```
How is Amazon Transcribe priced?
```

## Benefits of Using AWS Documentation MCP Server

1. **Accurate Information**: Get information directly from AWS documentation
2. **Up-to-Date**: Access the latest AWS service features and best practices
3. **Context-Aware**: Kiro can provide AWS information relevant to your EchoGuard project
4. **Time-Saving**: No need to switch to a web browser to search AWS documentation

## Troubleshooting

If you encounter issues with the AWS Documentation MCP server:

1. **Check MCP Server Status**:
   - Open Command Palette (Ctrl+Shift+P)
   - Type "Kiro: Show MCP Server Status"
   - Check if the aws-docs server is connected

2. **Restart MCP Servers**:
   - Open Command Palette (Ctrl+Shift+P)
   - Type "Kiro: Restart MCP Servers"
   - Select this command to restart the servers

3. **Verify Module Installation**:
   ```cmd
   python test_mcp_modules.py
   ```
   This should show that the AWS Documentation MCP Server module is successfully imported.

4. **Check MCP Logs**:
   - Open Command Palette (Ctrl+Shift+P)
   - Type "Kiro: Show MCP Logs"
   - Look for any error messages related to the aws-docs server

## Next Steps

Now that you have the AWS Documentation MCP server set up, you can:

1. **Use it for EchoGuard development**: Get AWS information directly in Kiro
2. **Explore other MCP tools**: Consider adding more MCP tools as they become available
3. **Update the MCP configuration**: Modify `.kiro/settings/mcp.json` if needed

For more information about MCP tools, refer to the `docs/MCP_SETUP_GUIDE.md` file.