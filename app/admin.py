import aiosqlite
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter, Command
from aiogram.fsm.context import FSMContext

import app.keyboard as kb
from app.states import Send_Mes, AddEvent
from app.database.requests import get_users
import config as cfg

admin = Router()

class Admin(Filter):
    async def __call__(self, message: Message):
        return message.from_user.id in [2066791910, 361226470]

@admin.message(Admin(), Command('send_mes'))
async def newsletter(message: Message, state: FSMContext):
    await state.set_state(Send_Mes.message)
    await message.answer('Введитие сообщение для рассылки')

@admin.message(Send_Mes.message)
async def newsletter_message(message: Message, state: FSMContext):
    await state.clear()
    await  message.answer('Рассылка началась')
    users = await get_users()
    for user in users:
        try:
            await message.send_copy(chat_id=user.tg_id)
        except Exception as e:
            print(e)
    await message.answer('Рассылка завершена')

@admin.message(Command('new_event'))
async def new_event_1(message: Message, state: FSMContext):
    await state.set_state(AddEvent.title)
    await message.answer(f'Введите название для нового мероприятия')
@admin.message(AddEvent.title)
async def new_event_2(message: Message, state: FSMContext):
    await state.update_data(title = message.text)
    await state.set_state(AddEvent.description)
    await message.answer('Введите небольшое описание для мероприятия(введенный текст появится в ссобщении с выбором события)')
@admin.message(AddEvent.description)
async def new_event_3(message: Message, state: FSMContext):
    await state.update_data(description = message.text)
    await state.set_state(AddEvent.about)
    await message.answer('Введите текст, подробно описывающий мероприятие')
@admin.message(AddEvent.about)
async def new_event_4(message: Message, state: FSMContext):
    await state.update_data(about = message.text)
    await state.set_state(AddEvent.date)
    await message.answer('Введите дату и время начала мероприятия')
@admin.message(AddEvent.date)
async def new_event_5(message: Message, state: FSMContext):
    await state.update_data(date = message.text)
    await state.set_state(AddEvent.place)
    await message.answer('Введите место проведения мероприятия')
@admin.message(AddEvent.place)
async def new_event_6(message: Message, state: FSMContext):
    await state.update_data(place = message.text)
    await state.set_state(AddEvent.price)
    await message.answer('Введите цену (в батах)')
@admin.message(AddEvent.price)
async def new_event_7(message: Message, state: FSMContext):
    await state.update_data(price = message.text)
    await state.set_state(AddEvent.price_rub)
    await message.answer('Введите цену (в рублях)')
@admin.message(AddEvent.price_rub)
async def new_event_8(message: Message, state: FSMContext):
    await state.update_data(price_rub = message.text)
    await state.set_state(AddEvent.duration)
    await message.answer('Введите продолжительность события')
@admin.message(AddEvent.duration)
async def new_event_9(message: Message, state: FSMContext):
    await state.update_data(duration = message.text)
    await state.set_state(AddEvent.how_to)
    await message.answer('Введите "Как попасть на событие?"')
@admin.message(AddEvent.how_to)
async def new_event_image(message: Message, state: FSMContext):
    await state.update_data(how_to = message.text)
    await state.set_state(AddEvent.image)
    await message.answer('Отправьте афишу для события(если нету, то напишите NoneType)')


@admin.message(AddEvent.image)
async def new_event_10(message: Message, state: FSMContext):
    if message.text == 'NoneType':
        await state.update_data(image = 'NoneType')
    elif message == message.photo:
        file_image = message.photo[-1].file_id
        await state.update_data(image = file_image)
    data = await state.get_data()
    title = data['title']
    description = data['description']
    about = data['about']
    date = data['date']
    place = data['place']
    price = data['price']
    price_rub = data['price_rub']
    duration = data['duration']
    how_to_get_there = data['how_to']
    image = data['image']
    try:
        async with aiosqlite.connect('db.sqlite3') as db:
            await db.execute('INSERT INTO events (title, description, image, about, date, place, price, price_rub, duration, how_to_get_there) VALUES (?,?,?,?,?,?,?,?,?,?)',
                         (title, description, image, about, date, place, price, price_rub, duration, how_to_get_there))
            await db.commit()
    except Exception as e:
        await message.answer(e)

@admin.message(Admin(), Command('del_event'))
async def del_event(message: Message):
    await message.answer('Выберите событие, которое хотите удалить', reply_markup=await kb.del_event())

@admin.callback_query(Admin(), F.data.startswith('del_'))
async def dell_(callback: CallbackQuery):
    del_id = callback.data.split('_')[1]
    try:
        async with aiosqlite.connect('db.sqlite3') as db:
            await db.execute(f'DELETE FROM events WHERE id = {del_id}')
            await db.commit()
        await callback.message.answer('Событие успешно удалено')
    except Exception as e:
        await callback.message.answer(e)

