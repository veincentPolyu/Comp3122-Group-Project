import asyncio
import os
from dotenv import load_dotenv
import json
from extractor import LocationExtractor

async def test_youtube_extraction():
    # Load environment variables
    load_dotenv()
    
    # Get API keys from environment variables
    youtube_api_key = os.getenv("YOUTUBE_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not youtube_api_key or not openai_api_key:
        print("Error: Missing API keys in environment variables")
        print("Please ensure YOUTUBE_API_KEY and OPENAI_API_KEY are set")
        return

    # Initialize the extractor
    extractor = LocationExtractor(
        youtube_api_key=youtube_api_key,
        openai_api_key=openai_api_key
    )
    
    # Test URL
    test_url = "https://youtu.be/IuTDuvYr7f0?si=kkdl43cWpU0vZEjw"
    
    print(f"Testing extraction for YouTube video: {test_url}")
    
    try:
        # Process the URL
        result = await extractor.process_url(test_url)
        
        # Print results in a readable format
        print("\nExtraction Results:")
        print(json.dumps(result, indent=2))
        
        # Print locations in a more readable format
        if result["extracted_locations"]["success"]:
            locations = result["extracted_locations"]["locations"]
            print("\nExtracted Locations:")
            for loc in locations:
                print(f"\nLocation: {loc['name']}")
                print(f"Category: {loc['category']}")
                print(f"Description: {loc['description']}")
                print(f"Tags: {', '.join(loc['tags'])}")
        
    except Exception as e:
        print(f"Error during extraction: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_youtube_extraction()) 