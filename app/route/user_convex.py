import os
import sys
from fastapi import APIRouter, status,  HTTPException
import app.schema as schema 
from convex import Convex


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '')))
import session 

router = APIRouter(
    prefix="/v1/convex/users",  
    tags=["Convex Users"],
)

convex = Convex("http://localhost:3001")

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserResponseModel)
def create_user(user: schema.User):
    data = {
        "name": user.name,
    }
    result = convex.create_user(data)
    return result

    



@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schema.UserResponseModel)
def get_user_with_id(id: str):
    result = convex.get_user(id)
    return result



#? This on is working fine
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_with_token(id: str):
    convex.delete_user(id)
