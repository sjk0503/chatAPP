import pandas as pd
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
import json


def drop_trash_data(_movie_df):
    indices_to_drop = [19730, 29502, 35585]
    for index in indices_to_drop:
        if index < len(_movie_df):
            _movie_df.drop(_movie_df.index[index], inplace=True)
        else:
            print(f"Index {index} is out of bounds for axis 0 with size {_movie_df.shape[0]}")
    return _movie_df


def parse_column(column):
    try:
        return [entry['name'] for entry in json.loads(column.replace("'", "\""))]
    except (json.JSONDecodeError, TypeError, KeyError):
        return []


def filter_movies(movies_df, genre, country, rating):
    movies_df['genres_list'] = movies_df['genres'].apply(parse_column)
    movies_df['production_countries_list'] = movies_df['production_countries'].apply(parse_column)

    filtered_movies = movies_df[
        movies_df['genres_list'].apply(lambda x: genre in x) &
        movies_df['production_countries_list'].apply(lambda x: country in x) &
        (movies_df['vote_average'] >= rating)
        ]
    return filtered_movies[['title', 'genres', 'production_countries', 'vote_average', 'vote_count', 'id']]


def recommend_movies(favorite_movie, genre, country, rating, num_recommendations=10):
    movies_df = pd.read_csv('data/tmdb_5000_movies.csv')
    movies_df['id'] = movies_df['id'].astype(str)

    ratings_df = pd.read_csv('data/ratings_small.csv')
    movies_df = drop_trash_data(movies_df)

    filtered_movies = filter_movies(movies_df, genre, country, rating)

    pivot_table = ratings_df.pivot(index='movieId', columns='userId', values='rating').fillna(0)
    csr_data = csr_matrix(pivot_table.values)

    model = NearestNeighbors(metric='cosine', algorithm='brute')
    model.fit(csr_data)

    recommended_movies = []

    favorite_movie_id = movies_df[movies_df['title'].str.contains(favorite_movie, case=False, na=False)]['id']
    if not favorite_movie_id.empty:
        favorite_movie_id = favorite_movie_id.values[0]
        if str(favorite_movie_id) in pivot_table.index:
            movie_index = pivot_table.index.get_loc(str(favorite_movie_id))
            distances, indices = model.kneighbors(csr_data[movie_index], n_neighbors=num_recommendations + 1)

            for i in range(1, len(distances.flatten())):
                recommended_movie_id = pivot_table.index[indices.flatten()[i]]
                if recommended_movie_id not in filtered_movies['id'].values:
                    recommended_movies.append(
                        movies_df[movies_df['id'] == str(recommended_movie_id)]['title'].values[0])

    recommended_movies = list(set(recommended_movies))  # Remove duplicates
    return recommended_movies[:num_recommendations]


def main(favorite_movie, genre, country, rating):
    recommended_movies = recommend_movies(favorite_movie, genre, country, rating)
    result = "Recommended Movies based on your preferences:\n\n"
    for movie in recommended_movies:
        result += f"Title: {movie}\n"
    return result

