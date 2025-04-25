from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import TelegramObject
from typing import Any, Dict, Callable, Awaitable, List, Type

from app.services.client.base import BaseClient

class ClientMiddleware(BaseMiddleware):
    """Middleware that injects clients into handler data."""
    
    def __init__(self, client_classes: List[Type[BaseClient]]):
        self.client_classes = client_classes
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        for client_class in self.client_classes:
            class_name = client_class.__name__
            param_name = class_name[0].lower() + class_name[1:]
            if param_name.endswith("Client"):
                param_name = param_name[:-6]
            
            # Make client available by both type annotation and parameter name
            client = get_client(client_class)
            data[client_class.__name__] = client
            data[param_name] = client
            
            print(f"Adding client {client_class.__name__} as {param_name}")
        
        print(f"Data keys: {list(data.keys())}")
        
        return await handler(event, data)


def setup_client_middleware(dp: Dispatcher, client_classes: List[Type[BaseClient]] | None = None):
    """Set up the client middleware for a dispatcher with specified client classes."""
    if client_classes is None:
        # Default to BaseCLient if no classes specified
        client_classes = [BaseClient]
    
    dp.update.middleware(ClientMiddleware(client_classes))


class ClientRegistry:
    """Registry for managing multiple client instances."""
    
    def __init__(self):
        self._clients: Dict[Type[BaseClient], BaseClient] = {}
    
    def register_client(self, client_class: Type[BaseClient]) -> BaseClient:
        """Register and get a client instance by class."""
        if client_class not in self._clients:
            self._clients[client_class] = client_class()
        return self._clients[client_class]
    
    def get_client(self, client_class: Type[BaseClient]) -> BaseClient | None:
        """Get a registered client instance by class."""
        return self._clients.get(client_class)
    
    def get_all_clients(self) -> List[BaseClient]:
        """Get all registered client instances."""
        return list(self._clients.values())
    
    async def close_all(self):
        """Close all registered client connections."""
        for client in self._clients.values():
            await client.close()
        self._clients.clear()


_client_registry = ClientRegistry()


def get_client(client_class: Type[BaseClient]) -> BaseClient:
    """Get or register a client by its class."""
    return _client_registry.register_client(client_class)

async def close_all_clients():
    """Close all registered client connections."""
    await _client_registry.close_all()
