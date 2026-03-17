from fastapi import APIRouter, Request, Depends

from app.schemas.dtos.input.membership_input import CreateMembershipInput, UpdateMembershipInput
from app.schemas.dtos.output.membership_output import MembershipOutput
from app.services.membership_service import MembershipService, get_membership_service

router = APIRouter(prefix="/memberships", tags=["memberships"])

@router.post("/", summary="Créer un mandat")
async def create_membership(
        payload: CreateMembershipInput,
        service: MembershipService = Depends(get_membership_service)
):
    membership = await service.create_membership(payload)
    return MembershipOutput.model_validate(membership)

@router.get("/", summary="Récupérer tous les mandats")
async def get_memberships(
        request: Request,
        service: MembershipService = Depends(get_membership_service)
):
    filters = dict(request.query_params)
    memberships = await service.get_memberships(filters if filters else None)
    return [MembershipOutput.model_validate(m) for m in memberships]

@router.get("/{membership_id}", summary="Récupérer un mandat spécifique")
async def get_membership(
        membership_id: int,
        service: MembershipService = Depends(get_membership_service)
):
    membership = await service.get_membership_by_id(membership_id)
    return MembershipOutput.model_validate(membership)

@router.put("/{membership_id}", summary="Modifier un mandat")
async def update_membership(
        membership_id: int,
        payload: UpdateMembershipInput,
        service: MembershipService = Depends(get_membership_service)
):
    membership = await service.update_membership(membership_id, payload)
    return MembershipOutput.model_validate(membership)

@router.delete("/{membership_id}", summary="Supprimer un mandat")
async def delete_membership(
        membership_id: int,
        service: MembershipService = Depends(get_membership_service)
):
    membership = await service.delete_membership(membership_id)
    return MembershipOutput.model_validate(membership)