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
                   'You can control me using these commands\n\n/' \
                   '/start-to start chatting with the bot\n' \
                   '/help-to get more information about bot.\n\n'
    bot.send_message(chat_id, text_message)
    # my_calendar.create_event(2023, 12, 11, 'fortrexofer@gmail.com')


@bot.message_handler(func=lambda msg: re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}', msg.text))
def text_from_message(message):
    string = message.text
    msg_str = []
    for i in string.split(','):
        msg_str.append(i)
        print(msg_str)
    my_calendar.create_event(int(msg_str[3]),int(msg_str[1]),int(msg_str[2]),int(msg_str[4].split(":")[0]),msg_str[0],msg_str[5])
    print(list_of_events)


@bot.message_handler(commands=['create'])
def create_event(message):
    chat_id = message.chat.id
    text_message = 'For creating an event write email,date,time,name_of_event \n' \
                   'Example: example@example.com,1,11,2023,13:00,train '
    bot.send_message(chat_id, text_message)
    print(message.text)
    if 'For creating an event write email,date,time,name_of_even' in message.text:
        print('true')

def check_text(text):
    text1='for deleting an event write event id'
    if text1 in text:
        return True
    else:
        False
def message_return(message):
    return message
@bot.message_handler(commands=['delete'])
def delete_event(message):
    chat_id = message.chat.id
    text_message = 'For deleting an event write event id\n' \
                   'To get event id write getid'
    #bot.send_message(chat_id, text_message)
    print(message.text)
    bot.register_next_step_handler(message,my_calendar.delete_event)


@bot.message_handler(commands=['geteventsid'])
def geteventsid(message):
    chat_id = message.chat.id
    my_calendar.get_list_of_events()
    text_message=''
    for i in my_calendar.get_list_of_events():
        print(i)
        text_message += str(i) + '\n'
    bot.send_message(chat_id, text_message)

bot.infinity_polling()
