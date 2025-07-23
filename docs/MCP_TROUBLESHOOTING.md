# MCP Server Troubleshooting Guide

This guide provides detailed troubleshooting steps for common MCP server issues in the EchoGuard project.

## Common Error: "Failed to connect to MCP server"

### Error Message
```
Failed to connect to MCP server "cloudformation-validator": MCP error -32000: Connection closed
```

### Root Causes and Solutions

#### 1. Python Not Installed

**Symptoms:**
- Error message: `'python' is not recognized as an internal or external command`
- MCP servers fail to start

**Solution:**
1. Download and install Python from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Restart your computer
4. Verify installation with `python --version`

#### 2. MCP Server Packages Not Installed

**Symptoms:**
- Error message: `No module named 'awslabs.aws_documentation_mcp_server'`
- MCP servers fail to start

**Solution:**
1. Run the `install_mcp_tools.bat` script in the project root
2. Or manually install the packages:
   ```cmd
   pip install awslabs-aws-documentation-mcp-server
   pip install cloudformation-validator-mcp-server
   ```
3. Restart MCP servers in Kiro

#### 3. Incorrect MCP Configuration

**Symptoms:**
- Error message: `'uvx' is not recognized as an internal or external command`
- MCP servers fail to start

**Solution:**
1. Ensure your `.kiro/settings/mcp.json` uses Python modules:
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
2. Restart MCP servers in Kiro

#### 4. Firewall or Antivirus Blocking

**Symptoms:**
- MCP servers start but time out
- Error message: `MCP server connection + listTools timed out after 60 seconds`

**Solution:**
1. Check firewall settings
2. Add exceptions for Python and Kiro
3. Temporarily disable antivirus to test
4. If this works, add proper exceptions

#### 5. Port Conflicts

**Symptoms:**
- Error message: `Address already in use`
- MCP servers fail to start

**Solution:**
1. Check if other applications are using the same ports
2. Close those applications
3. Restart MCP servers in Kiro

## Diagnostic Steps

### 1. Check MCP Server Status

1. Open Command Palette (Ctrl+Shift+P)
2. Type "Kiro: Show MCP Server Status"
3. Check the status of each server

### 2. Test Module Imports

Run the `test_mcp_modules.py` script to check if modules can be imported:

```cmd
python test_mcp_modules.py
```

### 3. Check MCP Logs

1. Open Command Palette (Ctrl+Shift+P)
2. Type "Kiro: Show MCP Logs"
3. Look for specific error messages

### 4. Verify Python Environment

```cmd
python --version
pip list | findstr aws
pip list | findstr cloudformation
```

## Advanced Troubleshooting

### Manually Starting MCP Servers

You can try starting the MCP servers manually to see detailed error messages:

```cmd
python -m awslabs.aws_documentation_mcp_server
```

```cmd
python -m cloudformation_validator_mcp_server
```

### Reinstalling Packages

If you're still having issues, try reinstalling the packages:

```cmd
pip uninstall -y awslabs-aws-documentation-mcp-server
pip uninstall -y cloudformation-validator-mcp-server
pip install awslabs-aws-documentation-mcp-server
pip install cloudformation-validator-mcp-server
```

### Using a Virtual Environment

Creating a clean virtual environment can help isolate issues:

```cmd
python -m venv mcp-env
mcp-env\Scripts\activate
pip install awslabs-aws-documentation-mcp-server
pip install cloudformation-validator-mcp-server
```

Then update your MCP configuration to use the Python from this virtual environment:

```json
{
  "mcpServers": {
    "aws-docs": {
      "command": "mcp-env\\Scripts\\python",
      "args": ["-m", "awslabs.aws_documentation_mcp_server"],
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "disabled": false,
      "autoApprove": ["aws-docs.search"]
    }
  }
}
```

## Still Having Issues?

If you're still experiencing problems after trying these solutions:

1. Temporarily disable MCP servers in the configuration
2. Check for system-specific issues (permissions, environment variables)
3. Try using the alternative `uvx` approach if Python modules aren't working
4. Contact the Kiro support team for further assistance