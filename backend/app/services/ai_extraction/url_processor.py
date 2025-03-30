import asyncio
import os
from dotenv import load_dotenv
import json
from extractor import LocationExtractor
import sys
import re
import urllib.parse
import requests
import time
from datetime import datetime

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

def format_to_api_response_extended(url: str, locations: list, source_type: str = "web", title: str = "", timestamp: str = "") -> dict:
    """Format locations to match the new extended API response format"""
    # Generate current timestamp if none provided
    if not timestamp:
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Ensure each location has the required fields in the right format
    formatted_locations = []
    duplicate_check = {"success": True, "duplicates": []}
    
    for idx, loc in enumerate(locations):
        # Extract description from the location
        description = loc.get('description', '')
        
        # Parse address from description if possible
        address = ""
        if "address" in description.lower() or "located" in description.lower():
            # Try to extract address using simple heuristics
            address_patterns = [
                r'(?:address|located at)[:\s]+([^\.]+)',
                r'(?:in|at)\s+([^\.]+)'
            ]
            for pattern in address_patterns:
                address_match = re.search(pattern, description, re.IGNORECASE)
                if address_match:
                    address = address_match.group(1).strip()
                    break
        
        # Create the formatted location object with all required fields
        formatted_loc = {
            "id": loc.get("id", f"loc{idx+1}"),
            "name": loc.get("name", "Unknown Location"),
            "address": address,
            "category": loc.get("category", "point_of_interest"),
            "coordinates": {
                "lat": loc.get("coordinates", {}).get("lat") if isinstance(loc.get("coordinates"), dict) else None,
                "lng": loc.get("coordinates", {}).get("lng") if isinstance(loc.get("coordinates"), dict) else None
            },
            "business_hours": extract_business_hours(description),
            "busy_periods": extract_busy_periods(description),
            "rating": extract_rating(description),
            "price_level": extract_price_level(description),
            "photos": [],
            "description": description,
            "source": {
                "url": url,
                "type": source_type,
                "title": title,
                "timestamp": timestamp
            },
            "tags": loc.get("tags", ["travel"])
        }
        formatted_locations.append(formatted_loc)
    
    # Check for duplicates (simple implementation)
    if len(formatted_locations) > 1:
        for i in range(len(formatted_locations)):
            for j in range(i+1, len(formatted_locations)):
                # Simple name similarity check
                name1 = formatted_locations[i]["name"].lower()
                name2 = formatted_locations[j]["name"].lower()
                
                # Calculate simple similarity score
                similarity = calculate_similarity(name1, name2)
                
                # If names are similar, add to duplicates
                if similarity > 0.8:
                    duplicate_check["duplicates"].append({
                        "original": formatted_locations[i]["id"],
                        "duplicate": formatted_locations[j]["id"],
                        "similarity_score": round(similarity, 2)
                    })
    
    # Create the full response structure
    response = {
        "extracted_locations": {
            "success": True,
            "url": url,
            "locations": formatted_locations
        },
        "duplicate_check": duplicate_check,
        "place_details": {
            "success": True,
            "place_id": formatted_locations[0]["id"] if formatted_locations else None,
            "updated_fields": {
                "business_hours": formatted_locations[0]["business_hours"] if formatted_locations else [],
                "busy_periods": formatted_locations[0]["busy_periods"] if formatted_locations else []
            }
        }
    }
    
    return response

def calculate_similarity(str1: str, str2: str) -> float:
    """Simple similarity calculation between two strings"""
    # Convert to sets of words
    set1 = set(str1.lower().split())
    set2 = set(str2.lower().split())
    
    # Calculate Jaccard similarity
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    
    if union == 0:
        return 0
    return intersection / union

def extract_business_hours(text: str) -> list:
    """Extract business hours from text"""
    hours = []
    
    # Look for common patterns in business hours
    patterns = [
        r'(?:open|hours)(?:[\s:]+)([^\.]+)',
        r'(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)[^\.]+?(?:\d{1,2}:\d{2})',
        r'\b(?:opening hours|business hours)[^\.]+',
        r'\b\d{1,2}(?:am|pm)\s*-\s*\d{1,2}(?:am|pm)\b'
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            hours.append(match.group(0).strip())
    
    # If found, format properly, otherwise return empty list
    if hours:
        # Remove duplicates
        hours = list(set(hours))
        
        # If we found general text but not structured hours, create a more structured format
        if len(hours) == 1 and (":" not in hours[0] or "-" not in hours[0]):
            return ["Hours: " + hours[0]]
        return hours[:3]  # Limit to 3 entries
    
    return []

def extract_busy_periods(text: str) -> list:
    """Extract busy periods from text"""
    busy_periods = []
    
    # Look for common patterns in busy period descriptions
    patterns = [
        r'(?:busy|peak|crowded)[^\.]*?(\d{1,2}(?::\d{2})?(?:\s*[ap]m)?[^\.]*?\d{1,2}(?::\d{2})?(?:\s*[ap]m)?)',
        r'(?:avoid|wait times)[^\.]*?(\d{1,2}(?::\d{2})?(?:\s*[ap]m)?[^\.]*?\d{1,2}(?::\d{2})?(?:\s*[ap]m)?)'
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            busy_periods.append(match.group(1).strip())
    
    return busy_periods

def extract_rating(text: str) -> float:
    """Extract rating from text"""
    # Look for common patterns in ratings
    patterns = [
        r'(?:rated|rating|score)[^\.]*?(\d+(?:\.\d+)?)\s*(?:stars|points|out of \d+)',
        r'(\d+(?:\.\d+)?)\s*(?:stars|star rating)',
        r'(\d+(?:\.\d+)?)\s*/\s*\d+'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                pass
    
    return None

def extract_price_level(text: str) -> int:
    """Extract price level (1-4) from text"""
    # Look for common patterns in price level descriptions
    patterns = [
        r'(?:price|cost)[^\.]*?(\$+)',
        r'(?:price|cost)[^\.]*?(inexpensive|affordable|moderate|expensive|very expensive)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            result = match.group(1).lower()
            if '$' in result:
                return len(result)  # Count the number of $ symbols
            elif 'inexpensive' in result:
                return 1
            elif 'affordable' in result:
                return 1
            elif 'moderate' in result:
                return 2
            elif 'expensive' in result and 'very' not in result:
                return 3
            elif 'very expensive' in result:
                return 4
    
    return None

async def process_url_input(url: str = None, force_audio: bool = False, skip_ai: bool = False):
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
        source_type = "video"
    elif is_instagram_url(url):
        url_type = "Instagram content"
        source_type = "social_media"
    else:
        url_type = "Web page"
        source_type = "web"
        
    print(f"URL type: {url_type}")
    
    try:
        if force_audio and is_youtube_url(url):
            # Extract video ID
            video_id = None
            parsed_url = urllib.parse.urlparse(url)
            if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
                query_params = urllib.parse.parse_qs(parsed_url.query)
                video_id = query_params.get('v', [None])[0]
            elif parsed_url.hostname == 'youtu.be':
                video_id = parsed_url.path[1:]
                
            if video_id:
                print(f"Forcing audio extraction for video ID: {video_id}")
                
                # Create a test mode that extracts the audio but doesn't try to transcribe
                extract_only = '--extract-only' in sys.argv or '-eo' in sys.argv
                
                if extract_only:
                    print("Extract-only mode: Will download audio but skip transcription")
                    # Call a custom method that just extracts the audio without transcription
                    audio_path = await extract_youtube_audio_only(extractor, video_id)
                    if audio_path:
                        print(f"\nSuccessfully extracted audio to: {audio_path}")
                    else:
                        print("Failed to extract audio")
                    return
                
                # Standard mode - extract and transcribe
                transcript_text = await extractor._extract_and_transcribe_youtube_audio(video_id)
                if transcript_text:
                    print("\nSuccessfully extracted and transcribed audio:")
                    print("=" * 50)
                    print("TRANSCRIPTION RESULT:")
                    print("=" * 50)
                    
                    # Print transcript in chunks to make it more readable
                    chunk_size = 200
                    for i in range(0, len(transcript_text), chunk_size):
                        chunk = transcript_text[i:i+chunk_size]
                        print(chunk)
                    
                    print("=" * 50)
                    print(f"Total length: {len(transcript_text)} characters")
                    
                    # Create a file with the transcript for further inspection
                    transcript_file = f"youtube_transcript_{video_id}.txt"
                    with open(transcript_file, "w", encoding="utf-8") as f:
                        f.write(transcript_text)
                    print(f"Transcript saved to: {transcript_file}")
                    
                    # Process with AI if requested
                    if not skip_ai:
                        print("\nProcessing transcript with AI...")
                        # Get video metadata for better context
                        try:
                            video_info = extractor.youtube.videos().list(
                                part="snippet",
                                id=video_id
                            ).execute()

                            if 'items' in video_info and video_info['items']:
                                video_title = video_info['items'][0]['snippet']['title']
                                timestamp = video_info['items'][0]['snippet'].get('publishedAt', '')
                            else:
                                video_title = "Unknown Title"
                                timestamp = ""
                                
                            # Create full content with both title and transcript
                            full_content = f"Title: {video_title}\n\nTranscript:\n{transcript_text}"
                            
                            # Process with LLM
                            locations = await extractor._process_with_llm(full_content)
                            
                            # Format locations to match the extended API response
                            youtube_url = f"https://www.youtube.com/watch?v={video_id}"
                            api_response = format_to_api_response_extended(
                                url=youtube_url, 
                                locations=locations,
                                source_type="video",
                                title=video_title,
                                timestamp=timestamp
                            )
                            
                            # Print results in a more readable format
                            print("\nExtracted Locations (API format):")
                            print(json.dumps(api_response, indent=2))
                            
                            # Also show in a simplified format
                            print("\nExtracted Locations (Simplified):")
                            if locations:
                                for loc in locations:
                                    print("\n" + "="*50)
                                    print(f"Location: {loc['name']}")
                                    print(f"Category: {loc['category']}")
                                    print(f"Description: {loc['description']}")
                                    print(f"Tags: {', '.join(loc['tags'])}")
                            else:
                                print("No locations found in the content.")
                                
                            # Save formatted response to file
                            response_file = f"locations_response_{video_id}.json"
                            with open(response_file, "w", encoding="utf-8") as f:
                                json.dump(api_response, f, indent=2)
                            print(f"\nFormatted response saved to: {response_file}")
                            
                        except Exception as e:
                            print(f"Error processing with AI: {str(e)}")
                else:
                    print("Failed to extract or transcribe audio")
                return
            else:
                print("Could not extract video ID from URL")
                return
        
        # Process the URL normally if not forcing audio extraction
        raw_result = await extractor.process_url(url)
        
        # Convert to extended format
        if raw_result["extracted_locations"]["success"]:
            # Get original locations
            orig_locations = raw_result["extracted_locations"]["locations"]
            
            # Format to extended API response
            result = format_to_api_response_extended(
                url=url,
                locations=orig_locations,
                source_type=source_type
            )
        else:
            # Keep error response as is
            result = raw_result
        
        # Print results in API format
        print("\nExtraction Results (API format):")
        print(json.dumps(result, indent=2))
        
        # Also print in a simplified readable format
        print("\nExtraction Results (Simplified):")
        if result["extracted_locations"]["success"]:
            locations = result["extracted_locations"]["locations"]
            print(f"\nFound {len(locations)} locations:")
            for loc in locations:
                print("\n" + "="*50)
                print(f"Location: {loc['name']}")
                if loc["address"]:
                    print(f"Address: {loc['address']}")
                print(f"Category: {loc['category']}")
                print(f"Description: {loc['description']}")
                if loc["business_hours"]:
                    print(f"Business Hours: {', '.join(loc['business_hours'])}")
                if loc["busy_periods"]:
                    print(f"Busy Periods: {', '.join(loc['busy_periods'])}")
                if loc["rating"]:
                    print(f"Rating: {loc['rating']}")
                if loc["price_level"]:
                    print(f"Price Level: {'$' * loc['price_level']}")
                print(f"Tags: {', '.join(loc['tags'])}")
        else:
            print("\nError in extraction:")
            print(result["extracted_locations"].get("error", "Unknown error occurred"))
        
        # Save to file
        output_file = "location_extraction_result.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(f"\nFull results saved to: {output_file}")
        
    except Exception as e:
        print(f"Error during extraction: {str(e)}")
        import traceback
        traceback.print_exc()

async def extract_youtube_audio_only(extractor, video_id: str):
    """Extract audio from YouTube video without transcription"""
    import tempfile
    import os
    import pytube
    
    try:
        print(f"Downloading YouTube video with ID: {video_id}")
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a permanent directory for the output
            output_dir = os.path.join(os.getcwd(), "extracted_audio")
            os.makedirs(output_dir, exist_ok=True)
            
            # Download video from YouTube
            youtube_url = f"https://www.youtube.com/watch?v={video_id}"
            try:
                yt = pytube.YouTube(youtube_url)
                title = yt.title
                print(f"Video title: {title}")
            except Exception as e:
                print(f"Error getting video info: {str(e)}")
                title = f"video_{video_id}"
            
            # Get the audio stream
            print("Extracting audio stream")
            audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
            if not audio_stream:
                print("No audio stream found")
                return None
            
            # Download the audio to the temp directory
            print(f"Downloading audio to temporary directory: {temp_dir}")
            audio_file_path = audio_stream.download(output_path=temp_dir)
            print(f"Downloaded audio to: {audio_file_path}")
            
            # Convert to mp3 if ffmpeg is available
            safe_title = "".join([c if c.isalnum() or c in [' ', '-', '_'] else '_' for c in title])
            mp3_path = os.path.join(output_dir, f"{safe_title}_{video_id}.mp3")
            
            try:
                print(f"Converting audio to mp3 format at: {mp3_path}")
                import subprocess
                subprocess.run(
                    ["ffmpeg", "-i", audio_file_path, "-q:a", "0", "-map", "a", mp3_path],
                    check=True, capture_output=True, timeout=120
                )
                print(f"Successfully converted to mp3: {mp3_path}")
                return mp3_path
            except Exception as e:
                print(f"FFmpeg conversion failed: {str(e)}.")
                
                # If conversion fails, copy the original file
                import shutil
                orig_ext = os.path.splitext(audio_file_path)[1]
                orig_path = os.path.join(output_dir, f"{safe_title}_{video_id}{orig_ext}")
                shutil.copy2(audio_file_path, orig_path)
                print(f"Copied original audio file to: {orig_path}")
                return orig_path
    
    except Exception as e:
        print(f"Error in YouTube audio extraction: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def main():
    # Check if URL was provided as command line argument
    url = sys.argv[1] if len(sys.argv) > 1 else None
    
    # Check for flags
    force_audio = '--force-audio' in sys.argv or '-fa' in sys.argv
    skip_ai = '--skip-ai' in sys.argv or '-sa' in sys.argv
    
    asyncio.run(process_url_input(url, force_audio, skip_ai))

if __name__ == "__main__":
    main() 