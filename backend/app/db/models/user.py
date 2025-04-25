from __future__ import annotations

from datetime import date, datetime
import enum
import uuid
from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import UUID, BigInteger, ForeignKey, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .address import Address
    from .order import Order
    from .courier_user import CourierUser
    from .user_permission import UserPermission
    from .favorite_store import FavoriteStore
    from .review import Review


class User(UUIDAuditBase):
    __tablename__ = "users"
    __table_args__ = {"comment": "User accounts for application access"}
    __pii_columns__ = {"name", "email", "avatar_url"}

    tg_id: Mapped[int | None] = mapped_column(
        BigInteger, unique=True, nullable=True, index=True
    )
    email: Mapped[str | None] = mapped_column(unique=True, index=True, nullable=True)
    username: Mapped[str | None] = mapped_column(nullable=True, default=None)
    first_name: Mapped[str | None] = mapped_column(nullable=True, default=None)
    last_name: Mapped[str | None] = mapped_column(nullable=True, default=None)
    phone_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    hashed_password: Mapped[str | None] = mapped_column(String(length=255), nullable=True, default=None)
    avatar: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("files.id"), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    # Relationships
    addresses: Mapped[list["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    orders: Mapped[list["Order"]] = relationship(
        back_populates="user", foreign_keys="[Order.user_id]", cascade="all, delete-orphan"
    )
    reviews: Mapped[list["Review"]] = relationship(back_populates="user")
    favorite_stores: Mapped[list["FavoriteStore"]] = relationship(back_populates="user")
    permissions: Mapped[list["UserPermission"]] = relationship(back_populates="user")

    @hybrid_property
    def has_password(self) -> bool:
        return self.hashed_password is not None