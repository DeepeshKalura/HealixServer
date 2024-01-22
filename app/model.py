from pydantic import BaseModel


# User Model 
class User(BaseModel):
    name: str
    token: str
    pyq_score: float

class UserRequestMode(User):
    created_at: str


class UserResponseModel(User):
    id: int
    message: str
