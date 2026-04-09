from pydantic import BaseModel, UUID4
from datetime import date
from app.schemas.dtos.output.address_output import AddressOutput

class ContactOutput(BaseModel):
    id: UUID4
    email:str | None = None
    phone:str | None = None
    website:str | None = None

    # Allows Pydantic to read attributes from a SQLAlchemy object directly
    # without this, Pydantic cannot convert an ORM object to a Pydantic model

class UserOutput(BaseModel):
    id: UUID4
    first_names: list[str]
    last_name: str
    birth_date: date | None = None
    gender: str | None = None
    totem: str | None = None
    quali: str | None = None
    is_legal_guardian: bool
    contact: ContactOutput | None = None
    home_address: AddressOutput | None = None
    residential_address: AddressOutput | None = None

    model_config = {"from_attributes": True}