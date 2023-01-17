from aiogram.dispatcher.filters.state import StatesGroup, State


class states(StatesGroup):
    state = State()
    sendCredentials = State()
    buttonState = State()
    createState = State()
