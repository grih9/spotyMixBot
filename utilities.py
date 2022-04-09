import csv
import json
import os
import uuid

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

def create_playlist_with_recommended_songs(sp):
    results = sp.recommendations(seed_genres=["classical"])
    tracks = []
    for idx, item in enumerate(results['tracks']):
        tracks.append(item["id"])

    user = sp.current_user()
    playlist_name = f"SpotyMix Bot - {uuid.uuid1()}"
    playlist = sp.user_playlist_create(user["id"], playlist_name)
    sp.playlist_add_items(playlist['id'], tracks)
    return True

if __name__ == "__main__":
    write_data_to_file()