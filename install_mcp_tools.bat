@echo off
echo ===================================
echo Installing MCP Tools for EchoGuard
echo ===================================

REM Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in your PATH.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

REM Check Python version
python --version
echo.

REM Install required packages
echo Installing AWS Documentation MCP Server...
pip install awslabs-aws-documentation-mcp-server
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install AWS Documentation MCP Server.
    pause
    exit /b 1
)

echo.
echo Installing CloudFormation Validator MCP Server...
pip install cloudformation-validator-mcp-server
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install CloudFormation Validator MCP Server.
    pause
    exit /b 1
)

echo.
echo ===================================
echo Installation complete!
echo.
echo Next steps:
echo 1. Open Kiro
echo 2. Open Command Palette (Ctrl+Shift+P)
echo 3. Type "Kiro: Restart MCP Servers"
echo 4. Check MCP server status in Kiro
echo ===================================
pause