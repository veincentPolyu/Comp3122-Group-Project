import json
import asyncio
from pathlib import Path
# Import directly since we're in the same directory
from extractor import LocationExtractor
import os

async def test_extractor():
    # Load mock data
    current_dir = Path(__file__).parent
    mock_data_path = current_dir.parent.parent / 'mock_data' / 'api_responses.json'
    
    print(f"Looking for mock data at: {mock_data_path}")
    
    with open(mock_data_path, 'r') as f:
        mock_data = json.load(f)

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

    # Initialize extractor with a dummy API key
    extractor = LocationExtractor("dummy_api_key")

    try:
        # Test location extraction (removed await since it's not an async method)
        print("Testing location extraction...")
        locations = extractor._extract_locations_from_text(test_blog_content)
        
        # Print results
        print("\nExtracted Locations:")
        for loc in locations:
            print(f"- {loc['name']}")
        
        # Compare with expected locations from mock data
        expected_locations = {
            mock_data['extracted_locations']['locations'][0]['name'],
            'Toshima City',
            'Tokyo'
        }
        
        found_locations = {loc['name'] for loc in locations}
        
        print("\nValidation:")
        print(f"Expected locations: {expected_locations}")
        print(f"Found locations: {found_locations}")
        if len(expected_locations) > 0:
            success_rate = len(found_locations.intersection(expected_locations)) / len(expected_locations) * 100
            print(f"Success rate: {success_rate}%")
        else:
            print("No expected locations to compare against")

    except Exception as e:
        print(f"Error during testing: {str(e)}")

    finally:
        # Clean up temporary file
        if test_file_path.exists():
            test_file_path.unlink()

if __name__ == "__main__":
    asyncio.run(test_extractor()) 