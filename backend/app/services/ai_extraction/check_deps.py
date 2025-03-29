import shutil
import subprocess
import importlib
import sys

def check_dependencies():
    # Check Python packages
    packages = ["yt_dlp", "instaloader", "openai", "requests", "bs4"]
    for package in packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is NOT installed. Run: pip install {package}")
    
    # Check command-line tools
    tools = ["ffmpeg", "yt-dlp"]
    for tool in tools:
        path = shutil.which(tool)
        if path:
            # Get version
            try:
                result = subprocess.run([tool, "--version"], capture_output=True, text=True)
                version = result.stdout.split("\n")[0]
                print(f"✅ {tool} found at {path} ({version})")
            except:
                print(f"✅ {tool} found at {path}")
        else:
            print(f"❌ {tool} NOT found in PATH")
    
    # Check if we can access the cookies file
    import os
    import json
    cookies_path = os.path.join(os.path.dirname(__file__), 'instagram_cookies.json')
    if os.path.exists(cookies_path):
        try:
            with open(cookies_path, 'r') as f:
                cookies = json.load(f)
                print(f"✅ Instagram cookies file found with {len(cookies)} cookies")
        except:
            print("❌ Instagram cookies file exists but couldn't be read")
    else:
        print("❌ Instagram cookies file not found")

if __name__ == "__main__":
    check_dependencies() 