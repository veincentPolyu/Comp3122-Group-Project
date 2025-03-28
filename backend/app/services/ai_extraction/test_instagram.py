import asyncio
import os
from dotenv import load_dotenv
import json
from extractor import LocationExtractor

async def test_instagram_extraction():
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
    
    # Ask user for Instagram URL
    url = input("Enter an Instagram URL (post or reel): ").strip()
    if not url:
        url = "https://www.instagram.com/p/sample_post_id/"  # Default sample URL
    
    print(f"Testing Instagram extraction for URL: {url}")
    
    try:
        # Check if it's an Instagram URL
        if "instagram.com" not in url and "instagr.am" not in url:
            print("Error: Not an Instagram URL")
            return
        
        # Extract Instagram ID and type
        content_type, content_id = extractor._extract_instagram_id(url)
        if not content_id:
            print("Error: Could not extract Instagram ID from URL")
            return
        
        print(f"Instagram content type: {content_type}, ID: {content_id}")
        
        # Extract content
        print("\nExtracting content...")
        content = await extractor._extract_instagram_content(url)
        
        if content:
            print("\nExtracted Content:")
            print("=" * 60)
            print(content[:300] + "..." if len(content) > 300 else content)
            print("=" * 60)
            
            # Process for locations
            print("\nProcessing for locations...")
            result = await extractor.extract_from_instagram(url)
            
            print("\nExtraction Results:")
            if result["extracted_locations"]["success"]:
                locations = result["extracted_locations"]["locations"]
                if locations:
                    print(f"\nFound {len(locations)} locations:")
                    for loc in locations:
                        print("\n" + "=" * 50)
                        print(f"Location: {loc['name']}")
                        print(f"Category: {loc['category']}")
                        print(f"Description: {loc['description']}")
                        print(f"Tags: {', '.join(loc['tags'])}")
                else:
                    print("No locations found in the content.")
            else:
                print("\nError in extraction:")
                print(result["extracted_locations"].get("error", "Unknown error occurred"))
        else:
            print("Failed to extract content from Instagram")
            
    except Exception as e:
        print(f"Error during testing: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_instagram_extraction()) 