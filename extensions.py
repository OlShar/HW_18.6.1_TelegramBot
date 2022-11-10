import requests
import json
from config import currency

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if quote == base:
            raise APIException(f"Нельзя конвертировать одинаковые валюты {base}.")

        try:
            base_ticker = currency[base]
        except KeyError:
            raise APIException(f"Нет такой валюты {base}")

        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise APIException(f"Нет такой валюты {quote}")

        try:
            amount = int(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество {amount}")

        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}")
        total_quote = float(json.loads(r.content)[currency[quote]]) * int(amount)

        return total_quote