from fastapi import Body, FastAPI, File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from app.logic.audioFileLogic import audioFileProceesing
import io
from pydantic import BaseModel




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

    audioFileProceesing(audio.audio_url)
    return FileResponse("response.mp3", media_type="audio/mpeg")