from litestar import Litestar
from litestar.openapi import OpenAPIConfig
from app.settings.db import alchemy
from litestar.plugins.sqlalchemy import SQLAlchemyPlugin
from app.domain.user.controller import UserController
from app.domain.auth.controller import AuthController
from app.domain.address.controller import AddressController
from app.domain.auth.guards import jwt_auth
from litestar.openapi.plugins import ScalarRenderPlugin
from litestar.logging import LoggingConfig

alchemy_plugin = SQLAlchemyPlugin(config=alchemy)

logging_config = LoggingConfig(
    root={"level": "INFO", "handlers": ["queue_listener"]},
    formatters={
        "standard": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}
    },
    log_exceptions="always",
)


openapi_config = OpenAPIConfig(
    title="My API",
    version="1.0.0",
    description="My API description",
    path="/docs",
    render_plugins=[ScalarRenderPlugin(version="latest")],
)

app = Litestar(
    route_handlers=[UserController, AuthController, AddressController],
    plugins=[alchemy_plugin],
    openapi_config=openapi_config,
    logging_config=logging_config,
    middleware=[jwt_auth.middleware],
)