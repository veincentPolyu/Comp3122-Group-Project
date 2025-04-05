from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

class MongoDBHandler:
    def __init__(self):
        self.MONGODB_URL = "mongodb+srv://chukahang96:1234@travelplanner.7qkjpj1.mongodb.net/?retryWrites=true&w=majority&appName=TravelPlanner"
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        try:
            self.client = MongoClient(self.MONGODB_URL)
            self.db = self.client.travel_planner
            self.collection = self.db.YoutubeURL_Database
            self.client.admin.command('ping')
            return True
        except Exception as e:
            print(f"Connection error: {str(e)}")
            return False

    def _format_doc_to_dict(self, doc):
        """Helper method to format MongoDB document"""
        if not doc:
            return None
        # Handle date fields
        created_at = doc.get("created_at", {})
        updated_at = doc.get("updated_at", {})
        
        # Clean up tags (remove extra brackets and quotes)
        tags = doc.get("tags", [])
        cleaned_tags = [tag.strip('[]"\'') for tag in tags] if tags else []
        
        return {
            "url": doc.get("url", ""),
            "title": doc.get("title", ""),
            "rating": doc.get("rating", ""),
            "description": doc.get("description", ""),
            "locations": doc.get("locations", []),
            "tags": cleaned_tags,
            "created_at": created_at.get("$date", None) if isinstance(created_at, dict) else created_at,
            "updated_at": updated_at.get("$date", None) if isinstance(updated_at, dict) else updated_at
        }

    def get_all_entries(self):
        try:
            entries = self.collection.find()
            results = []
            for doc in entries:
                doc_dict = self._format_doc_to_dict(doc)
                if doc_dict:
                    results.append(doc_dict)
            return results, None
        except Exception as e:
            return None, str(e)

    def get_by_url(self, url: str):
        try:
            url = url.strip()
            doc = self.collection.find_one({"url": url})
            return (self._format_doc_to_dict(doc), None) if doc else (None, "Document not found")
        except Exception as e:
            print(f"Fetch error: {str(e)}")
            return None, str(e)

    def update_entry(self, url: str, update_data: dict):
        try:
            url = url.strip()
            
            # Clean up tags before updating
            if "tags" in update_data:
                update_data["tags"] = [tag.strip('[]"\'') for tag in update_data["tags"]]
            
            result = self.collection.update_one(
                {"url": url},
                {"$set": {
                    **update_data,
                    "updated_at": datetime.now()
                }}
            )
            
            if result.modified_count > 0:
                updated_doc = self.collection.find_one({"url": url})
                return (self._format_doc_to_dict(updated_doc), None) if updated_doc else (None, "Update failed")
            return None, "Document not found"
        except Exception as e:
            print(f"Update error: {str(e)}")
            return None, str(e)

    def close(self):
        if self.client:
            self.client.close()
