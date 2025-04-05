from fastapi import FastAPI, HTTPException, Query, Body
from pydantic import BaseModel, constr, validator
from typing import Optional, List, Dict
from urllib.parse import unquote
from mongodb_handler import MongoDBHandler
import os
import asyncio
from dotenv import load_dotenv
# Import the LocationExtractor
import sys
sys.path.append('../backend')
from app.services.ai_extraction.extractor import LocationExtractor

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Travel Planner API",
    description="API for managing YouTube URLs in MongoDB",
    version="1.0.0"
)

class UpdateRating(BaseModel):  # Renamed from UpdateEntry
    rating: constr(strip_whitespace=True)
    locations: Optional[List[str]] = []
    tags: Optional[List[str]] = []

    @validator('rating')
    def validate_rating(cls, v):
        if v is not None:
            return str(v)
        raise ValueError("Rating is required")

    @validator('tags')
    def clean_tags(cls, v):
        if v:
            return [tag.strip('[]"\'') for tag in v]  # Clean any extra formatting
        return []

    class Config:
        json_schema_extra = {
            "example": {
                "rating": "5",
                "locations": ["Tokyo", "Kyoto"],
                "tags": ["travel", "relax"]
            }
        }

# Add new request model
class ExtractionRequest(BaseModel):
    url: str

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://www.youtube.com/watch?v=example"
            }
        }

# Initialize MongoDB handler
mongodb = MongoDBHandler()

@app.on_event("startup")
async def startup_db_client():
    if not mongodb.connect():
        raise Exception("Failed to connect to MongoDB")
    print("✅ Connected to MongoDB!")

@app.on_event("shutdown")
async def shutdown_db_client():
    mongodb.close()

@app.get("/YoutubeURL_Database/", tags=["Database"])
async def get_database_entries():
    """Get all entries directly from YoutubeURL_Database"""
    results, error = mongodb.get_all_entries()
    if error:
        raise HTTPException(status_code=500, detail=f"Database error: {error}")
    return results

@app.get("/YoutubeURL_Database/get", tags=["Database"])
async def get_entry_by_url(
    url: str = Query(..., description="YouTube URL to fetch", example="https://www.youtube.com/watch?v=0MQKLUkAUf8")
):
    """Get an entry from YoutubeURL_Database by URL"""
    result, error = mongodb.get_by_url(url)
    if error:
        raise HTTPException(
            status_code=404 if error == "Document not found" else 500,
            detail=f"Fetch error: {error}"
        )
    return result

@app.put("/YoutubeURL_Database/update_rating", tags=["Database"])  # Changed from /update
async def update_video_rating(
    url: str = Query(..., description="YouTube URL to update rating", example="https://www.youtube.com/watch?v=0MQKLUkAUf8"),
    update_data: UpdateRating = Body(..., description="New rating value")
):
    """Update rating for a YouTube URL entry"""
    updated_doc, error = mongodb.update_entry(url, {"rating": update_data.rating})
    if error:
        raise HTTPException(status_code=404 if error == "Document not found" else 500, 
                          detail=f"Update error: {error}")
    return updated_doc

@app.post("/extract-locations/", tags=["Extraction"])
async def extract_locations(request: ExtractionRequest):
    """Extract locations from URL using LocationExtractor"""
    try:
        # Initialize extractor
        extractor = LocationExtractor(
            youtube_api_key=os.getenv("YOUTUBE_API_KEY"),
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Process URL and get results
        result = await extractor.process_url(request.url)
        
        return result
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
