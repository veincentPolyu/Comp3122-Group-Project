import asyncio
import os
import json
from dotenv import load_dotenv
from extractor import LocationExtractor

async def test_raw_extraction():
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
    
    # Test with an example containing location information in different formats
    example_text = """
    來啦來啦！澀谷的年度櫻花祭典開始了！由今日3月28日晚上開始，澀谷桜丘町的さくら坂 (櫻坂)開始櫻點燈活動，令整道斜道都是櫻花色的氣氛！另外根據記者現場觀察，現時吉野櫻花已開8成，大家快點行動！！！

    渋谷桜丘 さくら坂
    地址：東京都渋谷区桜丘町 16-12
    活動時間：2025年3月28日-4月4日 1800-2100
    
    Instagram post mentions the iconic Taj Mahal in Agra, India. It's open daily from 6am to 7pm except on Fridays. Tickets cost 1100 INR for foreigners.
    
    We visited the Grand Canyon (coordinates: 36.0544, -112.2583) during our road trip. The South Rim is open 24/7 year-round.
    """
    
    print("\nTesting raw content extraction with example text...")
    locations = await extractor._process_with_llm(example_text)
    
    print("\nExtraction Results:")
    if locations:
        for loc in locations:
            print("\n" + "=" * 50)
            print(f"Location: {loc['name']}")
            print(f"Category: {loc['category']}")
            print(f"Description: {loc['description']}")
            print(f"Tags: {', '.join(loc['tags'])}")
    else:
        print("No locations found in the content.")
    
    # Now test with a real URL
    print("\n\nNow testing with a URL...")
    url = input("Enter a URL (YouTube, Instagram, or web page): ").strip()
    
    if url:
        print(f"\nProcessing URL: {url}")
        
        # Extract raw content first
        if "instagram.com" in url or "instagr.am" in url:
            content_type, content_id = extractor._extract_instagram_id(url)
            content = await extractor._extract_instagram_content(url)
        elif "youtube.com" in url or "youtu.be" in url:
            video_id = extractor._extract_video_id(url)
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                content = " ".join([entry['text'] for entry in transcript_list])
            except:
                content = "Failed to extract transcript"
        else:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.get_text()
        
        # Show a snippet of the raw content
        if content:
            print("\nExtracted Content (first 300 chars):")
            print("=" * 60)
            print(content[:300] + "..." if len(content) > 300 else content)
            print("=" * 60)
            
            # Process for locations
            print("\nProcessing with AI for location extraction...")
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
        else:
            print("Failed to extract content from the URL")

if __name__ == "__main__":
    asyncio.run(test_raw_extraction()) 