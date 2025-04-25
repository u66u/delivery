import httpx
from typing import Optional, Dict, Any, ClassVar, Callable, Awaitable, Dict, cast, Type, List
import logging

from app.config import bot_config, backend_config

logger = logging.getLogger(__name__)

class BaseClient:

    base_url = backend_config.url
    headers: ClassVar[Dict[str, str]] = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Bot-Secret": bot_config.secret_token,
    }
    default_timeout: ClassVar[float] = 10.0
    
    def __init__(self):
        self._client: Optional[httpx.AsyncClient] = None
    
    @property
    def client(self) -> httpx.AsyncClient:
        """Lazy initialization of the httpx client."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers=self.headers,
                timeout=self.default_timeout,
            )
        return self._client
    
    async def close(self):
        """Close the client connection."""
        if self._client:
            await self._client.aclose()
            self._client = None
    
    async def get(self, url: str, **kwargs) -> httpx.Response:
        """Send a GET request."""
        try:
            response = await self.client.get(url, **kwargs)
            response.raise_for_status()
            return response
        except Exception as e:
            logger.error(f"Error during GET request to {url}: {e}")
            raise
    
    async def post(self, url: str, **kwargs) -> httpx.Response:
        """Send a POST request."""
        try:
            response = await self.client.post(url, **kwargs)
            response.raise_for_status()
            return response
        except Exception as e:
            logger.error(f"Error during POST request to {url}: {e}")
            raise

