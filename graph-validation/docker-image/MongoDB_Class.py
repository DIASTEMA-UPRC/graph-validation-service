import os
from pymongo import MongoClient

class MongoDB_Class:
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))

    DATABASE = os.getenv("DATABASE", "UIDB")
    COLLECTION = os.getenv("COLLECTION", "datasets")

    def __init__(self):
        mongo_host = MongoDB_Class.MONGO_HOST+":"+str(MongoDB_Class.MONGO_PORT)
        self.mongo_client = MongoClient("mongodb://"+mongo_host+"/")
        return

    def getMongoRecord(self, key_record):
        mongo_db = self.mongo_client[MongoDB_Class.DATABASE]
        mongo_collection = mongo_db[MongoDB_Class.COLLECTION]
        return mongo_collection.find_one(key_record)