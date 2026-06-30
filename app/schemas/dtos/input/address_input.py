from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
import pycountry
import re

from app.core.communes import BE_COMMUNES

# Postal code patterns by country, extend as needed
POSTAL_CODE_PATTERNS: dict[str, re.Pattern] = {
    "BE": re.compile(r"^[1-9][0-9]{3}$"),
    "FR": re.compile(r"^[0-9]{5}$"),
    "LU": re.compile(r"^[0-9]{4}$"),
    "NL": re.compile(r"^[0-9]{4}\s?[A-Z]{2}$"),
    "DE": re.compile(r"^[0-9]{5}$"),
    "GB": re.compile(r"^[A-Z]{1,2}[0-9][0-9A-Z]?\s?[0-9][A-Z]{2}$"),
}
_GENERIC_POSTAL_CODE = re.compile(r"^[A-Z0-9\s\-]{2,10}$", re.IGNORECASE)


class AddressCreateInput(BaseModel):
    thoroughfare: str = Field(..., alias="locn:thoroughfare")
    box_number: str | None = Field(default=None, alias="locn:poBox")
    post_name: str = Field(..., alias="locn:postName")
    post_code: str = Field(..., alias="locn:postCode")
    country: str = Field(..., alias="locn:adminUnitL1")
    model_config = ConfigDict(populate_by_name=True)

    @field_validator("country")
    @classmethod
    def validate_country(cls, v):
        if pycountry.countries.get(alpha_2=v) is None:
            raise ValueError("Country must be a valid ISO 3166-1 alpha-2 code (e.g. 'BE', 'FR')")
        return v

    @field_validator("post_name")
    @classmethod
    def validate_post_name(cls, v):
        stripped = v.strip()
        if not stripped:
            raise ValueError("City name is required")
        if len(stripped) > 100:
            raise ValueError("City name is too long")
        if stripped.isdigit():
            raise ValueError("City name is invalid")
        return stripped

    @model_validator(mode="after")
    def validate_post_code_and_name(self):
        country = self.country
        post_code = self.post_code
        post_name = self.post_name
        if country and post_code:
            pattern = POSTAL_CODE_PATTERNS.get(country, _GENERIC_POSTAL_CODE)
            if not pattern.match(post_code):
                raise ValueError("Invalid postal code for the selected country")
        if country == "BE" and post_name and post_name.strip().lower() not in BE_COMMUNES:
            raise ValueError("Unknown Belgian commune name")
        return self


class AddressUpdateInput(BaseModel):
    thoroughfare: str | None = Field(default=None, alias="locn:thoroughfare")
    box_number: str | None = Field(default=None, alias="locn:poBox")
    post_name: str | None = Field(default=None, alias="locn:postName")
    post_code: str | None = Field(default=None, alias="locn:postCode")
    country: str | None = Field(default=None, alias="locn:adminUnitL1")
    model_config = ConfigDict(populate_by_name=True)

    @field_validator("country")
    @classmethod
    def validate_country(cls, v):
        if v is not None and pycountry.countries.get(alpha_2=v) is None:
            raise ValueError("Country must be a valid ISO 3166-1 alpha-2 code (e.g. 'BE', 'FR')")
        return v

    @field_validator("post_name")
    @classmethod
    def validate_post_name(cls, v):
        if v is None:
            return v
        stripped = v.strip()
        if not stripped:
            raise ValueError("City name is required")
        if len(stripped) > 100:
            raise ValueError("City name is too long")
        if stripped.isdigit():
            raise ValueError("City name is invalid")
        return stripped

    @model_validator(mode="after")
    def validate_post_code_and_name(self):
        country = self.country
        post_code = self.post_code
        post_name = self.post_name
        if country and post_code:
            pattern = POSTAL_CODE_PATTERNS.get(country, _GENERIC_POSTAL_CODE)
            if not pattern.match(post_code):
                raise ValueError("Invalid postal code for the selected country")
        if country == "BE" and post_name and post_name.strip().lower() not in BE_COMMUNES:
            raise ValueError("Unknown Belgian commune name")
        return self