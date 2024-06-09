import requests
import pandas as pd
import random
import time

MOVIE_NUMBER=5000

API_KEY = '74515a054c6205e60808a297767040ba'
BASE_URL = 'https://api.themoviedb.org/3'

def get_random_movie_ids(api_key):
    movie_ids = set()
    while len(movie_ids) < MOVIE_NUMBER:
        page = random.randint(1, 500)
        response = requests.get(f"{BASE_URL}/discover/movie", params={
            'api_key': api_key,
            'sort_by': 'popularity.desc',
            'page': page
        })
        if response.status_code == 200:
            movies = response.json().get('results', [])
            for movie in movies:
                movie_ids.add(movie['id'])
                if len(movie_ids) >= MOVIE_NUMBER:
                    break
        time.sleep(0.1)  # Rate limiting
    return list(movie_ids)

def get_movie_details(movie_id, api_key):
    response = requests.get(f"{BASE_URL}/movie/{movie_id}", params={
        'api_key': api_key,
        'append_to_response': 'keywords,translations,release_dates'
    })
    if response.status_code == 200:
        data = response.json()
        
        # Find the Korean title from translations
        korean_title = None
        translations = data.get('translations', {}).get('translations', [])
        for translation in translations:
            if translation['iso_639_1'] == 'ko':
                korean_title = translation['data']['title']
                break
            
        
          # Find the age rating for Korea
        kr_rating = None
        release_dates = data.get('release_dates', {}).get('results', [])
        for country in release_dates:
            if country['iso_3166_1'] == 'KR':
                for release_date in country['release_dates']:
                    kr_rating = release_date.get('certification')
                    if kr_rating:
                        break
                if kr_rating:
                    break

        return {
            'genres': [genre['name'] for genre in data.get('genres', [])],
            'keywords': [keyword['name'] for keyword in data.get('keywords', {}).get('keywords', [])],
            'original_language': data.get('original_language'),
            'original_title': data.get('original_title'),
            'korean_title': korean_title,
            'kr_rating': kr_rating,
            'popularity': data.get('popularity'),
            'production_countries': [country['name'] for country in data.get('production_countries', [])],
            'release_date': data.get('release_date'),
            'spoken_languages': [lang['name'] for lang in data.get('spoken_languages', [])],
            'vote_average': data.get('vote_average'),
            'vote_count': data.get('vote_count')
        }
    return None

def collect_movie_data(api_key):
    movie_ids = get_random_movie_ids(api_key)
    movies_data = []
    for idx, movie_id in enumerate(movie_ids):
        print(f"Fetching movie {idx + 1}/{MOVIE_NUMBER}")
        movie_details = get_movie_details(movie_id, api_key)
        if movie_details:
            movies_data.append(movie_details)
        time.sleep(0.1)  # Rate limiting
    return movies_data

def main():
    movie_data = collect_movie_data(API_KEY)
    df = pd.DataFrame(movie_data)
    df.to_csv('movies.csv', index=False, encoding='utf-8')
    print(f"Saved {MOVIE_NUMBER} movies to movies.csv")

if __name__ == "__main__":
    main()
