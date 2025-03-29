"""
Test OpenAI API configuration and connectivity
"""
import os
import openai
from dotenv import load_dotenv

def test_configuration():
    load_dotenv()
    
    print("Testing OpenAI API configuration")
    print("-" * 50)
    
    # Get configuration from environment
    openai_key = os.getenv("OPENAI_API_KEY")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_deployment = os.getenv("AZURE_DEPLOYMENT_NAME")
    azure_version = os.getenv("AZURE_API_VERSION", "2023-05-15")
    
    # Mask the API key for security
    masked_key = f"{openai_key[:4]}...{openai_key[-4:]}" if openai_key and len(openai_key) > 8 else "Not set"
    
    # Print configuration
    print(f"OpenAI API Key: {masked_key}")
    print(f"Azure Endpoint: {azure_endpoint or 'Not set'}")
    print(f"Azure Deployment: {azure_deployment or 'Not set'}")
    print(f"Azure API Version: {azure_version}")
    print("-" * 50)
    
    # Test Standard OpenAI API
    if openai_key and not azure_endpoint:
        print("Testing Standard OpenAI API connection...")
        try:
            client = openai.OpenAI(api_key=openai_key)
            models = client.models.list()
            print(f"✅ Successfully connected to OpenAI API!")
            print(f"Available models: {len(models.data)}")
            print(f"Sample models: {', '.join([m.id for m in models.data[:3]])}")
            
            # Test a simple completion
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello, how are you?"}],
                max_tokens=10
            )
            print(f"Test completion: {response.choices[0].message.content}")
            print("✅ Test completion successful!")
            
        except Exception as e:
            print(f"❌ Error connecting to OpenAI API: {str(e)}")
    
    # Test Azure OpenAI API
    elif openai_key and azure_endpoint and azure_deployment:
        print("Testing Azure OpenAI API connection...")
        try:
            client = openai.AzureOpenAI(
                api_key=openai_key,
                api_version=azure_version,
                azure_endpoint=azure_endpoint
            )
            
            # Try a simple completion as a test
            response = client.chat.completions.create(
                model=azure_deployment,
                messages=[{"role": "user", "content": "Hello, how are you?"}],
                max_tokens=10
            )
            print(f"Test completion: {response.choices[0].message.content}")
            print("✅ Azure OpenAI connection and test completion successful!")
            
        except Exception as e:
            print(f"❌ Error connecting to Azure OpenAI API: {str(e)}")
    
    else:
        print("❌ Missing required configuration parameters.")
        print("Please set either OPENAI_API_KEY for standard OpenAI API")
        print("or OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, and AZURE_DEPLOYMENT_NAME for Azure OpenAI.")

if __name__ == "__main__":
    test_configuration() 