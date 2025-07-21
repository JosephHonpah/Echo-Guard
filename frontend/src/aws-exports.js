// AWS Amplify configuration

const awsmobile = {
    "aws_project_region": "us-east-1",
    "aws_cognito_identity_pool_id": "us-east-1:3bedc326-033f-488f-a661-d3ee011a5a94",
    "aws_cognito_region": "us-east-1",
    "aws_user_pools_id": "us-east-1_CAVA949mz",
    "aws_user_pools_web_client_id": "31pugqqnb64lq0vkfnim20f09l",
    "oauth": {},
    "aws_cloud_logic_custom": [
        {
            "name": "echoguardApi",
            "endpoint": "https://j5pdd9cbul.execute-api.us-east-1.amazonaws.com/prod",
            "region": "us-east-1"
        }
    ],
    "aws_user_files_s3_bucket": "echoguard-audio-656570226565-us-east-1",
    "aws_user_files_s3_bucket_region": "us-east-1"
};

export default awsmobile;