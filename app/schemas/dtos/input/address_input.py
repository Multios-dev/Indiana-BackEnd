from pydantic import BaseModel, field_validator

class AddressCreateInput(BaseModel):
    thoroughfare: str
    box_number: str | None = None
    post_name: str
    post_code: str
    country: str

    @field_validator("country")
    @classmethod
    def validate_country(cls, v):
        if not v.isupper() or len(v) != 2:
            raise ValueError("Country must be an ISO 3166-1 alpha-2 code (e.g. 'BE', 'FR')")
        return v

class AddressUpdateInput(BaseModel):
    thoroughfare: str | None = None
    box_number: str | None = None
    post_name: str | None = None
    post_code: str | None = None
    country: str | None = None

    @field_validator("country")
    @classmethod
    def validate_country(cls, v):
        if not v.isupper() or len(v) != 2:
            raise ValueError("Country must be an ISO 3166-1 alpha-2 code (e.g. 'BE', 'FR')")
        return v