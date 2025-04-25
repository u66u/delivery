from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String, Text, Numeric, DateTime, Index, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from advanced_alchemy.base import UUIDAuditBase
import enum

class OrderStatus(str, enum.Enum):
    PENDING_PAYMENT = "pending_payment"
    PROCESSING = "processing"
    AWAITING_CONFIRMATION = "awaiting_confirmation"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY_FOR_PICKUP = "ready_for_pickup"
    DELIVERING = "delivering"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    FAILED = "failed"


if TYPE_CHECKING:
    from .user import User
    from .store import Store
    from .address import Address
    from .courier_user import CourierUser
    from .order_item import OrderItem
    from .payment import Payment
    from .review import Review

class Order(UUIDAuditBase):
    __tablename__ = "orders"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    store_id: Mapped[UUID] = mapped_column(
        ForeignKey("stores.id"), nullable=False, index=True
    )
    delivery_address_id: Mapped[UUID] = mapped_column(
        ForeignKey("addresses.id"), nullable=False
    )
    courier_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("courier_users.id"), nullable=True, index=True
    )
    status: Mapped[OrderStatus] = mapped_column(
        String(30), default=OrderStatus.PENDING_PAYMENT, nullable=False, index=True
    )
    subtotal_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    delivery_fee: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), default=0.00, nullable=False
    )
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    order_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    estimated_delivery_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    actual_delivery_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="orders", foreign_keys=[user_id])
    courier: Mapped["CourierUser | None"] = relationship(
        back_populates="orders", foreign_keys=[courier_id]
    )
    store: Mapped["Store"] = relationship(back_populates="orders")
    delivery_address: Mapped["Address"] = relationship(back_populates="orders")
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="order")
    payment: Mapped["Payment | None"] = relationship(back_populates="order", uselist=False)
    review: Mapped["Review | None"] = relationship(back_populates="order", uselist=False)

    __table_args__ = (
        Index("idx_orders_user_id", "user_id"),
        Index("idx_orders_courier_id", "courier_id"),
        Index("idx_orders_store_id", "store_id"),
    )
