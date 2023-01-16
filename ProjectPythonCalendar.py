import io
import json
import os
import re
import telebot

import my_calendar

SCOPES = ['https://www.googleapis.com/auth/calendar']
api_key = '5794601950:AAFufudQPfNBTp-yh8QfzgRB88p6TX24f60'
bot = telebot.TeleBot('5794601950:AAFufudQPfNBTp-yh8QfzgRB88p6TX24f60')
date_from_message = []
list_of_events = []


def get_text_from(message):
    date_from_message = [i for i in message.text.split(',')]
    print(date_from_message)


@bot.message_handler(commands=['start'])
def start_of_bot(message):
    chat_id = message.chat.id
    text_message = 'Hi! I am your calendar Bot!\nI can help you book an appointment.\n\n' \
                   'But before we start you need to do few steps.\n' \
                   '1) you need to add your credentials\n' \
                   'You can control me using these commands\n\n/' \
                   '/start-to start chatting with the bot\n' \
                   '/help-to get more information about bot.\n\n' \
                   '/geteventsid - write to get events id'
    bot.send_message(chat_id, text_message)
    # my_calendar.create_event(2023, 12, 11, 'fortrexofer@gmail.com')


@bot.message_handler(func=lambda msg: re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}', msg.text))
def text_from_message(message):
    string = message.text
    msg_str = []
    for i in string.split(','):
        msg_str.append(i)
        print(msg_str)
    my_calendar.My_calendar(f"{message.chat.id}.json").create_event(int(msg_str[3]), int(msg_str[1]), int(msg_str[2]),
                                                                    int(msg_str[4].split(":")[0]),
                                                                    msg_str[0], msg_str[5])
    print(list_of_events)


@bot.message_handler(commands=['create'])
def create_event(message):
    chat_id = message.chat.id
    text_message = 'For creating an event write email,date,time,name_of_event \n' \
                   'Example: example@example.com,1,11,2023,13:00,train '
    bot.send_message(chat_id, text_message)


def check_text(text):
    text1 = 'for deleting an event write event id'
    if text1 in text:
        return True
    else:
        return False


def message_return(message):
    return message


@bot.callback_query_handler(func=lambda call: True)
def delete_event(message):
    print('1')
    print(message.message.json['reply_markup']['inline_keyboard'][0][0]['text'].replace("'", ''))
    if my_calendar.My_calendar(f"{message.chat.id}.json").delete_event(
            message.message.json['reply_markup']['inline_keyboard'][0][0]['text'].replace("'", '')):
        bot.send_message(message.message.json['chat']['id'], 'delete successful')
    else:
        bot.send_message(message.message.json['chat']['id'], 'delete unsuccessful')


@bot.message_handler(commands=['geteventsid'])
def geteventsid(message):
    my_calendar.My_calendar(f"{message.chat.id}.json").get_list_of_events()
    text_message = ''
    markup = telebot.types.InlineKeyboardMarkup()
    for i in my_calendar.My_calendar(f"{message.chat.id}.json").get_list_of_events():
        print(str(i).split(' ')[-1].replace('}', ''))
        text_message += str(i).split(' ')[-1].replace('}', '')
        button = telebot.types.InlineKeyboardButton(text_message, callback_data='unseen')
        markup.add(button)
    bot.send_message(message.chat.id, 'if you whant to delete only press on it', reply_markup=markup)


def check_is_jsoncreated(message):
    if os.path.isfile(f"{message.chat.id}.json"):
        print(True)
    else:
        with open(f"{message.chat.id}.json", "w") as to_file:
            json.dump({}, to_file)


@bot.message_handler(content_types=['document', 'photo', 'audio', 'video', 'voice'])  # list relevant content types
def addfile(message):
    try:
        os.remove(f"{message.chat.id}.json")
    except OSError:
        pass
    check_is_jsoncreated(message)
    with open(message.document.file_name, "r") as from_file, open(f"{message.chat.id}.json", "w") as to_file:
        to_insert = json.load(from_file)
        json.dump(to_insert, to_file)  # The exact nature of this line varies. See below.


bot.infinity_polling()
