import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

rating = pd.read_csv('data/BX-Book-Ratings.csv', sep=',', error_bad_lines=False, encoding="utf-8")
user = pd.read_csv('data/BX-Users.csv', sep=',', error_bad_lines=False, encoding="utf-8")
book = pd.read_csv('data/BX-Books.csv', sep=',', error_bad_lines=False, encoding="utf-8")
book_rating = pd.merge(rating, book, on='ISBN')
cols = ['Year-Of-Publication', 'Publisher', 'Book-Author', 'Image-URL-S', 'Image-URL-M', 'Image-URL-L']
book_rating.drop(cols, axis=1, inplace=True)

rating_count = (book_rating.
    groupby(by=['Book-Title'])['Book-Rating'].
    count().
    reset_index().
    rename(columns={'Book-Rating': 'RatingCount_book'})
[['Book-Title', 'RatingCount_book']]
    )

threshold = 25
rating_count = rating_count.query('RatingCount_book >= @threshold')

user_rating = pd.merge(rating_count, book_rating, left_on='Book-Title', right_on='Book-Title', how='left')

user_count = (user_rating.
    groupby(by=['User-ID'])['Book-Rating'].
    count().
    reset_index().
    rename(columns={'Book-Rating': 'RatingCount_user'})
[['User-ID', 'RatingCount_user']]
    )

threshold = 20
user_count = user_count.query('RatingCount_user >= @threshold')

combined = user_rating.merge(user_count, left_on='User-ID', right_on='User-ID', how='inner')

print('Number of unique books: ', combined['Book-Title'].nunique())
print('Number of unique users: ', combined['User-ID'].nunique())