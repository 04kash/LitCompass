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


def get_books():
    urls = get_page_urls()
    books = []
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        book_infos = soup.find_all('div', class_='BookListItem__body')
        for book_info in book_infos:
            title = book_info.find('h3', class_='Text Text__title3 Text__umber').text
            author = book_info.find('div', class_='BookListItem__authors').text
            description = book_info.find('span',class_="Formatted").text
            rating = book_info.find('span', class_="AverageRating__ratingValue").text
            rating_count = book_info.find('span',class_="Text Text__body3 Text__subdued").text
            book = [title,author,description,rating,rating_count]
            books.append(book)
    return books


def write_books_to_csv():
    books = get_books()
    existing_books = []
    with open('books_goodreads.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            existing_books.append(row)
    new_books = []
    for i in range(len(books)):
        if books[i] not in existing_books:
            new_books.append(books[i])

    with open('books_goodreads.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        for book in new_books:
            writer.writerow(book)

# TODO:make sure there are no duplicate books
