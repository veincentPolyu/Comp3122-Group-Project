import asyncio
import os
from dotenv import load_dotenv
from extractor import LocationExtractor

async def test_multilingual_extraction():
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
    
    # Example text with Chinese location information
    example_text = """
    來啦來啦！澀谷的年度櫻花祭典開始了！由今日3月28日晚上開始，澀谷桜丘町的さくら坂 (櫻坂)開始櫻點燈活動，令整道斜道都是櫻花色的氣氛！另外根據記者現場觀察，現時吉野櫻花已開8成，大家快點行動！！！

    渋谷桜丘 さくら坂
    地址：東京都渋谷区桜丘町 16-12
    活動時間：2025年3月28日-4月4日 1800-2100
    """
    
    print("Testing multilingual location extraction...")
    print("\nExample Text:")
    print("=" * 60)
    print(example_text)
    print("=" * 60)
    
    # Process with LLM
    locations = await extractor._process_with_llm(example_text)
    
    print("\nExtraction Results:")
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
    
    # Now test with an Instagram URL
    print("\n\nNow testing with an Instagram URL...")
    url = input("Enter an Instagram URL with non-English content: ").strip()
    
    if url:
        print(f"\nProcessing Instagram URL: {url}")
        result = await extractor.process_url(url)
        
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

if __name__ == "__main__":
    asyncio.run(test_multilingual_extraction()) 