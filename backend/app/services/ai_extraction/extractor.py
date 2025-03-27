from typing import List, Dict
import re
import requests
from googleapiclient.discovery import build
from bs4 import BeautifulSoup

class LocationExtractor:
    def __init__(self, youtube_api_key: str):
        self.youtube = build('youtube', 'v3', developerKey=youtube_api_key)

    async def extract_from_youtube(self, video_id: str) -> List[Dict]:
        captions = await self._get_video_captions(video_id)
        if not captions.get('items'):
            return []

        # Extract text from the captions
        caption_texts = []
        for item in captions['items']:
            caption_id = item['id']
            caption_details = await self._get_caption_details(video_id, caption_id)
            caption_texts.append(caption_details.get('body', ''))

        # Combine all captions into a single string
        full_text = ' '.join(caption_texts)

        # Extract locations from the full text
        locations = self._extract_locations_from_text(full_text)
        return locations

    async def extract_from_blog(self, url: str) -> List[Dict]:
        response = requests.get(url)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, 'html.parser')

        # Assuming blog content is within <p> tags
        paragraphs = soup.find_all('p')
        blog_text = ' '.join([p.get_text() for p in paragraphs])

        # Extract locations from the blog text
        locations = self._extract_locations_from_text(blog_text)
        return locations

    async def _get_video_captions(self, video_id: str):
        request = self.youtube.captions().list(
            part="snippet",
            videoId=video_id
        )
        return request.execute()

    async def _get_caption_details(self, video_id: str, caption_id: str) -> Dict:
        request = self.youtube.captions().download(id=caption_id)
        response = request.execute()
        return {'body': response.decode('utf-8')}

    def _extract_locations_from_text(self, text: str) -> List[Dict]:
        # Enhanced regex pattern for better location detection
        location_patterns = [
            # Cities and countries
            r'\b(?:[A-Z][a-z]+(?:[\s-][A-Z][a-z]+)*)\b(?=.*?(?:city|capital|country|town|village|province|state))',
            # Landmarks and attractions
            r'\b(?:[A-Z][a-z]+(?:[\s-][A-Z][a-z]+)*)\b(?=.*?(?:Park|Museum|Temple|Castle|Palace|Bridge|Mountain|Lake|Beach))',
            # General capitalized location names
            r'\b(?:[A-Z][a-z]+(?:[\s-][A-Z][a-z]+)*),\s*(?:[A-Z][a-z]+(?:[\s-][A-Z][a-z]+)*)\b'
        ]
        
        locations = set()  # Using set to avoid duplicates
        for pattern in location_patterns:
            matches = re.finditer(pattern, text, re.MULTILINE)
            for match in matches:
                location_name = match.group(0)
                # Skip common false positives
                if location_name not in ['I', 'The', 'A', 'An', 'This', 'That']:
                    locations.add(location_name)
        
        # Convert matches to structured data
        return [
            {
                'name': location,
                'description': f'Location mentioned in content',
                'confidence': 'high' if any(keyword in text[max(0, text.find(location)-50):text.find(location)+50] 
                                         for keyword in ['visit', 'travel', 'located', 'destination', 'tour'])
                             else 'medium',
                'context': text[max(0, text.find(location)-100):text.find(location)+100].strip()
            }
            for location in locations
        ]