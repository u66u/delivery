from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String, Text, Numeric, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from advanced_alchemy.base import UUIDAuditBase
import enum

if TYPE_CHECKING:
    from .order import Order

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"

class Currency(str, enum.Enum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"

class Payment(UUIDAuditBase):
    __tablename__ = "payments"

    order_id: Mapped[str] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    payment_gateway: Mapped[str] = mapped_column(String(50), nullable=False)
    gateway_transaction_id: Mapped[str | None] = mapped_column(
        String(255), nullable=True, index=True
    )
    status: Mapped[PaymentStatus] = mapped_column(
        String(20), default=PaymentStatus.PENDING, nullable=False, index=True
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[Currency] = mapped_column(String(3), default=Currency.RUB, nullable=False)
    payment_method_details: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationship
    order: Mapped["Order"] = relationship(back_populates="payment")


    # Indexes
    __table_args__ = (
        Index("idx_payments_status", "status"),
        Index("idx_payments_gateway_transaction_id", "gateway_transaction_id"),
    )
