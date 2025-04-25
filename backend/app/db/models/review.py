from typing import TYPE_CHECKING
import uuid
from sqlalchemy import UUID, ForeignKey, String, Text, CheckConstraint, Index, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from advanced_alchemy.base import UUIDAuditBase

if TYPE_CHECKING:
    from .order import Order
    from .user import User
    from .store import Store
    from .courier_user import CourierUser
    from .menu_item import MenuItem


class Review(UUIDAuditBase):
    """
    A review of a store, order, courier, or menu item.
    """
    __tablename__ = "reviews"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    order_id: Mapped[UUID] = mapped_column(
        ForeignKey("orders.id"), nullable=False, index=True
    )
    store_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("stores.id"), nullable=True, index=True
    )
    courier_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("courier_users.id"), nullable=True, index=True
    )
    menu_item_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("menu_items.id"), nullable=True, index=True
    )

    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    order: Mapped["Order"] = relationship(back_populates="review")
    user: Mapped["User"] = relationship(back_populates="reviews")
    store: Mapped["Store | None"] = relationship(back_populates="reviews")
    courier: Mapped["CourierUser | None"] = relationship(back_populates="reviews")
    menu_item: Mapped["MenuItem | None"] = relationship(back_populates="reviews")

    __table_args__ = (
        CheckConstraint(
            "(CASE WHEN store_id IS NOT NULL THEN 1 ELSE 0 END + "
            " CASE WHEN courier_id IS NOT NULL THEN 1 ELSE 0 END + "
            " CASE WHEN menu_item_id IS NOT NULL THEN 1 ELSE 0 END) = 1",
            name="chk_review_target_single",
        ),
        CheckConstraint("rating >= 1 AND rating <= 5", name="chk_review_rating_range"),
        Index("idx_reviews_user_order", "user_id", "order_id"),
    )
