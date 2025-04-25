from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base schema for user data."""
    email: EmailStr | None = None
    username: str | None = None


class UserCreate(UserBase):
    """Schema for creating a new user."""
    email: EmailStr
    password: str
    

class UserUpdate(UserBase):
    """Schema for updating a user."""
    password: str | None = None


class UserResponse(BaseModel):
    """Schema for reading user data."""
    id: UUID
    tg_id: int | None = None
    email: EmailStr | None = None
    username: str | None = None
    is_active: bool = True
   
    model_config = {"from_attributes": True}
