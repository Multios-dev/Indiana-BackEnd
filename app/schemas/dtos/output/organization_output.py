from pydantic import BaseModel, UUID4, Field, ConfigDict
from app.db.models.enums.organization_type import OrganizationType
from app.schemas.dtos.output.address_output import AddressOutput
from app.schemas.dtos.output.identifier_output import IdentifierOutput

class ContactOutput(BaseModel):
    id: UUID4
    email: str | None = Field(default=None, alias="cpsvap:email")
    phone: str | None = Field(default=None, alias="cpsvap:telephone")
    website: str | None = Field(default=None, alias="cpsvap:contactPage")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

class OrganizationOutput(BaseModel):
    identifiers: list[IdentifierOutput] = Field(alias="dcterms:identifier")
    name: str = Field(alias="skos:prefLabel")
    acronym: str | None = Field(default=None, alias="skos:altLabel")
    purpose: str = Field(alias="org:purpose")
    org_type: OrganizationType = Field(alias="rov:orgType")
    sgp_type: str | None = Field(default=None, alias="dcterms:type")
    billable: bool = Field(alias="sgp:billable")
    is_legal_entity: bool = Field(alias="sgp:isLegalEntity")
    parent_id: UUID4 | None = Field(default=None, alias="org:suborganizationOf")
    contact: ContactOutput | None = Field(default=None, alias="cpsvap:contactPoint")
    address: AddressOutput | None = Field(default=None, alias="cpsvap:hasAddress")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)