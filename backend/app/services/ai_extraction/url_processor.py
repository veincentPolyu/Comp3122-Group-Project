import asyncio
import os
from dotenv import load_dotenv
import json
from extractor import LocationExtractor
import sys
import re

def is_youtube_url(url: str) -> bool:
    """Check if the URL is a YouTube URL"""
    youtube_patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=[\w-]+',
        r'(?:https?://)?(?:www\.)?youtu\.be/[\w-]+'
    ]
    return any(re.match(pattern, url) for pattern in youtube_patterns)

def is_instagram_url(url: str) -> bool:
    """Check if the URL is an Instagram URL"""
    instagram_patterns = [
        r'(?:https?://)?(?:www\.)?instagram\.com/p/[\w-]+/?',  # Posts
        r'(?:https?://)?(?:www\.)?instagram\.com/reel/[\w-]+/?',  # Reels
        r'(?:https?://)?(?:www\.)?instagram\.com/tv/[\w-]+/?',  # IGTV
        r'(?:https?://)?(?:www\.)?instagr\.am/p/[\w-]+/?',  # Short URLs for posts
        r'(?:https?://)?(?:www\.)?instagr\.am/reel/[\w-]+/?'  # Short URLs for reels
    ]
    return any(re.match(pattern, url) for pattern in instagram_patterns)

async def process_url_input(url: str = None):
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
    
    # If no URL provided, ask for input
    if not url:
        url = input("Please enter a URL (YouTube, Instagram, or web page): ").strip()
    
    # Validate URL format
    if not url.startswith(('http://', 'https://')):
        print("Error: Invalid URL format. URL must start with http:// or https://")
        return
    
    print(f"\nProcessing URL: {url}")
    
    # Determine URL type
    if is_youtube_url(url):
        url_type = "YouTube video"
    elif is_instagram_url(url):
        url_type = "Instagram content"
    else:
        url_type = "Web page"
        
    print(f"URL type: {url_type}")
    
    try:
        # Process the URL
        result = await extractor.process_url(url)
        
        # Print results in a readable format
        print("\nExtraction Results:")
        if result["extracted_locations"]["success"]:
            locations = result["extracted_locations"]["locations"]
            print(f"\nFound {len(locations)} locations:")
            for loc in locations:
                print("\n" + "="*50)
                print(f"Location: {loc['name']}")
                print(f"Category: {loc['category']}")
                print(f"Description: {loc['description']}")
                print(f"Tags: {', '.join(loc['tags'])}")
        else:
            print("\nError in extraction:")
            print(result["extracted_locations"].get("error", "Unknown error occurred"))
        
    except Exception as e:
        print(f"Error during extraction: {str(e)}")

def main():
    # Check if URL was provided as command line argument
    url = sys.argv[1] if len(sys.argv) > 1 else None
    asyncio.run(process_url_input(url))

if __name__ == "__main__":
    main() 