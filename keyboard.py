import telebot
from telebot import types
from utils import calculate_password_reliability
import logging

bot = telebot.TeleBot("7162935874:AAEYu08BRTJIb5ZEHVBOGh_1MDF9UzrgaLI")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def welcome(message):
    try:
        # Создаем клавиатуру
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        markup.add("ℹ️ Информация о боте", "Как создать безопасный пароль?", "Продемонстрировать бота преподавателю")

        # Отправляем приветственное сообщение с клавиатурой
        bot.send_message(message.chat.id,
                         f"Добро пожаловать, {message.from_user.username}!\nЯ - <b>{bot.get_me().first_name}</b>, "
                         f"бот, созданный студентами группы Б9123-01.03.02ии для помощи в создании безопасных "
                         f"паролей, и проверки паролей на надежность.",
                         parse_mode='html', reply_markup=markup)
        logger.info(f"User {message.from_user.first_name} started the bot")
    except Exception as e:
        logger.error(f"An error occurred in the welcome function: {e}")
        bot.reply_to(message, "Произошла ошибка при обработке команды /start. Пожалуйста, попробуйте еще раз.")


# Обработчик команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Доступные команды:\n"
                          "- /start - Запустить бота и получить информацию о нем.\n"
                          "- /help - Получить список доступных команд.\n"
                          "- ℹ️ Информация о боте - Получить информацию о создателях бота и его функциях.\n"
                          "- Как создать безопасный пароль? - Получить советы по созданию безопасных паролей.\n"
                          "- Продемонстрировать бота преподавателю - Запросить устройство преподавателя для "
                          "демонстрации возможностей бота.")


# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        # Обработка команд
        if message.text == 'ℹ️ Информация о боте':
            bot.send_message(message.chat.id, "Данный чат-бот создан студентами группы Б9123-01.03.02ии:\nСемибратов "
                                              "Вадим\nГамиловская Алёна\nБелоусов Иван")
        elif message.text == 'Как создать безопасный пароль?':
            bot.send_message(message.chat.id, "Советы по созданию безопасных паролей:\n- используйте как минимум 12 "
                                              "символов.\n- включайте в пароль буквы разных регистров, "
                                              "цифры и специальные символы.\n- избегайте использования "
                                              "распространенных слов или личной информации.\n- не используйте один и "
                                              "тот же пароль для нескольких учетных записей.\n- регулярно меняйте "
                                              "свои пароли.")
        elif message.text == 'Продемонстрировать бота преподавателю':
            # Создаем inline-клавиатуру
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("Хорошо", callback_data='yes'),
                       types.InlineKeyboardButton("Нет", callback_data='no'))
            bot.send_message(message.chat.id, 'Передайте мне устройство преподавателя, чтобы я мог продемонстрировать '
                                              'свои возможности.', reply_markup=markup)
        else:
            # Проверка надежности пароля
            password_reliability = calculate_password_reliability(message.text)
            bot.send_message(message.chat.id, f"Надежность пароля: {password_reliability}")
    except Exception as e:
        logger.error(f"An error occurred in the handle_text function: {e}")
        bot.reply_to(message, "Произошла ошибка при обработке текстового сообщения. Пожалуйста, попробуйте еще раз.")


# Обработчик inline-клавиатуры
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.data == 'yes':
            bot.send_message(call.message.chat.id, "Введите пароль для проверки надежности:")
            bot.register_next_step_handler(call.message, check_password_reliability)
        elif call.data == 'no':
            bot.send_message(call.message.chat.id, "Хорошо, не проблема.")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Продемонстрировать бота преподавателю",
                              reply_markup=None)
    except Exception as e:
        logger.error(f"An error occurred in the callback_inline function: {e}")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Произошла ошибка при обработке inline-клавиатуры. Пожалуйста, попробуйте еще раз.",
                              reply_markup=None)


# Функция для проверки надежности пароля
def check_password_reliability(message):
    try:
        password_reliability = calculate_password_reliability(message.text)
        bot.send_message(message.chat.id, f"Надежность пароля: {password_reliability}")
    except Exception as e:
        logger.error(f"An error occurred in the check_password_reliability function: {e}")
        bot.reply_to(message, "Произошла ошибка при проверке надежности пароля. Пожалуйста, попробуйте еще раз.")
