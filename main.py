import uvicorn
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.sql.annotation import Annotated
from app.db.models import BookModel
from app.db.database import Base

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
async def get_all_books():
    ...

@app.get("/get_book_by_id")
async def get_book_by_id():
    ...

@app.put("/update_all")
async def update_all():
    ...

@app.delete("/del_by_id")
async def del_by_id():
    ...



# Точка входа в приложение
if __name__== "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port= 8000, reload=True)

