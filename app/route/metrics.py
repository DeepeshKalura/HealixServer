import os
import sys
from dotenv import load_dotenv, find_dotenv
from fastapi import APIRouter

from collections import Counter
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
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
                "thread": {"$push": "$session.thread"}
            }
        },
        {
            "$unwind": "$thread"
        },
        {
            "$project": {
                # "sentiment_compound": "$thread.sentiment_compound"
                "avg_sentiment_compound": {"$avg" : "$thread.sentiment_compound"}
            }
        }
    ]
    result = thearpy_collection.aggregate(pipeline=pipeline)
    l = [i for i in result]
    return l



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
                "user_theme": "$thread.theme"  # Include the response field from each thread
            }
        }
        
    ]
    result = thearpy_collection.aggregate(pipeline=pipeline)

    count = 5

    sum_user_theme = {
        'Personal': 0,
        'Work': 0,
        'Technology': 0,
        'Education': 0,
        'Love': 0
    }

    for res in result:
        print(res)
        for i in res['user_theme']:
            if i in sum_user_theme:
                sum_user_theme[i] +=  res['user_theme'][i]
    for i in sum_user_theme:
        sum_user_theme[i] = sum_user_theme[i] / count
    return sum_user_theme

def every_session_utt_count(token: str):
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
            "$project": {
                    "_id": "$session.session_id",
                    "thread": "$session.thread",
                }
        },
        {
            "$unwind": "$thread"
        },
        {
            "$group": {
                "_id": "$_id",
                "utt_count": {"$sum": 1},
                
            }
        },


    ]
    l = [i for i in thearpy_collection.aggregate(pipeline)]
    return l
    

def user_interaction_time_per_session(token: str):
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
            "$project": {
                # "_id": 0,
                "duration": "$duration"
            }
        }
    ]
    l = [i for i in thearpy_collection.aggregate(pipeline)]
    return l

def platform_utt_count_average():
    pipeline = [
        {
            "$unwind": "$session"
        }, 
        {
            "$project": {
                "_id": "$session.session_id",
                "thread": "$session.thread",
            
            }
        }, 
        {
            "$unwind": "$thread"
        },
        {
            "$project": {
                "_id": "$_id",
                "thread_id": "$thread.thread_id",
            }
        }
    ]

    result = thearpy_collection.aggregate(pipeline)
    id_counts = {}
    for item in result:
        _id = item['_id']
        thread_id = item['thread_id']
        if _id in id_counts:
            id_counts[_id][thread_id] += 1
        else:
            id_counts[_id] = Counter({thread_id: 1})



    # Convert counts to list of dictionaries
    result = [{ '_id': _id, 'counts': counts} for _id, counts in id_counts.items()]

    result_with_counts = [{item['_id']: sum(item['counts'].values())} for item in result]



    sum_of_value = 0
    total = 0
    for i in result_with_counts:
        total += 1
        for key, value in i.items():
            sum_of_value += value

    return (sum_of_value/total) 


def platform_interaction_time_average():
    pipeline = [
        {
            "$project": {
                "token": "$token",
                "session": "$session",
            }
        },
        {
            "$unwind" : "$session"
        }, 
        {
            "$project" : {
                "_id": "$_id",
                "duration": {"$sum": {"$subtract": [{"$toDate": "$session.ended_at"}, {"$toDate": "$session.created_at"}]}},
            }
        }
    
    ]

    result = thearpy_collection.aggregate(pipeline)
    sum_of_duration = 0
    total_session = 0
    for i in result:
        total_session += 1
        sum_of_duration += float(i["duration"])
        

    result = (sum_of_duration/total_session)
    if(result == 0):
        return 1.0
    return result

def engagement_factor(token: str):
    W1 = W2 = 0.5
    t = user_interaction_time_per_session(token)
    # print(t)
    l = every_session_utt_count(token)

    aac = platform_utt_count_average()
    paic = platform_interaction_time_average()
    # print(aac)

    if(aac == 0):
        aac = 1
    if(paic == 0):
        paic = 1

    # print(paic)
    en_fct = []

    for i in t:
        f = (i["_id"])
        for j in l:
            # print(j["_id"])
            if f == j["_id"]:
                temp1 = j["utt_count"] / aac
                temp2 = i["duration"] / paic
                en = W1 * temp1 + W2 * temp2
                en_fct_temp = ({"_id": f, "engagement_factor": str(en)})
                en_fct += [en_fct_temp]
                f = None
        if(f != None):
            en_fct_temp = ({"_id": f, "engagement_factor": str(0.0)})
            en_fct += [en_fct_temp]

    return en_fct




@router.get("/{token}")
def get_metrics(token: str):
    return {
        "total_time_user_in_session": total_time_user_in_session(token),
        "list_of_duration_of_each_session": list_of_duration_of_each_session(token),
        "last_session": last_session(token),
        "total_session_attended": total_session_attended(token),
        "sentiment_compound": sentiment_compound(token),
        # "theme_of_user": theme_of_user(token),
        "engagement_factor": engagement_factor(token)
    }

