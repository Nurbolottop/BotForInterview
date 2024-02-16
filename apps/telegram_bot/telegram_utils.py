# apps/telegram_bot/telegram_utils.py

from telebot import TeleBot

TELEGRAM_TOKEN = "6966818358:AAExpZzm8czP9vVkeP61r5bEqvn-TJOnDP8"
ADMIN_ID = "-1002082761055"
bot = TeleBot(TELEGRAM_TOKEN, threaded=False)

def get_chat_title(chat_id):
    try:
        chat = bot.get_chat(chat_id)
        return chat.title
    except Exception as e:
        print(f"Ошибка при получении информации о чате: {e}")
        return None
