import os
import openai
from dotenv import load_dotenv

def test_openai_credentials():
    """Test OpenAI API credentials"""
    load_dotenv()
    
    # Get API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not found in environment variables or .env file")
        return False
    
    # Mask API key for logging
    masked_key = f"{api_key[:4]}...{api_key[-4:]}" if len(api_key) > 8 else "***"
    print(f"Using API key: {masked_key}")
    
    # Test with direct OpenAI API (not Azure)
    try:
        print("Testing connection to OpenAI API...")
        client = openai.OpenAI(api_key=api_key)
        models = client.models.list()
        print(f"Success! Connected to OpenAI API. Available models: {len(models.data)}")
        print(f"Models include: {', '.join([model.id for model in models.data[:5]])}")
        return True
    except Exception as e:
        print(f"ERROR connecting to OpenAI API: {str(e)}")
    
    # Try with Azure OpenAI
    try:
        print("\nTesting connection to Azure OpenAI...")
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        if not azure_endpoint:
            print("AZURE_OPENAI_ENDPOINT not found in environment")
            return False
            
        print(f"Using Azure endpoint: {azure_endpoint}")
        client = openai.AzureOpenAI(
            api_key=api_key,
            api_version="2023-05-15",
            azure_endpoint=azure_endpoint
        )
        
        models = client.models.list()
        print(f"Success! Connected to Azure OpenAI. Available models: {len(models.data)}")
        return True
    except Exception as e:
        print(f"ERROR connecting to Azure OpenAI: {str(e)}")
        
    return False

if __name__ == "__main__":
    test_openai_credentials() 