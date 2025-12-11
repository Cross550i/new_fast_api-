import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select
from typing import Annotated
from app.db.database import Base
from app.db.models import BookModel

app = FastAPI()

# Движок
engine = create_async_engine("sqlite+aiosqlite:///books.db", echo=True)

# Фабрика сессий
async_session = async_sessionmaker(engine)




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



# Pydantic схема
class BookAddSchema(BaseModel):
    name:str
    author:str
    published_year:int

class BookSchema(BookAddSchema):
    id:int



@app.post("/add_new_book")
async def add_new_book(data: BookSchema, session: SessionDep):
    new_book = BookModel(
        name=data.name,
        author=data.author,
        published_year=data.published_year
    )
    session.add(new_book)
    await session.commit()
    return {"Add!": True}



@app.get("/get_all_books")
async def get_all_books(session: SessionDep):
    query = select(BookModel)
    result = await session.execute(query)
    return result.scalars().all()



@app.get("/get_book_by_id")
async def get_book_by_id(book_id: int, session: SessionDep):
    book = await session.get(BookModel, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book


@app.put("/update_books_by_id")
async def update_books_by_id(book_id: int, data:BookAddSchema, session: SessionDep):
    book = await session.get(BookModel, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    book.name = data.name
    book.author = data.author
    book.published_year = data.published_year
    await session.commit()
    await session.refresh(book)
    return {"Книги обновлены"}



@app.delete("/del_by_id")
async def del_by_id(book_id: int, session: SessionDep):
    book = await session.get(BookModel, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    await session.delete(book)
    await session.commit()
    return {"Книга удалена": True, "id": book_id}






# Точка входа в приложение
if __name__== "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port= 8000, reload=True)

