from telebot import types

# Функція для відправлення розкладу дзвінків
def send_bell_schedule(bot, message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("1 КЛАС")
    btn2 = types.KeyboardButton("2-4 КЛАС")
    btn3 = types.KeyboardButton("5-9 КЛАС")
    back = types.KeyboardButton("Головне меню 🏠")
    markup.add(btn1, btn2, btn3, back)
    bot.send_message(message.chat.id, text="Виберіть клас для розкладу дзвінків", reply_markup=markup)

# Функція для відправлення розкладу дзвінків для певного класу
def send_bell_schedule_for_class(bot, message, class_number):
    if class_number == "1 КЛАС":
        bot.send_message(message.chat.id,
                         "*-=(РОЗКЛАД ДЗВІНКІВ 1 КЛАС)=-* \n"+
                         "1) 08:30 - 09:05\n"+
                         "2) 09:15 - 09:50\n"+
                         "3) 10:10 - 10:45\n"+
                         "4) 10:55 - 11:30\n"+
                         "5) 11:40 - 12:15\n", parse_mode='Markdown')
    elif class_number == "2-4 КЛАС":
        bot.send_message(message.chat.id,
                         "*-=(РОЗКЛАД ДЗВІНКІВ 2-4 КЛАС)=-* \n"+
                         "1) 08:30 - 09:10\n"+
                         "2) 09:20 - 10:00\n"+
                         "3) 10:20 - 11:00\n"+
                         "4) 11:10 - 11:40\n"+
                         "5) 11:50 - 12:20\n"+
                         "6) 12:30 - 13:10\n", parse_mode='Markdown')
    elif class_number == "5-9 КЛАС":
        bot.send_message(message.chat.id,
                         "*-=(РОЗКЛАД ДЗВІНКІВ 5-9 КЛАС)=-* \n"+
                         "1) 08:30 - 09:15\n"+
                         "2) 09:25 - 10:10\n"+
                         "3) 10:20 - 11:05\n"+
                         "4) 11:15 - 12:00\n"+
                         "5) 12:20 - 13:05\n"+
                         "6) 13:15 - 14:00\n"+
                         "7) 14:10 - 14:55\n", parse_mode='Markdown')