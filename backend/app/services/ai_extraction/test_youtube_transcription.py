import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path
from extractor import LocationExtractor
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from utils.setup_ffmpeg import setup_ffmpeg

async def test_youtube_transcription():
    """Test YouTube audio extraction and transcription specifically"""
    # Load environment variables
    load_dotenv()
    
    # Get API keys from environment variables
    youtube_api_key = os.getenv("YOUTUBE_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not youtube_api_key or not openai_api_key:
        print("Error: Missing API keys in environment variables")
        print("Please ensure YOUTUBE_API_KEY and OPENAI_API_KEY are set")
        return

    # Initialize the extractor
    extractor = LocationExtractor(
        youtube_api_key=youtube_api_key,
        openai_api_key=openai_api_key
    )
    
    while True:
        # Get URL from user input
        print("\nEnter a YouTube URL to test transcription (or 'q' to quit):")
        url = input().strip()
        
        if url.lower() == 'q':
            break
            
        if not url.startswith(('http://', 'https://')):
            print("Error: Invalid URL format. URL must start with http:// or https://")
            continue
            
        if "youtube.com" not in url and "youtu.be" not in url:
            print("Error: Not a YouTube URL. Please enter a valid YouTube URL.")
            continue
        
        print(f"\nTesting video URL: {url}")
        
        # Extract video ID
        video_id = extractor._extract_video_id(url)
        if not video_id:
            print("✗ Failed to extract video ID")
            continue
            
        print(f"Video ID: {video_id}")
        
        # Test transcription
        try:
            print("\nAttempting transcription...")
            transcript = await extractor._extract_and_transcribe_youtube_audio(video_id)
            
            if transcript:
                print("✓ Successfully extracted and transcribed audio")
                print(f"\nTranscript length: {len(transcript)} characters")
                print("\nFirst 150 characters of transcript:")
                print("-" * 50)
                print(transcript[:150] + "...")
                
                # Save transcript for inspection
                output_dir = Path("transcription_tests")
                output_dir.mkdir(exist_ok=True)
                
                transcript_file = output_dir / f"{video_id}_transcript.txt"
                with open(transcript_file, "w", encoding="utf-8") as f:
                    f.write(f"Video URL: {url}\n")
                    f.write("\nTranscript:\n")
                    f.write(transcript)
                    
                print(f"\nFull transcript saved to: {transcript_file}")
                
                # Ask if user wants to test another URL
                print("\nTest another URL? (y/n):")
                if input().lower() != 'y':
                    break
                
            else:
                print("✗ Failed to get transcript")
                
        except Exception as e:
            print(f"✗ Error during transcription: {str(e)}")
            import traceback
            traceback.print_exc()

def main():
    """Main test function"""
    # Store FFmpeg check result
    if not hasattr(main, 'ffmpeg_checked'):
        # Ensure FFmpeg is installed
        if not setup_ffmpeg():
            print("Cannot proceed without FFmpeg. Please install FFmpeg and try again.")
            return
        main.ffmpeg_checked = True
    
    # Run transcription tests
    asyncio.run(test_youtube_transcription())
    
    print("\nTests completed! Check the transcription_tests directory for results.")

if __name__ == "__main__":
    main()
