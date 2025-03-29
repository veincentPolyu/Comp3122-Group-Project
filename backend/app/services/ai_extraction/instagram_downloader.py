"""
Utility for downloading Instagram content without external dependencies.
This is a fallback when yt-dlp is not available.
"""

import requests
import re
import json
import tempfile
import os
import random
import time

def get_random_user_agent():
    """Return a random user agent string to avoid detection"""
    user_agents = [
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    ]
    return random.choice(user_agents)

def download_instagram_video(url, output_path):
    """
    Download Instagram video without external tools.
    Returns the path to the downloaded file or None if failed.
    """
    try:
        # Set up headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.instagram.com/',
        }
        
        # Try to fetch the page
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Look for video URL in the HTML
        # First try to find video URL in JSON data
        json_data_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', response.text)
        for json_match in json_data_matches:
            try:
                data = json.loads(json_match)
                if 'contentUrl' in data and data['contentUrl']:
                    video_url = data['contentUrl']
                    print(f"Found video URL in JSON: {video_url}")
                    
                    # Download the video
                    video_response = requests.get(video_url, headers=headers, stream=True)
                    video_response.raise_for_status()
                    
                    with open(output_path, 'wb') as f:
                        for chunk in video_response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    print(f"Successfully downloaded video to {output_path}")
                    return output_path
            except json.JSONDecodeError:
                continue
        
        # If not found in JSON, try regex pattern matching for video URL
        video_url_match = re.search(r'"video_url":"([^"]*)"', response.text)
        if video_url_match:
            video_url = video_url_match.group(1).replace('\\u0026', '&')
            print(f"Found video URL with regex: {video_url}")
            
            # Download the video
            video_response = requests.get(video_url, headers=headers, stream=True)
            video_response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in video_response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"Successfully downloaded video to {output_path}")
            return output_path
        
        print("Could not find video URL in Instagram page")
        return None
        
    except Exception as e:
        print(f"Error downloading Instagram video: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    import sys
    if len(sys.argv) > 1:
        url = sys.argv[1]
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp:
            output_path = temp.name
        
        result = download_instagram_video(url, output_path)
        if result:
            print(f"Video downloaded to: {result}")
        else:
            print("Failed to download video")
    else:
        print("Usage: python instagram_downloader.py <instagram_url>") 