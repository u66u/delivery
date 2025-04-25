import uuid
from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String, Text, Numeric, Index, CheckConstraint, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from advanced_alchemy.base import UUIDAuditBase

if TYPE_CHECKING:
    from .user import User
    from .store import Store
    from .order import Order

class Address(UUIDAuditBase):
    __tablename__ = "addresses"

    # Foreign keys to owner entities - only one should be non-NULL, or both can be NULL
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True
    )
    store_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("stores.id", ondelete="SET NULL"), nullable=True, index=True
    )

    # Address fields
    label: Mapped[str | None] = mapped_column(String(50), nullable=True) 
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=True, index=True)
    street: Mapped[str] = mapped_column(String(255), nullable=False)
    apartment: Mapped[str | None] = mapped_column(String(50), nullable=True)
    building: Mapped[str | None] = mapped_column(String(100), nullable=True)
    floor: Mapped[str | None] = mapped_column(String(50), nullable=True)
    entrance: Mapped[str | None] = mapped_column(String(50), nullable=True)
    details: Mapped[str | None] = mapped_column(Text, nullable=True) 
    latitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6), nullable=True)
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(9, 6), nullable=True)

    # Relationships
    user: Mapped["User | None"] = relationship(back_populates="addresses")
    store: Mapped["Store | None"] = relationship(back_populates="address")
    orders: Mapped[list["Order"]] = relationship(back_populates="delivery_address")

    # Unique constraint and index
    __table_args__ = (
        Index("idx_addresses_user_id", "user_id"),
        Index("idx_addresses_store_id", "store_id"),
        CheckConstraint(
            "(user_id IS NOT NULL AND store_id IS NULL) OR "
            "(user_id IS NULL AND store_id IS NOT NULL) OR "
            "(user_id IS NULL AND store_id IS NULL)",
            name="chk_address_owner_type"
        )
    )
