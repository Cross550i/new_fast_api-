from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from datetime import datetime
from sqlalchemy.sql import func
from app.db.database import Base
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from enum import Enum
from sqlalchemy import Enum as SAEnum


class Gender(str, Enum):
    male = "male"
    female = "female"


class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    published_year: Mapped[int] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name: Mapped[str] = mapped_column(String(64), nullable=True) # nullable True - может быть пустым, а если False - не может
    last_name: Mapped[str] = mapped_column(String(64), nullable=True)
    username: Mapped[str] = mapped_column(String(32), nullable=False)
    age: Mapped[int] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(String(64), nullable=False)
    password: Mapped[str] = mapped_column(String(64), nullable=False)

    # типизация лучше по enum-классу
    gender: Mapped[Gender] = mapped_column(SAEnum(Gender), nullable=False)
    reg_date: Mapped[datetime] = mapped_column(server_default=func.now())
    country: Mapped[str] = mapped_column(String(32), nullable=True)
    balance: Mapped[float] = mapped_column(default=0.0)
    bonus_balance: Mapped[int] = mapped_column(default=0)


