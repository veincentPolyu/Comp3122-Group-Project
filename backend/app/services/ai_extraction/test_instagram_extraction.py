"""
Test script for Instagram location extraction
"""
import asyncio
import json
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_extraction.extractor import LocationExtractor

async def test_instagram_extraction(url):
    """Test the Instagram location extraction"""
    load_dotenv()
    
    youtube_api_key = os.getenv("YOUTUBE_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    print(f"Testing location extraction from {url}")
    extractor = LocationExtractor(youtube_api_key, openai_api_key)
    result = await extractor.extract_from_instagram(url)
    
    print("\n=== EXTRACTION RESULTS ===")
    print(json.dumps(result, indent=2))
    
    if result["extracted_locations"]["success"] and result["extracted_locations"]["locations"]:
        print("\nLocations found:")
        for location in result["extracted_locations"]["locations"]:
            print(f"- {location['name']} ({location['category']}): {location['description']}")
    else:
        print("\nNo locations found or extraction failed")
    
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_instagram_extraction.py <instagram_url>")
    else:
        url = sys.argv[1]
        asyncio.run(test_instagram_extraction(url)) 