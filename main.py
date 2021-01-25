import telebot
from config import TOKEN
from config import keys
import requests
import json
from extensions import APIException


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def start(message: telebot.types.Message):
    text = "Чтобы начать работу введите боту комманду <имя валюты>\n <Валюты в каторую перевести>\n <Колличество необходимой валют>\n"
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = '\n'.join((text, key))
        bot.reply_to(message, text)


@bot.message_handler(content_types=["text"])
def convert(message: telebot.types.Message):
    value = message.text.split(" ")
    if len(value) > 3:
        raise APIException("Слишком много параметров")

    quote, base, amount = value
    if quote == base:
        raise APIException("Невозможно перевести одинаковые валюты")


    r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}")
    total_base = json.loads(r.content)[keys[base]]
    text = f"Цена {amount} {quote} в {base} - {total_base}"
    bot.send_message(message.chat.id, text)


bot.polling()
