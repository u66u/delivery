from aiogram import Router
from app.handlers.start import router as start_router

# Create the main router that includes all other routers
main_router = Router()

# Include all command routers
main_router.include_router(start_router)

# Export the main router
__all__ = ["main_router"] 