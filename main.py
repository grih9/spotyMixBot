import json
import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from constants import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, SPOTIPY_SCOPE
from song_map import get_playlists

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI, scope=SPOTIPY_SCOPE))
get_playlists(sp)
# results = sp.recommendations(seed_genres=["classical"])
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

