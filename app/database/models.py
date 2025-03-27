from sqlalchemy import ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from config import DB_URL

engine = create_async_engine(url=DB_URL,
                             echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    username = mapped_column(String(128))

class Event(Base):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(String(300))
    image: Mapped[str] = mapped_column(String(256))
    about: Mapped[str] = mapped_column(String(600))
    date: Mapped[str] = mapped_column(String(64))
    place: Mapped[str] = mapped_column(String(128))
    price: Mapped[int] = mapped_column()
    price_rub: Mapped[int] = mapped_column()
    duration: Mapped[str] = mapped_column(String(20))
    how_to_get_there: Mapped[str] = mapped_column(String(128))

class Question(Base):
    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(650))
    image: Mapped[str] = mapped_column(String(256))

class Member(Base):
    __tablename__ = 'members'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    username: Mapped[str] = mapped_column(String(128))
    event: Mapped[str] = mapped_column(String(256))
    quantity: Mapped[int] = mapped_column()
    bank: Mapped[str] = mapped_column(String(64))
    pay: Mapped[str] = mapped_column(String(256))

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)