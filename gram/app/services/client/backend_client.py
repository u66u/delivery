import httpx
from typing import Optional, Dict, Any
import logging

from app.config import bot_config, backend_config

logger = logging.getLogger(__name__)

# Consider using a context manager or dependency injection for the client in a real app
# for better resource management (e.g., lifespan events in Litestar/FastAPI).
# For simplicity here, we create a global client instance.

_backend_client: Optional[httpx.AsyncClient] = None

def get_backend_client() -> httpx.AsyncClient:
    """Returns a shared httpx.AsyncClient instance."""
    global _backend_client
    if _backend_client is None:
        _backend_client = httpx.AsyncClient(
            base_url=backend_config.url,
            headers={
                "X-Bot-Secret": bot_config.secret_token,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=10.0, # Example timeout
        )
    return _backend_client

async def register_or_get_user_in_backend(tg_user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Sends Telegram user data to the backend to register or retrieve the user.

    Args:
        tg_user_data: A dictionary containing Telegram user info (e.g., id, username, first_name).

    Returns:
        The user data dictionary from the backend response if successful, otherwise None.
    """
    client = get_backend_client()
    auth_endpoint = "/api/auth/tg"

    try:
        response = await client.post(auth_endpoint, json=tg_user_data)
        response.raise_for_status() # Raise an exception for 4xx or 5xx status codes
        logger.info(f"Backend response cookies: {response.cookies}")
        return response.json()
    except httpx.RequestError as exc:
        logger.error(f"HTTP Request error occurred while calling {exc.request.url!r}: {exc}")
    except httpx.HTTPStatusError as exc:
        logger.error(
            f"HTTP Status error {exc.response.status_code} occurred while calling {exc.request.url!r}. "
            f"Response: {exc.response.text}"
        )
    except Exception as e:
        logger.exception(f"An unexpected error occurred during backend communication: {e}")

    return None

async def get_me(tg_user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    client = get_backend_client()
    auth_endpoint = "/api/users/me"

    try:
        response = await client.get(auth_endpoint)
        response.raise_for_status() # Raise an exception for 4xx or 5xx status codes
        logger.info(f"Backend response cookies: {response.cookies}")
        return response.json()
    except httpx.RequestError as exc:
        logger.error(f"HTTP Request error occurred while calling {exc.request.url!r}: {exc}")
    except httpx.HTTPStatusError as exc:
        logger.error(
            f"HTTP Status error {exc.response.status_code} occurred while calling {exc.request.url!r}. "
            f"Response: {exc.response.text}"
        )
    except Exception as e:
        logger.exception(f"An unexpected error occurred during backend communication: {e}")

    return None


async def close_backend_client():
    """Closes the shared httpx.AsyncClient."""
    global _backend_client
    if _backend_client:
        await _backend_client.aclose()
        _backend_client = None

# Example Usage (within an async function in your bot handlers):
# from aiogram import types
# async def handle_start(message: types.Message):
#     user_info = {
#         "telegram_id": message.from_user.id,
#         "username": message.from_user.username,
#         "first_name": message.from_user.first_name,
#         "last_name": message.from_user.last_name,
#         # Add any other relevant fields
#     }
#     backend_user = await register_or_get_user_in_backend(user_info)
#     if backend_user:
#         await message.answer(f"Successfully synced with backend. Backend User ID: {backend_user.get('id')}")
#     else:
#         await message.answer("Could not sync user with backend.")

# Remember to call close_backend_client() during bot shutdown (e.g., using lifespan events if available). 