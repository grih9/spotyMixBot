import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth

from constants import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI

scope = "user-library-read streaming app-remote-control user-library-modify playlist-modify-public user-top-read " \
        "user-read-playback-position user-read-recently-played user-read-currently-playing user-read-playback-state " \
        "user-modify-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope))
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,
#                                                redirect_uri=SPOTIPY_REDIRECT_URI))

results = sp.current_user_saved_tracks()

for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])



result = sp.current_user_top_artists(limit=100, time_range="short_term")
for idx, item in enumerate(result['items']):
    name = item["name"]
    print(idx, name)
result = sp.current_user_top_artists(limit=100, time_range="medium_term")
for idx, item in enumerate(result['items']):
    name = item["name"]
    print(idx, name)
result = sp.current_user_top_artists(limit=100, time_range="long_term")
for idx, item in enumerate(result['items']):
    name = item["name"]
    print(idx, name)

result = sp.current_user_top_tracks(limit=100, time_range="short_term")
for idx, item in enumerate(result['items']):
    track = item['name']
    print(idx, item['artists'][0]['name'], " – ", track)
result = sp.current_user_top_tracks(limit=100, time_range="medium_term")
for idx, item in enumerate(result['items']):
    track = item['name']
    print(idx, item['artists'][0]['name'], " – ", track)
result = sp.current_user_top_tracks(limit=100, time_range="long_term")
for idx, item in enumerate(result['items']):
    track = item['name']
    print(idx, item['artists'][0]['name'], " – ", track)
