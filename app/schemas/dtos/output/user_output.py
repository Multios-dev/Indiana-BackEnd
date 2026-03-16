from pydantic import BaseModel
from datetime import date

class UserOutput(BaseModel):
    id: int
    first_names: list[str]
    last_name: str
    birth_date: date | None
    gender: str | None
    totem: str | None
    quali: str | None
    is_legal_guardian: bool

    class Config:
        from_attributes = True