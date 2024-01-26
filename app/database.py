import os
from pymongo.mongo_client import MongoClient


from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

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

#! From this code I wanted  to build an abstraction layer for the database connection

