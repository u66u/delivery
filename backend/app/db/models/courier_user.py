import enum
from decimal import Decimal
from datetime import datetime

from sqlalchemy import String, Text, Numeric, DateTime, Index, BigInteger, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from advanced_alchemy.base import UUIDAuditBase

class CourierStatus(str, enum.Enum):
    OFFLINE = "offline"
    AVAILABLE = "available"
    BUSY = "busy"

class CourierUser(UUIDAuditBase):
    __tablename__ = "courier_users"
    __table_args__ = {"comment": "Courier user accounts for delivery"}
    __pii_columns__ = {"name", "email", "avatar_url"}
    
    tg_id: Mapped[int] = mapped_column(
        BigInteger, unique=True, nullable=True, index=True
    )
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=True)
    username: Mapped[str | None] = mapped_column(nullable=True, default=None)
    first_name: Mapped[str | None] = mapped_column(nullable=True, default=None)
    last_name: Mapped[str | None] = mapped_column(nullable=True, default=None)
    phone_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    hashed_password: Mapped[str | None] = mapped_column(String(length=255), nullable=True, default=None)
    avatar: Mapped[UUID | None] = mapped_column(ForeignKey("files.id"), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    
    status: Mapped[CourierStatus] = mapped_column(
        String(20), default=CourierStatus.OFFLINE, nullable=False, index=True
    )
    current_latitude: Mapped[Decimal | None] = mapped_column(
        Numeric(9, 6), nullable=True
    )
    current_longitude: Mapped[Decimal | None] = mapped_column(
        Numeric(9, 6), nullable=True
    )
    last_location_update: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    vehicle_details: Mapped[str | None] = mapped_column(Text, nullable=True)
    avg_rating: Mapped[Decimal | None] = mapped_column(Numeric(3, 2), nullable=True)

    # Relationships
    orders: Mapped[list["Order"]] = relationship(back_populates="courier")
    reviews: Mapped[list["Review"]] = relationship(back_populates="courier")

    @hybrid_property
    def has_password(self) -> bool:
        return self.hashed_password is not None

    __table_args__ = (Index("idx_courierprofiles_status", "status"),)

