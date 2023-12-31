import pymongo
from dotenv import load_dotenv
import os

from datetime import datetime

load_dotenv()

mongodb_url = os.getenv('MONGODB_LOCAL_URL')
mongodb = os.getenv('MONGODB_LOCAL_DB')
mongodb_collection = os.getenv('MONGODB_LOCAL_COLLECTION')

class DbManagement:
    def __init__(self, text: str, name_module: str, subject: str,n_subjects: int):
        self.text = text
        self.name_module = name_module
        self.n_subjects = n_subjects        
        self.subject = subject
        
    def get_mongodb_connection(self):
        
        # Replace with your MongoDB connection string
        connection_string = mongodb_url

        # Connect to MongoDB
        client = pymongo.MongoClient(connection_string)

        # Replace with your database and collection names
        db = client[mongodb]
        
        return db

    def add_text_to_db(self, page_iterator):
        
        # Connect to MongoDB
        db = self.get_mongodb_connection()
        
        # Select a collection
        collection = db[mongodb_collection]  # Replace with your collection name

        
        target_dict = {
            'Module': self.name_module,
            'Number of subjects': str(self.n_subjects),
            'Content': {
                'subject': self.subject,
                'page': str(page_iterator),
                'content': self.text                
            },
            "timestamp": datetime.now()  # Add the current timestamp to the document       
}

        # Insert the dictionary into the collection
        collection.insert_one(target_dict)
    
    def find_last_page(self):
        
        # Connect to MongoDB
        db = self.get_mongodb_connection()
        
        # Select a collection
        collection = db[mongodb_collection]  # Replace with your collection name

        # Define the timestamp field to sort by (assuming a "timestamp" field in your documents)
        timestamp_field = "timestamp"

        # Query the latest document
        latest_document = collection.find_one(sort=[(timestamp_field, pymongo.DESCENDING)])

        return latest_document['Content']['page']