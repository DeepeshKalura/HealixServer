from fastapi import Body, FastAPI, File, UploadFile, WebSocket
from fastapi.responses import FileResponse, StreamingResponse
import io
from pydantic import BaseModel
from app.model.chatModel import ChatWithModel
from fastapi.middleware.cors import CORSMiddleware
import os
from app.model.chatModel import ChatWithModel

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

