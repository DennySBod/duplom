from telebot import types
from air_raid_alert import send_air
from events import send_events, send_news
from lesson_schedule import send_lesson_schedule, send_day_selection_menu, send_class_schedule, load_schedules
from admin import is_admin, send_global_message, send_admin_menu, edit_lesson_schedule, edit_class_schedule, edit_day_schedule, update_lesson
from bell_schedule import send_bell_schedule_for_class, send_bell_schedule
from telegram import bot

selected_class = ""
selected_day = ""
selected_lesson_index = -1

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    try:
        with open("user_ids.txt", 'r') as file:
            user_ids = file.read().splitlines()
    except FileNotFoundError:
        user_ids = []

    if str(user_id) not in user_ids:
        with open("user_ids.txt", 'a') as file:
            file.write(f"{user_id}\n")

    bot.reply_to(message, "*Вітаю!*\nЯ твій особистий помічник у всіх шкільних питаннях. \n\nЯк я можу тобі допомогти сьогодні?", parse_mode='Markdown')
    send_main_menu(message)

def send_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Розклад дзвінків")
    button2 = types.KeyboardButton("Розклад уроків")
    button4 = types.KeyboardButton("Події")
    button5 = types.KeyboardButton("Повітряна тривога")
    if is_admin(message.from_user.id):
        button3 = types.KeyboardButton("Адмін панель")
    markup.add(button1, button2, button4, button5)
    if is_admin(message.from_user.id):
        markup.add(button3)

    bot.send_message(message.chat.id, text=f"Вітаємо, *{message.chat.username}* \n\n*Оберіть дію:*", reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text in ["1 КЛАС", "2-4 КЛАС", "5-9 КЛАС"])
def handle_class_schedule_request(message):
    class_number = message.text
    send_bell_schedule_for_class(bot, message, class_number)

@bot.message_handler(
    func=lambda message: message.text in ["1 клас", "2 клас", "3 клас", "4 клас", "5 клас", "6 клас", "7 клас",
                                          "8 клас", "9 клас"])
def handle_class_selection(message):
    global selected_class
    selected_class = message.text
    send_day_selection_menu(bot, message)

@bot.message_handler(func=lambda message: message.text in ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця"])
def handle_day_selection(message):
    global selected_class, selected_day
    selected_day = message.text
    send_class_schedule(bot, message, str(selected_class.split()[0]), selected_day.lower())

@bot.message_handler(func=lambda message: message.text == "Повітряна тривога")
def handle_air_raid_alert(message):
    send_air(bot, message)

@bot.message_handler(func=lambda message: message.text == "Карта України")
def handle_air_raid_map(message):
    send_air(bot, message)

@bot.message_handler(func=lambda message: message.text == "Алгоритм дій")
def handle_action_algorithm(message):
    send_air(bot, message)

@bot.message_handler(func=lambda message: message.text == "Назад")
def handle_back_button(message):
    send_lesson_schedule(bot, message)

@bot.message_handler(func=lambda message: message.text == "Адмін панель" and is_admin(message.from_user.id))
def handle_admin_panel(message):
    send_admin_menu(bot, message)

@bot.callback_query_handler(func=lambda call: call.data == "edit_lesson_schedule" and is_admin(call.from_user.id))
def handle_edit_lesson_schedule(call):
    edit_lesson_schedule(bot, call.message)

def process_global_message(message):
    text = message.text
    send_global_message(bot, text)
    bot.send_message(message.chat.id, text="Повідомлення надіслано всім користувачам.")

@bot.callback_query_handler(
    func=lambda call: call.data == "send_global_message" and is_admin(call.from_user.id))
def handle_send_global_message(call):
    bot.send_message(call.message.chat.id, text="Введіть повідомлення для надсилання всім користувачам:")
    bot.register_next_step_handler(call.message, process_global_message)

@bot.callback_query_handler(func=lambda call: call.data == "send_news")
def handle_send_news(call):
    send_news(bot, call.message)

@bot.callback_query_handler(func=lambda call: call.data.startswith("class_") and is_admin(call.from_user.id))
def handle_edit_class_schedule(call):
    class_number = str(call.data.split("_")[1])
    edit_class_schedule(bot, call.message, class_number)

@bot.callback_query_handler(func=lambda call: call.data.startswith("day_") and is_admin(call.from_user.id))
def handle_edit_day_schedule(call):
    _, class_number, day = call.data.split("_")
    edit_day_schedule(bot, call.message, str(class_number), day)

@bot.callback_query_handler(func=lambda call: call.data.startswith("lesson_") and is_admin(call.from_user.id))
def handle_edit_lesson(call):
    _, class_number, day, lesson_index = call.data.split("_")
    bot.send_message(call.message.chat.id, text="Введіть нову назву уроку:")
    bot.register_next_step_handler(call.message, process_new_lesson_name, str(class_number), day, int(lesson_index))

def process_new_lesson_name(message, class_number, day, lesson_index):
    new_lesson = message.text
    update_lesson(bot, message, class_number, day, lesson_index, new_lesson)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "Розклад дзвінків":
        send_bell_schedule(bot, message)
    elif message.text == "Розклад уроків":
        send_lesson_schedule(bot, message)
    elif message.text == "Події":
        send_events(bot, message)
    elif message.text == "Головне меню":
        send_main_menu(message)
    else:
        bot.send_message(message.chat.id, text="Команди не існує")
        send_main_menu(message)

try:
    bot.infinity_polling(none_stop=True)
except Exception as e:
    print(f"Помилка: {e}")
