from typing import List, Dict
from bs4 import BeautifulSoup
import requests
import re
from googleapiclient.discovery import build

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

    # Use a regex pattern or LLM to find locations in the text
    locations = self._extract_locations_from_text(full_text)
    return locations

async def _get_caption_details(self, video_id: str, caption_id: str) -> Dict:
    request = self.youtube.captions().download(id=caption_id)
    response = request.execute()
    return {'body': response.decode('utf-8')}

def _extract_locations_from_text(self, text: str) -> List[Dict]:
    # Basic regex for location extraction (can be improved)
    location_pattern = r'(\b[A-Z][a-z]+(?: [A-Z][a-z]+)*\b)'  # Example pattern
    matches = re.findall(location_pattern, text)

    locations = []
    for match in matches:
        # Here you would ideally validate the match and enrich it with more data
        locations.append({
            'name': match,
            'description': f'Location mentioned in YouTube video',
            # Add more fields as needed
        })
    return locations

from bs4 import BeautifulSoup

async def extract_from_blog(self, url: str) -> List[Dict]:
    response = requests.get(url)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Assuming blog content is within <p> tags
    paragraphs = soup.find_all('p')
    blog_text = ' '.join([p.get_text() for p in paragraphs])

    # Use a regex pattern or LLM to find locations in the text
    locations = self._extract_locations_from_text(blog_text)
    return locations

    async def _get_video_captions(self, video_id: str):
        request = self.youtube.captions().list(
            part="snippet",
            videoId=video_id
        )
        return request.execute()
