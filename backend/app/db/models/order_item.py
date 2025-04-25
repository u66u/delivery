from decimal import Decimal
from sqlalchemy import ForeignKey, Text, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from advanced_alchemy.base import UUIDAuditBase

if TYPE_CHECKING:
    from .order import Order
    from .menu_item import MenuItem

class OrderItem(UUIDAuditBase):
    __tablename__ = "order_items"

    order_id: Mapped[str] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True
    )
    menu_item_id: Mapped[str | None] = mapped_column(
        ForeignKey("menu_items.id"), nullable=True
    )
    external_item_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    quantity: Mapped[int] = mapped_column(nullable=False)
    price_per_item: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    # Relationships
    order: Mapped["Order"] = relationship(back_populates="order_items")
    menu_item: Mapped["MenuItem"] = relationship(back_populates="order_items")
