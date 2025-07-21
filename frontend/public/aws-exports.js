// AWS Amplify configuration
const awsmobile = {
  Auth: {
    region: 'us-east-1',
    userPoolId: 'us-east-1_q03tLrCfS',
    userPoolWebClientId: '4ks45uv9681eh9hnevrutksqru',
    mandatorySignIn: true,
    authenticationFlowType: 'USER_PASSWORD_AUTH'
  },
  Storage: {
    AWSS3: {
      bucket: 'echoguard-audio-656570226565-us-east-1',
      region: 'us-east-1'
    }
  }
};

export default awsmobile;