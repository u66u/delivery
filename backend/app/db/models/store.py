import uuid
from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, ForeignKey, String, Text, Numeric, JSON, Index, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from advanced_alchemy.base import UUIDAuditBase

if TYPE_CHECKING:
    from .address import Address
    from .menu_item import MenuItem
    from .order import Order
    from .review import Review
    from .favorite_store import FavoriteStore


class Store(UUIDAuditBase):
    __tablename__ = "stores"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    phone_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    avg_rating: Mapped[Decimal | None] = mapped_column(Numeric(3, 2), nullable=True)
    logo_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    has_internal_menu: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    external_app_link_pattern: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False, index=True
    )
    opening_hours: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Relationships
    address: Mapped["Address | None"] = relationship(back_populates="store")
    menu_items: Mapped[list["MenuItem"]] = relationship(back_populates="store")
    orders: Mapped[list["Order"]] = relationship(back_populates="store")
    reviews: Mapped[list["Review"]] = relationship(back_populates="store")
    favorite_users: Mapped[list["FavoriteStore"]] = relationship(back_populates="store")

    # Index for active stores
    __table_args__ = (Index("idx_stores_is_active", "is_active"),)
