import csv
from datetime import datetime
import json
import os
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob
import re

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from tensorflow.python.keras.models import load_model
import numpy as np

from pr_constants import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SPOTIPY_SCOPE, GIN
from song_map import get_playlists, Track
from song_recomendation.models.model_final import recommend_from_playlist
from utilities import create_playlist_with_recommended_songs
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI, scope=SPOTIPY_SCOPE))
types = {1: "short",
         2: "medium",
         3: "long"}

r_type = input("Выберите временной промежуток:\n1. Короткий, 2. Средний. 3. Длительный: ")
while r_type not in ["1", "2", "3"]:
    r_type = input("Выберите временной промежуток:\n1. Короткий, 2. Средний. 3. Длительный: ")

r_type = types[int(r_type)]

top_tracks = input("Введите число треков от 1 до 50: ")
while int(top_tracks) not in range(1, 51):
    top_tracks = input("Введите число треков от 1 до 50: ")
top_tracks = int(top_tracks)

use_genre = input("Создать плейлист по жанрам?\n1. Да, 0. Нет: ")
while use_genre != "1" and use_genre != "0":
    use_genre = input("Создать плейлист по жанрам?\n1. Да, 0. Нет: ")
use_genre = int(use_genre)

result_short = sp.current_user_top_tracks(limit=top_tracks, time_range="short_term")
result_mid = sp.current_user_top_tracks(limit=top_tracks, time_range="medium_term")
result_long = sp.current_user_top_tracks(limit=top_tracks, time_range="long_term")
if r_type == "long":
    res = result_long
elif r_type == "medium":
    res = result_mid
else:
    res = result_short

print(f"\nВаш топ-{top_tracks} за выбранный промежуток времени:")
with open("playlist_create.csv", 'w', encoding="utf-8", newline='') as write_file:
    csv_writer = csv.writer(write_file)
    csv_writer.writerow(["danceability", "energy", "loudness", "speechiness", "acousticness", "instrumentalness",
                         "liveness", "valence", "tempo", "name", "id"])
    ids = [item['id'] for item in res['items']]
    features_result = sp.audio_features(ids)
    for idx, item in enumerate(res['items']):
        track = item['name']
        id = item['id']
        print(idx + 1, item['artists'][0]['name'], " – ", track)
        del features_result[idx]["key"]
        del features_result[idx]["analysis_url"]
        del features_result[idx]["time_signature"]
        del features_result[idx]["track_href"]
        del features_result[idx]["type"]
        del features_result[idx]["uri"]
        del features_result[idx]["duration_ms"]
        del features_result[idx]["mode"]
        result = features_result[idx]
        val = Track(**result)
        csv_writer.writerow(
            [val.danceability, val.energy, val.loudness, val.speechiness, val.acousticness,
             val.instrumentalness, val.liveness, val.valence,
             val.tempo, track, val.id])

genre_cid = None
if int(use_genre) == 1:
    print("Определяю жанры...")
    print_data = input("Вывести данные определения жанров?\n1. Да, 0. Нет: ")
    while print_data != "1" and print_data != "0":
        print_data = input("Вывести данные определения жанров?\n1. Да, 0. Нет: ")
    print_data = int(print_data)
    predictions = []
    model = load_model("Model5.h5")
    with open("playlist_create.csv", "r", encoding="utf-8") as read_file:
        csv_reader = csv.reader(read_file)
        next(csv_reader, None)
        for row in csv_reader:
            track = row[9]
            a = np.array([[float(row[0]), float(row[1]), float(row[2]) / -60.0, float(row[3]),
                           float(row[4]), float(row[5]), float(row[6]), float(row[7]), float(row[8]) / 240]])
            prediction = model.predict(a)
            if print_data == 1:
                print(track)
            data = {}
            for i, elem in enumerate(prediction[0]):
                data[GIN[i]] = elem
            data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}
            b = 0
            if print_data == 1:
                for key, value in data.items():
                    print(key, value)
                    b += 1
                    if b == 4:
                        break
            if abs(list(data.values())[0] - list(data.values())[1]) < 0.045:
                predictions.append(list(data.keys())[0])
                predictions.append(list(data.keys())[1])
            else:
                predictions.append(list(data.keys())[0])

    values = set(predictions)
    dict_pred = {}
    for val in values:
        dict_pred[val] = predictions.count(val)

    dict_pred = {k: v for k, v in sorted(dict_pred.items(), key=lambda item: item[1], reverse=True)}
    print(dict_pred)

    print(f"Похоже вам нравится {list(dict_pred.keys())[0]}, целых {list(dict_pred.values())[0]} песен такого жанра!")
    genre_cid = list(dict_pred.keys())[0]

train_features = pd.read_csv("train_data.csv")
train_features = train_features.drop(columns="genre")
playlist_features = pd.read_csv("playlist_create.csv")
playlist_features = playlist_features.drop(columns="name")

spotify_features = pd.read_csv("spotify.csv")
spotify_features = spotify_features.loc[spotify_features['popularity'] > 60]
sp_feat = spotify_features[["danceability", "energy", "loudness", "speechiness", "acousticness", "instrumentalness",
                            "liveness", "valence", "tempo", "id"]].reset_index(drop=True)

train_features = pd.concat([train_features, playlist_features, sp_feat], axis=0)
pop = train_features[["danceability", "energy", "loudness", "speechiness", "acousticness", "instrumentalness",
                      "liveness", "valence", "tempo"]].reset_index(drop=True)
names = train_features[["id"]].reset_index(drop=True)
scaler = MinMaxScaler()
pop_scaled = pd.DataFrame(scaler.fit_transform(pop), columns=pop.columns)
pop_scaled.head()

train_features = pd.concat([pop_scaled, names], axis=1)
songDF = pd.read_csv("spotify.csv")
# songDF.columns = ["artist", "song", "id", 'data1', 'data2', 'data3', 'data4', 'data5', 'data6', 'data7', 'data8',
#                   'data9', 'data10']
songDF = spotify_features
train_features.drop_duplicates("id", inplace=True)
data_recommend = recommend_from_playlist(songDF=songDF, complete_feature_set=train_features, playlistDF_test=playlist_features)[:40]
#print(data_recomend)
ids_recommend = data_recommend['id'].values
playlist_name = str(input("Введите имя для плейлистов:"))
create_playlist_with_recommended_songs(sp=sp, tracks=ids_recommend, playlist_name=f"{playlist_name} [SpotyMixBot {r_type[0]}{top_tracks}]")
print("Плейлист на основе прослушиваний создан! Наслаждайтесь!")
if use_genre == 1:
    create_playlist_with_recommended_songs(sp=sp, genre_cid=genre_cid,
                                           playlist_name=f"{playlist_name} [Spotify {genre_cid}]")
print("Плейлист с рекомендациями по жанру создан! Наслаждайтесь!")

