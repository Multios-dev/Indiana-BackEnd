from pydantic import BaseModel

class UserOutput(BaseModel):
    id:int
    email:str