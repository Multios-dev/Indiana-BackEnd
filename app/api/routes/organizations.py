from fastapi import APIRouter, Request, Depends, HTTPException

from app.schemas.dtos.input.organization_input import CreateOrganizationInput, UpdateOrganizationInput
from app.schemas.dtos.output.organization_output import GetOrganizationOutput
from app.services.organization_service import OrganizationService, get_organization_service

router = APIRouter(prefix="/organizations", tags=["organizations"])

@router.post("", summary="Créer une organisation")
async def create_organization(
        payload:CreateOrganizationInput,
        service:OrganizationService = Depends(get_organization_service)
):
    try:
        return await service.create_organization(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", summary="Récupérer toutes les organisations")
async def get_organizations(
        request:Request,
        service: OrganizationService = Depends(get_organization_service)
):
    try:
        filters = dict(request.query_params)
        organizations = await service.get_all_organizations(filters if filters else None)

        return [
            GetOrganizationOutput(
                id = organization.id,
                name = organization.name,
                acronym = organization.acronym,
                type = organization.type,
                parent_id = organization.parent_id,
                email = organization.email,
                phone = organization.phone,
                website = organization.website,
                street = organization.street,
                city = organization.city,
                zip = organization.zip,
                country = organization.country,
                legal_form = organization.legal_form,
                purpose = organization.purpose,
                billable = organization.billable
            )
            for organization in organizations
        ]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{org_id}", summary="Récupérer une organisation spécicifique")
async def get_organization(
        org_id:int,
        service:OrganizationService = Depends(get_organization_service)
):
    try:
        organization = await service.get_organization_by_id(org_id)
        return organization
    except:
        raise HTTPException(status_code=404, detail="Organization not found")

@router.put("/{org_id}", summary="Modifier une organisation")
async def update_organization(
        org_id: int,
        payload: UpdateOrganizationInput,
        service: OrganizationService = Depends(get_organization_service)
):
    try:
        return await service.update_organization(org_id, payload)
    except ValueError as e:
        message = str(e)

        if message == "Organization not found":
            raise HTTPException(status_code=404, detail=message)

        raise HTTPException(status_code=400, detail=message)

@router.delete("/{org_id}", summary="Supprimer une organisation")
async def delete_organization(
        org_id: int,
        service: OrganizationService = Depends(get_organization_service)
):
    try:
        return await service.delete_organization(org_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))