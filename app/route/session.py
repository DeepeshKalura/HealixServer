import os
import sys
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from uuid import uuid4
from fastapi import APIRouter, HTTPException, status

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import database as db
import pre_processing as pp
from pydantic import BaseModel
from response import use_model, ChatGPTModel, user_input

load_dotenv(find_dotenv())

database = db.get_db()

collection = database["thearpy"]


def update_time(token: str, session_id: str):
    query = {
        "token": token,
        "session.session_id": session_id
    }
    collection.update_one(query, {"$set": {"session.$.ended_at": datetime.now().isoformat()}})

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


class session(BaseModel):
    token: str
    session_id: str
    message: str

@router.get("/{token}")
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

@router.post("/takesession/promot")
def create_thread_by_promot(input: session):
    query = {
        "token": input.token,
        "session.session_id": input.session_id
    }
    response = use_model(message=input.message, model=ChatGPTModel())
    # pp.audio(response)
    document = collection.find_one(query)


    if (document == None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with token {input.token} not found"
        )
    sentiment_compound = pp.store_compound_score(input.message)
    theme = pp.store_theme_of_user(input.message)
    new_thread = {
        "thread_id" : uuid4().hex,
        "message": input.message,
        "response": response,
        "sentiment_compound": sentiment_compound,
        "theme": theme,
        "created_at": datetime.now().isoformat()
    }

    collection.update_one(query, {"$push": {"session.$.thread": new_thread}})

    # response = FileResponse(path="audio.mp3", media_type="audio/mp3", filename="audio.mp3")
    # update_time(token=input.token, session_id=input.session_id)
    return {
        "message":  response
    }

@router.post("/takesession/rag")
def create_thread_by_rag(input: session):
    query = {
        "token": input.token,
        "session.session_id": input.session_id
    }
    response = user_input(input.message)
    document = collection.find_one(query)
    if (document == None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with token {input.token} not found"
        )
    sentiment_compound = pp.store_compound_score(input.message)
    theme = pp.store_theme_of_user(input.message)
    new_thread = {
        "thread_id" : uuid4().hex,
        "message": input.message,
        "response": response,
        "sentiment_compound": sentiment_compound,
        "theme": theme,
        "created_at": datetime.now().isoformat()
    }
    collection.update_one(query, {"$push": {"session.$.thread": new_thread}})
    return {
        "message":  response
    }


    




