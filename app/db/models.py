# from sqlalchemy.orm import Mapped, mapped_column
# from app.db.database import Base
#
#
# class BookModel(Base):
#     __tablename__ = "books"
#
#     id: Mapped[str] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(nullable=False)
#     author: Mapped[str] = mapped_column(nullable=False)
#     published_year: Mapped[int] = mapped_column(nullable=False)


from sqlalchemy import Column, String, Integer
from uuid import uuid4
from app.db.database import Base


class BookModel(Base):
    __tablename__ = "books"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    published_year = Column(Integer, nullable=False)

