"""
Test script to check if MCP server modules can be imported.
"""

def test_aws_docs():
    print("Testing AWS Documentation MCP Server...")
    try:
        import awslabs.aws_documentation_mcp_server
        print("✅ AWS Documentation MCP Server module imported successfully")
    except ImportError as e:
        print(f"❌ Error importing AWS Documentation MCP Server: {e}")
        print("Try installing with: pip install awslabs-aws-documentation-mcp-server")

def test_cloudformation_validator():
    print("\nTesting CloudFormation Validator MCP Server...")
    try:
        import cloudformation_validator_mcp_server
        print("✅ CloudFormation Validator MCP Server module imported successfully")
    except ImportError as e:
        print(f"❌ Error importing CloudFormation Validator MCP Server: {e}")
        print("Try installing with: pip install cloudformation-validator-mcp-server")

if __name__ == "__main__":
    print("MCP Server Module Test\n" + "=" * 20)
    test_aws_docs()
    test_cloudformation_validator()
    print("\nTest complete. If any modules failed to import, install them using pip.")