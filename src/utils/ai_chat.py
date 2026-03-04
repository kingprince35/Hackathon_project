"""Simple AI Chat Assistant using Amazon Bedrock - Nova Lite"""

import boto3
import json
import os

class AIChatAssistant:
    """GST Q&A using Amazon Nova Lite"""
    
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
            
            self.system_prompt = """You are a GST compliance expert for Indian businesses.
Answer questions about:
- GST rates for different products
- HSN codes
- Invoice requirements
- Compliance rules

Keep answers short (2-3 sentences) and practical. Use simple language that Indian business owners understand."""
            
            self.enabled = True
            print(f"✅ Chat using Amazon Nova Lite")
            
        except Exception as e:
            print(f"Warning: Bedrock chat not configured: {e}")
            self.enabled = False
    
    def ask(self, question: str) -> str:
        """Ask GST question"""
        
        if not self.enabled:
            return "AI assistant not available. Please configure AWS Bedrock credentials."
        
        # Combine system prompt with user question
        full_prompt = f"{self.system_prompt}\n\nQuestion: {question}\n\nAnswer:"
        
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
                                    "text": full_prompt
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
            answer = result['output']['message']['content'][0]['text']
            
            return answer
            
        except Exception as e:
            error_msg = str(e)
            print(f"Chat error: {error_msg}")
            return f"Error: {error_msg}"