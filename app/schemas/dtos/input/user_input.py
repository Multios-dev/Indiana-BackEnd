from pydantic import BaseModel

class UserRegisterInput(BaseModel):
    email: str
    password: str

class UserLoginInput(BaseModel):
    email: str
    password: str