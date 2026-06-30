from pydantic import BaseModel, UUID4, Field, ConfigDict

class AddressOutput(BaseModel):
    id: UUID4
    thoroughfare: str = Field(alias="locn:thoroughfare")
    box_number: str | None = Field(default=None, alias="locn:poBox")
    post_name: str = Field(alias="locn:postName")
    post_code: str = Field(alias="locn:postCode")
    country: str = Field(alias="locn:adminUnitL1")
    address_id: str | None = Field(default=None, alias="locn:addressId")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)