from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from advanced_alchemy.base import UUIDAuditBase

if TYPE_CHECKING:
    from .user import User
    from .store import Store

class FavoriteStore(UUIDAuditBase):
    __tablename__ = "favorite_stores"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    store_id: Mapped[str] = mapped_column(
        ForeignKey("stores.id", ondelete="CASCADE"), primary_key=True
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="favorite_stores")
    store: Mapped["Store"] = relationship(back_populates="favorite_users")
