from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, Request
from app.schemas.dtos.input.participation_input import ParticipationUpdateInput
from app.schemas.dtos.output.participation_output import ParticipationOutput
from app.services.participation_service import get_participation_service, ParticipationService

router = APIRouter(prefix="/participations", tags=["participations"])

@router.get("/", response_model=List[ParticipationOutput], summary="Récupérer les participations (avec ou sans filtres)")
async def get_all_participations(
        request: Request,
        service: ParticipationService = Depends(get_participation_service)
):
    filters = dict(request.query_params)
    return await service.get_all_participations(filters)

@router.put("/{participation_id}", response_model=ParticipationOutput, summary="Modifier une participation")
async def update_participation(
        participation_id: UUID,
        payload:ParticipationUpdateInput,
        service: ParticipationService = Depends(get_participation_service)
):
    return await service.update_participation(participation_id, payload)

@router.delete("/{participation_id}", response_model=dict, summary="Supprimer une participation")
async def delete_participation(
        participation_id: UUID,
        service: ParticipationService = Depends(get_participation_service)
):
    return await service.delete_participation(participation_id)