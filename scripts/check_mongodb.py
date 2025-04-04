from pymongo import MongoClient

def check_mongodb_connection():
    # Connection string
    connection_string = "mongodb+srv://chukahang96:1234@travelplanner.7qkjpj1.mongodb.net/?retryWrites=true&w=majority&appName=TravelPlanner"
    
    try:
        # Create a MongoDB client
        client = MongoClient(connection_string)
        
        # Check connection by getting server info
        server_info = client.server_info()
        print(f"✅ Successfully connected to MongoDB!")
        print(f"Server version: {server_info['version']}")
        
        # List all databases
        print("\n📚 Available databases:")
        databases = client.list_database_names()
        for db in databases:
            print(f"\nDatabase: {db}")
            # Get collections in each database
            collections = client[db].list_collection_names()
            if collections:
                print("Collections:")
                for collection in collections:
                    print(f"  - {collection}")
                    # Get one document as sample (optional)
                    sample = client[db][collection].find_one()
                    if sample:
                        print(f"    Sample document: {sample}")
            else:
                print("  No collections found")
                
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {str(e)}")
    finally:
        client.close()
        print("\n👋 Connection closed")

if __name__ == "__main__":
    check_mongodb_connection()
