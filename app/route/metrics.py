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

def sentiment_compound(token: str):
    pipeline = [
        {
            "$match": {
                "token": token
            } 
        },
        {
            "$unwind": "$session"
        },
        {
            "$group": {
                "_id": "$session.session_id",
                "last_session": {"$last": "$session"}  # Get the last session for each session_id
            }
        },
        {
            "$replaceRoot": {"newRoot": "$last_session"}  # Replace the document with the last_session
        },
        {
            "$unwind": "$thread"  # Unwind the thread array
        },
        {
            "$project": {
                "_id": "$thread.thread_id",
                "sentiment_compound" : "$thread.sentiment_compound"     
            }
        }    
    ]
    result = thearpy_collection.aggregate(pipeline=pipeline)
    average_of_sentiment_compound = 0
    print(result)
    j = 0
    for i in result:
        j += 1
        average_of_sentiment_compound += float(i["sentiment_compound"])

    return (average_of_sentiment_compound/j)



def theme_of_user(token: str):
    pipeline = [
        {
            "$match": {
                "token": token
            } 
        }, 
        {
            "$unwind": "$session"
        }, 
        {
            "$group": {
                    "_id": "$session.session_id",
                    "last_session": {"$last": "$session"}  # Get the last session for each session_id
            }
        }, 
        {
                "$replaceRoot": {"newRoot": "$last_session"}  # Replace the document with the last_session
        },
        {
            "$unwind": "$thread"
        },
        {
            "$project": {
                "_id": 0,  # Exclude _id from the output
                "response": "$thread.response"  # Include the response field from each thread
            }
        }
        
    ]
    result = thearpy_collection.aggregate(pipeline=pipeline)

    count = 0

    sum_user_theme = {
        'Personal': 0,
        'Work': 0,
        'Technology': 0,
        'Education': 0,
        'Love': 0
    }
    for response in result:
        count += 1
        for category, value in response['response'].items():
            sum_user_theme[category] += value
        

    average_values = {category: sum_value / count for category, sum_value in sum_user_theme.items()}


    return average_values

def engagement_factor(token: str):
    W1 = W2 = 0.5
    utt_count = 1
    interaction_time = 1
    avg_platform_utt_count = 1
    avg_platform_interaction_time = 1

    return ( W1 * (utt_count/avg_platform_utt_count)  +  W2 * (interaction_time/avg_platform_interaction_time) ) * 100




@router.get("/{token}")
def get_metrics(token: str):
    return {
        "total_time_user_in_session": total_time_user_in_session(token),
        "list_of_duration_of_each_session": list_of_duration_of_each_session(token),
        "last_session": last_session(token=token),
        "total_session_attended": total_session_attended(token),
        "sentiment_compound": sentiment_compound(token),
        "theme_of_user": theme_of_user(token),
    }
