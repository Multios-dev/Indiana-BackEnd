from pydantic import BaseModel
from datetime import date

class UserRegisterInput(BaseModel):
    firstNames: list[str]
    lastName:str
    birthDate: date
    gender:str
    nationality:str
    street:str
    zip:str
    city:str
    email:str
    phone:str

class UserLoginInput(BaseModel):
    email: str
    password: str

class UserUpdateInput(BaseModel):
    firstNames: list[str]
    lastName: str
    birthDate: date
    gender: str
    nationality: str
    street: str
    zip: str
    city: str
    email: str
    phone: str

class UserCreateInput(BaseModel):
    firstNames: list[str]
    lastName:str
    birthDate: date
    gender:str
    nationality:str
    street:str
    zip:str
    city:str
    email:str
    phone:str