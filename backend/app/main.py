from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from .models.location import Location
from .services.ai_extraction.extractor import LocationExtractor
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UrlInput(BaseModel):
    url: str

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient('mongodb://localhost:27017')
    app.mongodb = app.mongodb_client.travel_planner

@app.post("/api/process-url")
async def process_url(url_input: UrlInput):
    extractor = LocationExtractor(os.getenv("YOUTUBE_API_KEY"))
    
    if "youtube.com" in url_input.url:
        locations = await extractor.extract_from_youtube(url_input.url)
    else:
        locations = await extractor.extract_from_blog(url_input.url)
    
    # Store locations in MongoDB
    for location in locations:
        await app.mongodb.locations.insert_one(location)
    
    return {"status": "completed", "locations": locations}

@app.get("/api/locations/{location_id}")
async def get_location(location_id: str):
    location = await app.mongodb.locations.find_one({"id": location_id})
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return Location(**location)
