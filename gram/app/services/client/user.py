from typing import Optional, Dict, Any, ClassVar, Callable, Awaitable, Dict, cast, Type, List

from app.config import BackendConfig
from app.services.client.base import BaseClient, logger


class UserClient(BaseClient):
    
    async def register_or_get_user(self, tg_user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Register or retrieve a user from the backend."""
        try:
            response = await self.post("/api/auth/tg", json=tg_user_data)
            return response.json()
        except Exception as e:
            logger.error(f"Failed to register/get user: {e}")
            return None
    
    async def get_me(self) -> Optional[Dict[str, Any]]:
        """Get the current user's data."""
        try:
            response = await self.get("/api/users/me")
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get user data: {e}")
            return None
