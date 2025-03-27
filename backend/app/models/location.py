class LocationExtractor:
    def __init__(self, youtube_api_key: str, openai_api_key: str):
        self.youtube = build('youtube', 'v3', developerKey=youtube_api_key)
        self.client = OpenAI(
            api_key=openai_api_key,
            base_url="https://api.openai.com/v1"  # Use official OpenAI endpoint
        )
        # Load mock data
        self.mock_data = self._load_mock_data()
        openai.api_key = openai_api_key

    def _load_mock_data(self) -> Dict:
        """Load mock data from api_responses.json"""
        mock_data_path = Path(__file__).parent.parent.parent / 'mock_data' / 'api_responses.json'
        with open(mock_data_path, 'r') as f:
            return json.load(f)

    # ... other methods ...

    async def _process_with_llm(self, text: str) -> List[Dict]:
        """Process text with GPT to extract locations"""
        prompt = """Extract travel-related locations from this text. For each location, provide:
        - name: The official name if available, or descriptive name
        - type: Type of location (restaurant, temple, park, etc.)
        - details: Key details about the location
        - context: How/why it was mentioned in the text
        
        Return ONLY a valid JSON array following this exact format:
        [
            {
                "name": "location name",
                "type": "location type",
                "details": "location details",
                "context": "visit context"
            }
        ]
        
        Text: {text}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that returns valid JSON."},
                    {"role": "user", "content": prompt.format(text=text[:4000])}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            
            # Clean and parse the response
            try:
                if content.startswith('```json'):
                    content = content[7:-3].strip()
                elif content.startswith('```'):
                    content = content[3:-3].strip()
                    
                locations = json.loads(content)
                
                if isinstance(locations, dict) and 'locations' in locations:
                    return self._format_locations(locations['locations'])
                elif isinstance(locations, list):
                    return self._format_locations(locations)
                else:
                    print(f"Unexpected response format: {content}")
                    return []
                    
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {str(e)}")
                print(f"Response content: {content}")
                return []
                
        except Exception as e:
            print(f"LLM processing error: {str(e)}")
            return []

    # ... rest of the class methods ...