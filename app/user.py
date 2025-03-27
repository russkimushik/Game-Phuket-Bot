import asyncio
import aiosqlite

import config as cfg
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

import app.keyboard as kb
import sqlite3

from app.database.requests import set_user, get_eventt, get_question, get_price_event
from app.states import SignIn

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
user = Router()



@user.message(CommandStart())
async def start(message: Message):
    await set_user(message.from_user.id, message.from_user.username)
    await message.delete()
    await message.answer(f'Приветствую! <b>\nВыбери, где ты сейчас:</b>', parse_mode='HTML', reply_markup=kb.start)


@user.callback_query(F.data == 'SPB')
async def spb(callback: CallbackQuery):
    await callback.answer('Сейчас наши мероприятия в Санкт-Петербурге еще находится на стадии разработки, но уже совсем скоро мы будем радовать вас нашими играми!', show_alert=True)

@user.callback_query(F.data == 'Phuket')
async def phuket(callback: CallbackQuery):
    cursor.execute('SELECT title, description FROM events')
    data = cursor.fetchall()
    text = ''
    for row in data:
        text+= f'\n<b>{row[0]}</b>{row[1]}\n'

    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(f'Какое мероприятие вас интересует?\n{text}', parse_mode='HTML',
                                     reply_markup = await kb.show_events_and_questions())

@user.callback_query(F.data.startswith('event_'))
async def get_event(callback: CallbackQuery):
    global event_info
    event_info = await get_eventt(callback.data.split('_')[1])
    global event_title
    event_title = event_info.title
    image = event_info.image
    try:
        if image == 'NoneType':
            await callback.answer(f'Вы выбрали {event_info.title}')
            await callback.message.edit_text(f'<b>🔥{event_info.title}🔥</b>\n{event_info.about}\n<b>📅Когда?</b>\n{event_info.date}\n'
                                        f'<b>Где?</b>\n{event_info.place}\n\n<b>💰Стоимость участия: </b>{event_info.price} бат'
                                        f'\n<b>⏳ Продолжительность: </b>{event_info.duration}\n'
                                        f'\n<b>🚀 Как попасть?</b>\n{event_info.how_to_get_there}', reply_markup=kb.in_event)
        else:
            await callback.message.delete()
            await callback.message.answer_photo(photo=image, caption=f'<b>🔥{event_info.title}🔥</b>\n{event_info.about}\n<b>📅Когда?</b>\n{event_info.date}\n'
                                     f'<b>Где?</b>\n{event_info.place}\n\n<b>💰Стоимость участия: </b>{event_info.price} бат'
                                     f'\n<b>⏳ Продолжительность: </b>{event_info.duration}\n'
                                     f'\n<b>🚀 Как попасть?</b>\n{event_info.how_to_get_there}', reply_markup=kb.in_event)
            await callback.answer(f'Вы выбрали {event_info.title}')
    except Exception as e:
        await callback.message.answer(e)


    @user.callback_query(F.data == 'sign_in')
    async def sign_in(callback: CallbackQuery, state: FSMContext):
        await state.set_state(SignIn.username)
        await callback.message.answer(f'Давайте пройдем быструю регистрацию на мероприятие!')
        await callback.message.answer(f'Ожидайте, мы проверяем наличие свободных мест...')
        await asyncio.sleep(1)
        await callback.message.answer(f'Благодарю за ожидание, для регистрации потребуется дополнительная информация.')
        await state.set_state(SignIn.username)
        await callback.message.answer(f'Введите Ваш ник в Telegram')

    @user.message(SignIn.username)
    async def sign_name(message: Message, state: FSMContext):
        await state.update_data(username = message.text)
        await state.set_state(SignIn.name)
        await message.answer(f'Введите Ваше имя')

    @user.message(SignIn.name)
    async def sign_quntity(message: Message, state: FSMContext):
        await state.update_data(name = message.text)
        await state.set_state(SignIn.quantity)
        await message.answer(f'Какое количество участников записать на мероприятие?', reply_markup=kb.quantity)

    @user.message(SignIn.quantity)
    async def sign_1qua(message: Message, state: FSMContext):
        await state.update_data(quantity = message.text)
        await state.set_state(SignIn.bank)
        await message.answer(f'Как будет удобнее оплатить участие на мероприятие?', reply_markup=kb.bank)

        @user.callback_query(F.data == 'Thailand_Bank')
        async def sign_pay_tha(callback: CallbackQuery, state: FSMContext):
            await state.update_data(bank = callback.data)
            event_price = event_info.price
            data = await state.get_data()
            global total
            total = int(data['quantity'])*event_price
            await callback.message.answer(f"Количество участников: {data['quantity']}.\nЦена за одного участника{event_price} бат.\nИтого: {total} бат"
                                          f'\nПроизведите оплату в размере {total} бат по следующим реквизитам:\n'
                                          f'💳Bangkok Bank\nSergei Lobyr\n766-0-187787')
            await callback.message.answer(f'⬇⁣Отправьте чек об оплате')
            event_price = 0
            if message == message.document:
                check = message.document
            elif message == message.photo:
                check = message.photo


        @user.callback_query(F.data == 'Rub_pay')
        async def sign_pay_rub(callback: CallbackQuery, state: FSMContext):
            await state.update_data(bank = callback.data)
            global event_price_rub
            event_price_rub = event_info.price_rub
            data = await state.get_data()
            global total
            total = int(data['quantity']) * event_price_rub
            await callback.message.answer(f"Количество участников: {data['quantity']}.\nЦена за одного участника{event_price_rub} рублей.\nИтого: {total} рублей"
                                          f'\nПроизведите оплату в размере {total} рублей по следующим реквизитам:\n'
                                          f'💳Перевод по номеру телефона Т-БАНК\nПолучатель: Сергей Л.\n89811604463\nПо номеру карты\n'
                                          f'Получатель: Сергей Л. 2200700111650874')
            await callback.message.answer(f'⬇⁣Отправьте чек об оплате')


            if message == message.document:
                check = message.document
            elif message == message.photo:
                check = message.photo

        @user.callback_query(F.data=='No_pay')
        async def sign_no_pay(callback: CallbackQuery, state: FSMContext):
            await callback.message.answer('Мы свяжемся с вами')
            event_price = 0



        @user.message(F.document)
        async def sign_doc(message: Message, state: FSMContext, bot: Bot):
            await state.update_data(check = message.document.file_id)
            data = await state.get_data()
            username = data['username']
            name = data['name']
            event = event_title
            quantity = data['quantity']
            bank = data['bank']
            pay = data['check']
            global cur
            if bank == 'Rub_pay':
                cur = 'рублей'
            else:
                cur = 'бат'
            try:
                async with aiosqlite.connect('db.sqlite3') as db:
                    await db.execute('INSERT INTO members ( username, name, event, quantity, bank, pay) VALUES (?, ?, ?, ?, ?, ?)', (username, name, event_title, quantity, bank, pay))
                    await db.commit()
                await message.answer(f'Вы записаны на мероприятие {event}, хорошего вам дня и до встречи!', reply_markup=kb.finish)
                await bot.send_document(chat_id=cfg.ADMIN, document=data['check'])
                await bot.send_message(chat_id=cfg.ADMIN, text = f"Новая запись на мероприятие\n{event}.\nЮзернейм: {data['username']},\nИмя: {data['name']},\nКоличество записанных участников:{data['quantity']}\nБанк: {data['bank']}\nИтого: {total} {cur}")
                await state.clear()
                event_price_rub = 0
                cur = 0

            except Exception as e:
                await message.answer(f'Произошла ошибка: {e}')

        @user.message(F.photo)
        async def sign_doc(message: Message, state: FSMContext, bot: Bot):
            await state.update_data(check=message.photo[-1].file_id)
            data = await state.get_data()
            username = data['username']
            name = data['name']
            event = event_title
            quantity = data['quantity']
            bank = data['bank']
            pay = data['check']
            global cur
            if bank == 'Rub_pay':
                cur = 'рублей'
            else:
                cur = 'бат'
            try:
                async with aiosqlite.connect('db.sqlite3') as db:
                    await db.execute(
                        'INSERT INTO members ( username, name, event, quantity, bank, pay) VALUES (?, ?, ?, ?, ?, ?)',
                        (username, name, event_title, quantity, bank, pay))
                    await db.commit()
                await message.answer(f'Вы записаны на мероприятие {event}, хорошего вам дня и до встречи!',
                                     reply_markup=kb.finish)
                await bot.send_photo(chat_id=cfg.ADMIN, photo=data['check'])
                await bot.send_message(chat_id=cfg.ADMIN,
                                       text=f"Новая запись на мероприятие \n{event}.\n Юзернейм: {data['username']},\nИмя: {data['name']}, \nКоличество записанных участников:{data['quantity']}\n'Банк: {data['bank']}\nИтого: {total} {cur}")
                await state.clear()
                event_price_rub = 0
                cur = 0

            except Exception as e:
                await message.answer(f'Произошла ошибка: {e}')




@user.callback_query(F.data == 'quest_2')
async def quest_2(callback: CallbackQuery):
    quest_2_info = await get_question(callback.data.split('_')[1])
    await callback.answer(f'Вы выбрали {quest_2_info.title}')
    await callback.message.delete()
    await callback.message.answer_photo(photo='AgACAgIAAxkBAAM5Z-HBdDsvIpZgsIUf5pWwJVXy4JIAAlPuMRvXehFLqwnz8NGuQA0BAAMCAAN5AAM2BA', caption=quest_2_info.description, reply_markup=kb.finish)
@user.callback_query(F.data.startswith('quest_'))
async def get_event(callback: CallbackQuery):
    quest_info = await get_question(callback.data.split('_')[1])
    await callback.answer(f'Вы выбрали {quest_info.title}')
    await callback.message.delete()
    await callback.message.answer(text=quest_info.description ,reply_markup=kb.finish)







#@user.message(F.photo)
#async def get_id_photo(message: Message):
#    await message.answer(text=message.photo[-1].file_id)