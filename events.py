from telebot import types
from parse_news import fetch_news, parse_news
from telegram import school_url

def send_events(bot, message):
    markup = types.InlineKeyboardMarkup()
    # Приклад кнопок для подій
    button1 = types.InlineKeyboardButton("Наш сайт школи🖥️", url="https://goncharivkaschool.e-schools.info/m/")
    button2 = types.InlineKeyboardButton("Спільнота у Facebook 👥 ", url="https://www.facebook.com/profile.php?id=100076188379496")
    button3 = types.InlineKeyboardButton("Останні новини 📣", callback_data="send_news")
    markup.add(button1)
    markup.add(button2)
    markup.add(button3)
    bot.send_message(message.chat.id, text="Виберіть дію, яка вас цікавить: ", reply_markup=markup)

def send_news(bot, message):
    markup = types.InlineKeyboardMarkup()
    html = fetch_news(school_url)
    if html:
        news_list = parse_news(html)
        for news in news_list:
            button = types.InlineKeyboardButton(news['title'], url=news['link'])
            markup.add(button)
        bot.send_message(message.chat.id, text="Останні новини 📰:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="Останніх новин немає 📰:(")
