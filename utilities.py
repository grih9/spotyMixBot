import csv
import datetime
import json
import os
import uuid

from pr_constants import GENRES, G


def process_data_files(path):
    filenames = os.listdir(path)
    data = []
    for filename in sorted(filenames):
        if filename.startswith("mpd.slice.") and filename.endswith(".json"):
            fullpath = os.sep.join((path, filename))
            with open(fullpath) as f:
                js = f.read()

            mpd_slice = json.loads(js)
            for playlist in mpd_slice["playlists"]:
                process_playlist(data, playlist)
    return data


def process_playlist(data, playlist):
    tracks = []
    for track in playlist["tracks"]:
        tracks.append(str(track["track_uri"]).split(":track:")[1])

    data.append(tracks)

def write_data_to_file():
    data = process_data_files("data")
    with open("playlist_data.csv", "w", newline='') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["playlist_id", "uid"])
        playlist_id = 1
        for playlist in data:
            for track in playlist:
                csv_writer.writerow([playlist_id, track])
            playlist_id += 1

def create_playlist_with_recommended_songs(sp, tracks=None, playlist_name=None):
    if tracks is None:
        results = sp.recommendations(seed_genres=["classical"])
        tracks = []
        for idx, item in enumerate(results['tracks']):
            tracks.append(item["id"])
    if playlist_name is None:
        playlist_name = f"SpotyMix Bot - {datetime.datetime.now()}"
    user = sp.current_user()
    playlist = sp.user_playlist_create(user["id"], playlist_name)
    sp.playlist_add_items(playlist['id'], tracks)
    return playlist

def read_genres():
    data = process_data_files("data")
    with open("song_data.csv", "r", encoding="utf-8") as file:
        csv_reader = csv.reader(file)
        result = []
        for row in csv_reader:
            genres = row[15].split()
            for genre in genres:
                if genre in GENRES.values() and genre not in result:
                    result.append(genre)

        print(result)
        print(len(result))

def create_train_data():
    with open("train_data.csv", "w", encoding="utf-8", newline='') as write_file:
        csv_writer = csv.writer(write_file)
        csv_writer.writerow(["danceability", "energy", "loudness", "speechiness", "acousticness", "instrumentalness",
                             "liveness", "valence", "tempo", "genre", "id"])
        with open("song_data.csv", "r", encoding="utf-8") as read_file:
            csv_reader = csv.reader(read_file)
            for row in csv_reader:
                genres = row[15].split()
                added = []
                for elem in G:
                    for genre in genres:
                        if elem in genre:
                            if elem not in added:
                                added.append(elem)
                                csv_writer.writerow([row[3], row[4], row[6], row[8], row[9], row[10], row[11], row[12], row[13], elem, row[1]])

        with open("song_new.csv", "r", encoding="utf-8") as read_file:
            csv_reader = csv.reader(read_file)
            for row in csv_reader:
                genres = row[12]
                added = []
                if genres == "[]":
                    continue
                genres = genres[1: -1].split()
                for elem in G:
                    for genre in genres:
                        if elem in genre:
                            if elem not in added:
                                added.append(elem)
                                csv_writer.writerow([row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], elem, row[2]])


if __name__ == "__main__":
    #write_data_to_file()
    #read_genres()
    create_train_data()