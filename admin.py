import requests
from telebot import types
from telegram import API_URL

def is_admin(user_id):
    admin_ids = [937416743, 750610422, 471644637]  # Замість цих чисел впишіть реальні Telegram ID адмінів
    return user_id in admin_ids

def send_global_message(bot, message_text):
    with open("user_ids.txt", 'r') as file:
        user_ids = file.readlines()
    for user_id in user_ids:
        try:
            bot.send_message(user_id.strip(), message_text, parse_mode='Markdown')
        except Exception as e:
            print(f"Не вдалося надіслати повідомлення користувачу {user_id.strip()}: {e}")

def load_class_schedules():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Помилка завантаження розкладів: {response.status_code}")
        return []

def save_class_schedules(schedules):
    for schedule in schedules:
        response = requests.put(f"{API_URL}/{schedule['id']}", json=schedule)
        if response.status_code != 200:
            print(f"Помилка збереження розкладу для класу {schedule['id']}: {response.status_code}")

def send_admin_menu(bot, message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Редагувати розклад уроків", callback_data="edit_lesson_schedule")
    button2 = types.InlineKeyboardButton("Надіслати повідомлення всім", callback_data="send_global_message")
    markup.add(button1)
    markup.add(button2)
    bot.send_message(message.chat.id, text="Адмін панель:", reply_markup=markup)

def edit_lesson_schedule(bot, message):
    schedules = load_class_schedules()
    markup = types.InlineKeyboardMarkup()
    for schedule in schedules:
        button = types.InlineKeyboardButton(f"{schedule['id']} клас", callback_data=f"class_{schedule['id']}")
        markup.add(button)
    bot.send_message(message.chat.id, text="Оберіть клас для редагування:", reply_markup=markup)

def edit_class_schedule(bot, message, class_number):
    schedules = load_class_schedules()
    class_schedule = next((item for item in schedules if item["id"] == class_number), None)
    if class_schedule:
        markup = types.InlineKeyboardMarkup()
        for day in class_schedule["days"]:
            button = types.InlineKeyboardButton(day.capitalize(), callback_data=f"day_{class_number}_{day}")
            markup.add(button)
        bot.send_message(message.chat.id, text=f"Оберіть день для класу {class_number}:", reply_markup=markup)

def edit_day_schedule(bot, message, class_number, day):
    schedules = load_class_schedules()
    class_schedule = next((item for item in schedules if item["id"] == class_number), None)
    if class_schedule:
        day_schedule = class_schedule["days"][day]
        markup = types.InlineKeyboardMarkup()
        for i, lesson in enumerate(day_schedule):
            button = types.InlineKeyboardButton(f"{i + 1}) {lesson}", callback_data=f"lesson_{class_number}_{day}_{i}")
            markup.add(button)
        bot.send_message(message.chat.id, text=f"Оберіть урок для редагування на {day.capitalize()}:", reply_markup=markup)

def update_lesson(bot, message, class_number, day, lesson_index, new_lesson):
    schedules = load_class_schedules()
    class_schedule = next((item for item in schedules if item["id"] == class_number), None)
    if class_schedule:
        if new_lesson == "-":
            del class_schedule["days"][day][lesson_index]  # Видалити урок
        else:
            class_schedule["days"][day][lesson_index] = new_lesson
        save_class_schedules(schedules)
        bot.send_message(message.chat.id, text="Розклад оновлено.")
    else:
        bot.send_message(message.chat.id, text="Помилка при оновленні розкладу.")
