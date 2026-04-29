from uuid import UUID

from fastapi import APIRouter, Depends
from app.schemas.dtos.input.participation_input import ParticipationUpdateInput
from app.schemas.dtos.output.participation_output import ParticipationOutput
from app.services.participation_service import get_participation_service, ParticipationService

router = APIRouter(prefix="/participations", tags=["participations"])

@router.put("/{participation_id}", response_model=ParticipationOutput)
async def update_participation(
        participation_id: UUID,
        payload:ParticipationUpdateInput,
        service: ParticipationService = Depends(get_participation_service)
):
    return await service.update_participation(participation_id, payload)