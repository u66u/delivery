import asyncio
import logging
from aiogram import Bot, Dispatcher
from app.config import bot_config
from app.handlers import main_router
from app.services.client import setup_client_middleware, get_client, close_all_clients, UserClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(token=bot_config.token)
    
    dp = Dispatcher()
    # setup_client_middleware(dp, [
    #     UserClient
    # ])

    @dp.shutdown()
    async def on_shutdown():
        await close_all_clients()
    
    dp.include_router(main_router)
    
    logger.info("Starting bot...")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
