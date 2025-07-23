# Setting Up MCP Tools for EchoGuard

This guide explains how to set up Model Context Protocol (MCP) tools for the EchoGuard project.

## What is MCP?

MCP (Model Context Protocol) allows Kiro to integrate with external tools, such as AWS documentation search and CloudFormation validators. These tools enhance Kiro's capabilities by providing specialized functionality.

## Installation Options

### Option 1: Using pip (Recommended for Windows)

1. Install the required packages:

```cmd
pip install awslabs-aws-documentation-mcp-server
pip install cloudformation-validator-mcp-server
```

2. Update the MCP configuration to use Python modules:

```json
{
  "mcpServers": {
    "aws-docs": {
      "command": "python",
      "args": ["-m", "awslabs.aws_documentation_mcp_server"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": ["aws-docs.search"]
    },
    "cloudformation-validator": {
      "command": "python",
      "args": ["-m", "cloudformation_validator_mcp_server"],
      "disabled": false,
      "autoApprove": ["validate-template"]
    }
  }
}
```

3. Save this configuration to `.kiro/settings/mcp.json`

### Option 2: Using uv/uvx (Alternative)

If you prefer using `uv` and `uvx`:

1. Install uv:

```cmd
pip install uv
```

2. Install uvx:

```cmd
uv pip install uvx
```

3. Install the MCP servers:

```cmd
uvx install awslabs.aws-documentation-mcp-server@latest
uvx install cloudformation-validator-mcp-server@latest
```

4. Use the original MCP configuration:

```json
{
  "mcpServers": {
    "aws-docs": {
      "command": "uvx",
      "args": ["awslabs.aws-documentation-mcp-server@latest"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": ["aws-docs.search"]
    },
    "cloudformation-validator": {
      "command": "uvx",
      "args": ["cloudformation-validator-mcp-server@latest"],
      "disabled": false,
      "autoApprove": ["validate-template"]
    }
  }
}
```

## Troubleshooting

### Common Issues

1. **"Failed to connect to MCP server"**:
   - Check if the required packages are installed
   - Verify the command path is correct
   - Check if any firewalls are blocking the connection

2. **"Command not found"**:
   - Ensure the specified command (python or uvx) is in your PATH
   - Try using absolute paths to the command

3. **"Module not found"**:
   - Verify the package is installed correctly
   - Check for typos in the module name

### Checking MCP Server Status

You can check the status of MCP servers in Kiro:

1. Open the Command Palette (Ctrl+Shift+P)
2. Type "Kiro: Show MCP Server Status"
3. Check if servers are connected

### Restarting MCP Servers

If a server is not connecting:

1. Open the Command Palette (Ctrl+Shift+P)
2. Type "Kiro: Restart MCP Servers"
3. Try using the tool again

## Using MCP Tools

### AWS Documentation Search

Once connected, you can search AWS documentation directly:

```
What's the best way to configure S3 event notifications for Lambda?
```

Kiro will use the AWS documentation server to provide accurate information.

### CloudFormation Validator

To validate a CloudFormation template:

```
#File: infrastructure/echoguard-complete.yaml
Validate this CloudFormation template.
```

The validator will check for errors and best practices.

## Updating MCP Configuration

If you need to update the MCP configuration:

1. Edit `.kiro/settings/mcp.json`
2. Save the file
3. Restart MCP servers from the Command Palette

## Additional MCP Tools

You can add more MCP tools to enhance Kiro's capabilities:

1. Install the tool package
2. Add the configuration to `.kiro/settings/mcp.json`
3. Restart MCP servers

For example, to add a SQL validator:

```json
"sql-validator": {
  "command": "python",
  "args": ["-m", "sql_validator_mcp_server"],
  "disabled": false,
  "autoApprove": ["validate-sql"]
}
```