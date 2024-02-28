import os
import sys

from fastapi import APIRouter

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from convex import Convex

import pre_processing as pp
from response import use_model, GeminiModel


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

@router.post("/takesession/{session_id}")
def create_thread(session_id: str, message: str):
    response = use_model(message, model=GeminiModel())
    sentiment_compound = pp.store_compound_score(message)
    result = convex.create_thread(session_id, message, response, sentiment_compound)
    return result



