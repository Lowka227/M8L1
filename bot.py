import telebot
from telebot import types

from config import *
from logic import *

bot = telebot.TeleBot(token)
init_db()


@bot.message_handler(commands=['start', 'help'])
@bot.message_handler(func=lambda m: m.text in ["← Назад", "← Назад в меню"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет! Это бот поддержки.\n\nЧто нужно сделать?",
        reply_markup=main_keyboard()
    )

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.send_message(
            message.chat.id,
            "Эта команда доступна только администраторам."
        )
        return

    info_text = (
        "Панель администратора\n\n"
        "Доступные возможности:\n"
        "• Получать обращения пользователей в этот чат\n"
        "• Отвечать на обращения:\n"
          "  1. Нажмите «Ответить» (Reply) на сообщение с обращением\n"
          "  2. Напишите текст ответа\n"
          "  → сейчас эта функция отключена в коде\n\n"
        "• Пока нет активных обращений — просто ждите уведомлений\n"

    )

    bot.send_message(
        message.chat.id,
        info_text,
        reply_markup=types.ReplyKeyboardRemove()
    )

@bot.message_handler(func=lambda m: m.text == "❓ Задать вопрос")
def show_faq(message):
    bot.send_message(
        message.chat.id,
        "Выберите вопрос:",
        reply_markup=faq_keyboard()
    )

@bot.message_handler(func=lambda m: m.text in faq)
def send_answer(message):
    question = message.text
    answer = faq[question]
    bot.send_message(
        message.chat.id,
        f"{question}\n\n{answer}",
        reply_markup=back_keyboard()
    )

@bot.message_handler(func=lambda m: m.text == "📩 Написать специалисту")
def to_specialist(message):
    bot.send_message(
        message.chat.id,
        "Напишите ваш вопрос или проблему текстом.",
        reply_markup=back_keyboard()
    )

@bot.message_handler(content_types=['text'])
def handle_text(message):
    text = message.text.strip()
    user = message.from_user
    user_id = user.id

    if user_id in ADMIN_IDS:
        if message.reply_to_message:
            replied = message.reply_to_message
            if "ID:" in replied.text:
                for line in replied.text.split("\n"):
                    if line.strip().startswith("ID:"):
                        target_id_str = line.split(":", 1)[1].strip()
                        target_user_id = int(target_id_str)
                        bot.send_message(
                            target_user_id,
                            f"Ответ от поддержки:\n{text}",
                            reply_markup=main_keyboard()
                        )
                        bot.send_message(
                            message.chat.id,
                            f"Ответ отправлен пользователю (ID {target_user_id})"
                        )
                        return

        return


    if text in [
        "❓ Задать вопрос",
        "📩 Написать специалисту",
        "← Назад",
        "← Назад в меню"
    ]:
        return

    username = user.username or "нет"
    first_name = user.first_name or "Пользователь"

    save_request(user_id, username, first_name, text)

    notification = (
        f"Новое обращение:\n"
        f"Имя: {first_name}\n"
        f"Username: @{username}\n"
        f"ID: {user_id}\n"
        f" Текст: {text}\n"
        f"Чтобы ответить → нажмите «Ответить» на это сообщение и напишите текст"
    )
    for admin_id in ADMIN_IDS:
            bot.send_message(admin_id, notification)

    bot.send_message(
        message.chat.id,
        "Ваше сообщение принято!\nСпециалист ответит в ближайшее время.",
        reply_markup=main_keyboard()
    )

if __name__ == "__main__":
    bot.infinity_polling()
