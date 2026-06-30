from pydantic import BaseModel, UUID4, Field, ConfigDict
from datetime import date
from decimal import Decimal
from app.schemas.dtos.output.identifier_output import IdentifierOutput

class MembershipOutput(BaseModel):
    identifiers: list[IdentifierOutput] = Field(alias="dcterms:identifier")
    user_id: UUID4 = Field(alias="org:member")
    organization_id: UUID4 = Field(alias="org:organization")
    role: str = Field(alias="org:role")
    # start_date and end_date are structural (should form org:memberDuring time:Interval), to be addressed in a later pass
    start_date: date
    end_date: date | None = None
    price: Decimal | None = Field(default=None, alias="cac:LegalMonetaryTotal")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)