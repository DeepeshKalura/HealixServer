import os
import sys
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from uuid import uuid4
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import database as db
import pre_processing as pp
from response import use_model, ChatGPTModel

load_dotenv(find_dotenv())

database = db.get_db()

collection = database["thearpy"]
    
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



router = APIRouter(
    prefix="/v1/cup/thearpy",  
    tags=["Therapy"],
)


from pydantic import BaseModel

class session(BaseModel):
    token: str
    session_id: str
    message: str

@router.post("/{token}")
def create_session(token): 
    session_id = uuid4().hex
    session = {
        "session_id": session_id,
        "created_at": datetime.now().isoformat(),
        "thread": [],
        "ended_at": datetime.now().isoformat()
    }
    
    collection.update_one({"token": token}, {"$push": {"session": session}})
    
    return {
        "session_id": session_id
    }

@router.get("/takesession")
def create_thread(input: session):
    query = {
        "token": input.token,
        "session.session_id": input.session_id
    }
    response = use_model(message=input.message, model=ChatGPTModel())
    pp.audio(response)
    document = collection.find_one(query)

    document = collection.find_one(query)

    if (document == None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with token {input.token} not found"
        )

    new_thread = {
        "thread_id" : uuid4().hex,
        "message": input.message,
        "response": response,
        "created_at": datetime.now().isoformat()
    }
    update_query = {
        "_id": document["_id"],
        "$push": {"session.$.thread": new_thread}
    }

    collection.update_one(query, {"$push": {"session.$.thread": new_thread}})

    response = FileResponse(path="audio.mp3", media_type="audio/mp3", filename="audio.mp3")
    return response

