import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select
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


@app.patch("/users/{user_id}")
async def partial_update_user_by_id(
        user_id: UUID,
        data: UserAddSchema,
        session: SessionDep
):
    user = await session.get(UserModel, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = data.model_dump(exclude_unset=True, exclude_none=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    await session.commit()
    await session.refresh(user)
    return {"User updated!"}


@app.put("/update_book_by_id")
async def update_book_by_id(book_id: UUID, data:BookAddSchema, session: SessionDep):
    book = await session.get(BookModel, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    book.name = data.name
    book.author = data.author
    book.published_year = data.published_year
    await session.commit()
    await session.refresh(book)
    return {"Книга обновлена"}


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
