from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from app.db.database import Base

class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key = True)  # (primary_key = True) ОДИН в таблице
    name: Mapped[str] = mapped_column(String(20))
    author: Mapped[str] = mapped_column(String(20))
    published_year: Mapped[int] = mapped_column(Integer)





