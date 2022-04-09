import numpy as np
import pandas as pd


# artist_name,id,track_name,danceability,energy,key,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo,artist_pop,genres,track_pop,genres_list,subjectivity,polarity

class Track:
    def __init__(self,
                 id='',
                 danceability=0.0,
                 energy=0.0,
                 loudness=0.0,
                 speechiness=0.0,
                 acousticness=0.0,
                 instrumentalness=0.0,
                 liveness=0.0,
                 valence=0.0,
                 tempo=0.0,
                 genre_list=[],
                 track_name='',
                 artist_name='',
                 ):
        self.artist_name = artist_name
        self.track_name = track_name
        self.genre_list = genre_list
        self.tempo = tempo
        self.valence = valence
        self.liveness = liveness
        self.instrumentalness = instrumentalness
        self.acousticness = acousticness
        self.speechiness = speechiness
        self.loudness = loudness
        self.energy = energy
        self.danceability = danceability
        self.id = id


def getSongMap():
    df_spec = pd.read_csv("./song_data.csv", usecols=['id', 'danceability', 'energy', 'loudness', 'speechiness',
                                                      'acousticness', 'instrumentalness', 'liveness', 'valence',
                                                      'tempo', 'genres_list', 'track_name', 'artist_name'])
    df_spec.head()

    _dict = dict()

    for i in range(0, len(df_spec['id'])):
        _dict[df_spec['id'][i]] = Track(df_spec['id'][i], df_spec['danceability'][i], df_spec['energy'][i],
                                        df_spec['loudness'][i],
                                        df_spec['speechiness'][i], df_spec['acousticness'][i],
                                        df_spec['instrumentalness'][i],
                                        df_spec['liveness'][i], df_spec['valence'][i], df_spec['tempo'][i],
                                        df_spec['genres_list'][i], df_spec['track_name'][i], df_spec['artist_name'][i])

    return _dict

def getPlaylists(sp):
    df_spec = pd.read_csv("./playlist_data.csv", usecols=['uid'])
    df_spec.head()

    _dict = getSongMap()

    for uid in df_spec['uid']:

        if _dict.get(uid) is None:

            result = sp.audio_features(tracks)
            print(result)



