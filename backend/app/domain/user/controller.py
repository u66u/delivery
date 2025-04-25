from litestar import Controller, get, post, patch, delete, Request
from litestar.di import Provide
from litestar.params import Parameter
from litestar.pagination import OffsetPagination
from litestar.repository.filters import LimitOffset
from litestar.exceptions import HTTPException
from typing import Optional, List
from uuid import UUID

from app.domain.auth.guards import requires_active_user
from app.domain.auth.deps import get_current_user, provide_current_user
from app.domain.user.services import UserService, provide_user_service
from app.db.models.user import User
from app.domain.user.schema import UserCreate, UserResponse, UserUpdate
from app.domain.user.urls import USER_ME
from app.lib.crypt import get_password_hash

class UserController(Controller):
    dependencies = {
        "users_service": Provide(provide_user_service),
        "current_user": Provide(get_current_user)
    }
    tags = ["users"]

    @get(path=USER_ME)
    async def me(self, current_user: User, users_service: UserService) -> UserResponse:
        """User Profile."""
        return users_service.to_schema(current_user, schema_type=UserResponse)