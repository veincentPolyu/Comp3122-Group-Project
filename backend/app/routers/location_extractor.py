from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Dict
import os
from ..services.ai_extraction.extractor import LocationExtractor

router = APIRouter(prefix="/api/extractor", tags=["location-extractor"])

class UrlRequest(BaseModel):
    url: HttpUrl

@router.post("/extract")
async def extract_locations(request: UrlRequest) -> Dict:
    try:
        # Initialize extractor with API keys
        extractor = LocationExtractor(
            youtube_api_key=os.getenv("YOUTUBE_API_KEY"),
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Process URL and get locations
        result = await extractor.process_url(str(request.url))
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing URL: {str(e)}"
        )
