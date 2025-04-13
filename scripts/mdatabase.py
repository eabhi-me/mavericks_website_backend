from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
# seting the environment
from dotenv import load_dotenv
import os
load_dotenv()

uri = os.environ.get('mongodburi')

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


# Access a specific database
mongodb = client["mavdatabase"]

# Create collections
members_collection = mongodb["members"]
projects_collection = mongodb["projects"]
latest_news_collection = mongodb["latest_news"]
def init_db():
    # Check if the collections are empty and insert data if they are
    if members_collection.count_documents({}) == 0:
        members_collection.insert_many([
            {"name": "John Doe", "email": "john.doe@example.com", "role": "Developer"},
            {"name": "Jane Smith", "email": "jane.smith@example.com", "role": "Designer"}
        ])

    if projects_collection.count_documents({}) == 0:
        projects_collection.insert_many([
            {"title": "Project Alpha", "description": "First project", "status": "Ongoing"},
            {"title": "Project Beta", "description": "Second project", "status": "Completed"}
        ])

    if latest_news_collection.count_documents({}) == 0:
        latest_news_collection.insert_many([
            {"headline": "New Feature Released", "content": "We have released a new feature.", "date": "2023-10-01"},
            {"headline": "Maintenance Scheduled", "content": "Scheduled maintenance on 2023-10-05.", "date": "2023-10-03"}
        ])

# Call the init_db function to initialize the database if empty
init_db()
# # Close the connection (optional, as the client will handle it automatically)
# client.close()
