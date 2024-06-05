import requests
from bs4 import BeautifulSoup
from datetime import datetime
from telegram import weather_url
import pytz

def get_page_content(url):
    response = requests.get(url)
    return response.text

def parse_weather_today(page_content, start_tag, end_tag):
    start_index = page_content.find(start_tag)
    if start_index == -1:
        return ""
    end_index = page_content.find(end_tag, start_index)
    return BeautifulSoup(page_content[start_index:end_index], "html.parser").get_text()

def get_today_date(timezone_str):
    timezone = pytz.timezone(timezone_str)
    return datetime.now(timezone).strftime("%Y-%m-%d")

def get_weather_data(page_content):
    min_temp = parse_weather_today(page_content.lower(), '<div class="min">', '</div>').replace("&deg;", "°")
    max_temp = parse_weather_today(page_content.lower(), '<div class="max">', '</div>').replace("&deg;", "°")
    description = parse_weather_today(page_content.lower(), '<div class="description">', '</div>').replace("&#039;", "ʼ")
    current_temp = parse_weather_today(page_content.lower(), '<p class="today-temp">', '</p>').replace("&deg;", "°")
    return min_temp, max_temp, description, current_temp

def format_weather_message(min_temp, max_temp, current_temp, description):
    return f"*Погода на сьогодні 📡*\n{max_temp}\n{min_temp}\nЗараз на вулиці: {current_temp}\n\n{description}"

def send_weather(bot, message):
    timezone_str = "Europe/Kiev"
    today = get_today_date(timezone_str)
    url = weather_url + today
    
    page_content = get_page_content(url)
    min_temp, max_temp, description, current_temp = get_weather_data(page_content)
    
    weather_message = format_weather_message(min_temp, max_temp, current_temp, description)
    bot.send_message(message.chat.id, text=weather_message, parse_mode="Markdown")
