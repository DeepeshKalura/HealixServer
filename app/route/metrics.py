import os
from dotenv import load_dotenv, find_dotenv
from fastapi import APIRouter
from datetime import datetime

from database import get_db, get_collection


load_dotenv(find_dotenv())


router = APIRouter(
    prefix="/v1/cup/metrix",  
    tags=["Metrics"],
)

db = get_db()
thearpy_collection = get_collection(db, "thearpy")



def total_time_user_in_app():
    pipeline = [
        {
            "$unwind": "$session"
        },
        {
            "$group": {
                "_id": "$session.session_id",
                "user_id": {"$first": "$_id"},
                "total_time": {"$sum": {"$subtract": [datetime.fromisoformat("$session.ended_at"), datetime.fromisoformat("$session.created_at")]}}
            }
        },
        {
            "$group": {
                "_id": "$user_id",
                "total_session_time": {"$sum": "$total_time"}
            }
        }
    ]

    result = db.collection.aggregate(pipeline)
    print(result)




    pass

def total_time_user_in_session():
    pass


def last_session(): 
    pass

def total_session_attended():
    pass

def sentiment_compound():
    pass

def theme_of_user():
    pass

def engagement_factor():
    pass



@router.get("/{token}")
def get_metrics(token: str):

    return {
        "message": "Hello World"
    }