from pydantic import BaseModel, UUID4

class AddressOutput(BaseModel):
    id: UUID4
    thoroughfare: str
    box_number: str | None = None
    post_name: str
    post_code: str
    country: str

    model_config = {"from_attributes": True}