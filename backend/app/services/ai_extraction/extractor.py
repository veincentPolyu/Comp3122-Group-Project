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



load_dotenv()

class LocationExtractor:
    def __init__(self, youtube_api_key: str, openai_api_key: str):
        self.youtube = build('youtube', 'v3', developerKey=youtube_api_key)
        openai.api_key = openai_api_key  # Set the API key
        self.base_url = "https://models.inference.ai.azure.com"
        # Load mock data
        self.mock_data = self._load_mock_data()

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
        """Process text with GPT to extract locations"""
        prompt = """
        You are an expert at extracting locations from text content. I'll provide you with text extracted from a webpage, social media post, or video transcript, and your task is to identify all travel-related locations mentioned in it.

        The text may contain content in multiple languages including English, Chinese, Japanese, or others. It may also include raw JSON data or HTML fragments - try to extract meaningful location information from all of it.

        Please analyze the text carefully and extract ALL locations mentioned, including:
        - The exact name of the location
        - The type/category of the location (e.g., temple, park, restaurant, city, attraction)
        - Any details about the location (address, opening hours, etc.)
        - Any context provided about the location

        Format your response as a JSON array of location objects with these fields:
        - name: The name of the location
        - type: The category or type of the location
        - details: Any specific details about the location (address, opening times, etc.)
        - context: Any additional context about the location from the content

        Here's the text to analyze:
        {text}
        """

        try:
            model_name = "gpt-4o-mini"
            client = openai.OpenAI(
                base_url=self.base_url,
                api_key=openai.api_key,
            )
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that extracts location information from text and returns it in JSON format.",
                    },
                    {
                        "role": "user",
                        "content": prompt.format(text=text[:8000]),  # Expand to 8000 chars to include more content
                    }
                ],
                temperature=0.3,  # Lower temperature for more reliable extraction
                response_format={"type": "json_object"},  # Request JSON format specifically
                max_tokens=2000,
                model=model_name,
            )
            
            # Log the API response
            print(f"Received response from LLM API")
            
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
                return []
                
        except Exception as e:
            print(f"Error with LLM API call: {str(e)}")
            return []

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
            
            # Extract Instagram content type and ID
            content_type, content_id = self._extract_instagram_id(url)
            if not content_id:
                return self._create_error_response(url, "Invalid Instagram URL")
            
            print(f"Instagram content type: {content_type}, ID: {content_id}")
            
            # Get Instagram content
            content = await self._extract_instagram_content(url)
            if not content:
                print("No content extracted from Instagram, using minimal information")
                # Use minimal information for processing
                content = f"Instagram {content_type} with ID {content_id} at URL {url}."
            
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
            return self._create_error_response(url, str(e))

    def _extract_instagram_id(self, url: str) -> tuple:
        """Extract Instagram content type and ID from URL"""
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
        
        return content_type, content_id

    async def _extract_instagram_content(self, url: str) -> str:
        """Extract all available text content from Instagram post or reel using multiple techniques"""
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
            
            # Combine all content and log
            combined_text = "\n\n".join(all_content)
            print(f"Total extracted content length: {len(combined_text)} characters")
            
            return combined_text
            
        except Exception as e:
            print(f"Error in Instagram content extraction: {str(e)}")
            # Return minimal information that can be used by LLM
            content_type, content_id = self._extract_instagram_id(url)
            return f"Instagram {content_type} with ID {content_id} at URL {url}. Content extraction failed with error: {str(e)}"

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