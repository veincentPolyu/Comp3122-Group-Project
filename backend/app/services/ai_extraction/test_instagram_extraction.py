import asyncio
import os
import json
import random
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import sys
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
    
    # Get Instagram URL from command line or user input
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Enter an Instagram URL: ").strip()
    
    if not url:
        print("No URL provided. Exiting.")
        return
    
    print(f"\nTesting Instagram extraction for URL: {url}")
    
    # Test direct content extraction
    print("\n1. Testing content extraction only:")
    print("=" * 60)
    content = await extractor._extract_instagram_content(url)
    
    if content:
        print(f"\nSuccess! Extracted {len(content)} characters")
        print("\nContent sample (first 300 chars):")
        print("-" * 60)
        print(content[:300] + "..." if len(content) > 300 else content)
        print("-" * 60)
    else:
        print("\nFailed to extract any content from Instagram")
    
    # Test full processing
    print("\n2. Testing full Instagram URL processing:")
    print("=" * 60)
    result = await extractor.extract_from_instagram(url)
    
    print("\nExtraction Results:")
    if result["extracted_locations"]["success"]:
        locations = result["extracted_locations"]["locations"]
        if locations:
            print(f"\nFound {len(locations)} locations:")
            for loc in locations:
                print("\n" + "-" * 50)
                print(f"Location: {loc['name']}")
                print(f"Category: {loc['category']}")
                print(f"Description: {loc['description']}")
                print(f"Tags: {', '.join(loc['tags'])}")
        else:
            print("\nNo locations found in the content")
            if "note" in result["extracted_locations"]:
                print(f"Note: {result['extracted_locations']['note']}")
    else:
        print("\nError in extraction:")
        print(result["extracted_locations"].get("error", "Unknown error occurred"))

if __name__ == "__main__":
    asyncio.run(test_instagram_extraction()) 