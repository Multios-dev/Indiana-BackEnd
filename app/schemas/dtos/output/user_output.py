from pydantic import BaseModel
from datetime import date

class UserOutput(BaseModel):
    id:int
    email:str

class GetUserOutput(BaseModel):
    id:int
    firstNames:list[str]
    lastName:str
    birthDate:date
    gender:str
    nationality:str
    street:str
    zip:str
    city:str
    email:str
    phone:str