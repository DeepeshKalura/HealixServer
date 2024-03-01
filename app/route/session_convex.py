import os
import sys

from fastapi import APIRouter, WebSocket

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from convex import Convex

import pre_processing as pp
from response import use_model, GeminiModel
from app.schema import session 

router = APIRouter(
    prefix="/v1/convex/heal",  
    tags=["Therapy"],
)

convex = Convex("http://localhost:3001")

@router.get("/{user_id}")
def create_session(user_id: str):
    session_id = convex.create_session(user_id)
    return {
        "session_id": session_id
    }

@router.post("/")
def create_thread(session: session):
    response = use_model(message=session.message, model=GeminiModel())
    print(response)
    sentiment_compound = pp.store_compound_score(session.message)
    print(sentiment_compound)
    result = convex.create_thread(session_id=session.session_id, message=session.message, response=response, sentiment_compound=sentiment_compound)
    return result

@router.websocket("/ws")
async def audio_excahnge(websocket: WebSocket):
    data = await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
  

