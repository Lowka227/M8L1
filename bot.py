
import telebot
from telebot import types
from googletrans import Translator
from config import token
from logic import *

bot = telebot.TeleBot(token)
translator = Translator()

init_db()

@bot.message_handler(commands=['start', 'help'])
@bot.message_handler(func=lambda m: m.text == "← Назад")
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет! Это бот тех поддержки.\nЧто нужно сделать?",
        reply_markup=main_keyboard()
    )


@bot.message_handler(func=lambda m: m.text == "❓ Задать вопрос")
def show_questions(message):
    bot.send_message(
        message.chat.id,
        "Выберите вопрос:",
        reply_markup=faq_keyboard()
    )


@bot.message_handler(func=lambda message: message.text in faq)
def send_answer(message):
    question = message.text
    answer = faq[question]
    bot.send_message(message.chat.id, f"{answer}")



bot.infinity_polling()
