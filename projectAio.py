import json
import os

from aiogram import Bot, Dispatcher, executor
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

import my_calendar
from config import *
from states import *

bot = Bot(token=Config.botToken, parse_mode='html')
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=["start"], state="*")
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "Please send your credentials before start\n"
        "How to creaete them you can watch wia this link http------\n"
        "For more information write /help")
    await states.sendCredentials.set()


def check_is_jsoncreated(message):
    if os.path.isfile(f"{message.chat.id}.json"):
        return True
    else:
        with open(f"{message.chat.id}.json", "w") as to_file:
            json.dump({}, to_file)


@dp.message_handler(state=states.sendCredentials, content_types=types.ContentType.DOCUMENT)
async def credentials(message: types.Message, state: FSMContext):
    await state.finish()
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, message.document.file_name)
    print(message)
    try:
        os.remove(f"{message.chat.id}.json")
    except OSError:
        pass
    check_is_jsoncreated(message)
    with open(message.document.file_name, "r") as from_file, open(f"{message.chat.id}.json", "w") as to_file:
        to_insert = json.load(from_file)
        json.dump(to_insert, to_file)  # The exact nature of this line varies. See below.


@dp.message_handler(commands=["help"])
async def help_info(message: types.Message):
    await message.answer(
        "/geteventsid - to get id of events,pressing on this id will delete it\n"
        "/create - will create event write him in that format email,date,time,name_of_event\n"
        "   Example: example@example.com,1,11,2023,13:00,train")


@dp.message_handler(commands=["create"])
async def write_Event(message: types.Message):
    await message.answer("Example: example@example.com,1,11,2023,13:00,train")
    await states.createState.set()


@dp.message_handler(state=states.createState)
async def createEvent(message: types.Message, state: FSMContext):
    await state.finish()
    string = message.text
    msg_str = []
    for i in string.split(','):
        msg_str.append(i)
    my_calendar.My_calendar(f"{message.chat.id}.json").create_event(int(msg_str[3]), int(msg_str[1]), int(msg_str[2]),
                                                                    int(msg_str[4].split(":")[0]),
                                                                    msg_str[0], msg_str[5])


@dp.message_handler(commands=["geteventsid"])
async def getid(message: types.Message):
    my_calendar.My_calendar(f"{message.chat.id}.json").get_list_of_events()
    text_message = ''
    for i in my_calendar.My_calendar(f"{message.chat.id}.json").get_list_of_events():
        text_message += str(i).split(' ')[-1].replace('}', '')
        button = types.InlineKeyboardButton(text_message, callback_data='unseen')
        inline_button = types.InlineKeyboardMarkup().add(button)
    await message.reply('if you whant to delete only press on it', reply_markup=inline_button)
    await states.buttonState.set()


@dp.message_handler(state=states.buttonState)
async def deleteevent(message: types.Message, state: FSMContext):
    await state.finish()
    if my_calendar.My_calendar(f"{message.message.json['chat']['id']}.json").delete_event(
            message.message.json['reply_markup']['inline_keyboard'][0][0]['text'].replace("'", '')):
        await bot.send_message(message.message.json['chat']['id'], 'delete successful')
    else:
        await bot.send_message(message.message.json['chat']['id'], 'delete unsuccessful')


executor.start_polling(dp, skip_updates=True, fast=True)
