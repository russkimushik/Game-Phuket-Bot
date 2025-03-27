from app.database.models import async_session
from app.database.models import User, Event, Question
from sqlalchemy import select, update, delete, desc


async def set_user(tg_id, username):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id).where(User.username == username))

        if not user:
            session.add(User(tg_id=tg_id, username = username))
            await session.commit()

async def get_events():
    async with async_session() as session:
        return await session.scalars(select(Event))

async def get_eventt(event_id):
    async with async_session() as session:
        return await session.scalar(select(Event).where(Event.id == event_id))

async def get_questions():
    async with async_session() as session:
        return await session.scalars(select(Question))

async def get_question(question_id):
    async with async_session() as session:
        return await session.scalar(select(Question).where(Question.id == question_id))

async def get_price_event(event_id):
    async with async_session() as session:
        return await session.scalar(select(Event.price).where(Event.id == event_id))

async def get_users():
    async with async_session() as session:
        return await session.scalars(select(User))
