# core/apps/telegram_bot/management/commands/send_birthday_greetings.py

from django.core.management.base import BaseCommand
from datetime import datetime
from telebot import TeleBot
from apps.secondary.models import AddStudent  # Замените "yourapp" на имя вашего Django приложения

class Command(BaseCommand):
    help = 'Send birthday greetings to users'

    def handle(self, *args, **options):
        today = datetime.now().date()
        students_with_birthday = AddStudent.objects.filter(age__month=today.month, age__day=today.day)

        bot_token = 'your_telegram_bot_token'  # Замените 'your_telegram_bot_token' на ваш токен бота
        bot = TeleBot(bot_token)

        for student in students_with_birthday:
            chat_id = student.user_id
            birthday_message = f"С Днем Рождения, {student.name}!"

            if not chat_id:
                self.stderr.write(self.style.ERROR(f"Invalid chat_id for user with name {student.name}"))
                continue  # Пропустить этого пользователя и перейти к следующему

            try:
                bot.send_message(chat_id, birthday_message)
                self.stdout.write(self.style.SUCCESS(f"Sent message to user with chat_id {chat_id}"))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error sending message to user with chat_id {chat_id}: {str(e)}"))
                self.stderr.write(self.style.ERROR(f"User details - Name: {student.name}, Chat ID: {chat_id}"))

