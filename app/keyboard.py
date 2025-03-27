from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from app.database.requests import get_events, get_questions, get_eventt, get_question

start = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text='Пхукет', callback_data='Phuket')],
    [InlineKeyboardButton(text='Санкт-Петербург', callback_data ='SPB')]
])

in_event = InlineKeyboardMarkup(inline_keyboard = [
    [InlineKeyboardButton(text='Записаться на мероприятие', callback_data='sign_in')],
    [InlineKeyboardButton(text='Задать вопрос', callback_data='quest_4')],
    [InlineKeyboardButton(text='Вернуться назад', callback_data='Phuket')]
])

quantity = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='1')], [KeyboardButton(text='2')],
    [KeyboardButton(text='3')], [KeyboardButton(text='4')]
], resize_keyboard=True)


bank = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Thailand Bank (QR)', callback_data='Thailand_Bank')],
    [InlineKeyboardButton(text = 'Перевод в рублях', callback_data='Rub_pay')],
    [InlineKeyboardButton(text = 'Нет возможности оплатить ', callback_data='No_pay')]
])

finish = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Вернуться в главное меню', callback_data='Phuket')]
])


async def show_events_and_questions():
    all_events = await get_events()
    all_questions = await get_questions()
    keyboard = InlineKeyboardBuilder()
    for event in all_events:
        keyboard.add(InlineKeyboardButton(text=event.title, callback_data =f'event_{event.id}'))

    for question in all_questions:
        keyboard.add(InlineKeyboardButton(text=question.title, callback_data = f'quest_{question.id}'))
    return keyboard.adjust(1).as_markup()

async def del_event():
    all_event =await get_events()

    keyboardd = InlineKeyboardBuilder()

    for event in all_event:
        keyboardd.add(InlineKeyboardButton(text=event.title, callback_data=f'del_{event.id}'))

    return keyboardd.adjust(1).as_markup()


