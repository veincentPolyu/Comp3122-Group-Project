import os
import json
import requests

def load_cookies():
    cookies_path = os.path.join(os.path.dirname(__file__), 'instagram_cookies.json')
    if os.path.exists(cookies_path):
        with open(cookies_path, 'r') as f:
            return json.load(f)
    return None

def cookies_to_header(cookies):
    if not cookies:
        return {}
    cookie_string = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    return {'Cookie': cookie_string}

def test_instagram_auth():
    cookies = load_cookies()
    if not cookies:
        print("No cookies found!")
        return False
    
    print(f"Loaded {len(cookies)} cookies")
    print(f"Cookie names: {[c['name'] for c in cookies]}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    headers.update(cookies_to_header(cookies))
    
    # Test authentication by trying to access Instagram API
    response = requests.get('https://www.instagram.com/accounts/edit/', headers=headers)
    
    if response.status_code == 200 and 'viewer' in response.text:
        print("Authentication successful!")
        return True
    else:
        print(f"Authentication failed: Status code {response.status_code}")
        return False

if __name__ == "__main__":
    test_instagram_auth() 