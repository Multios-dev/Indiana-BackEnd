from datetime import date

from pydantic import BaseModel

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