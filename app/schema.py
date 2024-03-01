from pydantic import BaseModel
from datetime import datetime

# User Model 
class User(BaseModel):
    name: str
    class Config:
        from_attribute = True

class UserResponseModel(User):
    id: str
    created_at: datetime

class UserUpdateModel(BaseModel):
    name: str


# Therapy Model
    
class session(BaseModel):
    session_id: str
    message: str

