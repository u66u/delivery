from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase

if TYPE_CHECKING:
    from .admin_permission import AdminPermission

class AdminUser(UUIDAuditBase):
    __tablename__ = "admin_users"

    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Relationships
    permissions: Mapped[list["AdminPermission"]] = relationship(back_populates="admin")
