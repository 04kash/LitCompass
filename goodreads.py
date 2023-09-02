from bs4 import BeautifulSoup
import requests
import re
import csv
from datetime import datetime
import statistics
import ast

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
            description = book_info.find('span', class_="Formatted").text
            rating = book_info.find('span', class_="AverageRating__ratingValue").text
            rating_count = book_info.find('span', class_="Text Text__body3 Text__subdued").text
            book = [title, author, description, rating, rating_count]
            books.append(book)
    return books


def write_books_to_csv():
    books = get_books()
    existing_books = []
    with open('books_goodreads.csv', encoding='UTF8') as f:
        reader = csv.reader(f)
        for row in reader:
            existing_books.append(row[0])
    new_books = []
    for i in range(len(books)):
        if books[i][0] not in existing_books:  # checks if title names are same
            new_books.append(books[i])

    with open('books_goodreads.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        for book in new_books:
            writer.writerow(book)


def get_books_from_csv(file: str):
    books = []
    with open(file, encoding='UTF8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            books.append(row)
    return books


def get_popularity_score(books: list):
    weight_avg_rating = 0.4  # giving more weight to number of ratings than ratings.
    weight_num_ratings = 0.6
    ratings = [int(book[3]) for book in books]
    # ratings_count = [int(book[4].replace('k','000')) for book in books]
    mean_rating = statistics.mean(ratings)
    sd_ratings = statistics.stdev(ratings)
    pop_scores = []
    for book in books:
        z_score = (int(book[
                           3]) - mean_rating) / sd_ratings  # measure of a book's rating wrt mean_rating of books in the given list
        pop_score = (weight_avg_rating * z_score) + (weight_num_ratings * int(book[4].replace('k', '000')))
        pop_scores.append([book[0], book[1], book[2], book[3], book[4], book[5], pop_score])
    return pop_scores

def get_available_genres():
    books = get_books_from_csv('genres.csv')
    #print(books)
    genres = []
    for book in books:
        genre = ast.literal_eval(str(book[2]))
        genres.extend(genre)
        print(genres)
    print(genres)
    print(len(genres))
    # print(genres_unique)
    # print(len(genres_unique))
