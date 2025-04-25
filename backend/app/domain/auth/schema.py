from pydantic import BaseModel, EmailStr
from uuid import UUID

class AuthLogin(BaseModel):
    email: EmailStr
    password: str

class AuthSignUp(BaseModel):
    email: EmailStr
    password: str
    username: str | None = None
    
class TgAuthLogin(BaseModel):
    tg_id: int
    email: EmailStr | None = None
    username: str
    first_name: str | None = None
    last_name: str | None = None

    model_config = {"from_attributes": True}
    