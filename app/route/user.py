import os
import sys
from fastapi import APIRouter, status,  HTTPException
import app.schema as schema 
from datetime import  datetime
from pymongo.mongo_client import MongoClient
from typing import List

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '')))
import session 

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

name=os.getenv("MONGO_NAME")
password=os.getenv("MONGO_PASSWORD")

uri = f"mongodb+srv://{name}:{password}@cluster1.ussxiyu.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri)

db = client["dev"]
collection = db["users"]

router = APIRouter(
    prefix="/v1/cup/users",  
    tags=["Users"],
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserResponseModel)
def post_user(user: schema.User):
    data = {
        "name": user.name,
        "token": user.token,
        "pyq_score": user.pyq_score,
        "created_at": datetime.now().isoformat()
    }
    intermediateResult = collection.find_one({"token": user.token})
    if(intermediateResult != None):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with token {user.token} already exists"
        )
    else:
        ack_id = collection.insert_one(data)
        session.thearpy_to_user(user.token)  
        if(ack_id.acknowledged == True):
            result = collection.find_one({"_id": ack_id.inserted_id})
            result["id"] = str(result.pop("_id"))
            return result
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error in inserting the data"
            )

# @router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schema.UserResponseModel)
# def get_user(id: str):
#     documentId = ObjectId(id)
#     result = collection.find_one({"_id": documentId})
#     if (result == None):
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"User with id {id} not found"
#         )
#     result.pop("_id")
#     return {
#         "id": id,
#         **result
#     }

@router.get("/{token}", status_code=status.HTTP_200_OK, response_model=schema.UserResponseModel)
def get_user_with_token(token: str):
    result = collection.find_one({"token": token})
    if (result == None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with token {token} not found"
        )
    result["id"] = str(result.pop("_id"))
    return result

# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_user(id: str):
#     result = collection.delete_one({"_id": id})
#     if(result.acknowledged == True and result.deleted_count == 0):
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"User with id {id} not found"
#         )
#     elif(result.acknowledged == False):
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail="Error in deleting the data"
#         )

#? This on is working fine
@router.delete("/{token}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_with_token(token: str):
    result = collection.delete_one({"token": token})
    if(result.acknowledged == True and result.deleted_count == 0):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with token {token} not found"
        )
    elif(result.acknowledged == False):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error in deleting the data"
        )

#? This one is working fine
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schema.UserResponseModel])
def get_all_users():
    result = collection.find()
    if(result == None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No users found"
        )
    result = list(result)
    for user in result:
        user["id"] = str(user.pop("_id"))
        
    return result

@router.patch("/{token}", status_code=status.HTTP_200_OK, response_model=schema.UserResponseModel)
def patch_name(token: str, user: schema.UserUpdateModel):
    result = collection.update_one({"token": token}, {"$set": {"name": user.name, "pyq_score": user.pyq_score}})
    if (result == None):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with token {token} not found"
        )
    result = collection.find_one({"token": token})
    for user in result:
        user["id"] = str(user.pop("_id")) 
    return result