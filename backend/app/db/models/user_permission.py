from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID  # noqa: TC003

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import ForeignKey
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .permission import Permission
    from .user import User


class UserPermission(UUIDAuditBase):
    """User Permission."""

    __tablename__ = "user_permissions"
    __table_args__ = {"comment": "Links a user to a specific permission."}
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="cascade"), nullable=False)
    permission_id: Mapped[UUID] = mapped_column(ForeignKey("permissions.id", ondelete="cascade"), nullable=False)
    assigned_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))

    # -----------
    # ORM Relationships
    # ------------
    user: Mapped[User] = relationship(back_populates="permissions", innerjoin=True, uselist=False, lazy="joined")
    user_name: AssociationProxy[str] = association_proxy("user", "name")
    user_email: AssociationProxy[str] = association_proxy("user", "email")
    permission: Mapped[Permission] = relationship(back_populates="users", innerjoin=True, uselist=False, lazy="joined")
    permission_name: AssociationProxy[str] = association_proxy("permission", "name")
    permission_slug: AssociationProxy[str] = association_proxy("permission", "slug")
