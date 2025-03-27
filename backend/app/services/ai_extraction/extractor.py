from typing import List, Dict
import re
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from openai import OpenAI  # Updated import
from youtube_transcript_api import YouTubeTranscriptApi
import urllib.parse
from dotenv import load_dotenv

load_dotenv()  # Add this at the top of the file

class LocationExtractor:
    def __init__(self, youtube_api_key: str, openai_api_key: str):
        self.youtube = build('youtube', 'v3', developerKey=youtube_api_key)
        self.client = OpenAI(api_key=openai_api_key)  # Updated OpenAI client initialization

    async def process_url(self, url: str) -> Dict:
        """Main entry point - processes any URL and returns locations"""
        if "youtube.com" in url or "youtu.be" in url:
            return await self.extract_from_youtube(url)
        else:
            return await self.extract_from_web(url)

    async def extract_from_youtube(self, url: str) -> Dict:
        """Extract locations from YouTube video"""
        video_id = self._extract_video_id(url)
        if not video_id:
            return self._create_error_response(url, "Invalid YouTube URL")

        try:
            # Get video transcript
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            full_text = " ".join([entry['text'] for entry in transcript_list])
            
            # Get video metadata
            video_info = self.youtube.videos().list(
                part="snippet",
                id=video_id
            ).execute()

            if 'items' in video_info:
                video_title = video_info['items'][0]['snippet']['title']
                timestamp = video_info['items'][0]['snippet']['publishedAt']
            else:
                video_title = "Unknown Title"
                timestamp = ""

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
            # Try different common content containers
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
            
            return self._format_response(
                url=url,
                locations=locations,
                source_type="blog",
                title=title,
                timestamp=timestamp
            )

        except Exception as e:
            return self._create_error_response(url, str(e))

    async def _process_with_llm(self, text: str) -> List[Dict]:
        """Process text with GPT to extract locations"""
        prompt = """
        Extract travel-related locations from the following text. For each location, provide:
        1. The full name of the location
        2. The type of location (city, restaurant, landmark, etc.)
        3. Any mentioned details about the location
        4. Any context about why someone might visit

        Format the response as a JSON array of locations.
        
        Text to analyze:
        {text}
        """

        try:
            # Changed model from "gpt-4" to "gpt-3.5-turbo"
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a travel location extraction specialist."},
                    {"role": "user", "content": prompt.format(text=text[:4000])}  # Limit text length
                ]
            )
            
            locations = self._parse_gpt_response(response.choices[0].message.content)
            return locations

        except Exception as e:
            print(f"LLM processing error: {str(e)}")
            return []

    def _parse_gpt_response(self, gpt_response: str) -> List[Dict]:
        """Parse GPT response into structured location data"""
        try:
            # Assuming GPT returns JSON-formatted string
            import json
            locations = json.loads(gpt_response)
            
            # Format each location according to our API spec
            formatted_locations = []
            for idx, loc in enumerate(locations):
                formatted_loc = {
                    "id": f"loc{idx + 1}",
                    "name": loc.get("name", ""),
                    "category": loc.get("type", "point_of_interest"),
                    "description": loc.get("details", ""),
                    "coordinates": {"lat": None, "lng": None},  # Would need geocoding
                    "tags": [loc.get("type", "travel")] if loc.get("type") else ["travel"]
                }
                formatted_locations.append(formatted_loc)
            
            return formatted_locations

        except Exception as e:
            print(f"GPT response parsing error: {str(e)}")
            return []

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
                "duplicates": []  # Would need implementation
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