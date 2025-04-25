from litestar import Controller, get, post, patch, delete, Request
from litestar.di import Provide
from litestar.params import Parameter
from litestar.pagination import OffsetPagination
from litestar.repository.filters import LimitOffset
from litestar.exceptions import HTTPException
from typing import Optional, List
from uuid import UUID

from app.domain.address.services import AddressService, provide_address_service
from app.domain.auth.deps import get_current_user, provide_current_user
from app.db.models.user import User
from app.domain.address.schema import AddressResponse, NewAddress
from app.domain.address.urls import ADDRESS_ADD, ADDRESS_LIST_MINE, ADDRESS_DELETE
from app.db.models.address import Address

class AddressController(Controller):
    dependencies = {
        "address_service": Provide(provide_address_service),
        "current_user": Provide(get_current_user)
    }
    tags = ["addresses"]

    @post(path=ADDRESS_ADD, status_code=201)
    async def add_address(self, current_user: User, address_service: AddressService, data: NewAddress) -> AddressResponse:
        data_dict = data.model_dump(exclude_unset=False)
        data_dict["user_id"] = current_user.id
        
        address = await address_service.create(data_dict)
        return address_service.to_schema(address, schema_type=AddressResponse)
    
    @get(path=ADDRESS_LIST_MINE, status_code=200)
    async def get_my_addresss(self, current_user: User, address_service: AddressService) -> List[AddressResponse]:
        addresses = await address_service.list(Address.user_id == current_user.id)
        return [address_service.to_schema(address, schema_type=AddressResponse) for address in addresses]
    
    @delete(path=ADDRESS_DELETE, status_code=204)
    async def delete_my_address(self, current_user: User, address_service: AddressService, id: UUID) -> None:
        address = await address_service.get_one_or_none(Address.id == id)
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")
        if address.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="You don't have permission to delete this address")
        await address_service.delete(id)
        return None
