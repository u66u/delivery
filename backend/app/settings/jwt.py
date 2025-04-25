from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class JWTConfig:
    secret: str = os.getenv("JWT_SECRET", "abcd123")

jwt_config = JWTConfig()
