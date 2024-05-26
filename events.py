# events.py
from telebot import types

def send_events(bot, message):
    markup = types.InlineKeyboardMarkup()
    # Приклад кнопок для подій
    button1 = types.InlineKeyboardButton("Сайт", url="https://goncharivkaschool.e-schools.info/m/")
    button2 = types.InlineKeyboardButton("Фейсбук", url="https://www.facebook.com/profile.php?id=100076188379496")
    button3 = types.InlineKeyboardButton("Подія 3", url="http://example.com/event3")
    markup.add(button1)
    markup.add(button2)
    markup.add(button3)
    bot.send_message(message.chat.id, text="Оберіть дію:", reply_markup=markup)
    
