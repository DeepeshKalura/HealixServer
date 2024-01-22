from fastapi import APIRouter, status
from model import UserResponseModel, User
from main import db
from datetime import datetime

db = db["users"]

router = APIRouter(
    prefix="v1/cup/users",
    tags=["Users"],
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponseModel)
def post_user(user: User):

    data = {
        "name": user.name,
        "token": user.token,
        "pyq_score": user.pyq_score,
        "created_at": datetime.now()
    }
    result = db.insert_one(data)
    return {
        "id": str(result.inserted_id),
        **result
    }

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserResponseModel)
def get_user(id: str):
    result = db.find_one({"_id": id})
    return {
        "id": str(result["_id"]),
        **result
    }

# @router.put("/{id}", status_code=status.HTTP_200_OK, response_model=UserResponseModel)
# def put_user(id: str, user: User):
#     result = db.update_one({"_id": id}, {"$set": user.dict()})
#     return {
#         "id": str(result["_id"]),
#         **user.dict()
#     }

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: str):
    db.delete_one({"_id": id})

