from app.db.models.membership_model import Membership
from app.schemas.dtos.input.membership_input import CreateMembershipInput

class MembershipMapper:
    @staticmethod
    def to_membership_entity(payload: CreateMembershipInput) -> Membership:
        data = payload.model_dump(
            exclude_none=True
        )
        return Membership(**data)