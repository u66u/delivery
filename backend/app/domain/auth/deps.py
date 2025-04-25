from typing import Any, AsyncGenerator, Annotated, Optional
from litestar import Request
from litestar.connection import ASGIConnection
from litestar.exceptions import HTTPException
from litestar.params import Dependency
from litestar.security.jwt import Token

from app.db.models.user import User
from app.settings.tg import tg_config
from app.domain.auth.services import AuthService, provide_auth_service
from app.settings.db import alchemy

async def provide_current_user(request: Request) -> AsyncGenerator[User, None]:
    """Provide the current authenticated user.
    
    Args:
        request: The request object which contains the authenticated user
        
    Yields:
        The current user
    """
    yield request.user

async def verify_tg_bot_token(request: Request) -> AsyncGenerator[bool, None]:
    expected_token = tg_config.bot_secret_token
    received_token = request.headers.get("X-Bot-Secret")
    if not received_token or received_token != expected_token:
        raise HTTPException(status_code=401, detail="Invalid Telegram bot token")
    return True

async def get_current_user(
    request: Request,
) -> User:
    """Get the current user from either JWT token or Telegram authentication.
    
    Args:
        connection: The ASGI connection
        auth_service: Auth service instance (optional, will be provided if not passed)
        
    Returns:
        The current authenticated user
        
    Raises:
        HTTPException: If no user is authenticated
    """
    # if hasattr(request, "user") and request.user is not None:
    #     return request.user
    
    # If not JWT authenticated, try to get auth_service if not provided
    auth_service = await anext(provide_auth_service(
        alchemy.provide_session(request.app.state, request.scope)
    ))
    
    is_token_valid = await verify_tg_bot_token(request)
    if not is_token_valid:
        raise HTTPException(status_code=401, detail="Invalid Telegram bot token")
    
    tg_id = request.cookies.get("tg_id") or request.headers.get("X-Tg-Id")
    tg_id = int(tg_id) if tg_id else None
    if tg_id:
        user: User | None = await auth_service.repository.get_one_or_none(User.tg_id == tg_id)
        if user and user.is_active:
            return user
    
    raise HTTPException(status_code=401, detail="Not authenticated")
