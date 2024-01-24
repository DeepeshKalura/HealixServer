import os

from dotenv import load_dotenv, find_dotenv
import database as db

load_dotenv(find_dotenv())

database = db.get_db()

# what will going to happened is there will be a fun

collection = database["sessions"]
