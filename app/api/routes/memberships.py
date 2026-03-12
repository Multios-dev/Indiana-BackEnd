from fastapi import APIRouter, Request, Depends, HTTPException

from app.schemas.dtos.input.membership_input import CreateMembershipInput, UpdateMembershipInput
from app.schemas.dtos.output.membership_output import GetMembershipOutput
from app.services.membership_service import MembershipService, get_membership_service

router = APIRouter(prefix="/memberships", tags=["memberships"])

@router.post("", summary="Créer un mandat")
async def create_membership(
        payload: CreateMembershipInput,
        service:MembershipService = Depends(get_membership_service)
):
    try:
        return await service.create_membership(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", summary="Récupérer tous les mandats")
async def get_memberships(
        request: Request,
        service:MembershipService = Depends(get_membership_service)
):
    try:
        filters=dict(request.query_params)
        memberships = await service.get_memberships(filters)

        return [
            GetMembershipOutput(
                id = membership.id,
                user_id = membership.id,
                organization_id = membership.organization_id,
                start_date = membership.start_date,
                end_date = membership.end_date,
                price = membership.price
            )
            for membership in memberships
        ]
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{membership_id}", summary="Récupérer un mandat spécifique")
async def get_membership(
        membership_id: int,
        service:MembershipService = Depends(get_membership_service)
):
    try:
        membership = await service.get_membership_by_id(membership_id)
        return GetMembershipOutput(
            id = membership.id,
            user_id = membership.user_id,
            organization_id = membership.organization_id,
            start_date = membership.start_date,
            end_date = membership.end_date,
            price = membership.price
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{membership_id}", summary="Modifier un mandat")
async def update_membership(
        membership_id: int,
        payload: UpdateMembershipInput,
        service:MembershipService = Depends(get_membership_service)
):
    try:
        return await service.update_membership(membership_id, payload)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))