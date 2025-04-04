from fastapi import FastAPI, HTTPException, Query, Body
from pydantic import BaseModel, constr, validator
from typing import Optional, List
from urllib.parse import unquote
from mongodb_handler import MongoDBHandler

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
