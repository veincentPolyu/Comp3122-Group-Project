from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

class YoutubeUrlAPI:
    def __init__(self):
        # Connection string
        self.connection_string = "mongodb+srv://chukahang96:1234@travelplanner.7qkjpj1.mongodb.net/?retryWrites=true&w=majority&appName=TravelPlanner"
        self.client = MongoClient(self.connection_string)
        self.db = self.client.travel_planner
        self.collection = self.db.YoutubeURL_Database

    def add_youtube_url(self, url: str, title: str, description: str = ""):
        """Add a new YouTube URL to the database"""
        try:
            document = {
                "url": url,
                "title": title,
                "description": description,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
            result = self.collection.insert_one(document)
            print(f"✅ Added URL with ID: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            print(f"❌ Error adding URL: {str(e)}")
            return None

    def get_youtube_url(self, url_id: str):
        """Get a YouTube URL by ID"""
        try:
            document = self.collection.find_one({"_id": ObjectId(url_id)})
            return document
        except Exception as e:
            print(f"❌ Error getting URL: {str(e)}")
            return None

    def get_all_youtube_urls(self):
        """Get all YouTube URLs"""
        try:
            documents = list(self.collection.find())
            return documents
        except Exception as e:
            print(f"❌ Error getting URLs: {str(e)}")
            return []

    def update_youtube_url(self, url_id: str, update_data: dict):
        """Update a YouTube URL"""
        try:
            update_data["updated_at"] = datetime.now()
            result = self.collection.update_one(
                {"_id": ObjectId(url_id)},
                {"$set": update_data}
            )
            if result.modified_count > 0:
                print(f"✅ Updated URL with ID: {url_id}")
                return True
            print("⚠️ No document was updated")
            return False
        except Exception as e:
            print(f"❌ Error updating URL: {str(e)}")
            return False

    def delete_youtube_url(self, url_id: str):
        """Delete a YouTube URL"""
        try:
            result = self.collection.delete_one({"_id": ObjectId(url_id)})
            if result.deleted_count > 0:
                print(f"✅ Deleted URL with ID: {url_id}")
                return True
            print("⚠️ No document was deleted")
            return False
        except Exception as e:
            print(f"❌ Error deleting URL: {str(e)}")
            return False

    def close_connection(self):
        """Close the MongoDB connection"""
        self.client.close()

# Example usage
if __name__ == "__main__":
    api = YoutubeUrlAPI()
    
    # Example: Add a new URL
    new_id = api.add_youtube_url(
        url="https://www.youtube.com/watch?v=example",
        title="Travel Video",
        description="A beautiful travel video"
    )
    
    # Example: Get URL by ID
    if new_id:
        url_data = api.get_youtube_url(new_id)
        print(f"\nRetrieved URL data: {url_data}")
        
        # Example: Update URL
        update_result = api.update_youtube_url(
            new_id,
            {"title": "Updated Travel Video"}
        )
        
        # Example: Get all URLs
        all_urls = api.get_all_youtube_urls()
        print("\nAll URLs in database:")
        for url in all_urls:
            print(f"- {url['title']}: {url['url']}")
    
    api.close_connection()
