from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class File(UUIDAuditBase):
    __tablename__ = "files"
    
    bucket: Mapped[str] = mapped_column(String(255), nullable=False)
    key: Mapped[str] = mapped_column(String(500), nullable=False, index=True)