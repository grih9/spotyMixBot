import csv

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


def get_song_map():
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

def get_playlists(sp):
    df_spec = pd.read_csv("./playlist_data.csv", usecols=['uid'])
    df_spec.head()

    _dict = get_song_map()

    tracks = df_spec['uid']
    max_num = 50
    total_num = len(tracks)
    k = 276231
    with open("song_new.csv", "a", newline='', encoding="utf-8") as file:
        csv_writer = csv.writer(file)
        while k < total_num:
            track_slice = tracks[k:k + max_num]
            features_result = sp.audio_features(track_slice)
            info_result = sp.tracks(track_slice)
            artists = [elem["artists"][0]["id"] for elem in info_result['tracks'] if elem is not None]
            genre_result = sp.artists(artists)

            for i in range(len(track_slice)):
                try:
                    if genre_result["artists"][i] == []:
                        print(k + i, "ERROR1")
                        continue
                except Exception:
                    print(k + i, "ERROR1")
                if info_result['tracks'][i] is None:
                    print(k + i, "ERROR2")
                    continue
                current_track = track_slice[k + i]
                if _dict.get(current_track) is None:
                    del features_result[i]["key"]
                    del features_result[i]["analysis_url"]
                    del features_result[i]["time_signature"]
                    del features_result[i]["track_href"]
                    del features_result[i]["type"]
                    del features_result[i]["uri"]
                    del features_result[i]["duration_ms"]
                    del features_result[i]["mode"]
                    result = features_result[i]
                    print(k + i)
                    if info_result['tracks'][i] is None:
                        print("None")
                    result["artist_name"] = info_result['tracks'][i]["artists"][0]["name"]
                    result["track_name"] = info_result['tracks'][i]["name"]
                    result["genre_list"] = genre_result["artists"][i]["genres"]
                    _dict[current_track] = Track(**result)
                    val = _dict[current_track]
                    csv_writer.writerow(
                        [val.artist_name, val.track_name, val.id, val.danceability, val.energy, val.loudness,
                         val.speechiness, val.acousticness, val.instrumentalness, val.liveness, val.valence,
                         val.tempo, val.genre_list])
            k += max_num

    # with open("song_new.csv", "w", newline='', encoding="utf-8") as file:
    #     csv_writer = csv.writer(file)
    #     for val in _dict.values():
    #         csv_writer.writerow([val.artist_name, val.track_name, val.genre_list, val.tempo, val.valence, val.liveness,
    #                              val.instrumentalness, val.acousticness, val.speechiness, val.loudness, val.energy,
    #                              val.danceability, val.id])
    #
    #     if _dict.get(uid) is None:
    #
    #     features['uid']
    # #_dict[uid] = result
    # features = result
    #
    # for uid in df_spec['uid']:
    #
    #     if _dict.get(uid) is None:
    #         _dict[uid] = None
    #         result = sp.audio_features(tracks)
    #         print(result)



