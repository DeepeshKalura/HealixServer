import os
import sys

from fastapi import APIRouter

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from convex import Convex

import pre_processing as pp
from response import  user_input


router = APIRouter(
    prefix="/v1/convex/awareness",  
    tags=["Therapy"],
)

convex = Convex("http://localhost:3001")


#  need to update the logic here
@router.get("/{user_id}")
def create_awarness(user_id: str):
    awarness_id = convex.create_session(user_id)
    return {
        "awarness_id": awarness_id
    }

@router.post("/askquestion/{session_id}")
def create_thread(session_id: str, message: str):
    response = user_input(user_question=message)
    sentiment_compound = pp.store_compound_score(message)
    result = convex.create_thread(session_id, message, response, sentiment_compound)
    return result
