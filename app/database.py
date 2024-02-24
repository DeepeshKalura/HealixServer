from abc import ABC, abstractmethod
import os
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Database(ABC):
    @abstractmethod
    def connect_to_database(self):
        pass

    @abstractmethod
    def store_data(self, db, collectionName):
        pass

    @abstractmethod
    def get_data(self, db, collectionName):
        pass



# Mongo DB 
name=os.getenv("MONGO_NAME")
password=os.getenv("MONGO_PASSWORD")

uri = f"mongodb+srv://{name}:{password}@cluster1.ussxiyu.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri)

def get_db():
    db = client["dev"]
    return db

def get_collection(db, collectionName):
    collection = db[collectionName]
    return collection


# Convex Database 

class ConvexDatabase(Database):
    def connect_to_database(self):
        pass

    def store_data(self, tableName: str):
        pass

    def get_data(self):
        pass


#! From this code I wanted  to build an abstraction layer for the database connection

