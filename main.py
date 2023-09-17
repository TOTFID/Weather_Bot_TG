import telebot
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
key_tg = os.getenv('token_bot')
key_we = os.getenv('API_Weather')
API_Weather = key_we
bot = telebot.TeleBot(token=key_tg)


@bot.message_handler(commands=['start'])
def wither_start_com(message):

    file = open('Logo.jpeg', 'rb')
    bot.send_photo(message.chat.id, file)
    bot.send_message(message.chat.id, f'Привет <b>{message.chat.first_name}</b>!\n\n'
                                      f'Этот бот поможет вам узнать погоду\n\n'
                                      f'<u>Напиши свой город:</u>', parse_mode='html')


@bot.message_handler(content_types=['text'])
def get_сity(message):
    сity = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={сity}&appid={API_Weather}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        bot.reply_to(message, f'Сейчас в {сity}: <b>{round(data["main"]["temp"])} градусов </b>\n\n'
                          f'Ощущается как: <b>{round(data["main"]["feels_like"])} градусов </b>\n\n'
                          f'Вы также можете и дальше узнавать погоду в других городах\n'
                          f'Просто введите название следующего города', parse_mode='html')
    else:
        bot.reply_to(message, 'Город указан неверно')


bot.polling(none_stop=True)