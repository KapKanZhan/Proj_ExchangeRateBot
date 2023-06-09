import requests
import json
from config import currencies

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException("Невозможно перевести одинаковые валюты!")
        try:
            base_ticker = currencies[base]
        except KeyError:
            raise APIException(f"Неверное имя валюты {base}")
        try:
            quote_ticker = currencies[quote]
        except KeyError:
            raise APIException(f"Неверное имя валюты {quote}")
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Неверный ввод количества валюты {amount}")
        
            
        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}")
        rate = json.loads(r.content)[quote_ticker]
        return round(rate * float(amount), 2) 