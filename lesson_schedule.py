import json
from telebot import types

# Завантаження даних розкладу уроків з JSON файлу
def load_schedules(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

# Змінна для зберігання розкладу
class_schedules = load_schedules("class_schedules.json")

# Функція для збереження даних розкладу уроків у JSON файл
def save_schedules(filename, schedules):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(schedules, file, ensure_ascii=False, indent=4)

# Функція для оновлення розкладу уроків
def update_lesson_schedule(new_schedule):
    global class_schedules
    class_schedules = new_schedule
    save_schedules("class_schedules.json", class_schedules)


# Функція для відправлення розкладу уроків для певного класу
def send_lesson_schedule(bot, message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    class_buttons = [types.KeyboardButton(f"{i['клас']} Клас") for i in class_schedules]
    back = types.KeyboardButton("Головне меню")
    markup.add(*class_buttons, back)
    bot.send_message(message.chat.id, text="Виберіть клас для розкладу уроків", reply_markup=markup)

# Функція для відправлення розкладу уроків для певного класу та дня тижня
def send_class_schedule(bot, message, class_number, day):
    class_info = next((item for item in class_schedules if item["клас"] == int(class_number)), None)
    if class_info and day.lower() in class_info["дні"]:
        schedule = class_info["дні"][day.lower()]
        formatted_schedule = f"Розклад у {class_number} класі на {day}:\n" + "\n".join(f"{i+1}) {subj}" for i, subj in enumerate(schedule))
        bot.send_message(message.chat.id, formatted_schedule)

def send_day_selection_menu(bot, message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    days = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця"]
    markup.add(*[types.KeyboardButton(day) for day in days])
    back = types.KeyboardButton("Назад")
    markup.add(back)
    bot.send_message(message.chat.id, text="Виберіть день тижня", reply_markup=markup)
