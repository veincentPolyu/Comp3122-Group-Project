import asyncio
import json
import os
from dotenv import load_dotenv
from extractor import LocationExtractor

async def test_youtube_extraction(url):
    """Test YouTube extraction with audio transcription"""
    load_dotenv()
    
    # Get API keys from environment or provide directly
    youtube_api_key = os.getenv("YOUTUBE_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not youtube_api_key or not openai_api_key:
        print("Please set YOUTUBE_API_KEY and OPENAI_API_KEY in your .env file")
        return
    
    # Create the extractor
    extractor = LocationExtractor(youtube_api_key, openai_api_key)
    
    # Process the URL
    print(f"Processing YouTube URL: {url}")
    result = await extractor.process_url(url)
    
    # Display results
    print("\n" + "="*50)
    print("EXTRACTED LOCATIONS:")
    print("="*50)
    
    if result["extracted_locations"]["success"]:
        locations = result["extracted_locations"]["locations"]
        if locations:
            for i, location in enumerate(locations):
                print(f"{i+1}. {location['name']} ({location['category']})")
                print(f"   {location['description']}")
                print()
        else:
            print("No locations found in the video")
    else:
        print(f"Error: {result['extracted_locations'].get('error', 'Unknown error')}")
    
    # Return results for further processing if needed
    return result

if __name__ == "__main__":
    # Get URL from command line or use a default
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    # Run the test
    asyncio.run(test_youtube_extraction(url)) 