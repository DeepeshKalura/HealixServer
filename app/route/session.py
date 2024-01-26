import os
import sys
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from uuid import uuid4
import requests
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import database as db
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
    new_thread = {
        "thread_id" : uuid4().hex,
        "message": message,
        "response": response,
        "created_at": datetime.now().isoformat()
    }
    collection.update_one({"token": token, "session.session_id": session_id}, {"$push": {"session.$.thread": new_thread}})


# My case was like this:
token = "56743233" 
thearpy_to_user(token)
for i in range(2):

    session_id = create_session(token)
    text = input("Enter the message: ")
    while(text != "exit"):
        take_session(token, session_id, text)
        text = input("Enter the message: ")

print("End of Program")