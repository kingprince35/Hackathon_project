"""AI-Powered Error Explanation using Amazon Bedrock - Nova Lite"""

import boto3
import json
import os
from typing import Dict

class AIExplainer:
    """Generate human-friendly error explanations using Amazon Nova Lite"""
    
    def __init__(self):
        try:
            self.bedrock = boto3.client(
                service_name='bedrock-runtime',
                region_name=os.getenv('AWS_DEFAULT_REGION', 'ap-south-1'),
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
            )
            
            # Use Amazon Nova Lite - Fast and cost-effective!
            self.model_id = 'us.amazon.nova-lite-v1:0'
            self.enabled = True
            
            print(f"✅ Using Amazon Nova Lite for AI explanations")
            
        except Exception as e:
            print(f"Warning: Bedrock not configured: {e}")
            self.enabled = False
    
    def explain_error(self, error: Dict) -> str:
        """
        Generate AI explanation for an error
        
        Args:
            error: Error dictionary with field, message, values
            
        Returns:
            Human-friendly explanation in Hindi/English
        """
        
        if not self.enabled:
            return "AI explanation not available. Please configure AWS Bedrock credentials."
        
        prompt = f"""You are a GST compliance expert helping Indian small business owners.

Explain this invoice error in SIMPLE language (mix of Hindi and English that Indians use):

Field: {error.get('field')}
Error: {error.get('message')}
Current Value: {error.get('current_value', 'Missing')}
Correct Value: {error.get('expected_value', 'Unknown')}

Explain in 2-3 sentences:
1. What's the problem (क्या गलत है)
2. Why it matters (क्यों ज़रूरी है)
3. How to fix (कैसे ठीक करें)

Use simple words. Be helpful and friendly. Keep it under 100 words."""

        try:
            # Amazon Nova uses a different API format
            response = self.bedrock.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "text": prompt
                                }
                            ]
                        }
                    ],
                    "inferenceConfig": {
                        "max_new_tokens": 300,
                        "temperature": 0.3,
                        "top_p": 0.9
                    }
                })
            )
            
            result = json.loads(response['body'].read())
            
            # Extract text from Nova response format
            explanation = result['output']['message']['content'][0]['text']
            
            return explanation
            
        except Exception as e:
            error_msg = str(e)
            print(f"Error generating AI explanation: {error_msg}")
            
            # Fallback explanation
            return self._fallback_explanation(error)
    
    def _fallback_explanation(self, error: Dict) -> str:
        """Generate simple explanation without AI"""
        field = error.get('field', 'Unknown field')
        message = error.get('message', '')
        current = error.get('current_value', 'Missing')
        expected = error.get('expected_value')
        
        explanation = f"**Problem (समस्या):** {message}\n\n"
        
        if current:
            explanation += f"**Current value (वर्तमान मान):** {current}\n\n"
        
        if expected:
            explanation += f"**Correct value (सही मान):** {expected}\n\n"
            explanation += f"**How to fix (कैसे ठीक करें):** Change {field} from '{current}' to '{expected}'"
        else:
            explanation += "**How to fix (कैसे ठीक करें):** Please review this field and correct the value according to GST rules."
        
        return explanation
    
    def suggest_fix(self, error: Dict) -> str:
        """Generate auto-fix suggestion"""
        
        if 'expected_value' in error:
            return f"Change to: {error['expected_value']}"
        
        return "Please review and correct manually"