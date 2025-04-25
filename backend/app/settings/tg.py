from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class TgConfig:
    bot_secret_token: str = os.getenv("BOT_SECRET_TOKEN")

tg_config = TgConfig()
