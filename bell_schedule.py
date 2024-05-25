from telebot import types

# Функція для відправлення розкладу дзвінків
def send_bell_schedule(bot, message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("1 КЛАС")
    btn2 = types.KeyboardButton("2-4 КЛАС")
    btn3 = types.KeyboardButton("5-9 КЛАС")
    back = types.KeyboardButton("Головне меню")
    markup.add(btn1, btn2, btn3, back)
    bot.send_message(message.chat.id, text="Виберіть клас для розкладу дзвінків", reply_markup=markup)

# Функція для відправлення розкладу дзвінків для певного класу
def send_bell_schedule_for_class(bot, message, class_number):
    if class_number == "1 КЛАС":
        bot.send_message(message.chat.id,
                         "*-=(РОЗКЛАД ДЗВІНКІВ 1 КЛАС)=-*\n"
                         "1) 08:30 - 09:00\n"
                         "2) 09:10 - 09:40\n"
                         "3) 10:00 - 10:30\n"
                         "4) 10:40 - 11:10\n"
                         "5) 11:20 - 11:50\n"
                         "6) 12:00 - 12:30\n")
    elif class_number == "2-4 КЛАС":
        bot.send_message(message.chat.id,
                         "*-=(РОЗКЛАД ДЗВІНКІВ 2-4 КЛАС)=-*\n"
                         "1) 08:00 - 08:40\n"
                         "2) 08:50 - 09:30\n"
                         "3) 09:40 - 10:20\n"
                         "4) 10:30 - 11:10\n"
                         "5) 11:20 - 12:00\n"
                         "6) 12:10 - 12:50\n")
    elif class_number == "5-9 КЛАС":
        bot.send_message(message.chat.id,
                         "*-=(РОЗКЛАД ДЗВІНКІВ 5-9 КЛАС)=-*\n"
                         "1) 07:45 - 08:25\n"
                         "2) 08:35 - 09:15\n"
                         "3) 09:25 - 10:05\n"
                         "4) 10:15 - 10:55\n"
                         "5) 11:05 - 11:45\n"
                         "6) 11:55 - 12:35\n")
