from pydantic import BaseModel, Field, ConfigDict


class IdentifierOutput(BaseModel):
    creator: str = Field(alias="dcterms:creator")
    notation: str = Field(alias="skos:notation")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)
