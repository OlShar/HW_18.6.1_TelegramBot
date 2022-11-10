import telebot
from config import TOKEN, currency
from extensions import APIException, Converter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message: telebot.types.Message):
    text = f"Привет, {message.chat.username}! Я Бот - конвертер валют! Я могу следующее: " \
           f"\n* Показать список доступных валют. Команда   /values" \
           f"\n* Сделать конвертацию валюты. Для этого введи 3 параметра через пробел в виде:" \
           f"\n<исходная валюта> <валюта в которую хочешь перевести> <количество переводимой валюты>" \
           f"\n* Напомнить, что я могу делать. Команда   /help"
    bot.reply_to(message, text)


@bot.message_handler(commands=["help"])
def help(message: telebot.types.Message):
    text = f"* Чтобы начать конвертацию валюты, введи 3 параметра через пробел в виде:" \
           f"\n<исходная валюта> <валюта в которую хочешь перевести> <количество переводимой валюты>" \
           f"\n* Список доступных для конвертации валют. Команда   /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in currency.keys():
        text = "\n".join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text"])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) > 3:
            raise APIException("Введено больше 3 параметров")
        if len(values) < 3:
            raise APIException("Введено меньше 3 параметров")

        base, quote, amount = values
        total_quote = Converter.get_price(base, quote, amount)

    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Что-то пошло не так.  {e}")
    else:
        text = f"Цена {amount} {base} в {quote} = {total_quote} {quote}"
        bot.send_message(message.chat.id, text)


bot.polling()
