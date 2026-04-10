from fastapi import APIRouter, Depends, Request
from app.schemas.dtos.output.address_output import AddressOutput
from app.schemas.pagination import PaginationParams
from app.services.address_service import get_address_service, AddressService

router = APIRouter(prefix="/addresses", tags=["addresses"])

@router.get("/", response_model=list[AddressOutput], summary="Get all addresses")
async def get_all_addresses(
        request: Request,
        pagination: PaginationParams = Depends(),
        service: AddressService = Depends(get_address_service)
):
    filters = {
        key: value
        for key, value in request.query_params.items()
        if key not in {"skip", "limit"}
    }
    return await service.get_all_addresses(pagination.skip, pagination.limit, filters)