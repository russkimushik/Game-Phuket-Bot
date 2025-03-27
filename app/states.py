from aiogram.fsm.state import State, StatesGroup

class SignIn(StatesGroup):
    username = State()
    name = State()
    quantity = State()
    bank = State()
    check = State()

class Send_Mes(StatesGroup):
    message = State()

class AddEvent(StatesGroup):
    title = State()
    description = State()
    about = State()
    date = State()
    place = State()
    price = State()
    price_rub = State()
    duration = State()
    how_to = State()
    image = State()