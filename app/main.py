from fastapi import Body, FastAPI, File, UploadFile, WebSocket
import io
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from app.model.chatModel import ChatWithModel
import time

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
    pd_code: str

class session(BaseModel):
    name: str

def changeTotalTime(timestamp, user):
    with open(user+".txt", "r") as f:
        lines = f.readlines()
        lines[3] = str(float(lines[3])+(float(timestamp))-float(lines[4])) + "\n"
    with open(user+".txt", "w") as f:
        f.writelines(lines)
    return lines[3]

@app.post("/session")
async def session_values(username: session):
    timestamp = time.time()
    changeTotalTime(timestamp, username.name)
    with open(username.name+".txt", "a") as f:
        f.write(str(timestamp) + "\n")

        return {
            "tag": 0,
        }

@app.post("/newuser")
async def user_values(input: UserRequestMode):
    user_name = input.name
    timestamp = time.time()
    with open(user_name+".txt", "w") as f:
        f.write(input.name + "\n")
        f.write(str(input.tag) + "\n")
        f.write(input.pd_code + "\n")
        f.write("0" + "\n")
        f.write(str(timestamp) + "\n")
        return {
            "name": input.name,
            "tag": input.tag,
            "pd_code": input.pd_code,
            "total_session": "0",
            "timestamp": timestamp,
            "sessionOverTime": "0"
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