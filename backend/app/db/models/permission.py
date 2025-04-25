from advanced_alchemy.base import UUIDAuditBase
from advanced_alchemy.mixins import SlugKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.user_permission import UserPermission
    from app.db.models.admin_permission import AdminPermission

class Permission(UUIDAuditBase, SlugKey):

    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None]
    # -----------
    # ORM Relationships
    # ------------
    users: Mapped[list["UserPermission"]] = relationship(
        back_populates="permission",
        cascade="all, delete",
        lazy="noload",
        viewonly=True,
    )
    admin_users: Mapped[list["AdminPermission"]] = relationship(
        back_populates="permission",
        cascade="all, delete",
        lazy="noload",
        viewonly=True,
    )