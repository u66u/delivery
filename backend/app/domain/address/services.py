from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.address import Address

class AddressService(SQLAlchemyAsyncRepositoryService[Address]):
    """Handles database operations for addresses."""

    class AddressRepository(SQLAlchemyAsyncRepository[Address]):
        """Address SQLAlchemy Repository."""

        model_type = Address

    repository_type = AddressRepository

async def provide_address_service(db_session: AsyncSession) -> AsyncGenerator[AddressService]:
    async with AddressService.new(db_session) as service:
        yield service