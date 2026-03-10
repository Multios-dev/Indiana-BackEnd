from fastapi import APIRouter, Request, Depends, HTTPException

from app.db.models.organization_model import Organization
from app.schemas.dtos.input.create_organization_input import CreateOrganizationInput
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
async def get_all_organizations(
        request:Request,
        service: OrganizationService = Depends(get_organization_service)
):
    try:
        filters = dict(request.query_params)

        if filters:
            organizations = []
        else:
            organizations = await service.get_all_organizations()

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