import requests
from bs4 import BeautifulSoup
from datetime import datetime


KEYWORDS = ['дизайн', 'фото', 'web', 'python']
URL = 'https://habr.com/ru/all/'

def get_article_info(article):
    date_element = article.find('a', class_='tm-article-datetime-published tm-article-datetime-published_link').find('time')
    if date_element:
        date_str = date_element['datetime']
        date_obj = datetime.fromisoformat(date_str[:-1])
        date = date_obj.strftime('%d %B %Y, %H:%M')
    else:
        date = "Дата не найдена"

    title_element = article.find('h2', class_='tm-title tm-title_h2').find('a')
    if title_element:
        title = title_element.text.strip()
    else:
        title = "Заголовок не найден"

    link = title_element['href'] if title_element else "Ссылка не найдена"
    link = 'https://habr.com' + link
    return date, title, link

def get_full_article_text(link):
    response = requests.get(link)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    article_text = soup.find('div', class_='article-formatted-body').text.strip()
    return article_text

def main():
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article', class_='tm-articles-list__item')

    for article in articles:
        preview_text = article.text.lower()
        for keyword in KEYWORDS:
            if keyword in preview_text:
                date, title, link = get_article_info(article)
                print(f'{date} – {title} – {link}')
                break

if __name__ == "__main__":
    main()
