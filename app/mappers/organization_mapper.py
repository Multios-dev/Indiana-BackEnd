from app.db.models.contact_model import Contact
from app.schemas.dtos.input.organization_input import CreateOrganizationInput
from app.db.models.organization_model import Organization

class OrganizationMapper:
    @staticmethod
    def to_organization_entity(payload:CreateOrganizationInput) -> Organization:
        data = payload.model_dump(exclude_none=True)
        return Organization(**data)

    @staticmethod
    def to_contact_entity(payload:CreateOrganizationInput, org_id:int) -> Contact:
        if not payload.contact:
            return None
        data = payload.model_dump(exclude_none=True)
        return Contact(org_id=org_id, **data)