import requests
from telebot import types
from telegram import API_URL

# Завантаження даних розкладу уроків з API
def load_schedules():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Помилка завантаження розкладів: {response.status_code}")
        return []

# Функція для збереження даних розкладу уроків у API
def save_schedules(schedules):
    for schedule in schedules:
        response = requests.put(f"{API_URL}/{schedule['id']}", json=schedule)
        if response.status_code != 200:
            print(f"Помилка збереження розкладу для класу {schedule['id']}: {response.status_code}")


# Функція для відправлення розкладу уроків для певного класу
def send_lesson_schedule(bot, message):
    class_schedules = load_schedules()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    class_buttons = [types.KeyboardButton(f"{i['id']} клас") for i in class_schedules]
    back = types.KeyboardButton("Головне меню 🏠")
    markup.add(*class_buttons, back)
    bot.send_message(message.chat.id, text="Виберіть клас, для якого ви хочете переглянути розклад 📚: ", reply_markup=markup)

# Функція для відправлення розкладу уроків для певного класу та дня тижня
def send_class_schedule(bot, message, class_number, day):
    class_schedules = load_schedules()

    class_info = next((item for item in class_schedules if item["id"] == str(class_number)), None)
    if class_info and day.lower() in class_info["days"]:
        schedule = class_info["days"][day.lower()]
        formatted_schedule = f"Розклад у {class_number} класі на {day}:\n" + "\n".join(f"{i+1}) {subj}" for i, subj in enumerate(schedule))
        bot.send_message(message.chat.id, formatted_schedule)

def send_day_selection_menu(bot, message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    days = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця"]
    markup.add(*[types.KeyboardButton(day) for day in days])
    back = types.KeyboardButton("Назад 🔄")
    main_menu = types.KeyboardButton("Головне меню 🏠")
    markup.add(back)
    markup.add(main_menu)
    bot.send_message(message.chat.id, text="Оберіть день тижня для перегляду розкладу 📅: ", reply_markup=markup)
