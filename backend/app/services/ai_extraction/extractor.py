from typing import List, Dict
import re
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import urllib.parse
from dotenv import load_dotenv
import json
import os
from pathlib import Path

load_dotenv()

class LocationExtractor:
    def __init__(self, youtube_api_key: str = None, github_api_key: str = None, mock_data_path=None):
        self.youtube = build('youtube', 'v3', developerKey=youtube_api_key) if youtube_api_key else None
        self.github_api_key = github_api_key
        self.endpoint = "https://models.inference.ai.azure.com"
        self.model_name = "gpt-4o-mini"
        self.mock_data_path = mock_data_path
        self.mock_data = self._load_mock_data()

    def _load_mock_data(self) -> Dict:
        """Load mock data from api_responses.json"""
        if self.mock_data_path:
            with open(self.mock_data_path, 'r') as f:
                return json.load(f)
        mock_data_path = Path(__file__).parent.parent.parent / 'mock_data' / 'api_responses.json'
        print(f"Loading mock data from: {mock_data_path}")
        with open(mock_data_path, 'r') as f:
            return json.load(f)

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
            if self.mock_data_path:
                with open(self.mock_data_path, 'r') as f:
                    return json.load(f)
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
        """Process text with GitHub's LLM to extract locations"""
        headers = {
            "Authorization": f"Bearer {self.github_api_key}",
            "Content-Type": "application/json"
        }

        prompt = """
        Extract travel-related locations from the following text and provide the information in JSON format. Include details such as the name, type, details, and context of each location.

        Text: {text}
        """

        try:
            payload = {
                "model": self.model_name,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a JSON response bot. Provide the information in JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt.format(text=text[:4000])
                    }
                ],
                "temperature": 0.1
            }

            response = requests.post(
                f"{self.endpoint}/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Log the full response object
            print(f"Full API response object: {result}")
            
            try:
                content = result['choices'][0]['message']['content'].strip()
                print(f"\nRaw content: {content}")
                
                # Attempt to parse the JSON
                locations = json.loads(content)
                return self._format_locations(locations)
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error processing response: {str(e)}")
                return []
                
        except Exception as e:
            print(f"LLM processing error: {str(e)}")
            print(f"Full error details: {repr(e)}")
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