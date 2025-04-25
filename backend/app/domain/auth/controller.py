from litestar import Controller, Request, Response, get, post, patch, delete
from litestar.di import Provide
from litestar.params import Parameter
from litestar.pagination import OffsetPagination
from litestar.repository.filters import LimitOffset
from litestar.exceptions import HTTPException
from typing import Optional, List
from uuid import UUID

from app.domain.auth.deps import verify_tg_bot_token
from app.domain.auth.schema import AuthLogin, TgAuthLogin, AuthSignUp
from app.domain.auth.services import AuthService, provide_auth_service
from app.domain.auth.urls import AUTH_SIGNUP, AUTH_LOGIN, AUTH_TG
from app.domain.auth.guards import jwt_auth
from app.domain.user.services import UserService
from app.db.models.user import User
from app.domain.user.schema import UserCreate, UserResponse, UserUpdate
from litestar.datastructures import Cookie
from app.lib.crypt import get_password_hash

class AuthController(Controller):
    dependencies = {
        "auth_service": Provide(provide_auth_service),
        "validate_bot_token": Provide(verify_tg_bot_token)
    }
    tags = ["auth"]

    @post(AUTH_SIGNUP, status_code=200)
    async def signup(
        self,
        auth_service: AuthService,
        data: AuthSignUp
    ) -> UserResponse:
        exists = await auth_service.repository.get_one_or_none(User.email == data.email)
        if exists:
            raise HTTPException(status_code=400, detail="User already exists")
        data = data.model_dump(exclude_unset=False)
        data["hashed_password"] = await get_password_hash(data["password"])
        x = await auth_service.create(data)
        return auth_service.to_schema(x, schema_type=UserResponse)

    
    @post(AUTH_LOGIN, status_code=200)
    async def login(
        self,
        auth_service: AuthService,
        data: AuthLogin
    ) -> UserResponse:
        user = await auth_service.authenticate_jwt(data.email, data.password)
        return jwt_auth.login(user.email)

    
    @post(AUTH_TG, status_code=200)
    async def tg_login(
        self,
        validate_bot_token: bool,
        auth_service: AuthService,
        data: TgAuthLogin
    ) -> Response[UserResponse]:
        if not validate_bot_token:
            raise HTTPException(status_code=401, detail="Invalid Telegram bot token")
        user = await auth_service.repository.get_one_or_none(User.tg_id == data.tg_id)
        if user is None:
            user = await auth_service.create(data.model_dump(exclude_unset=False))
        data = auth_service.to_schema(user, schema_type=UserResponse)
        return Response(content=data, 
                        headers={"X-Tg-Id": str(data.tg_id)},
                        cookies=[Cookie(key="tg_id", value=str(data.tg_id))])
