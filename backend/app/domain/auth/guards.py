from typing import Any
from litestar.connection import ASGIConnection
from litestar.handlers.base import BaseRouteHandler
from litestar.exceptions import PermissionDeniedException
from litestar.security.jwt import JWTCookieAuth, Token

from app.db.models.user import User
from app.domain.auth.services import provide_auth_service
from app.domain.auth.urls import AUTH_LOGIN, AUTH_SIGNUP, AUTH_TG
from app.domain.user.urls import USER_ME
from app.settings.db import alchemy
from app.settings.jwt import jwt_config
from app.domain.address.urls import ADDRESS_ADD, ADDRESS_DELETE, ADDRESS_LIST_MINE, BASE_ADDRESS, MY_ADDRESSES

async def current_user_from_token(token: Token, connection: ASGIConnection[Any, Any, Any, Any]) -> User | None:
    """Lookup current user from local JWT token.

    Fetches the user information from the database


    Args:
        token (str): JWT Token Object
        connection (ASGIConnection[Any, Any, Any, Any]): ASGI connection.


    Returns:
        User: User record mapped to the JWT identifier
    """
    service = await anext(provide_auth_service(alchemy.provide_session(connection.app.state, connection.scope)))
    user = await service.get_one_or_none(email=token.sub)
    return user if user and user.is_active else None

def requires_active_user(connection: ASGIConnection[Any, Any, Any, Any], _: BaseRouteHandler) -> None:
    """Request requires active user.

    Verifies the request user is active.

    Args:
        connection (ASGIConnection): HTTP Request
        _ (BaseRouteHandler): Route handler

    Raises:
        PermissionDeniedException: Permission denied exception
    """
    if connection.user.is_active:
        return
    msg = "Inactive account"
    raise PermissionDeniedException(msg)

jwt_auth = JWTCookieAuth[User](
    retrieve_user_handler=current_user_from_token,
    token_secret=jwt_config.secret,
    exclude=[AUTH_SIGNUP, AUTH_LOGIN, "/docs", AUTH_TG, USER_ME, ADDRESS_LIST_MINE, ADDRESS_ADD, ADDRESS_DELETE],
)
