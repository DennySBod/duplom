import json
from telebot import types, TeleBot
from lesson_schedule import send_lesson_schedule, send_day_selection_menu, send_class_schedule, update_lesson_schedule, \
    class_schedules
from admin import is_admin, send_global_message
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

    bot.reply_to(message, "Вітаю! Я твій особистий помічник у всіх шкільних питаннях. Як я можу тобі допомогти сьогодні?")
    send_main_menu(message)

def send_main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Розклад дзвінків")
    button2 = types.KeyboardButton("Розклад уроків")
    if is_admin(message.from_user.id):
        button3 = types.KeyboardButton("Адмін панель")
    markup.add(button1, button2)
    if is_admin(message.from_user.id):
        markup.add(button3)
    bot.send_message(message.chat.id, text="Виберіть опцію:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ["1 КЛАС", "2-4 КЛАС", "5-9 КЛАС"])
def handle_class_schedule_request(message):
    class_number = message.text
    send_bell_schedule_for_class(bot, message, class_number)


@bot.message_handler(
    func=lambda message: message.text in ["1 Клас", "2 Клас", "3 Клас", "4 Клас", "5 Клас", "6 Клас", "7 Клас",
                                          "8 Клас", "9 Клас"])
def handle_class_selection(message):
    global selected_class
    selected_class = message.text
    send_day_selection_menu(bot, message)


@bot.message_handler(func=lambda message: message.text in ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця"])
def handle_day_selection(message):
    global selected_class, selected_day
    selected_day = message.text
    send_class_schedule(bot, message, int(selected_class.split()[0]), selected_day.lower())


@bot.message_handler(func=lambda message: message.text == "Назад")
def handle_back_button(message):
    send_lesson_schedule(bot, message)


@bot.message_handler(func=lambda message: message.text == "Адмін панель" and is_admin(message.from_user.id))
def handle_admin_panel(message):
    send_admin_menu(message)


def send_admin_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Редагувати розклад уроків")
    button2 = types.KeyboardButton("Редагувати розклад дзвінків")
    button3 = types.KeyboardButton("Надіслати повідомлення всім")
    button4 = types.KeyboardButton("Головне меню")
    markup.add(button1, button2, button3, button4)
    bot.send_message(message.chat.id, text="Адмін панель:", reply_markup=markup)


@bot.message_handler(
    func=lambda message: message.text == "Редагувати розклад уроків" and is_admin(message.from_user.id))
def handle_edit_lesson_schedule(message):
    send_lesson_schedule(bot, message)


@bot.message_handler(func=lambda message: message.text in ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця"])
def handle_day_selection(message):
    global selected_class, selected_day
    selected_day = message.text
    class_number = int(selected_class.split()[0])
    markup = types.InlineKeyboardMarkup()
    class_info = next((item for item in class_schedules if item["клас"] == class_number), None)
    if class_info and selected_day.lower() in class_info["дні"]:
        schedule = class_info["дні"][selected_day.lower()]
        for i, subj in enumerate(schedule):
            button = types.InlineKeyboardButton(text=f"{i + 1}: {subj}", callback_data=f"edit_{i}")
            markup.add(button)
        bot.send_message(message.chat.id, text=f"Розклад на {selected_day}:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("edit_"))
def handle_edit_lesson(call):
    global selected_lesson_index
    selected_lesson_index = int(call.data.split("_")[1])
    bot.send_message(call.message.chat.id, text="Введіть нову назву уроку:")


@bot.message_handler(func=lambda message: selected_lesson_index != -1)
def handle_new_lesson_name(message):
    global selected_class, selected_day, selected_lesson_index
    new_lesson_name = message.text
    class_number = int(selected_class.split()[0])
    class_info = next((item for item in class_schedules if item["клас"] == class_number), None)
    if class_info and selected_day.lower() in class_info["дні"]:
        class_info["дні"][selected_day.lower()][selected_lesson_index] = new_lesson_name
        update_lesson_schedule(class_schedules)
        bot.send_message(message.chat.id, text="Розклад оновлено.")
    selected_lesson_index = -1


@bot.message_handler(
    func=lambda message: message.text == "Надіслати повідомлення всім" and is_admin(message.from_user.id))
def handle_send_global_message(message):
    bot.send_message(message.chat.id, text="Введіть повідомлення для надсилання всім користувачам:")
    bot.register_next_step_handler(message, process_global_message)


def process_global_message(message):
    text = message.text
    send_global_message(bot, text)
    bot.send_message(message.chat.id, text="Повідомлення надіслано всім користувачам.")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "Розклад дзвінків":
        send_bell_schedule(bot, message)
    elif message.text == "Розклад уроків":
        send_lesson_schedule(bot, message)
    elif message.text == "Головне меню":
        send_main_menu(message)
    else:
        bot.send_message(message.chat.id, text="Команди не існує")
        send_main_menu(message)


try:
    bot.polling(none_stop=True)
except Exception as e:
    print(f"Помилка: {e}")
