import telebot
import requests
import json
from extensions import APIException, CurrencyConverter
from config import TOKEN,currencies

TOKEN = "5889948271:AAFwWqR9yCzGEvVpr2Vz-8391AhbxdGhXEs"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Чтобы получить информацию о цене валюты, отправьте сообщение в формате:\
\n<имя переводимой валюты>, <имя валюты, в которой вы хотите узнать цену>, \
<количество валюты>.\nНапример: евро рубль 100\nДля просмотра списка доступных валют введите /values.")

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    currency_list = "Доступные валюты:"
    for currency, ticker in currencies.items():
        currency_list ='\n'.join((currency_list, f"{currency} ({ticker})",))
    bot.reply_to(message, currency_list)

@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException("Неверное количество параметров. Должно быть 3 параметра.")
            
        base, quote, amount = values
        total_price = CurrencyConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя. {e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду. {e}")
    else:
        bot.reply_to(message, f"{amount} {currencies[base]} = {total_price} {currencies[quote]}")   
        
bot.polling()