import sqlite3
import requests
import random
import time
import pandas as pd
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

API_KEY = '74515a054c6205e60808a297767040ba'
BASE_URL = 'https://api.themoviedb.org/3'
MOVIE_NUMBER = 50

def initialize_database():
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()

    # c.execute('DROP TABLE IF EXISTS movies')

    c.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY,
            genres TEXT,
            keywords TEXT,
            original_language TEXT,
            original_title TEXT,
            korean_title TEXT,
            kr_rating TEXT,
            popularity REAL,
            production_countries TEXT,
            release_date TEXT,
            spoken_languages TEXT,
            vote_average REAL,
            vote_count INTEGER
        )
    ''')
    conn.commit()
    conn.close()



def get_movie_ids(api_key, count):
    movie_ids = []
    for page in range(251, count + 251):
        print(f"Selected page: {page}")

        response = requests.get(f"{BASE_URL}/discover/movie", params={
            'api_key': api_key,
            'sort_by': 'vote_count.desc,vote_average.desc',
            'page': page
        })
            
        if response.status_code == 200:
            movies = response.json().get('results', [])
            movie_ids.extend([movie['id'] for movie in movies])
        else:
            print(f"Error: Unable to fetch data from page {page} (status code: {response.status_code})")
    
    return movie_ids

def get_movie_details(movie_id, api_key):
    response = requests.get(f"{BASE_URL}/movie/{movie_id}", params={
        'api_key': api_key,
        'append_to_response': 'keywords,translations,release_dates'
    })
    if response.status_code == 200:
        data = response.json()

        korean_title = None
        translations = data.get('translations', {}).get('translations', [])
        for translation in translations:
            if translation['iso_639_1'] == 'ko':
                korean_title = translation['data']['title']
                break

        kr_rating = None
        release_dates = data.get('release_dates', {}).get('results', [])
        for country in release_dates:
            if country['iso_3166_1'] == 'KR':
                for release_date in country['release_dates']:
                    kr_rating = release_date.get('certification')
        
        if kr_rating == "":
            return None

        return {
            'id': movie_id,
            'genres': json.dumps([genre['name'] for genre in data.get('genres', [])]),
            'keywords': json.dumps([keyword['name'] for keyword in data.get('keywords', {}).get('keywords', [])]),
            'original_language': data.get('original_language'),
            'original_title': data.get('original_title'),
            'korean_title': korean_title,
            'kr_rating': kr_rating,
            'popularity': data.get('popularity'),
            'production_countries': json.dumps([country['name'] for country in data.get('production_countries', [])]),
            'release_date': data.get('release_date'),
            'spoken_languages': json.dumps([lang['name'] for lang in data.get('spoken_languages', [])]),
            'vote_average': data.get('vote_average'),
            'vote_count': data.get('vote_count')
        }
    return None

def collect_movie_data(api_key):
    movie_ids = get_movie_ids(api_key, MOVIE_NUMBER)

    movies_data = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(get_movie_details, movie_id, api_key) for movie_id in movie_ids]
        for future in as_completed(futures):
            details = future.result()
            if details:
                movies_data.append(details)
    return movies_data

def save_movies_to_db(movies):
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    for movie in movies:
        movie_id = movie['id'] if movie['id'] is not None else 0
        genres = movie['genres'] if movie['genres'] else '[]'
        keywords = movie['keywords'] if movie['keywords'] else '[]'
        original_language = movie['original_language'] if movie['original_language'] else ''
        original_title = movie['original_title'] if movie['original_title'] else ''
        korean_title = movie['korean_title'] if movie['korean_title'] else ''
        kr_rating = movie['kr_rating'] if movie['kr_rating'] else ''
        popularity = float(movie['popularity']) if movie['popularity'] is not None else 0.0
        production_countries = movie['production_countries'] if movie['production_countries'] else '[]'
        release_date = movie['release_date'] if movie['release_date'] else ''
        spoken_languages = movie['spoken_languages'] if movie['spoken_languages'] else '[]'
        vote_average = float(movie['vote_average']) if movie['vote_average'] is not None else 0.0
        vote_count = int(movie['vote_count']) if movie['vote_count'] is not None else 0
        
        
        c.execute('''
            INSERT OR IGNORE INTO movies (
                id, genres, keywords, original_language, original_title,
                korean_title, kr_rating, popularity, production_countries,
                release_date, spoken_languages, vote_average, vote_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            movie_id, genres, keywords, original_language, original_title,
            korean_title, kr_rating, popularity, production_countries,
            release_date, spoken_languages, vote_average, vote_count
        ))
    conn.commit()
    conn.close()

def print_movies_table():
    conn = sqlite3.connect('movies.db')
    query = 'SELECT * FROM movies'
    df = pd.read_sql_query(query, conn)
    conn.close()
    print(df)




def main():
    initialize_database()
    # update_table_structure()
    movies_data = collect_movie_data(API_KEY)
    save_movies_to_db(movies_data)
    print_movies_table()

if __name__ == "__main__":
    main()
