from typing import List
from fastapi import APIRouter, Request
from fastapi.params import Depends
from app.schemas.dtos.input.event_input import CreateEventInput, UpdateEventInput
from app.schemas.dtos.output.event_output import EventOutput
from app.services.event_service import get_event_service, EventService

router = APIRouter(prefix="/events", tags=["events"])

@router.post("/", response_model=EventOutput, summary="Créer un événement")
async def create_event(
        payload:CreateEventInput,
        service: EventService = Depends(get_event_service)
):
    return await service.create_event(payload)

@router.get("/", response_model=List[EventOutput], summary="Récupérer tous les événements")
async def get_all_events(
        request:Request,
        service: EventService = Depends(get_event_service)
):
    filters = dict(request.query_params) or None
    return await service.get_all_events(filters)

@router.get("/{event_id}", response_model=EventOutput, summary="Récupérer un événement spécifique")
async def get_event_by_id(
        event_id:int,
        service: EventService = Depends(get_event_service)
):
    return await service.get_event_by_id(event_id)

@router.put("/{event_id}", response_model=EventOutput, summary="Modifier un événement")
async def update_event(
        event_id:int,
        payload:UpdateEventInput,
        service: EventService = Depends(get_event_service)
):
    return await service.update_event(event_id, payload)

@router.delete("/{event_id}", response_model=EventOutput, summary="Supprimer un événement")
async def delete_event(
        event_id:int,
        service: EventService = Depends(get_event_service)
):
    return await service.delete_event(event_id)