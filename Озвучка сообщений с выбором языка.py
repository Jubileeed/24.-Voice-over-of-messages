import telebot
from gtts import gTTS
import os

bot = telebot.TeleBot('7081132142:AAEb6GIj30L0cbo7SZj2P2fHCzymIh79pvI')

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне текст, и я озвучу его.")

# Словарь для хранения выбранного языка пользователей
user_language = {}

# Обработчик команды /language для смены языка
@bot.message_handler(commands=['language'])
def change_language(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Русский', 'English', 'Español')
    msg = bot.reply_to(message, "Выберите язык:", reply_markup=markup)
    bot.register_next_step_handler(msg, set_language)

# Установка языка
def set_language(message):
    if message.text == 'Русский':
        user_language[message.chat.id] = 'ru'
    elif message.text == 'English':
        user_language[message.chat.id] = 'en'
    elif message.text == 'Español':
        user_language[message.chat.id] = 'es'
    else:
        bot.reply_to(message, "Извините, этот язык не поддерживается.")
        return  # Прекращаем выполнение, если язык не поддерживается
    bot.reply_to(message, f"Язык установлен на {message.text}.")

# Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message):
    lang = user_language.get(message.chat.id, 'ru')  # По умолчанию русский

    try:
        # Генерация аудио с помощью gTTS
        tts = gTTS(text=message.text, lang=lang)
        tts.save('audio.mp3')  # Сохраняем файл в формате .mp3

        # Открываем и отправляем аудио как аудиофайл
        with open('audio.mp3', 'rb') as audio:
            bot.send_audio(message.chat.id, audio)  # Отправка аудиофайла

    except Exception as e:
        bot.reply_to(message, "Произошла ошибка при озвучке текста.")
        print(f"Ошибка: {e}")

    finally:
        # Удаление аудиофайла, если он был создан
        if os.path.exists('audio.mp3'):
            os.remove('audio.mp3')

# Запуск бота
bot.polling()
