from app.db.models.participation_model import Participation
from app.schemas.dtos.input.participation_input import ParticipationInvitationInput

class ParticipationMapper:
    @staticmethod
    def to_participation_entity(payload: ParticipationInvitationInput):
        data = payload.model_dump()
        # Assurer que le champ 'role' n'est jamais nul avant de créer l'entité
        if data.get("role") is None:
            data["role"] = "invited"
        return Participation(**data)