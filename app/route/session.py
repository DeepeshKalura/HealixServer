import os
import sys
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from uuid import uuid4
from fastapi import APIRouter
from fastapi.responses import FileResponse
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import database as db
import pre_processing as pp
load_dotenv(find_dotenv())

database = db.get_db()

collection = database["thearpy"]

def gemini_model(message: str):
    url = "http://127.0.0.1:5000"
    response = requests.get(url+"/response", json={
        "message": message,
    })

    if(response.status_code == 200):
        output = response.json()["message"]
        return output
    print("Model have some issue")
    exit(2)



    
def thearpy_to_user(token):
    data = {
        "token": token,
        "created_at": datetime.now().isoformat(),
        "session": []
    }
    result = collection.find_one({"token": token})

    if(result == None):
        print("session not exit")
        # Is user exit
        user_collection = db.get_collection(database, "users")
        intermediateResult = user_collection.find_one({"token": token})
        print("user at least exit")
        if(intermediateResult != None):
            collection.insert_one(data)
            print("Session Created")
        else:
            print("Session Not Created: TO resolve this issue please create a user")
            exit(3)
    else:
        print("Session Already Exit: Don't worry Take the session ok")


# I am going to take a session

def create_session(token): 
    result = collection.find_one({"token": token})
    print(result)
    if(result == None):
        print("Session Not Taken")
        exit(4)
    
    session_id = uuid4().hex
    session = {
        "session_id": session_id,
        "created_at": datetime.now().isoformat(),
        "thread": []
    }
    
    collection.update_one({"token": token}, {"$push": {"session": session}})
    
    return session_id



# create_session(token)
        
def take_session(token, session_id, message):
    response = gemini_model(message)
    pp.audio(response)
    new_thread = {
        "thread_id" : uuid4().hex,
        "message": message,
        "response": response,
        "created_at": datetime.now().isoformat()
    }
    collection.update_one({"token": token, "session.session_id": session_id}, {"$push": {"session.$.thread": new_thread}})




router = APIRouter(
    prefix="/v1/cup/thearpy",  
    tags=["Therapy"],
)

@router.post("/createsession")
def session(token: str):
    session_id = create_session(token)
    return {
        "session_id": session_id
    }

from pydantic import BaseModel

class session(BaseModel):
    token: str
    session_id: str
    message: str

@router.post("/takesession")
def create_thread(input: session):
    take_session(input.token, input.session_id, input.message)
    response = FileResponse(path="audio.mp3", media_type="audio/mp3", filename="audio.mp3")
    return response


# print(create_thread(session_id="f78483949def4c7d82fbf899d4213df5", token="56743233", message="I am feeling sad"))