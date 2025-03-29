import requests

BASE_URL = "http://localhost:8000"

def test_extractor():
    print("\n=== Testing Location Extractor ===")
    response = requests.get(f"{BASE_URL}/api/test")
    print(f"Status Code: {response.status_code}")
    print("Response:", response.json())

if __name__ == "__main__":
    test_extractor()
