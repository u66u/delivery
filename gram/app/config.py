from dataclasses import dataclass

from dotenv import load_dotenv

import os

load_dotenv()

@dataclass
class BotConfig:
    token: str = os.getenv("BOT_TOKEN")
    secret_token: str = os.getenv("BOT_SECRET_TOKEN")

@dataclass
class BackendConfig:
    url: str = os.getenv("BACKEND_URL")

bot_config = BotConfig()
backend_config = BackendConfig()