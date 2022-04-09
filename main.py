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
results = sp.currently_playing()
results = sp.devices()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])

