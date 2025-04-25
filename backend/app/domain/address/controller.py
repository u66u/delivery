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
from app.domain.address.urls import ADD_ADDRESS

class AddressController(Controller):
    dependencies = {
        "address_service": Provide(provide_address_service),
        "current_user": Provide(get_current_user)
    }
    tags = ["addresses"]

    @post(path=ADD_ADDRESS)
    async def add_address(self, current_user: User, address_service: AddressService, data: NewAddress) -> AddressResponse:
        """Add a new address."""
        data_dict = data.model_dump(exclude_unset=False)
        data_dict["user_id"] = current_user.id
        
        address = await address_service.create(data_dict)
        
        return address_service.to_schema(address, schema_type=AddressResponse)