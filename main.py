import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Annotated
from app.db.database import Base
from app.db.models import BookModel, UserModel, Gender
from app.config import settings
from uuid import UUID
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Optional


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Движок
engine = create_async_engine(settings.database_url, echo=True)

# Фабрика сессий
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]



@app.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok": True}



# Pydantic схема (Book)
class BookAddSchema(BaseModel):
    name:str
    author:str
    published_year:int

class BookSchema(BookAddSchema):
    id:UUID


class BookUpdate(BaseModel):
    name:Optional[str] = None
    author:Optional[str] = None
    published_year:Optional[int] = None



# Pydantic схема (Model)
class UserAddSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    age: int
    email: str
    password: str
    country: str
    balance: float
    bonus_balance: int
    gender: Gender


class UserSchema(UserAddSchema):
    id:UUID
    reg_date: datetime



class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None
    password: Optional[str] = None
    country: Optional[str] = None
    balance: Optional[float] = None
    bonus_balance: Optional[int] = None
    gender: Optional[Gender] = None




@app.post("/add_new_user")
async def add_new_user(data: UserAddSchema, session: SessionDep):
    new_user = UserModel(**data.model_dump())
    session.add(new_user)
    await session.commit()
    return {"New_user add!": True}




@app.post("/add_new_book")
async def add_new_book(data: BookAddSchema, session: SessionDep):
    new_book = BookModel(**data.model_dump())
    session.add(new_book)
    await session.commit()
    return {"Add!": True}



@app.get("/get_all_users")
async def get_all_users (session: SessionDep):
    query = select(UserModel)
    result = await session.execute(query)
    return result.scalars().all()


@app.get("/get_user_by_id")
async def get_user_by_id(user_id: UUID, session: SessionDep):
    user = await session.get(UserModel, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return user

@app.get("/get_all_books")
async def get_all_books(session: SessionDep):
    query = select(BookModel)
    result = await session.execute(query)
    return result.scalars().all()



@app.get("/get_book_by_id")
async def get_book_by_id(book_id: UUID, session: SessionDep):
    book = await session.get(BookModel, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book


@app.put("/update_user_by_id")
async def update_user_by_id(user_id: UUID, user_update: UserUpdate, session: SessionDep):
    user = await session.get(UserModel, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)         # setattr цикл автоматом берет все поля из class UserUpdate

    await session.commit()
    await session.refresh(user)
    return user




@app.put("/update_book_by_id")
async def update_book_by_id(book_id: UUID, book_update: BookUpdate, session: SessionDep):
    book = await session.get(BookModel, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = book_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(book, field, value)

    await session.commit()
    await session.refresh(book)
    return {"Book update!"}


@app.delete("/del_user_by_id")
async def del_user_by_id(user_id: UUID, session: SessionDep):
    user = await session.get(UserModel, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await session.delete(user)
    await session.commit()
    return {"User deleted": True, "id": user_id}


@app.delete("/del_book_by_id")
async def del_book_by_id(book_id: UUID, session: SessionDep):
    book = await session.get(BookModel, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    await session.delete(book)
    await session.commit()
    return {"Book deleted": True, "id": book_id}




#Точка входа в приложение
if __name__== "__main__":
    uvicorn.run("main:app", host=settings.host, port=settings.port, reload=True)
