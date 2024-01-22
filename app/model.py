from pydantic import BaseModel


# User Model 
class User(BaseModel):
    name: str
    token: str
    pyq_score: float



class UserResponseModel(User):
    id: int
    created_at: str
