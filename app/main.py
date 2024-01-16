from fastapi import FastAPI, WebSocket
import io
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from app.model.chatModel import ChatWithModel
import datetime

origins = ["*"]



app = FastAPI()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/etc/secrets/application_default_credentials.json"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/etc/secrets/application_default_credentials.json"

@app.get("/")
async def root():
    return {"message": "Backend Client for the project"}


class AudioRequestModel(BaseModel):
    audio_url: str


@app.websocket("/text")
async def text_webscoket_endpoint(websocket: WebSocket):

    task = websocket.accept

    chat_model = ChatWithModel()

    await task()

    while True:
        data = await websocket.receive_text()
        if(data == 'exit' or data == 'Exit'):
            await websocket.close()
            break
        response = chat_model.Phykologist(message=data)
        
        await websocket.send_text(response)

class UserRequestMode(BaseModel):
    name: str
    tag: int
    pyq: str

class session(BaseModel):
    name: str

def changeTotalTime(timestamp, user):
    with open(user+".txt", "r") as f:
        lines = f.readlines()
        lines[4] = str(float(lines[4]) +(float(timestamp))-float(lines[4])) + "\n"
    with open(user+".txt", "w") as f:
        f.writelines(lines)
    return lines[3]


@app.post("/sessionover")
async def session_values(username: session):
    timestamp = datetime.datetime.now()
    changeTotalTime(timestamp, username.name)
    with open(username.name+".txt", "a") as f:
        f.write(str(timestamp) + "\n")
        return {
            "tag": 0,
        }

@app.post("/startsession")
async def session_values(username: session):
    numberOfSessions = 0
    sessionTime = datetime.datetime.now()
    name = session.name
    tag = 0
    pyq = ""
    with open(username.name+".txt", "r") as f:
        numberOfSessions = int(f.readlines()[1]) + 1
        tag = int(f.readlines()[2])
        pyq = f.readlines()[3]
    with open(username.name+".txt", "w") as f:
        f.write(name + "\n")
        f.write(str(numberOfSessions) + "\n")
        f.write(str(tag) + "\n")
        f.write(pyq + "\n")
        f.write("0" + "\n")
        f.write(str(sessionTime) + "\n")

    return {
        "message": "Session Started",
    }

@app.post("/newuser")
async def user_values(input: UserRequestMode):
    user_name = input.name
    with open(user_name+".txt", "w") as f:
        f.write(input.name + "\n") #name
        f.write("0"+"\n") #total session
        f.write(str(input.tag) + "\n") #propteries of user
        f.write(input.pyq + "\n") #pyq
        f.write("0" + "\n") #totalTimeSessions
        f.write("0" + "\n") #lastSession
        return {
            "name": input.name,
            "total_number_of_sessions": "0",
            "tag": input.tag,
            "pyq": input.pd_code,
            "total_session": "0",
            "last_session": "0",
        }

@app.get("/user")
async def get_user(username: session):
    with open(username.name+".txt", "r") as f:
        lines = [line.strip() for line in f.readlines()]

        return {
            "name": lines[0],
            "total_number_of_sessions": lines[1],
            "tag": lines[2],
            "pyq": lines[3],
            "total_time_sessions": lines[4],
            "last_sessions": lines[5],
        }

@app.get("/theorpy")
async def get_theorpy(username: session):
    theorpy = "Default"
    with open(username.name+".txt", "r") as f:
        lines = f.readlines()
        if(lines[2]==1):
            theorpy = "Depression"
        elif(lines[2]==2):
            theorpy = "Anxiety"
        else:
            theorpy = "Default"

    return {
        "theorpy": theorpy
    }
