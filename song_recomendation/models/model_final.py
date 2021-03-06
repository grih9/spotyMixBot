import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


# songDF = pd.read_csv("../data/allsong_data.csv")
# complete_feature_set = pd.read_csv("../data/complete_feature.csv")
# playlistDF_test = pd.read_csv("../data/test_playlist.csv")

def generate_playlist_feature(complete_feature_set, playlist_df):
    '''
    Summarize a user's playlist into a single vector
    ---
    Input: 
    complete_feature_set (pandas dataframe): Dataframe which includes all of the features for the spotify songs
    playlist_df (pandas dataframe): playlist dataframe
        
    Output: 
    complete_feature_set_playlist_final (pandas series): single vector feature that summarizes the playlist
    complete_feature_set_nonplaylist (pandas dataframe): 
    '''

    # Find song features in the playlist
    complete_feature_set_playlist = complete_feature_set[complete_feature_set['id'].isin(playlist_df['id'].values)]
    # print(complete_feature_set_playlist)
    # Find all non-playlist song features
    complete_feature_set_nonplaylist = complete_feature_set[~complete_feature_set['id'].isin(playlist_df['id'].values)]
    complete_feature_set_playlist_final = complete_feature_set_playlist.drop(columns="id")
    # complete_feature_set_playlist_final = playlist_df.drop(columns="id").drop(columns='name')
    # print(complete_feature_set_playlist_final.sum(axis=0))
    return complete_feature_set_playlist_final.sum(axis=0), complete_feature_set_nonplaylist


def generate_playlist_recos(df, features, nonplaylist_features):
    '''
    Generated recommendation based on songs in aspecific playlist.
    ---
    Input: 
    df (pandas dataframe): spotify dataframe
    features (pandas series): summarized playlist feature (single vector)
    nonplaylist_features (pandas dataframe): feature set of songs that are not in the selected playlist
        
    Output: 
    non_playlist_df_top_40: Top 40 recommendations for that playlist
    '''

    # print(len(df))
    non_playlist_df = df[df['id'].isin(nonplaylist_features['id'].values)]
    # print(len(non_playlist_df))
    # Find cosine similarity between the playlist and the complete song set
    b = cosine_similarity(nonplaylist_features.drop('id', axis=1).values, features.values.reshape(1, -1))[:, 0]
    non_playlist_df['sim'] = pd.Series(b)
    non_playlist_df_top_40 = non_playlist_df.sort_values('sim', ascending=False).head(40)

    return non_playlist_df_top_40


# songDF = pd.read_csv("../data/allsong_data.csv")
# complete_feature_set = pd.read_csv("../data/complete_feature.csv")
# playlistDF_test = pd.read_csv("../data/test_playlist.csv")

# train_features = pd.read_csv("../../train_data.csv")
# def recommend_from_playlist(songDF=songDF, complete_feature_set=complete_feature_set, playlistDF_test=playlistDF_test):
def recommend_from_playlist(songDF, complete_feature_set, playlistDF_test):
    # Find feature
    complete_feature_set_playlist_vector, complete_feature_set_nonplaylist = generate_playlist_feature(
        complete_feature_set, playlistDF_test)

    # Generate recommendation
    top40 = generate_playlist_recos(songDF, complete_feature_set_playlist_vector, complete_feature_set_nonplaylist)

    return top40


if __name__ == '__main__':
    print(recommend_from_playlist()[:10])
