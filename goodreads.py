from bs4 import BeautifulSoup
import requests
import re
import csv
from datetime import datetime


class Book:
    title: str
    author: str
    genres: list
    stars: float
    ratings: int

    def __init__(self, title, author, genres, stars, ratings):
        self.title = title
        self.author = author
        self.genres = genres
        self.stars = stars
        self.rating = ratings


def get_page_urls():
    urls = []
    curr_month = datetime.now().month
    curr_year = datetime.now().year
    last_year = curr_year - 1
    for i in range(1, 13):
        urls.append(f'https://www.goodreads.com/book/popular_by_date/{last_year}/{i}')
    for i in range(1, curr_month + 1):
        urls.append(f'https://www.goodreads.com/book/popular_by_date/{curr_year}/{i}')

    return urls


def get_book_urls():
    urls = get_page_urls()
    book_urls = []
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        titles = soup.find_all('h3', class_="Text Text__title3 Text__umber")
        for title in titles:
            book_url = title.find('a', attrs={'data-testid': "bookTitle"})['href']
            book_urls.append([book_url])
    return book_urls


def write_urls_to_csv():
    urls = get_book_urls()
    existing_urls = []
    with open('goodreads.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            existing_urls.append(row)
    new_urls = []
    for i in range(len(urls)):
        if urls[i] not in existing_urls:
            new_urls.append(urls[i])

    with open('goodreads.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        for url in new_urls:
            writer.writerow(url)
