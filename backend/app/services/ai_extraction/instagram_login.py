"""Instagram login helper functions"""
import json
import os

def load_cookies():
    """Load saved Instagram cookies"""
    cookies_path = os.path.join(os.path.dirname(__file__), 'instagram_cookies.json')
    if os.path.exists(cookies_path):
        with open(cookies_path, 'r') as f:
            return json.load(f)
    return None

def cookies_to_header(cookies):
    """Convert cookies to request header format"""
    if not cookies:
        return {}
    cookie_string = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
    return {'Cookie': cookie_string}

def login_and_get_cookies(username, password):
    """Placeholder for login function - not needed since we're using a cookies file"""
    print("Warning: Automatic login is not implemented. Using cookies from file instead.")
    return load_cookies() is not None 