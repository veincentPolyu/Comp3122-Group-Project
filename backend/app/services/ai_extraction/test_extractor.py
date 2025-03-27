import json
import asyncio
from pathlib import Path
# Import directly since we're in the same directory
from extractor import LocationExtractor
import os
from dotenv import load_dotenv  # Add this import

# Load environment variables from .env file
load_dotenv()

async def test_extractor():
    # Load mock data
    current_dir = Path(__file__).parent
    mock_data_path = current_dir.parent.parent / 'mock_data' / 'api_responses.json'
    
    print(f"Looking for mock data at: {mock_data_path}")
    
    with open(mock_data_path, 'r') as f:
        mock_data = json.load(f)

    test_url = "https://example-blog.com/tokyo-trip"
    test_blog_content = f"""
    During my trip to Tokyo, I had an amazing experience at {mock_data['extracted_locations']['locations'][0]['name']}.
    Located in {mock_data['extracted_locations']['locations'][0]['address']}, this place is truly special.
    The restaurant is in Toshima City, which is a great area to explore in Tokyo.
    """

    # Create a temporary HTML file with the test content
    test_html = f"""
    <html>
        <body>
            <p>{test_blog_content}</p>
        </body>
    </html>
    """
    
    test_file_path = current_dir / 'test_blog.html'
    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.write(test_html)

    # Get API key from environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    extractor = LocationExtractor(
        youtube_api_key="dummy_youtube_api_key",
        openai_api_key=openai_api_key
    )

    try:
        print("Testing location extraction...")
        # Use process_url instead of _extract_locations_from_text
        result = await extractor.extract_from_web(test_url)
        
        print("\nExtracted Result:")
        print(json.dumps(result, indent=2))
        
        # Validate structure matches mock data
        expected_keys = set(mock_data.keys())
        actual_keys = set(result.keys())
        
        print("\nValidation:")
        print(f"Expected keys: {expected_keys}")
        print(f"Actual keys: {actual_keys}")
        print(f"Structure match: {expected_keys == actual_keys}")
        
        # Check if required fields are present in locations
        if result["extracted_locations"]["locations"]:
            first_location = result["extracted_locations"]["locations"][0]
            required_fields = ["id", "name", "category", "description"]
            missing_fields = [field for field in required_fields if field not in first_location]
            
            print("\nLocation fields validation:")
            if missing_fields:
                print(f"Missing required fields: {missing_fields}")
            else:
                print("All required fields present")

    except Exception as e:
        print(f"Error during testing: {str(e)}")

    finally:
        # Clean up temporary file
        if test_file_path.exists():
            test_file_path.unlink()

if __name__ == "__main__":
    asyncio.run(test_extractor()) 