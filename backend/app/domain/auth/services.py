from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from collections.abc import AsyncGenerator
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from litestar.exceptions import PermissionDeniedException
from app.db.models.user import User
from app.lib import crypt

class AuthService(SQLAlchemyAsyncRepositoryService[User]):
    """Handles database operations for users."""

    class AuthRepository(SQLAlchemyAsyncRepository[User]):
        """User SQLAlchemy Repository."""

        model_type = User

    repository_type = AuthRepository

    async def authenticate_jwt(self, email: EmailStr, password: bytes | str) -> User:
        """Authenticate a user against the stored hashed password."""
        db_obj = await self.get_one_or_none(email=email)
        if db_obj is None:
            msg = "User not found or password invalid"
            raise PermissionDeniedException(detail=msg)
        if db_obj.hashed_password is None:
            msg = "User not found or password invalid."
            raise PermissionDeniedException(detail=msg)
        if not await crypt.verify_password(password, db_obj.hashed_password):
            msg = "User not found or password invalid"
            raise PermissionDeniedException(detail=msg)
        if not db_obj.is_active:
            msg = "User account is inactive"
            raise PermissionDeniedException(detail=msg)
        return db_obj

async def provide_auth_service(db_session: AsyncSession) -> AsyncGenerator[AuthService]:
    async with AuthService.new(db_session) as service:
        yield service