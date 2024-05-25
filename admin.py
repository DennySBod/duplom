def is_admin(user_id):
    admin_ids = [937416743, 750610422]  # Замість цих чисел впишіть реальні Telegram ID адмінів
    return user_id in admin_ids

def send_global_message(bot, message_text):
    with open("user_ids.txt", 'r') as file:
        user_ids = file.readlines()
    for user_id in user_ids:
        try:
            bot.send_message(user_id.strip(), message_text)
        except Exception as e:
            print(f"Не вдалося надіслати повідомлення користувачу {user_id.strip()}: {e}")
