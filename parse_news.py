import requests
from bs4 import BeautifulSoup
from telegram import school_url

def fetch_news(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

def parse_news(html):
    soup = BeautifulSoup(html, 'html.parser')
    news_items = soup.find_all('div', class_='sch_news_item')
    
    news_list = []
    
    for item in news_items:
        title_tag = item.find('div', class_='title')
        if title_tag:
            title = title_tag.text.strip()
            link_tag = item.find('a', href=True)
            link = link_tag['href'] if link_tag else 'No link available'
            
            news_list.append({
                'title': title,
                'link': f"https://goncharivkaschool.e-schools.info{link}"
            })
        else:
            print("Title not found for a news item")
    
    return news_list

