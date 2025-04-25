import asyncio
import logging
from aiogram import Bot, Dispatcher
from app.config import bot_config
from app.handlers import main_router
from app.services.backend_client import close_backend_client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(token=bot_config.token)
    
    dp = Dispatcher()
    
    dp.include_router(main_router)
    
    logger.info("Starting bot...")
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(f"Error occurred: {e}")
    finally:
        logger.info("Closing backend client...")
        await close_backend_client()
        
        logger.info("Bot stopped!")

if __name__ == "__main__":
    asyncio.run(main())
