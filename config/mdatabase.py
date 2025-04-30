from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
# seting the environment
from dotenv import load_dotenv
import os
from application.extensions import bcrypt
load_dotenv()

uri = os.environ.get('mongodburi')
if not uri:
    raise ValueError("MongoDB URI not found in environment variables. Please set 'mongodburi' environment variable.")

print("Attempting to connect to MongoDB...")
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
except Exception as e:
    print("Failed to connect to MongoDB:", str(e))
    raise

# Access a specific database
mongodb = client["mavdatabase"]

# Create collections
members_collection = mongodb["members"]
projects_collection = mongodb["projects"]
latest_news_collection = mongodb["latest_news"]
users_collection = mongodb["users"]

def init_db():
    try:
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

        if users_collection.count_documents({}) == 0:
            # Get master user credentials from environment variables
            master_username = os.getenv('Master_User1_Username', 'admin')
            master_email = os.getenv('Master_User1_Email_Address', 'admin@example.com')
            master_password = os.getenv('Master_User1_Password', 'admin123')
            
            print("Creating master user...")
            # Hash the password using Flask-Bcrypt
            hashed_password = bcrypt.generate_password_hash(master_password).decode('utf-8')
            
            users_collection.insert_many([
                {
                    "username": master_username,
                    "email_address": master_email,
                    "role": "Administrator",
                    "password": hashed_password
                }
            ])
            print("Master user created successfully")
    except Exception as e:
        print("Error initializing database:", str(e))
        raise

# Call the init_db function to initialize the database if empty
try:
    init_db()
    print("Database initialization completed successfully")
except Exception as e:
    print("Failed to initialize database:", str(e))
    raise
# # Close the connection (optional, as the client will handle it automatically)
# client.close()
