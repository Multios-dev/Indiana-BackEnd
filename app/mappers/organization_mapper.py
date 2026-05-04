from app.db.models.contact_model import Contact
from app.schemas.dtos.input.organization_input import CreateOrganizationInput
from app.db.models.organization_model import Organization
from app.db.models.address_model import Address

class OrganizationMapper:
    @staticmethod
    def to_organization_entity(payload: CreateOrganizationInput) -> Organization:
        data = payload.model_dump(exclude_none=True, exclude={"contact", "address"})
        return Organization(**data)

    @staticmethod
    def to_contact_entity(payload:CreateOrganizationInput, org_id:int) -> Contact | None:
        if not payload.contact:
            return None
        data = payload.contact.model_dump(exclude_none=True)
        return Contact(org_id=org_id, **data)

    @staticmethod
    def to_address_entity(address_payload) -> Address | None:
        data = address_payload.model_dump(exclude_none=True)
        return Address(**data)