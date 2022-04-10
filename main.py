import csv
import json
import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from tensorflow.python.keras.models import load_model
import numpy as np

from pr_constants import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SPOTIPY_SCOPE, GIN
from song_map import get_playlists

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI, scope=SPOTIPY_SCOPE))
# get_playlists(sp)

model = load_model("Model.h5")
# tracks = sp.current_user_top_tracks()
# track = tracks['tracks'][0]['name']


with open("spotify.csv", "r", encoding="utf-8") as read_file:
    csv_reader = csv.reader(read_file)
    next(csv_reader, None)
    for row in csv_reader:
        artist = row[1]
        track = row[12]
        a = np.array([[float(row[2]), float(row[4]), float(row[10])/-60.0, float(row[15]),
                       float(row[0]), float(row[7]), float(row[9]), float(row[17])]])
        prediction = model.predict(a)
        print(artist, track)
        data = {}
        for i, elem in enumerate(prediction[0]):
            data[GIN[i]] = elem
        data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}
        b = 0
        for key, value in data.items():
            print(key, value)
            b += 1
            if b == 4:
                break
# a = np.array([[0.511, 0.47200000000000003, -9.277000000000001/-60.0, 0.091, 0.534, 0.614, 0.11, 0.0399]])
# # a = np.array([[0.705,0.796,-6.845/-60.0,0.267,0.0708,0.0,0.388,0.864]])
# print(a)
# prediction = model.predict(a)
# for i, elem in enumerate(prediction[0]):
#     print(GIN[i], elem)
# print(prediction)
# danceability,energy,loudness,speechiness,acousticness,instrumentalness,liveness,valence,
# 0.534,['Lorde'],0.511,258969,0.47200000000000003,0,0TEekvXTomKt3hdXDZxxeW,0.614,4,0.11,-9.277000000000001,1,Ribs,76,2013-01-01,0.091,127.978,0.0399,2013
# acousticness,artists,danceability,duration_ms,energy,explicit,id,instrumentalness,key,liveness,loudness,mode,name,popularity,release_date,speechiness,tempo,valence,year
# resu lts = sp.recommendations(seed_genres=["classical"])
# tracks = []
# for idx, item in enumerate(results['tracks']):
#     track = item['name']
#     tracks.append(item["id"])
#     print(idx, item['artists'][0]['name'], " – ", track)
#
# result = sp.audio_features(tracks)
# print(result)



# # sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,
# #                                                redirect_uri=SPOTIPY_REDIRECT_URI))
# user = sp.current_user()
# playlist_name = f"SpotyMix Bot - {uuid.uuid1()}"
# playlist = sp.user_playlist_create(user["id"], playlist_name)
#
# res = sp.playlist_add_items(playlist['id'], tracks)
#
# results = sp.current_user_saved_tracks()
#
#
#
# for idx, item in enumerate(results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])
#
#
#
# result = sp.current_user_top_artists(limit=100, time_range="short_term")
# for idx, item in enumerate(result['items']):
#     name = item["name"]
#     print(idx, name)
# result = sp.current_user_top_artists(limit=100, time_range="medium_term")
# for idx, item in enumerate(result['items']):
#     name = item["name"]
#     print(idx, name)
# result = sp.current_user_top_artists(limit=100, time_range="long_term")
# for idx, item in enumerate(result['items']):
#     name = item["name"]
#     print(idx, name)
#
# result = sp.current_user_top_tracks(limit=100, time_range="short_term")
# for idx, item in enumerate(result['items']):
#     track = item['name']
#     print(idx, item['artists'][0]['name'], " – ", track)
# result = sp.current_user_top_tracks(limit=100, time_range="medium_term")
# for idx, item in enumerate(result['items']):
#     track = item['name']
#     print(idx, item['artists'][0]['name'], " – ", track)
# result = sp.current_user_top_tracks(limit=100, time_range="long_term")
# for idx, item in enumerate(result['items']):
#     track = item['name']
#     print(idx, item['artists'][0]['name'], " – ", track)

