from decimal import Decimal
from pydantic import BaseModel, UUID4, Field, ConfigDict
from app.schemas.dtos.output.identifier_output import IdentifierOutput

class ParticipationOutput(BaseModel):
    identifiers: list[IdentifierOutput] = Field(alias="dcterms:identifier")
    user_id: UUID4 = Field(alias="cpsvap:hasParticipant")
    event_id: UUID4  # no D-KMC equivalent (inverse relation), kept for client navigation
    role: str = Field(alias="cpsvap:role")
    price: Decimal | None = Field(default=None, alias="cac:LegalMonetaryTotal")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)