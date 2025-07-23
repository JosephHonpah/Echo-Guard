# Compliance Analysis Engine Spec

## Requirements
- Analyze transcribed text for compliance violations
- Identify potential regulatory issues in financial conversations
- Score risk level of conversations
- Categorize issues by compliance domain
- Generate detailed reports for auditing
- Flag high-risk conversations for human review

## Design
- Dual AI analysis approach:
  1. Amazon Bedrock for general compliance analysis
  2. Custom Kiro AI for specialized financial compliance
- Weighted scoring system combining both analyses
- Rule-based pattern matching for known violations
- ML-based anomaly detection for unusual patterns
- Real-time alerting for critical violations

## Implementation Tasks
1. Create Lambda function for transcript analysis
2. Implement Bedrock prompt engineering for compliance detection
3. Develop custom financial compliance rules engine
4. Create scoring algorithm combining both analyses
5. Implement categorization of compliance issues
6. Set up alerting system for high-risk content
7. Create detailed reporting system for audit trails

## Technical Approach

### Bedrock Integration
```python
def analyze_with_bedrock(transcript):
    prompt = f"""
    Analyze the following transcript for compliance issues:
    
    {transcript}
    
    Identify potential compliance violations and assign a risk score (0-1).
    Categorize each issue by type (KYC, AML, disclosure, suitability, etc.)
    Return JSON format with 'score', 'issues', and 'categories' fields.
    """
    
    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-sonnet-20240229-v1:0',
        body=json.dumps({
            'anthropic_version': 'bedrock-2023-05-31',
            'max_tokens': 1000,
            'messages': [{'role': 'user', 'content': prompt}]
        })
    )
    
    result = json.loads(response['body'].read())
    content = result['content'][0]['text']
    return json.loads(content)
```

### Kiro AI Integration
```python
def analyze_with_kiro_ai(transcript):
    # Financial regulations pattern matching
    financial_regulations = {
        'KYC': ['identity', 'verify', 'identification', 'know your customer'],
        'AML': ['money laundering', 'suspicious', 'transaction', 'cash deposit'],
        'Disclosure': ['disclose', 'disclosure', 'inform', 'notification'],
        'Suitability': ['suitable', 'appropriate', 'risk tolerance', 'investment objective']
    }
    
    issues = []
    categories = {}
    
    # Check each regulation category
    for category, keywords in financial_regulations.items():
        category_score = 0
        category_issues = []
        
        for keyword in keywords:
            if keyword.lower() in transcript.lower():
                # Context analysis around keyword
                context = extract_context(transcript, keyword)
                risk = assess_risk(context)
                
                if risk > 0.3:
                    category_score += risk
                    category_issues.append({
                        'keyword': keyword,
                        'context': context,
                        'risk': risk
                    })
        
        if category_issues:
            categories[category] = {
                'score': min(category_score, 1.0),
                'issues': category_issues
            }
            issues.extend(category_issues)
    
    return {
        'score': calculate_overall_score(categories),
        'issues': issues,
        'categories': categories
    }
```

### Combined Analysis
```python
def calculate_combined_score(bedrock_result, kiro_result):
    # Weighted combination: 60% Bedrock, 40% Kiro
    bedrock_weight = 0.6
    kiro_weight = 0.4
    
    # Calculate weighted score
    combined_score = (bedrock_result['score'] * bedrock_weight) + 
                     (kiro_result['score'] * kiro_weight)
    
    # Merge issues and categories
    all_issues = bedrock_result.get('issues', []) + kiro_result.get('issues', [])
    
    # Merge categories
    all_categories = {}
    for category, data in bedrock_result.get('categories', {}).items():
        all_categories[category] = data
    
    for category, data in kiro_result.get('categories', {}).items():
        if category in all_categories:
            # Merge category data
            all_categories[category]['score'] = max(
                all_categories[category]['score'],
                data['score']
            )
            all_categories[category]['issues'].extend(data['issues'])
        else:
            all_categories[category] = data
    
    return {
        'score': combined_score,
        'issues': all_issues,
        'categories': all_categories,
        'high_risk': combined_score > 0.7
    }
```

## References
#[[file:infrastructure/echoguard-complete.yaml]]
#[[file:backend/lambda/analyze_transcript.py]]