from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import UUID  # noqa: TC003

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import ForeignKey
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .permission import Permission
    from .admin_user import AdminUser


class AdminPermission(UUIDAuditBase):

    __tablename__ = "admin_permissions"
    admin_id: Mapped[UUID] = mapped_column(ForeignKey("admin_users.id", ondelete="cascade"), nullable=False)
    permission_id: Mapped[UUID] = mapped_column(ForeignKey("permissions.id", ondelete="cascade"), nullable=False)
    assigned_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))

    # Relationships
    admin: Mapped["AdminUser"] = relationship(back_populates="permissions")
    permission: Mapped["Permission"] = relationship(back_populates="admin_users")
