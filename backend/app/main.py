from flask import Flask, jsonify, send_from_directory, request
from flask_restful import Api, Resource
from flask_cors import CORS
import asyncio
from app.services.ai_extraction.test_extractor import test_extractor
import os
from app.services.ai_extraction.extractor import LocationExtractor

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)
api = Api(app)

# Swagger UI route
@app.route('/api/docs/')
def swagger_ui():
    return app.send_static_file('swagger.html')

# Swagger JSON route
@app.route('/api/docs/swagger.json')
def swagger_json():
    return app.send_static_file('swagger.json')

class TestExtractorAPI(Resource):
    async def get(self):
        try:
            # Run the test_extractor function
            result = await test_extractor()
            return {"status": "success", "result": result}
        except Exception as e:
            return {"error": str(e)}, 500

class ExtractorAPI(Resource):
    def post(self):
        try:
            data = request.get_json()
            if not data or 'url' not in data:
                return {"error": "URL is required"}, 400

            extractor = LocationExtractor(
                youtube_api_key=os.getenv("YOUTUBE_API_KEY"),
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
            
            # Run async operation in event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(extractor.process_url(data['url']))
            loop.close()
            
            return result

        except Exception as e:
            print(f"Error processing request: {str(e)}")
            return {"error": str(e)}, 500

# Register routes
api.add_resource(TestExtractorAPI, '/api/test')
api.add_resource(ExtractorAPI, '/api/extract')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
