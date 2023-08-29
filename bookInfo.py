"""
This file contains all the data about books entered by the user.
"""
from bs4 import BeautifulSoup
import requests
import re
import csv


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


def get_urls():
    urls = []
    for i in range(1, 11):
        library_url = 'https://openlibrary.org/trending/forever?page=' + str(i)
        response = requests.get(library_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        a_tags = soup.find_all('a', class_='results', attrs={'itemprop': "url"})
        for a_tag in a_tags:
            urls.append(['https://openlibrary.org' + a_tag['href']])
    return urls


def write_urls_to_csv():
    urls = get_urls()
    with open('openlibraryURLs.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        for url in urls:
            writer.writerow(url)


def book_title(soup):
    title_tag = soup.find('h1', class_="work-title", attrs={"itemprop": "name"})
    return title_tag.text


def book_author(soup):
    author = soup.find('a', attrs={"itemprop": "author"})
    return author.text


def genres(soup):
    genres_list = []
    genres_tag = soup.find_all('a', attrs={"data-ol-link-track": "BookOverview|SubjectClick"})
    # print(genres_tag)
    for genre in genres_tag:
        genres_list.append(genre.text)
    return genres_list


def description(soup):
    desc = soup.find('div', class_='book-description').text.split('\n')
    modified_desc=desc[:-2]


    return ''.join(modified_desc)


def stars_and_rating(soup):
    stars = soup.find('span', attrs={'itemprop': "ratingValue"}).text
    ratings = soup.find('span', attrs={'itemprop': "reviewCount"})
    return [stars, ratings.text]


def get_html_content(url: str):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def create_book(url: str):
    soup = get_html_content(url)
    stars_rating = stars_and_rating(soup)
    return Book(book_title(soup), book_author(soup), genres(soup), stars_rating[0], stars_rating[1])


def write_books_to_csv():
    urls = []
    with open('openlibraryURLs.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            urls.append(row)
    with open('books.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Title', 'Author', 'Description', 'Genres', 'Rating', 'Rating-count'])
        for url in urls:
            book = create_book(url[0])
            entry = [book.title, book.author, book.description, book.genres, book.stars, book.rating]
            writer.writerow(entry)
