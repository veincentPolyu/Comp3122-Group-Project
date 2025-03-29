from typing import List, Dict, Tuple
import re
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import urllib.parse
from dotenv import load_dotenv
import json
import os
from pathlib import Path
import openai  
from youtube_transcript_api import YouTubeTranscriptApi
import random
import subprocess
import sys
# Add the parent directory to the path so we can import modules from the same directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from instagram_login import load_cookies, cookies_to_header, login_and_get_cookies



load_dotenv()

class LocationExtractor:
    def __init__(self, youtube_api_key: str, openai_api_key: str, instagram_username=None, instagram_password=None):
        self.youtube = build('youtube', 'v3', developerKey=youtube_api_key)
        openai.api_key = openai_api_key  # Set the API key
        self.base_url = "https://models.inference.ai.azure.com"
        
        # Store API key for later use
        self.openai_api_key = openai_api_key
        
        # Set Azure-specific parameters
        self.api_version = os.getenv("AZURE_API_VERSION", "2023-05-15")
        self.model_name = os.getenv("AZURE_DEPLOYMENT_NAME", "Comp3122_project")
        
        # Log configuration
        print(f"Using Azure OpenAI endpoint: {self.base_url}")
        print(f"Using deployment: {self.model_name}")
        
        # Load mock data
        self.mock_data = self._load_mock_data()
        
        # Check environment and add FFmpeg to path if needed
        self._check_environment_paths()
        self._add_ffmpeg_to_path()
        self.instagram_username = instagram_username
        self.instagram_password = instagram_password
        
        # Load Instagram cookies if available
        self.instagram_cookies = load_cookies()
        
        # If we have credentials but no cookies, try to login
        if instagram_username and instagram_password and not self.instagram_cookies:
            login_and_get_cookies(instagram_username, instagram_password)
            self.instagram_cookies = load_cookies()

        if self.instagram_cookies:
            print(f"Instagram cookies loaded: {len(self.instagram_cookies)} cookies found")
            print(f"Cookie names: {[cookie['name'] for cookie in self.instagram_cookies]}")
        else:
            print("No Instagram cookies found")

    def _load_mock_data(self) -> Dict:
        """Load mock data from api_responses.json"""
        mock_data_path = Path(__file__).parent.parent.parent / 'mock_data' / 'api_responses.json'
        print(f"Loading mock data from: {mock_data_path}")
        with open(mock_data_path, 'r') as f:
            return json.load(f)

    async def process_url(self, url: str) -> Dict:
        """Main entry point - processes any URL and returns locations"""
        if "youtube.com" in url or "youtu.be" in url:
            return await self.extract_from_youtube(url)
        elif "instagram.com" in url or "instagr.am" in url:
            return await self.extract_from_instagram(url)
        else:
            return await self.extract_from_web(url)

    async def extract_from_youtube(self, url: str) -> Dict:
        """Extract locations from YouTube video"""
        video_id = self._extract_video_id(url)
        if not video_id:
            return self._create_error_response(url, "Invalid YouTube URL")

        try:
            print(f"Extracting transcript for video ID: {video_id}")
            # Get video transcript
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                full_text = " ".join([entry['text'] for entry in transcript_list])
            except Exception as e:
                print(f"Error getting transcript: {str(e)}")
                return self._create_error_response(url, f"Failed to get video transcript: {str(e)}")
            
            print("Successfully extracted transcript")
            
            # Get video metadata
            try:
                video_info = self.youtube.videos().list(
                    part="snippet",
                    id=video_id
                ).execute()

                if 'items' in video_info and video_info['items']:
                    video_title = video_info['items'][0]['snippet']['title']
                    timestamp = video_info['items'][0]['snippet']['publishedAt']
                else:
                    video_title = "Unknown Title"
                    timestamp = ""
            except Exception as e:
                print(f"Error getting video metadata: {str(e)}")
                video_title = "Unknown Title"
                timestamp = ""

            print(f"Processing video content with title: {video_title}")
            
            # Process with LLM
            locations = await self._process_with_llm(full_text)
            
            return self._format_response(
                url=url,
                locations=locations,
                source_type="youtube",
                title=video_title,
                timestamp=timestamp
            )

        except Exception as e:
            print(f"Error processing YouTube video: {str(e)}")
            return self._create_error_response(url, str(e))

    async def extract_from_web(self, url: str) -> Dict:
        """Extract locations from web content"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract title and timestamp if available
            title = soup.title.string if soup.title else "Unknown Title"
            timestamp = soup.find('meta', {'property': 'article:published_time'})
            timestamp = timestamp['content'] if timestamp else ""

            # Extract main content
            content = ""
            for container in ['article', 'main', '.post-content', '.entry-content']:
                if content_elem := soup.select_one(container):
                    content = content_elem.get_text()
                    break
            
            if not content:
                # Fallback to all paragraphs
                content = " ".join([p.get_text() for p in soup.find_all('p')])

            # Process with LLM
            locations = await self._process_with_llm(content)
            
            return {
                "extracted_locations": {
                    "success": True,
                    "url": url,
                    "locations": locations
                },
                "duplicate_check": {
                    "success": True,
                    "duplicates": []  # Implement duplicate checking logic if needed
                },
                "place_details": {
                    "success": True,
                    "place_id": locations[0]["id"] if locations else None,
                    "updated_fields": {}  # Implement updated fields logic if needed
                }
            }

        except Exception as e:
            print(f"Error processing URL {url}: {str(e)}")
            return {
                "extracted_locations": {
                    "success": False,
                    "url": url,
                    "locations": [],
                    "error": str(e)
                },
                "duplicate_check": {"success": False, "duplicates": []},
                "place_details": {"success": False, "place_id": None, "updated_fields": {}}
            }

    async def _process_with_llm(self, text: str) -> List[Dict]:
        """Process text with Azure OpenAI to extract locations"""
        prompt = """
        You are an expert at extracting locations from text content. I'll provide you with text extracted from an Instagram post or reel which may include:
        
        1. POST DESCRIPTION: The caption or description of the Instagram post
        2. AUDIO TRANSCRIPTION: A transcription of any spoken words from the video (marked with "AUDIO TRANSCRIPTION:" prefix)
        3. Other metadata from Instagram
        
        Your task is to identify ALL travel-related locations mentioned in BOTH the description AND the audio transcription. Locations might be mentioned in either source or both.

        Please analyze ALL the text carefully and extract ALL locations mentioned, including:
        - The exact name of the location (e.g., "Eiffel Tower", "Paris", "Le Jules Verne Restaurant")
        - The type/category of the location (e.g., monument, city, restaurant, park, beach, etc.)
        - Any details about the location (address, opening hours, etc.)
        - Any context provided about the location
        
        Be thorough and look for locations in all parts of the provided text.

        Format your response as a JSON array of location objects with these fields:
        - name: The name of the location
        - type: The category or type of the location
        - details: Any specific details about the location (address, opening times, etc.)
        - context: Any additional context about the location from the content
        - source: Where you found this location - must be one of: "description", "audio", or "both"

        Here's the text to analyze:
        {text}
        """

        try:
            # Debug API key (don't log the full key for security reasons)
            api_key = self.openai_api_key
            if api_key:
                print(f"API key found: {api_key[:4]}...{api_key[-4:] if len(api_key) > 8 else '***'}")
            else:
                print("WARNING: API key is empty or None")
                return await self._extract_locations_fallback(text)
            
            # Create Azure OpenAI client
            try:
                client = openai.AzureOpenAI(
                    api_key=api_key,
                    api_version=self.api_version,
                    azure_endpoint=self.base_url
                )
                print("Azure OpenAI client created successfully")
            except Exception as client_error:
                print(f"Error creating Azure OpenAI client: {str(client_error)}")
                return await self._extract_locations_fallback(text)
                
            # Make Azure API call
            response = client.chat.completions.create(
                model=self.model_name,  # This should be the deployment name
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that extracts location information from text and returns it in JSON format.",
                    },
                    {
                        "role": "user",
                        "content": prompt.format(text=text[:8000]),
                    }
                ],
                temperature=0.3,
                response_format={"type": "json_object"},
                max_tokens=2000,
            )
            
            # Log the API response
            print(f"Received response from Azure OpenAI API")
            
            # Process the response
            try:
                content = response.choices[0].message.content.strip()
                print(f"\nReceived raw content of length: {len(content)}")
                
                # Parse the JSON
                parsed_content = json.loads(content)
                
                # Extract the locations array - handle both formats:
                # 1. {"locations": [...]} 
                # 2. Direct array of locations
                if isinstance(parsed_content, dict) and "locations" in parsed_content:
                    locations = parsed_content["locations"]
                else:
                    locations = parsed_content
                    
                print(f"Successfully extracted {len(locations)} locations")
                return self._format_locations(locations)
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {str(e)}")
                print(f"Failed content: {content[:200]}...")  # Print first 200 chars
                return await self._extract_locations_fallback(text)
                
        except Exception as e:
            print(f"Error with Azure OpenAI API call: {str(e)}")
            # Use the fallback method when API call fails
            return await self._extract_locations_fallback(text)

    def _format_locations(self, locations: List[Dict]) -> List[Dict]:
        """Format the locations according to the API spec"""
        formatted_locations = []
        for idx, loc in enumerate(locations):
            if isinstance(loc, dict):  # Ensure loc is a dictionary
                try:
                    formatted_loc = {
                        "id": f"loc{idx + 1}",
                        "name": loc.get("name", "Unknown Location"),
                        "category": loc.get("type", "point_of_interest"),
                        "description": f"{loc.get('details', '')} {loc.get('context', '')}".strip(),
                        "coordinates": {"lat": None, "lng": None},
                        "tags": [loc.get("type", "travel")] if loc.get("type") else ["travel"]
                    }
                    formatted_locations.append(formatted_loc)
                except Exception as e:
                    print(f"Error formatting location {idx}: {str(e)}")
                    print(f"Location data: {loc}")
                    continue
            else:
                print(f"Skipping non-dictionary location at index {idx}: {loc}")
                
        return formatted_locations

    def _extract_video_id(self, url: str) -> str:
        """Extract YouTube video ID from URL"""
        parsed_url = urllib.parse.urlparse(url)
        if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
            query_params = urllib.parse.parse_qs(parsed_url.query)
            return query_params.get('v', [None])[0]
        elif parsed_url.hostname == 'youtu.be':
            return parsed_url.path[1:]
        return None

    def _format_response(self, url: str, locations: List[Dict], 
                        source_type: str, title: str, timestamp: str) -> Dict:
        """Format the final API response"""
        return {
            "extracted_locations": {
                "success": True,
                "url": url,
                "locations": locations
            },
            "duplicate_check": {
                "success": True,
                "duplicates": []
            },
            "place_details": {
                "success": True,
                "place_id": locations[0]["id"] if locations else None,
                "updated_fields": {}
            }
        }

    def _create_error_response(self, url: str, error_message: str) -> Dict:
        """Create error response"""
        return {
            "extracted_locations": {
                "success": False,
                "url": url,
                "locations": [],
                "error": error_message
            },
            "duplicate_check": {"success": False, "duplicates": []},
            "place_details": {"success": False, "place_id": None, "updated_fields": {}}
        }

    async def extract_from_instagram(self, url: str) -> Dict:
        """Extract locations from Instagram post or reel"""
        try:
            print(f"Processing Instagram URL: {url}")
            
            # Clean URL if it has quotes
            if url.startswith('"') and url.endswith('"'):
                url = url[1:-1]
                print(f"Cleaned URL: {url}")
            
            # Extract Instagram content type and ID
            content_type, content_id = self._extract_instagram_id(url)
            if not content_id:
                print(f"Failed to extract content ID from {url}")
                return self._create_error_response(url, "Invalid Instagram URL - could not extract content ID")
            
            print(f"Instagram content type: {content_type}, ID: {content_id}")
            
            # Get Instagram content text
            content = await self._extract_instagram_content(url)
            
            # For reels, try to get audio transcription using instaloader
            if content_type == 'reel' or '/reel/' in url:
                try:
                    audio_content = await self._extract_instagram_with_instaloader(url)
                    if audio_content and len(audio_content) > 10:
                        content += "\n\nAUDIO TRANSCRIPTION: " + audio_content
                        print(f"Successfully added audio transcription from instaloader")
                except Exception as e:
                    print(f"Error using instaloader for audio: {str(e)}")
            
            content_length = len(content)
            print(f"Content extracted with {content_length} characters")
            
            # Process with LLM
            locations = await self._process_with_llm(content)
            
            # If no locations found and we have minimal content, create a special response
            if not locations and content_length < 100:
                return {
                    "extracted_locations": {
                        "success": True,
                        "url": url,
                        "locations": [],
                        "note": "Limited content extracted from Instagram. Please provide additional information about this post for better location extraction."
                    },
                    "duplicate_check": {"success": True, "duplicates": []},
                    "place_details": {"success": False, "place_id": None, "updated_fields": {}}
                }
            
            return self._format_response(
                url=url,
                locations=locations,
                source_type="instagram",
                title=f"Instagram {content_type}",
                timestamp=""
            )
            
        except Exception as e:
            print(f"Error processing Instagram content: {str(e)}")
            import traceback
            traceback.print_exc()  # Print full exception traceback for debugging
            return self._create_error_response(url, str(e))

    def _extract_instagram_id(self, url: str) -> tuple:
        """Extract Instagram content type and ID from URL"""
        try:
            # Remove any quotes that might have been added
            if url.startswith('"') and url.endswith('"'):
                url = url[1:-1]
            
            parsed_url = urllib.parse.urlparse(url)
            path_parts = parsed_url.path.strip('/').split('/')
            
            content_type = None
            content_id = None
            
            if len(path_parts) >= 2:
                if path_parts[0] == 'p':
                    content_type = 'post'
                    content_id = path_parts[1]
                elif path_parts[0] == 'reel':
                    content_type = 'reel'
                    content_id = path_parts[1]
                elif path_parts[0] == 'tv':
                    content_type = 'tv'
                    content_id = path_parts[1]
            
            # If we couldn't extract an ID, try a different approach for URLs with parameters
            if not content_id and '/reel/' in url:
                # Extract ID from URLs like instagram.com/reel/ABCDEFG/?param=value
                match = re.search(r'/reel/([^/?]+)', url)
                if match:
                    content_type = 'reel'
                    content_id = match.group(1)
            
            print(f"Extracted Instagram ID: {content_id}, type: {content_type}")
            return content_type, content_id
        
        except Exception as e:
            print(f"Error extracting Instagram ID: {str(e)}")
            return None, None

    async def _extract_instagram_content(self, url: str) -> str:
        """Extract all available text content from Instagram post or reel"""
        try:
            # Use a random user agent
            headers = {
                'User-Agent': self._get_random_user_agent(),
                'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ja;q=0.6',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Referer': 'https://www.instagram.com/',
                'Origin': 'https://www.instagram.com',
                'Connection': 'keep-alive',
                'sec-ch-ua': '"Chromium";v="96", "Google Chrome";v="96"',
                'sec-ch-ua-platform': '"Windows"',
                'sec-ch-ua-mobile': '?0',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0'
            }
            
            # Use cookies in request headers
            if self.instagram_cookies:
                headers.update(cookies_to_header(self.instagram_cookies))
            
            # Try multiple fetching methods
            all_content = []
            success = False
            
            # Method 1: Direct fetch
            print(f"Method 1: Direct fetch from URL: {url}")
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract meta tags content
                for meta in soup.find_all('meta'):
                    if 'content' in meta.attrs and meta.attrs.get('content', '').strip():
                        if meta.attrs.get('name') in ['description', 'keywords'] or meta.attrs.get('property') in ['og:description', 'og:title']:
                            all_content.append(meta.attrs['content'])
                
                # Extract text from various HTML elements
                for tag in soup.find_all(['p', 'div', 'span', 'h1', 'h2', 'h3', 'article']):
                    text = tag.get_text().strip()
                    if len(text) > 10:  # Consider elements with at least some text
                        all_content.append(text)
                
                # Look for specific Instagram content elements
                for script in soup.find_all('script', {'type': 'application/ld+json'}):
                    if script.string:
                        try:
                            json_data = json.loads(script.string)
                            if isinstance(json_data, dict):
                                for key, value in json_data.items():
                                    if isinstance(value, str) and len(value) > 10:
                                        all_content.append(f"{key}: {value}")
                        except json.JSONDecodeError:
                            all_content.append(script.string)
                
                # Look for any JSON data in the page
                for script in soup.find_all('script'):
                    if script.string and ('_sharedData' in script.string or 'window.__additionalDataLoaded' in script.string):
                        all_content.append(script.string)
                
                # Check if we got any content
                if all_content:
                    success = True
                    print(f"Method 1 succeeded: Extracted {len(all_content)} content blocks")
                else:
                    print("Method 1 failed: No content extracted")
                    
            except Exception as e:
                print(f"Method 1 failed with error: {str(e)}")
            
            # Method 2: Try with a different URL format (for reels)
            if not success and 'reel' in url:
                try:
                    print("Method 2: Trying with modified URL format for reels")
                    # Extract content ID
                    content_type, content_id = self._extract_instagram_id(url)
                    if content_id:
                        alternate_url = f"https://www.instagram.com/p/{content_id}/"
                        response = requests.get(alternate_url, headers=headers, timeout=10)
                        response.raise_for_status()
                        
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Same extraction as above
                        for meta in soup.find_all('meta'):
                            if 'content' in meta.attrs and meta.attrs.get('content', '').strip():
                                if meta.attrs.get('name') in ['description', 'keywords'] or meta.attrs.get('property') in ['og:description', 'og:title']:
                                    all_content.append(meta.attrs['content'])
                        
                        # Check if we got any content
                        if all_content:
                            success = True
                            print(f"Method 2 succeeded: Extracted {len(all_content)} content blocks")
                        else:
                            print("Method 2 failed: No content extracted")
                except Exception as e:
                    print(f"Method 2 failed with error: {str(e)}")
            
            # If all extraction methods failed, create fallback content
            if not all_content:
                # Create a fallback text that includes the URL and content type
                content_type, content_id = self._extract_instagram_id(url)
                fallback_text = f"Instagram {content_type} with ID {content_id} at URL {url}. Unable to extract detailed content due to access restrictions. Please provide any additional information you know about this content for better location extraction."
                all_content.append(fallback_text)
                print("Using fallback content due to extraction failure")
            
            # Add audio transcription for reels
            if 'reel' in url or '/reel/' in url:
                try:
                    print("Attempting to extract and transcribe audio from reel...")
                    audio_content = await self._extract_and_transcribe_reel_audio(url)
                    if audio_content and len(audio_content) > 10:  # Only add non-empty transcriptions
                        all_content.append("AUDIO TRANSCRIPTION: " + audio_content)
                        print(f"Successfully added audio transcription ({len(audio_content)} chars)")
                    else:
                        print("Audio transcription failed or returned empty content")
                        # Try fallback method if first method failed
                        try:
                            try:
                                from instagram_downloader import download_instagram_video
                            except ImportError:
                                # Fallback to absolute import if relative fails
                                import sys
                                import os
                                sys.path.append(os.path.dirname(os.path.abspath(__file__)))
                                from instagram_downloader import download_instagram_video
                            
                            with tempfile.TemporaryDirectory() as temp_dir:
                                video_path = os.path.join(temp_dir, "instagram_video.mp4")
                                audio_path = os.path.join(temp_dir, "audio.mp3")
                                
                                print("Trying fallback download method...")
                                downloaded = download_instagram_video(url, video_path)
                                
                                if downloaded and os.path.exists(video_path):
                                    print("Successfully downloaded with fallback method")
                                    
                                    # Try to extract audio with ffmpeg if available
                                    try:
                                        print("Extracting audio...")
                                        subprocess.run(["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_path], 
                                                       check=True, timeout=30, capture_output=True)
                                                        
                                        if os.path.exists(audio_path):
                                            print("Successfully extracted audio")
                                            
                                            # Transcribe with OpenAI
                                            client = openai.AzureOpenAI(
                                                api_key=self.openai_api_key,
                                                api_version=self.api_version,
                                                azure_endpoint=self.base_url
                                            )
                                            
                                            transcript = client.audio.transcriptions.create(
                                                model="whisper-1",
                                                file=open(audio_path, "rb")
                                            )
                                            
                                            fallback_audio_content = transcript.text
                                            if fallback_audio_content:
                                                all_content.append("AUDIO TRANSCRIPTION: " + fallback_audio_content)
                                                print(f"Successfully added audio transcription with fallback method")
                                    except Exception as e:
                                        print(f"Fallback audio extraction failed: {str(e)}")
                
                        except ImportError:
                            print("Fallback method unavailable - instagram_downloader module not found")
                        except Exception as e:
                            print(f"Fallback audio transcription failed: {str(e)}")
                except Exception as e:
                    print(f"Audio transcription failed: {str(e)}")
            
            # Format the extracted content more clearly
            formatted_content = []
            
            # Add description if we have one
            description_content = [c for c in all_content if len(c) < 1000 and not c.startswith("AUDIO TRANSCRIPTION:")]
            if description_content:
                formatted_content.append("POST DESCRIPTION:")
                formatted_content.extend(description_content[:3])  # Limit to first few content blocks for clarity
            
            # Add audio transcription if available
            audio_blocks = [c for c in all_content if c.startswith("AUDIO TRANSCRIPTION:")]
            if audio_blocks:
                formatted_content.extend(audio_blocks)
            
            # Combine all content
            combined_text = "\n\n".join(formatted_content)
            print(f"Total formatted content length: {len(combined_text)} characters")
            print("Content includes description and audio transcription" if "AUDIO TRANSCRIPTION:" in combined_text else "Content only includes description")
            
            return combined_text
            
        except Exception as e:
            print(f"Error in Instagram content extraction: {str(e)}")
            # Return minimal information that can be used by LLM
            content_type, content_id = self._extract_instagram_id(url)
            return f"Instagram {content_type} with ID {content_id} at URL {url}. Content extraction failed with error: {str(e)}"

    async def _extract_and_transcribe_reel_audio(self, url: str) -> str:
        """Extract audio from Instagram reel and transcribe it"""
        try:
            # Step 1: Get the content ID from the URL
            content_type, content_id = self._extract_instagram_id(url)
            if not content_id:
                print("Could not extract content ID from URL")
                return ""
            
            print(f"Attempting audio extraction for {content_type} with ID: {content_id}")
            
            import subprocess
            import tempfile
            import os
            import sys
            
            # Check if yt-dlp is installed by trying to import it first
            try:
                import yt_dlp
                print("yt-dlp is installed as a Python package")
                has_yt_dlp_module = True
            except ImportError:
                has_yt_dlp_module = False
                print("yt-dlp Python module not found, will try as command line tool")
            
            # If module import failed, try checking if it's available as a command
            try:
                yt_dlp_cmd = getattr(self, 'yt_dlp_path', "yt-dlp")
                subprocess.run([yt_dlp_cmd, "--version"], check=True, capture_output=True)
                print("yt-dlp command line tool is available")
                has_yt_dlp_cmd = True
            except (subprocess.SubprocessError, FileNotFoundError):
                has_yt_dlp_cmd = False
                print("yt-dlp command line tool not found")
            
            if not (has_yt_dlp_module or has_yt_dlp_cmd):
                print("yt-dlp not found. Please install it with: pip install yt-dlp")
                # For now, return a placeholder message since yt-dlp is missing
                return "Audio transcription failed: yt-dlp not installed"
            
            with tempfile.TemporaryDirectory() as temp_dir:
                # Create output filename with the content ID to ensure uniqueness
                output_path = os.path.join(temp_dir, f"{content_id}")
                audio_path = os.path.join(temp_dir, f"{content_id}.mp3")
                
                # Clean URL - remove any quotes
                clean_url = url
                if clean_url.startswith('"') and clean_url.endswith('"'):
                    clean_url = clean_url[1:-1]
                
                print(f"Downloading from URL: {clean_url}")
                
                # Try downloading with Python API if available, fallback to command line
                downloaded_file = None
                
                if has_yt_dlp_module:
                    try:
                        # Instead of using browser cookies, use your loaded cookies in a cookie file
                        cookies_path = os.path.join(temp_dir, "instagram_cookies.txt")
                        
                        # Convert your JSON cookies to Netscape format for yt-dlp
                        with open(cookies_path, 'w') as f:
                            for cookie in self.instagram_cookies:
                                domain = cookie.get('domain', '.instagram.com')
                                path = cookie.get('path', '/')
                                secure = 'TRUE' if cookie.get('secure', True) else 'FALSE'
                                expiry = str(int(cookie.get('expirationDate', 0)))
                                name = cookie.get('name', '')
                                value = cookie.get('value', '')
                                
                                f.write(f"{domain}\tTRUE\t{path}\t{secure}\t{expiry}\t{name}\t{value}\n")
                        
                        # Use the cookie file instead of browser cookies
                        ydl_opts = {
                            'format': 'bestaudio/best',
                            'outtmpl': output_path,
                            'quiet': False,
                            'verbose': True,
                            'cookies': cookies_path,  # Use generated cookie file instead
                        }
                        
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(clean_url, download=True)
                            if info:
                                downloaded_file = ydl.prepare_filename(info)
                                print(f"Successfully downloaded to: {downloaded_file}")
                    except Exception as e:
                        print(f"Python module download failed: {str(e)}")
                
                # If Python module download failed, try command line
                if not downloaded_file and has_yt_dlp_cmd:
                    try:
                        # If we have credentials, pass them to yt-dlp
                        if self.instagram_username and self.instagram_password:
                            download_cmd = [
                                yt_dlp_cmd,
                                "--username", self.instagram_username,
                                "--password", self.instagram_password,
                                "--verbose",
                                "-o", output_path,
                                clean_url
                            ]
                        else:
                            download_cmd = [
                                yt_dlp_cmd,
                                "--verbose",
                                "-o", output_path,
                                clean_url
                            ]
                        
                        # Download video
                        print("Trying download with command line yt-dlp...")
                        result = subprocess.run(download_cmd, check=True, timeout=60, capture_output=True)
                        stdout = result.stdout.decode() if result.stdout else "No output"
                        print(f"Download output: {stdout[:200]}...")  # Print first 200 chars
                        
                        # Look for downloaded file
                        downloaded_files = [f for f in os.listdir(temp_dir) if os.path.isfile(os.path.join(temp_dir, f))]
                        print(f"Files in temp directory: {downloaded_files}")
                        
                        if downloaded_files:
                            for f in downloaded_files:
                                if content_id in f and not f.endswith('.mp3'):
                                    downloaded_file = os.path.join(temp_dir, f)
                                    print(f"Found downloaded file: {downloaded_file}")
                                    break
                    except Exception as e:
                        print(f"Command line download failed: {str(e)}")
                
                # Check if download was successful
                if not downloaded_file or not os.path.exists(downloaded_file):
                    print("Failed to download the video")
                    return "Audio transcription failed: could not download the video"
                
                # Extract audio using ffmpeg
                print("Extracting audio using ffmpeg...")
                try:
                    # Try with installed ffmpeg
                    subprocess.run(
                        ["ffmpeg", "-i", downloaded_file, "-q:a", "0", "-map", "a", audio_path],
                        check=True, timeout=30, capture_output=True
                    )
                except (subprocess.SubprocessError, FileNotFoundError):
                    print("Failed to use ffmpeg directly, trying to extract audio with yt-dlp...")
                    
                    # Try using yt-dlp's built-in audio extraction
                    try:
                        subprocess.run(
                            ["yt-dlp", "--extract-audio", "--audio-format", "mp3", 
                             "--audio-quality", "0", "-o", audio_path, downloaded_file],
                            check=True, timeout=30, capture_output=True
                        )
                    except Exception as e:
                        print(f"Failed to extract audio: {str(e)}")
                        return "Audio transcription failed: could not extract audio"
                
                if not os.path.exists(audio_path):
                    print("Audio extraction failed - no audio file created")
                    return "Audio transcription failed: no audio file created"
                    
                print(f"Successfully extracted audio to: {audio_path}")
                
                # Step 3: Transcribe the audio using OpenAI Whisper
                print("Transcribing audio with Whisper API...")
                
                try:
                    # Use OpenAI Whisper API for transcription
                    client = openai.AzureOpenAI(
                        api_key=self.openai_api_key,
                        api_version=self.api_version,
                        azure_endpoint=self.base_url
                    )
                    
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=open(audio_path, "rb")
                    )
                    
                    transcript_text = transcript.text if hasattr(transcript, 'text') else str(transcript)
                    
                    if not transcript_text:
                        print("Transcription yielded empty result")
                        return "Audio transcription: No speech detected in audio"
                        
                    print(f"Successfully transcribed audio, length: {len(transcript_text)} characters")
                    return transcript_text
                except Exception as e:
                    print(f"Transcription error: {str(e)}")
                    return f"Audio transcription failed: {str(e)}"
                
        except Exception as e:
            print(f"Error in audio extraction/transcription: {str(e)}")
            import traceback
            traceback.print_exc()
            return "Audio transcription failed due to an error."

    def _get_random_user_agent(self) -> str:
        """Return a random user agent string to avoid detection"""
        user_agents = [
            # Mobile user agents
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
            'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
            'Mozilla/5.0 (Android 11; Mobile; rv:89.0) Gecko/89.0 Firefox/89.0',
            
            # Desktop user agents
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0'
        ]
        return random.choice(user_agents)

    def _check_environment_paths(self):
        """Check if necessary executables are in PATH"""
        import shutil
        import os
        import sys
        
        # Print current environment for debugging
        print(f"Python executable: {sys.executable}")
        print(f"Current PATH: {os.environ.get('PATH', '')}")
        
        # Check for yt-dlp
        yt_dlp_path = shutil.which("yt-dlp")
        ffmpeg_path = shutil.which("ffmpeg")
        
        # Try to find yt-dlp in the Python Scripts directory
        if not yt_dlp_path:
            python_path = sys.executable
            python_dir = os.path.dirname(python_path)
            possible_yt_dlp_paths = [
                os.path.join(python_dir, "Scripts", "yt-dlp.exe"),
                os.path.join(python_dir, "yt-dlp.exe"),
                os.path.join(os.path.dirname(python_dir), "Scripts", "yt-dlp.exe"),
                # For Microsoft Store Python
                os.path.join(os.path.expanduser("~"), "AppData", "Local", "Packages", 
                            "PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0", 
                            "LocalCache", "local-packages", "Python310", "Scripts", "yt-dlp.exe")
            ]
            
            for path in possible_yt_dlp_paths:
                if os.path.exists(path):
                    yt_dlp_path = path
                    print(f"Found yt-dlp at: {yt_dlp_path}")
                    # Store it for later use
                    self.yt_dlp_path = yt_dlp_path
                    break
        else:
            self.yt_dlp_path = yt_dlp_path
        
        print(f"yt-dlp found at: {yt_dlp_path}")
        print(f"ffmpeg found at: {ffmpeg_path}")
        
        # Return status of each tool
        return {
            "yt-dlp": yt_dlp_path is not None,
            "ffmpeg": ffmpeg_path is not None
        }

    def _add_ffmpeg_to_path(self):
        """Add ffmpeg to PATH temporarily during runtime"""
        import os
        import sys
        import platform
        
        system = platform.system()
        
        # Define custom FFmpeg paths for different operating systems
        custom_paths = {
            'Windows': ['C:\\ffmpeg\\bin', 'C:\\Program Files\\ffmpeg\\bin'],
            'Darwin': ['/usr/local/bin', '/opt/homebrew/bin'],  # macOS
            'Linux': ['/usr/local/bin', '/usr/bin']
        }
        
        if system in custom_paths:
            current_path = os.environ.get('PATH', '')
            for path in custom_paths[system]:
                if os.path.exists(path) and path not in current_path:
                    os.environ['PATH'] = path + os.pathsep + current_path
                    print(f"Added {path} to PATH")
                    
        # Check if ffmpeg is now in path
        import shutil
        ffmpeg_path = shutil.which("ffmpeg")
        print(f"FFmpeg path after adjustment: {ffmpeg_path}")
        
        return ffmpeg_path is not None

    async def _extract_instagram_with_instaloader(self, url: str) -> str:
        """Extract Instagram reel content using instaloader"""
        try:
            import instaloader
            import tempfile
            import os
            
            # Extract the shortcode/ID from URL
            content_type, content_id = self._extract_instagram_id(url)
            if not content_id:
                return ""
            
            # Create a temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                # Initialize instaloader
                L = instaloader.Instaloader(dirname_pattern=temp_dir)
                
                # Login (optional but recommended)
                if self.instagram_username and self.instagram_password:
                    try:
                        L.login(self.instagram_username, self.instagram_password)
                        print("Successfully logged in to Instagram")
                    except Exception as e:
                        print(f"Instagram login failed: {str(e)}")
                
                # Download the post
                try:
                    post = instaloader.Post.from_shortcode(L.context, content_id)
                    L.download_post(post, target=temp_dir)
                    
                    # Find the video file
                    video_files = [f for f in os.listdir(temp_dir) if f.endswith('.mp4')]
                    if not video_files:
                        return ""
                        
                    video_path = os.path.join(temp_dir, video_files[0])
                    print(f"Found video file: {video_path}")
                    
                    # Extract audio using FFmpeg
                    audio_path = os.path.join(temp_dir, "audio.mp3")
                    subprocess.run(
                        ["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_path],
                        check=True, timeout=30, capture_output=True
                    )
                    
                    # Transcribe the audio
                    if os.path.exists(audio_path):
                        with open(audio_path, "rb") as audio_file:
                            client = openai.AzureOpenAI(
                                api_key=self.openai_api_key,
                                api_version=self.api_version,
                                azure_endpoint=self.base_url
                            )
                            
                            transcript = client.audio.transcriptions.create(
                                model="whisper-1",
                                file=audio_file
                            )
                        return transcript.text
                    
                except Exception as e:
                    print(f"Error downloading post: {str(e)}")
                    return ""
                
        except ImportError:
            print("Instaloader not installed. Install with: pip install instaloader")
            return ""
        except Exception as e:
            print(f"Error using Instaloader: {str(e)}")
            return ""

    async def _extract_locations_fallback(self, text: str) -> List[Dict]:
        """Fallback method to extract locations when API call fails"""
        print("Using fallback location extraction method")
        
        # Use regex to try to find locations
        locations = []
        
        # Look for location patterns in the text
        import re
        
        # Add some common location patterns
        location_patterns = [
            # Look for "in [Location]" pattern
            r'(?:in|at|near|to|from|visit(?:ing|ed)?|travel(?:ing|ed)? to) ([A-Z][a-zA-Z\s]{2,}(?:, [A-Z][a-zA-Z\s]{2,})?)',
            
            # Location hashtags
            r'#([a-zA-Z]+[Tt]ravel|[a-zA-Z]+[Tt]rip|[a-zA-Z]+[Vv]acation)',
            
            # Locations with emojis
            r'📍 ([A-Za-z\s,]+)',
            r'📌 ([A-Za-z\s,]+)',
            r'🌍 ([A-Za-z\s,]+)',
            r'🌎 ([A-Za-z\s,]+)',
            r'🏝️ ([A-Za-z\s,]+)',
            r'🏙️ ([A-Za-z\s,]+)',
        ]
        
        found_locations = set()
        for pattern in location_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple):  # If the match contains groups
                    for group in match:
                        if group and len(group) > 3 and group not in found_locations:
                            found_locations.add(group)
                elif match and len(match) > 3 and match not in found_locations:
                    found_locations.add(match)
        
        # Create location objects from matches
        for idx, loc_name in enumerate(found_locations):
            locations.append({
                "name": loc_name,
                "type": "place",
                "details": "",
                "context": f"Found in content using pattern matching",
                "source": "description"  # Default to description since it's more reliable
            })
        
        print(f"Fallback method found {len(locations)} potential locations")
        return self._format_locations(locations)

    def _verify_azure_credentials(self):
        """Verify Azure OpenAI API credentials"""
        try:
            print("Verifying Azure OpenAI credentials...")
            
            # Create Azure OpenAI client
            client = openai.AzureOpenAI(
                api_key=self.openai_api_key,
                api_version=self.api_version,
                azure_endpoint=self.base_url
            )
            
            # First try listing deployments (works on newer SDKs)
            try:
                deployments = client.deployments.list()
                print(f"Azure OpenAI credentials verified. Available deployments: {len(deployments.data)}")
                return True
            except (AttributeError, NotImplementedError):
                # If deployments list not available, try a minimal completion
                try:
                    response = client.chat.completions.create(
                        model=self.model_name,
                        messages=[{"role": "user", "content": "Test"}],
                        max_tokens=5
                    )
                    print("Azure OpenAI credentials verified with test completion.")
                    return True
                except Exception as e:
                    print(f"Azure OpenAI test completion failed: {str(e)}")
                    return False
            
        except Exception as e:
            print(f"Azure OpenAI credential verification failed: {str(e)}")
            print("Please check your Azure OpenAI key and endpoint configuration.")
            return False