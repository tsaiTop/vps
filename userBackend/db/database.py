
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import certifi
import os


async def connect_mongodb():
    try:
        
        client = MongoClient(os.getenv("MONGODB_URL"), os.getenv("MONGODB_PORT"), directConnection=True)
        db_name = os.getenv("MONGODB_DB_NAME")
        
        database = client[db_name]
        return client, database
    
    except ServerSelectionTimeoutError as err:
        print(err)
        return None
