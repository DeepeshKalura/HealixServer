from fastapi import Body, FastAPI, File, UploadFile, WebSocket
from fastapi.responses import FileResponse, StreamingResponse
from app.logic.audioFileLogic import audioFileProceesing
import io
from pydantic import BaseModel
from app.logic.chatModel import ChatWithModel




app = FastAPI()


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


@app.websocket("/audio")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Wait for incoming data from the client
        data = await websocket.receive_bytes()
        # Process the audio

        processed_audio = process_audio(data)

        # Send the processed audio back to the client
        await websocket.send_bytes(processed_audio)

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


        


def process_audio(raw_audio_data: bytes) -> bytes:
    return raw_audio_data
