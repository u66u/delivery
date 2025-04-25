from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User

class UserService(SQLAlchemyAsyncRepositoryService[User]):
    """Handles database operations for users."""

    class UserRepository(SQLAlchemyAsyncRepository[User]):
        """User SQLAlchemy Repository."""

        model_type = User

    repository_type = UserRepository

    async def get_by_tg_id(self, tg_id: int) -> User | None:
        return await self.repository.get_one_or_none(User.tg_id == tg_id)

async def provide_user_service(db_session: AsyncSession) -> AsyncGenerator[UserService]:
    async with UserService.new(db_session) as service:
        yield service