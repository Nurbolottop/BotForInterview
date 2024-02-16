from django.conf import settings
from telebot import TeleBot, types
from .models import TelegramUser,UserProfile
from apps.secondary.models import Nap,QuestionAdd
from apps.base.models import InterviewAnswer
import re

# Create your views here.
TELEGRAM_TOKEN = "6583047651:AAHT4PxFVmytmGGJo5E6yVSKDbLT7wC_HjU"
ADMIN_ID = "-1002082761055"

bot = TeleBot(TELEGRAM_TOKEN, threaded=False)
admin_id = ADMIN_ID

@bot.message_handler(commands=['start'])
def start(message: types.Message):
    welcome_text = "Приветствую тебя! 🌟\n\n"
    welcome_text += "Добро пожаловать в нашего телеграм бота! 🤖\n\n"
    welcome_text += "Мы рады приветствовать тебя здесь. Надеемся, что наш бот сделает твой день лучше! 💫\n\n"
    welcome_text += "Чтобы начать, выбери один из пунктов ниже:"
    # Проверяем, зарегистрирован ли пользователь
    if UserProfile.objects.filter(user_id=message.from_user.id).exists():
        # Если пользователь уже зарегистрирован, показываем кнопку "Кабинет"
        markup = types.ReplyKeyboardMarkup(row_width=2)
        item1 = types.KeyboardButton("ℹ️ Информация о нас")
        item2 = types.KeyboardButton("🔐 Кабинет")
        markup.add(item1, item2)
        bot.send_message(message.chat.id, welcome_text)
        
        bot.send_message(message.chat.id, "Выберите один из пунктов ниже:", reply_markup=markup)
    else:
        # Если пользователь не зарегистрирован, показываем кнопку "Зарегистрироваться"
        markup = types.ReplyKeyboardMarkup(row_width=1)
        item1 = types.KeyboardButton("📝 Зарегистрироваться")
        markup.add(item1)
        bot.send_message(message.chat.id, welcome_text)
        bot.send_message(message.chat.id, "Выберите один из пунктов ниже:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "◀️ Вернуться назад")
def back_to_main_menu(message: types.Message):
    # Отправляем пользователю начальное меню
    start(message)

@bot.message_handler(func=lambda message: message.text == "🔐 Кабинет")
def profile(message: types.Message):
    user_id = message.from_user.id
    user_profile = UserProfile.objects.filter(user_id=user_id).first()
    if user_profile:
        if user_profile.status:
            # Если у пользователя есть статус, получаем его название
            status_title = user_profile.status.title
            if status_title == "Выпускник":
                # Если статус выпускника, добавляем кнопку "Начать собеседование" и "Вернуться назад"
                markup = types.ReplyKeyboardMarkup(row_width=1)
                start_interview_button = types.KeyboardButton("🚀 Начать собеседование")
                back_button = types.KeyboardButton("◀️ Вернуться назад")
                markup.add(start_interview_button)
                markup.add(back_button)
                bot.send_message(message.chat.id, "Вы готовы к собеседованию?", reply_markup=markup)
            # Отправляем информацию о профиле с указанием статуса и общего счета баллов
            profile_text = f"👤 <b>Имя:</b> {user_profile.full_name}\n"
            profile_text += f"🎓 <b>Направление:</b> {user_profile.direction.title}\n"
            profile_text += f"🔖 <b>Статус:</b> {status_title}\n"
            profile_text += f"💯 <b>Общий счет баллов:</b> {user_profile.total_score}\n"  # Добавляем общий счет баллов
            profile_text += f"🥷 <b>Проходной балл:</b> 9\n"  # Добавляем общий счет баллов
            
            bot.send_message(message.chat.id, profile_text, parse_mode='HTML')
        else:
            # Если статус не указан, отправляем информацию о профиле соответственно
            profile_text = f"👤 <b>Имя:</b> {user_profile.full_name}\n"
            profile_text += f"🎓 <b>Направление:</b> {user_profile.direction.title}\n"
            profile_text += "🔖 <b>Статус:</b> не указан\n"
            profile_text += f"💯 <b>Общий счет баллов:</b> {user_profile.total_score}\n" 
            profile_text += f"🥷 <b>Проходной балл:</b> 9\n"  # Добавляем общий счет баллов
            # Добавляем общий счет баллов
            bot.send_message(message.chat.id, profile_text, parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, "Вы еще не зарегистрированы в нашем боте. Пожалуйста, нажмите кнопку '📝 Зарегистрировать', чтобы начать процесс регистрации.")

        
class Mail:
    def __init__(self): 
        self.description = None

mail = Mail()

    
def get_chat_title(chat_id):
    try:
        chat = bot.get_chat(chat_id)
        return chat.title
    except Exception as e:
        print(f"Ошибка при получении информации о чате: {e}")
        return None
    
def get_message(message:types.Message):
    mail.description = message.text 
    users = TelegramUser.objects.all()
    for user in users:
        bot.send_message(user.id_user, mail.description)
    bot.send_message(message.chat.id, "Рассылка окончена")

@bot.message_handler(commands=['mailing'])
def send_mailing(message:types.Message):
    if message.chat.id != int(admin_id):
        bot.send_message(message.chat.id, "Эта команда доступна только админу")
        return
    msg = bot.send_message(message.chat.id, "Введите текст для рассылки: ")
    bot.register_next_step_handler(msg, get_message)


@bot.message_handler(func=lambda message: message.text == "📝 Зарегистрироваться")
def register(message: types.Message):
    chat_id = message.chat.id
    
    # Проверяем, зарегистрирован ли пользователь
    if UserProfile.objects.filter(user_id=message.from_user.id).exists():
        bot.send_message(chat_id, "🛑 <b>Вы уже зарегистрированы!</b>", parse_mode='HTML')
    else:
        bot.send_message(chat_id, "📝 Пожалуйста, укажите ваше ФИО:")
        bot.register_next_step_handler(message, process_registration)

def process_registration(message: types.Message):
    full_name = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id
    
    markup = types.InlineKeyboardMarkup()
    nap_list = Nap.objects.all()
    for nap in nap_list:
        markup.add(types.InlineKeyboardButton(text=nap.title, callback_data=f"registration_{full_name}_{nap.id}"))
    
    bot.send_message(chat_id, "Выберите направление:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('registration_'))
def process_registration_callback(call):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item1 = types.KeyboardButton("ℹ️ Информация о нас")
    item2 = types.KeyboardButton("🔐 Кабинет")
    markup.add(item1, item2)
    full_name, direction_id = call.data.split('_')[1:]
    direction = Nap.objects.get(pk=int(direction_id))
    
    user, created = UserProfile.objects.get_or_create(
        user_id=call.from_user.id,
        chat_id=call.message.chat.id,
        defaults={
            'full_name': full_name,
            'direction': direction,
        }
    )
    
    bot.send_message(call.message.chat.id, f"Спасибо, {full_name}! Вы успешно зарегистрированы на направлении '{direction.title}'.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🚀 Начать собеседование")
def start_interview(message: types.Message):
    user_id = message.from_user.id
    user_profile = UserProfile.objects.filter(user_id=user_id).first()
    if user_profile and user_profile.status and user_profile.status.title == "Выпускник":
        if not InterviewAnswer.objects.filter(user_profile=user_profile).exists():
            interview_text = "🎙️ <b>Началось собеседование</b> 🎙️\n\n"
            if user_profile.direction.title == "UXUI":
                questions = QuestionAdd.objects.filter(question__direction=user_profile.direction).order_by('?')[:5]
            else:
                questions = QuestionAdd.objects.filter(question__direction=user_profile.direction).order_by('?')[:7]
            for idx, question in enumerate(questions, start=1):
                interview_text += f"{idx}. {question.text}\n"
            bot.send_message(message.chat.id, interview_text, parse_mode='HTML')
            # Устанавливаем флаг, что собеседование начато
            user_profile.interview_started = True
            user_profile.save()
            # Начинаем процесс получения ответов на вопросы
            bot.register_next_step_handler(message, process_interview, user_profile, questions, 0)
            # Удаляем кнопку "Начать собеседование"
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        else:
            bot.send_message(message.chat.id, "🛑 <b>Вы уже прошли собеседование</b>", parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, "🛑 <b>Недостаточно прав для начала собеседования</b>", parse_mode='HTML')

def process_interview(message, user_profile, questions, question_index):
    if question_index < len(questions):
        # Отправляем следующий вопрос пользователю
        bot.send_message(message.chat.id, f"Вопрос {question_index + 1}: {questions[question_index].text}")
        # Регистрируем следующий шаг для получения ответа на текущий вопрос
        bot.register_next_step_handler(message, save_answer_and_ask_next_question, user_profile, questions, question_index)
    else:
        # Все вопросы заданы, завершаем собеседование
        user_profile.interview_started = False
        user_profile.save()
        bot.send_message(message.chat.id, "✅ Все вопросы собеседования заданы. Спасибо за участие!")

def save_answer_and_ask_next_question(message, user_profile, questions, question_index):
    # Сохраняем ответ пользователя
    InterviewAnswer.objects.create(
        user_profile=user_profile,
        question=questions[question_index],
        answer=message.text
    )
    # Переходим к следующему вопросу
    process_interview(message, user_profile, questions, question_index + 1)


@bot.message_handler(func=lambda message: message.text == "ℹ️ Информация о нас")
def about_us(message: types.Message):
    about_text = "🌟 Добро пожаловать в нашего телеграм бота! 🌟\n\n"
    about_text += "Мы - команда профессионалов, предлагающая качественные и эффективные собеседования для вас! 🚀\n\n"
    about_text += "💼 Наш бот создан с целью обеспечить вам удобство и эффективность процесса собеседования. Мы стремимся предоставить вам все необходимые инструменты для успешного прохождения интервью. 💼\n\n"
    about_text += "👨‍💻 Наши эксперты тщательно подготовили вопросы, направленные на выявление ваших навыков и компетенций. Мы уверены, что благодаря нашим собеседованиям вы сможете проявить себя с лучшей стороны и добиться успеха в своей карьере! 👩‍💼\n\n"
    about_text += "📞 Не стесняйтесь связаться с нами, если у вас есть какие-либо вопросы или предложения. Мы всегда открыты к общению и готовы помочь вам в любое время! 📧\n\n"
    about_text += "📱 Контактные данные:\n"
    about_text += "Username: @erk1nbaew\n"
    about_text += "Номер телефона: 0225082021\n"
    about_text += "Почта: erk1nbaevw2711@gmail.com\n\n"
    about_text += "Не стесняйтесь обращаться к нам! Мы с нетерпением ждем возможности помочь вам достичь ваших целей! 💪😊"
    
    bot.send_message(message.chat.id, about_text)

def get_text(message):
    bot.send_message(admin_id, message, parse_mode='HTML')

def get_text_doctor(message, id):
    bot.send_message(id, message)


@bot.message_handler()  
def echo(message:types.Message):
    # bot.delete_message(message.chat.id, message.message_id)  
    bot.send_message(message.chat.id, "Я вас не понял")


