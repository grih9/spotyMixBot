import uuid


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
