from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import UUID, Boolean, ForeignKey, String, Text, Numeric, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from advanced_alchemy.base import UUIDAuditBase

if TYPE_CHECKING:
    from .store import Store
    from .order_item import OrderItem
    from .review import Review
class MenuItem(UUIDAuditBase):
    __tablename__ = "menu_items"

    store_id: Mapped[UUID] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    store: Mapped["Store"] = relationship(back_populates="menu_items")
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="menu_item")
    reviews: Mapped[list["Review"]] = relationship(back_populates="menu_item")
    # Indexes
    __table_args__ = (
        Index("idx_menuitems_store_id", "store_id"),
        Index("idx_menuitems_is_available", "is_available"),
    )
