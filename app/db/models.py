from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy.sql import func
from app.db.database import Base
from uuid import UUID, uuid4



class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True,)
    name: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    published_year: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 server_default=func.now())  # время создания при INSERT
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now())  # обновляется при UPDATE


