from pydantic import BaseModel

class AddressCreateInput(BaseModel):
    thoroughfare: str
    box_number: str | None = None
    post_name: str
    post_code: str
    country: str

class AddressUpdateInput(BaseModel):
    thoroughfare: str | None = None
    box_number: str | None = None
    post_name: str | None = None
    post_code: str | None = None
    country: str | None = None