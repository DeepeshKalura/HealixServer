from fastapi import Body, FastAPI, WebSocket
from fastapi.responses import FileResponse
from app.logic.audioFileLogic import audioFileProceesing
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from app.logic.chatModel import ChatWithModel

origins = ["*"]



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Backend Client for the project"}


# @app.post("/audio")
# async def process_audio_endpoint(audio_file: UploadFile = File(...)):
#     return audioFileProceesing(audio_file)

class AudioRequestModel(BaseModel):
    audio_url: str

@app.post("/audio")
async def process_audio_endpoint(audio: AudioRequestModel = Body(...)):
    chat_model = ChatWithModel()
    audioFileProceesing(audio_file=audio.audio_url, chatWithModel=chat_model)
    return FileResponse("response.mp3", media_type="audio/mpeg")

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