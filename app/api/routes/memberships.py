from fastapi import APIRouter, Request, Depends
from app.schemas.dtos.input.membership_input import CreateMembershipInput, UpdateMembershipInput
from app.schemas.dtos.output.membership_output import MembershipOutput
from app.services.membership_service import MembershipService, get_membership_service
from uuid import UUID

router = APIRouter(prefix="/memberships", tags=["memberships"])

@router.post("/", response_model=MembershipOutput, summary="Créer un mandat")
async def create_membership(
        payload: CreateMembershipInput,
        service: MembershipService = Depends(get_membership_service)
):
    return await service.create_membership(payload)

@router.get("/", response_model=list[MembershipOutput], summary="Récupérer tous les mandats")
async def get_memberships(
        request: Request,
        service: MembershipService = Depends(get_membership_service)
):
    filters = dict(request.query_params) or None
    return await service.get_memberships(filters)

@router.get("/{membership_id}", response_model=MembershipOutput, summary="Récupérer un mandat spécifique")
async def get_membership(
        membership_id: UUID,
        service: MembershipService = Depends(get_membership_service)
):
    return await service.get_membership_by_id(membership_id)

@router.put("/{membership_id}", response_model=MembershipOutput, summary="Modifier un mandat")
async def update_membership(
        membership_id: UUID,
        payload: UpdateMembershipInput,
        service: MembershipService = Depends(get_membership_service)
):
    return await service.update_membership(membership_id, payload)

@router.delete("/{membership_id}", status_code=200, response_model=dict, summary="Supprimer un mandat")
async def delete_membership(
        membership_id: int,
        service: MembershipService = Depends(get_membership_service)
):
    return await service.delete_membership(membership_id)