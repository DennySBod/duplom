from telebot import types
from telegram import bot

def send_air(bot, message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Карта України")
    button2 = types.KeyboardButton("Алгоритм дій")
    button3 = types.KeyboardButton("Головне меню")
    markup.add(button1, button2, button3)
    bot.send_message(message.chat.id, text="Повітряна тривога - Оберіть опцію:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Карта України")
def handle_air_raid_map(message):
    # URL зображення карти повітряних тривог в Україні
    map_image_url = "https://ubilling.net.ua/aerialalerts/?map=true"  # Реальний URL зображення
    bot.send_photo(message.chat.id, map_image_url, caption="Карта повітряних тривог в реальному часі")


@bot.message_handler(func=lambda message: message.text == "Алгоритм дій")
def handle_action_algorithm(message):
    # Тут можна додати код для відправлення алгоритму дій
    bot.send_message(message.chat.id, text="Тут буде алгоритм дій під час повітряної тривоги.")
