from fastapi import APIRouter, Request, Depends

from app.schemas.dtos.input.organization_input import CreateOrganizationInput, UpdateOrganizationInput
from app.schemas.dtos.output.organization_output import OrganizationOutput
from app.services.organization_service import OrganizationService, get_organization_service

router = APIRouter(prefix="/organizations", tags=["organizations"])

@router.post("", response_model=OrganizationOutput, summary="Créer une organisation")
async def create_organization(
        payload: CreateOrganizationInput,
        service: OrganizationService = Depends(get_organization_service)
):
    return await service.create_organization(payload)

@router.get("", response_model=list[OrganizationOutput], summary="Récupérer toutes les organisations")
async def get_organizations(
        request: Request,
        service: OrganizationService = Depends(get_organization_service)
):
    filters = dict(request.query_params) or None
    return await service.get_all_organizations(filters)

@router.get("/{org_id}", response_model=OrganizationOutput, summary="Récupérer une organisation spécifique")
async def get_organization(
        org_id: int,
        service: OrganizationService = Depends(get_organization_service)
):
    return await service.get_organization_by_id(org_id)

@router.put("/{org_id}", response_model=OrganizationOutput, summary="Modifier une organisation")
async def update_organization(
        org_id: int,
        payload: UpdateOrganizationInput,
        service: OrganizationService = Depends(get_organization_service)
):
    return await service.update_organization(org_id, payload)

@router.delete("/{org_id}", status_code=200, response_model=dict, summary="Supprimer une organisation")
async def delete_organization(
        org_id: int,
        service: OrganizationService = Depends(get_organization_service)
):
    return await service.delete_organization(org_id)