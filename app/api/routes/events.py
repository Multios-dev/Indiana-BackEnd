from typing import List
from fastapi import APIRouter, Request
from fastapi.params import Depends
from app.schemas.dtos.input.event_input import CreateEventInput, UpdateEventInput
from app.schemas.dtos.input.participation_input import ParticipationInvitationInput
from app.schemas.dtos.output.event_output import EventOutput
from app.schemas.pagination import PaginationParams
from app.services.event_service import get_event_service, EventService
from uuid import UUID
from app.services.participation_service import ParticipationService, get_participation_service

router = APIRouter(prefix="/events", tags=["events"])

@router.post("/", response_model=EventOutput, summary="Créer un événement")
async def create_event(
        payload:CreateEventInput,
        service: EventService = Depends(get_event_service)
):
    return await service.create_event(payload)

@router.post("/invite", response_model=dict, summary="Inviter un utilisateur à un événement")
async def invite_to_event(
        payload: ParticipationInvitationInput,
        service: ParticipationService = Depends(get_participation_service)
):
    return await service.invite_to_event(payload)

@router.get("/", response_model=List[EventOutput], summary="Récupérer tous les événements")
async def get_all_events(
        request:Request,
        pagination: PaginationParams = Depends(),
        service: EventService = Depends(get_event_service)
):
    filters = {
        key: value
        for key, value in request.query_params.items()
        if key not in {"skip", "limit"}
    }
    return await service.get_all_events(pagination.skip, pagination.limit, filters)

@router.get("/count", response_model=int, summary="Récupérer le nombre d'événements")
async def count_events(
        service: EventService = Depends(get_event_service)
):
    return await service.count_events()

@router.get("/{event_id}", response_model=EventOutput, summary="Récupérer un événement spécifique")
async def get_event_by_id(
        event_id:UUID,
        service: EventService = Depends(get_event_service)
):
    return await service.get_event_by_id(event_id)

@router.put("/{event_id}", response_model=EventOutput, summary="Modifier un événement")
async def update_event(
        event_id:UUID,
        payload:UpdateEventInput,
        service: EventService = Depends(get_event_service)
):
    return await service.update_event(event_id, payload)

@router.delete("/{event_id}", status_code=200, response_model=dict, summary="Supprimer un événement")
async def delete_event(
        event_id:UUID,
        service: EventService = Depends(get_event_service)
):
    return await service.delete_event(event_id)