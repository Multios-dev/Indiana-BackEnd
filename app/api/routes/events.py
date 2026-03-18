from typing import List

from fastapi import APIRouter, Request
from fastapi.params import Depends

from app.db.models.event_model import Event
from app.schemas.dtos.output.event_output import EventOutput
from app.services.event_service import get_event_service, EventService

router = APIRouter(prefix="/events", tags=["events"])

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