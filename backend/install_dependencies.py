"""
Dependency installer for the LocationExtractor
"""
import subprocess
import sys
import os

def install_dependencies():
    """Install required dependencies for audio extraction and transcription"""
    dependencies = [
        "pytubefix",      # For YouTube audio download
        "openai",         # For OpenAI/Azure OpenAI API access
        "youtube-transcript-api",  # For YouTube transcript extraction
        "requests",       # For web requests
        "beautifulsoup4", # For HTML parsing
        "google-api-python-client", # For YouTube Data API
        "python-dotenv",  # For environment variables
    ]
    
    print("Installing required Python packages...")
    for package in dependencies:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}. Please install manually: pip install {package}")
    
    print("\nChecking for FFmpeg (used for audio conversion)...")
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        print("FFmpeg is installed!")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("\nFFmpeg not found! Audio conversion may not work properly.")
        print("Installation instructions:")
        if os.name == 'nt':  # Windows
            print("Windows: Download from https://ffmpeg.org/download.html or install via:")
            print("         winget install ffmpeg")
            print("         or")
            print("         choco install ffmpeg (if you have Chocolatey)")
        elif os.name == 'posix':  # macOS or Linux
            print("macOS:  brew install ffmpeg")
            print("Ubuntu: sudo apt install ffmpeg")
            print("Fedora: sudo dnf install ffmpeg")
    
    print("\nAll dependencies installed! You can now use the LocationExtractor.")

if __name__ == "__main__":
    install_dependencies() 