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



def total_time_user_in_session(token: str) -> str:
    pipeline = [
        {
            "$match": {

                "token" :token
            } 
        },
        {
            "$unwind": "$session"
        },
        {
            "$group": {
                "_id": "$session.session_id",
                "start_time": {"$first": "$session.created_at"},
                "end_time": {"$last": "$session.ended_at"},
                "duration": {"$sum": {"$subtract": [{"$toDate": "$session.ended_at"}, {"$toDate": "$session.created_at"}]}},
            }
        }, 
        {
            "$group": {
                "_id": None,
                "total_duration": {"$sum": "$duration"},
            }
        }
    ]


    result = thearpy_collection.aggregate(pipeline)
    for i in result:
        return i["total_duration"]




def list_of_duration_of_each_session(token: str):
    pipeline = [
        {
            "$match": {

                "token" :token
            } 
        },
        {
            "$unwind": "$session"
        },
        {
            "$group": {
                "_id": "$session.session_id",
                "start_time": {"$first": "$session.created_at"},
                "end_time": {"$last": "$session.ended_at"},
                "duration": {"$sum": {"$subtract": [{"$toDate": "$session.ended_at"}, {"$toDate": "$session.created_at"}]}},
            }
        }, 
    ]
    return [i for i in thearpy_collection.aggregate(pipeline)]


def last_session(token: str): 
    pipeline = [
        {
            "$match": {

                "token" :token
            } 
        },
        {
            "$unwind": "$session"
        },
        {
            "$group": {
                "_id": "$session.session_id",
            }
        }, 
        {
            "$sort": {
                "_id": -1
            }
        },
        {
            "$limit": 1
        }
    ]
    for i in thearpy_collection.aggregate(pipeline):
        return i["_id"]


        
    

def total_session_attended(token: str):
    pipeline = [
        {
            "$match": {

                "token" :token
            } 
        },
        {
            "$unwind": "$session"
        },
        {
            "$group": {
                "_id": "$session.session_id",
            }
        }, 
        {
            "$count": "total_session_attended"
        }
    ]
    for i in thearpy_collection.aggregate(pipeline):
        return i["total_session_attended"]

def sentiment_compound():
    pass

def theme_of_user():
    pass

def engagement_factor():
    pass



@router.get("/{token}")
def get_metrics(token: str):
    return {
        "total_time_user_in_session": total_time_user_in_session(token),
        "list_of_duration_of_each_session": list_of_duration_of_each_session(token),
        "last_session": last_session(),
        "total_session_attended": total_session_attended(),
        "sentiment_compound": sentiment_compound(),
        "theme_of_user": theme_of_user(),
        "engagement_factor": engagement_factor()
    }
