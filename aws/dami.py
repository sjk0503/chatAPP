# 현재 배포중인 api 코드
# 다양한 api(검색 api, tmdb api, gpt api 등)와 다양한 함수를 조합하여 구현


import json
import os
from openai import OpenAI
import requests
from datetime import datetime, timedelta
import time
import sys
import logging
import math


# s3연결

import sqlite3
import ast

import boto3
import botocore

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

ASSISTANT_ID = ""
THREAD_ID = ""

Google_SEARCH_ENGINE_ID = ""
Google_API_KEY = ""
TMDB_API_KEY = ''
KOFIC_API_KEY = ""

country_to_iso = {
    "아랍": "ar",
    "중국": "cn",
    "체코": "cs",
    "덴마크": "da",
    "독일": "de",
    "그리스": "el",
    "미국": "en",
    "스페인": "es",
    "바스크": "eu",
    "이란": "fa",
    "핀란드": "fi",
    "프랑스": "fr",
    "아일랜드": "ga",
    "이스라엘": "he",
    "인도": "hi",
    "인도네시아": "id",
    "이탈리아": "it",
    "일본": "ja",
    "인도네시아 (자바)": "jv",
    "인도 (카르나타카)": "kn",
    "한국": "ko",
    "바티칸": "la",
    "북마케도니아": "mk",
    "인도 (케랄라)": "ml",
    "말레이시아": "ms",
    "네덜란드": "nl",
    "노르웨이": "no",
    "폴란드": "pl",
    "포르투갈": "pt",
    "러시아": "ru",
    "슬로베니아": "sl",
    "세르비아": "sr",
    "스웨덴": "sv",
    "인도 (타밀나두)": "ta",
    "인도 (안드라프라데시와 텔랑가나)": "te",
    "태국": "th",
    "필리핀": "tl",
    "터키": "tr",
    "우크라이나": "uk",
    "파키스탄": "ur",
    "베트남": "vi",
    "나이지리아 (요루바)": "yo",
    "중국": "zh"
}

# 함수 실행 목록. 모든 함수들은 return 값을 가진다.
# =====================================================================================================================
# S3 버킷 이름과 파일 경로를 설정합니다.
BUCKET_NAME = 'finefriends'
FILE_KEY = 'user_info.json'
FILE_KEY_movies = 'movies.db'
FILE_KEY_filterd_movies = 'filtered_movies.db'

s3 = boto3.client('s3')


# 사용자 취향 user_info.json을 업데이트하는 함수
def update_user_information(key_name, value):
    logger.info("S3에서 파일을 읽고 있습니다.")

    # 여러 값을 가질 수 있는 키들
    multiple_values_keys = ["like_movie", "dislike_movie", "dislike_country"]

    # S3에서 기존 정보를 읽어옵니다.
    logger.info("1")
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_KEY)
        user_data = json.loads(response['Body'].read().decode('utf-8'))
    except s3.exceptions.NoSuchKey:
        user_data = {}
    logger.info("1 done")

    logger.info("2")
    # 여러 값을 가질 수 있는 키인지 확인합니다.
    if key_name in multiple_values_keys:

        if isinstance(user_data[key_name], str):
            user_data[key_name] = user_data[key_name].split(',')

        if value in user_data[key_name]:
            return "알고 있어"
        else:

            values = value.split(',')
            for val in values:
                if val not in user_data[key_name]:
                    user_data[key_name].append(val)

            if key_name == "dislike_country":
                value = country_to_iso.get(value, value)

            if key_name in ["like_movie", "dislike_movie"]:
                genres, keywords = get_movie_genres_and_keywords(value)

                genre_key = 'like_genres' if key_name == "like_movie" else 'dislike_genres'
                keyword_key = 'like_keywords' if key_name == "like_movie" else 'dislike_keywords'

                for genre in genres:
                    user_data[genre_key][genre] = user_data[genre_key].get(genre, 0) + (
                        1 if key_name == "like_movie" else -1)

                user_data[keyword_key] = list(set(user_data[keyword_key] + keywords))

            save_user_data(user_data)
            return "그렇구나"

    elif key_name in ["like_genres", "dislike_genres"]:

        genres = value.split(',')

        for genre in genres:
            # 장르 이름 매핑을 통해 영어 장르 이름으로 변환
            user_data[key_name][genre] = user_data[key_name].get(genre, 0) + (1 if key_name == "like_genres" else -1)

        save_user_data(user_data)
        return "그렇구나"
    else:
        user_data[key_name] = value
        save_user_data(user_data)
        return "그렇구나"


def get_movie_genres_and_keywords(movie_name):
    search_url = f"https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": movie_name,
        "language": "ko"
    }
    response = requests.get(search_url, params=params)

    genres, keywords = [], []
    if response.status_code == 200:
        results = response.json().get('results', [])
        if results:
            movie_id = results[0]['id']
            details_url = f"https://api.themoviedb.org/3/movie/{movie_id}"
            details_params = {
                "api_key": TMDB_API_KEY,
                "append_to_response": "keywords"
            }
            response = requests.get(details_url, params=details_params)

            if response.status_code == 200:
                data = response.json()
                genres = [genre['name'] for genre in data['genres']]
                keywords = [keyword['name'] for keyword in data['keywords']['keywords']]

    return genres, keywords


def save_user_data(user_data):
    s3.put_object(Bucket=BUCKET_NAME, Key=FILE_KEY,
                  Body=json.dumps(user_data, ensure_ascii=False, indent=4).encode('utf-8'))


# =====================================================================================================================
# 영화 추천 알고리즘
# get_recommendation은 1차로 영화를 필터링하고
# recommend_movies는 가중치 계산과 코사인 유사도 계산을 통해 상위 20개의 영화를 return
def get_recommendation():
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_KEY)
        user_info = json.loads(response['Body'].read().decode('utf-8'))
    except s3.exceptions.NoSuchKey:
        user_info = {}
    logger.info("1 done")

    if not user_info:
        return {
            'statusCode': 404,
            'body': json.dumps('User info not found')
        }

    try:
        like_movie = user_info['like_movie']
        dislike_movie = user_info['dislike_movie']
        like_genre_value = user_info['like_genres']
        dislike_genre_value = user_info['dislike_genres']
        like_genre = list(like_genre_value.keys())
        dislike_genre = list(dislike_genre_value.keys())
        like_keywords = user_info['like_keywords']
        dislike_keywords = user_info['dislike_keywords']
    except KeyError as e:
        logger.error(f"Key error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Key error: {str(e)}")
        }

    user_age = user_info['age']
    old_movies = user_info.get('old_movies', True)
    dislike_country = user_info['dislike_country']
    
    # 새로운 데이터베이스에 연결 및 테이블 생성
    s3.download_file(BUCKET_NAME, FILE_KEY_filterd_movies, '/tmp/filterd_movies.db')
    conn_filtered = sqlite3.connect('/tmp/filterd_movies.db')
    c_filtered = conn_filtered.cursor()


    weighted_movies = recommend_movies(conn_filtered, like_genre_value, dislike_genre_value, like_genre, dislike_genre)
    top_list = calculate_similarity(weighted_movies, like_keywords, dislike_keywords)

    excluded_movies = set(like_movie + dislike_movie)

    result = [mv for mv in top_list if mv not in excluded_movies]

    conn_filtered.close()
    return result


def recommend_movies(conn, like_genre_value, dislike_genre_value, like_genre, dislike_genre):
    # 1선

    def filter_movies_by_genre(movies):
        # 다 계산하면 시간 오래걸리니까 장르 유사도 0개인걸 거름
        # 2선
        target = ast.literal_eval(movies[1])
        if any(genre in like_genre for genre in target):
            return movies
        else:
            return None

    def calculate_score(movie):
        # 계산용
        # 3선

        score = 0

        genres = ast.literal_eval(movie[1])
        for genre in genres:
            if genre in like_genre:
                score += like_genre_value[genre]
            if genre in dislike_genre:
                score += dislike_genre_value[genre]
        return score

    c = conn.cursor()
    c.execute('''
        SELECT * FROM filtered_movies
    ''')
    rows = c.fetchall()

    except_movies = []

    for movie in rows:
        filtered = filter_movies_by_genre(movie)
        if filtered is not None:
            except_movies.append(filtered)

    scored_movies = []
    for movie in except_movies:
        score = calculate_score(movie)
        if score > 0:  # Score가 0 이하인 영화는 제외
            scored_movies.append((movie, score))

    # 점수를 기준으로 영화 정렬
    scored_movies.sort(key=lambda x: x[1], reverse=True)

    return [title for title, score in scored_movies]


def calculate_similarity(movies, like_keywords, dislike_keywords):
    def parse_keywords(data):
        return " ".join(ast.literal_eval(data))

    def compute_tf(document):
        words = document.split()
        word_count = {}
        for word in words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
        total_words = len(words)
        tf = {word: count / float(total_words) for word, count in word_count.items()}
        return tf

    def compute_idf(documents):
        idf = {}
        total_docs = len(documents)
        for document in documents:
            words = set(document.split())
            for word in words:
                if word in idf:
                    idf[word] += 1
                else:
                    idf[word] = 1
        for word in idf:
            idf[word] = math.log(total_docs / float(idf[word]) + 1)
        return idf

    def compute_tfidf(tf, idf):
        tfidf = {}
        for word, value in tf.items():
            tfidf[word] = value * idf.get(word, 0.0)
        return tfidf

    def cosine_similarity(vec1, vec2):
        dot_product = sum(vec1.get(word, 0.0) * vec2.get(word, 0.0) for word in vec1)
        magnitude1 = math.sqrt(sum(val ** 2 for val in vec1.values()))
        magnitude2 = math.sqrt(sum(val ** 2 for val in vec2.values()))
        if not magnitude1 or not magnitude2:
            return 0.0
        return dot_product / (magnitude1 * magnitude2)

    # Prepare the documents
    movie_keywords = [parse_keywords(movie[2]) for movie in movies]
    preferred_keywords_str = " ".join(like_keywords)
    dislike_keywords_str = " ".join(dislike_keywords)

    all_documents = movie_keywords + [preferred_keywords_str, dislike_keywords_str]

    # Compute TF-IDF for each document
    idf = compute_idf(all_documents)
    tfidf_matrix = [compute_tfidf(compute_tf(doc), idf) for doc in all_documents]

    # Separate TF-IDF vectors for the preferred and dislike keywords
    preferred_vector = tfidf_matrix[-2]
    dislike_vector = tfidf_matrix[-1]

    # Calculate similarity scores
    similarity_scores = [
        cosine_similarity(tfidf_matrix[i], preferred_vector) - cosine_similarity(tfidf_matrix[i], dislike_vector)
        for i in range(len(movie_keywords))
    ]

    # Sort movies based on similarity scores
    sorted_movies = [movie for _, movie in sorted(zip(similarity_scores, movies), key=lambda x: x[0], reverse=True)]

    return sorted_movies


#========================================================================
#사용자 정보 가져오기
def get_user_info():
    
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_KEY)
        user_info = json.loads(response['Body'].read().decode('utf-8'))
    except s3.exceptions.NoSuchKey:
        user_info = {}
    logger.info("1 done")

    if not user_info:
        return {
            'statusCode': 404,
            'body': json.dumps('User info not found')
        }
        
    return user_info





# =====================================================================================================================
# 영화 정보 가져오기


def get_movie_info(movie_title):
    current_date, current_time = get_time()
    search_url = f"https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": movie_title,
        "language": "ko"  # 한국어 결과를 원할 경우 언어를 설정
    }
    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        results = response.json().get('results', [])
        if results:
            # 첫 번째 결과의 movie ID를 반환
            movie_id = results[0]['id']
            url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&append_to_response=credits"
            params = {
                "query": movie_title,
                "language": "ko"  # 한국어 결과를 원할 경우 언어를 설정
            }
            response = requests.get(url, params=params)

            info = []
            data = response.json()

            extracted_info = {
                'adult': data['adult'],
                'genres': [genre['name'] for genre in data['genres']],
                'Production_companies': [componies['name'] for componies in data['production_companies']],
                'production_countries': [countries['name'] for countries in data['production_countries']],
                'realse_date': data['release_date'],
                'runtime': data['runtime']
            }
            cast_info = [{"id": cast_member["id"], "name": cast_member["name"]} for cast_member in
                         data["credits"]["cast"]]
            info.append(extracted_info)

            return current_date, current_time, info, cast_info
        else:
            # 영화를 찾지 못하면 google search
            do_WebSearch(movie_title)
    else:
        do_WebSearch(movie_title)


# =====================================================================================================================
# 웹 검색
def do_WebSearch(query):
    current_date, current_time = get_time()
    api_key = Google_API_KEY  # 여기에 실제 API 키를 넣으세요
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": Google_SEARCH_ENGINE_ID,
        "q": query,
        "lowRange": 0,
        "highRange": 20
    }
    response = requests.get(search_url, params=params)
    results = response.json()

    return current_date, current_time, results


# =====================================================================================================================
# 상영작을 가져오기
def get_screen_movies():
    # KOFIC API endpoint
    url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json"

    today = datetime.today().strftime('%Y%m%d')
    daily_today = str(int(today) - 1)

    # Parameters for the API request
    params = {
        'key': KOFIC_API_KEY,
        'targetDt': daily_today
    }

    # Send GET request
    response = requests.get(url, params=params)

    # Check if request was successful
    if response.status_code == 200:

        data = response.json()
        daily_box_office_list = data['boxOfficeResult']['dailyBoxOfficeList']

        daily_movies = []
        for movie in daily_box_office_list:
            daily_movie = {
                "Rank": movie['rank'],
                "Movie Name": movie['movieNm'],
                "Release Date": movie['openDt'],
                "Total Audience": movie['audiAcc']
            }
            daily_movies.append(daily_movie)
        return daily_movies
    else:
        return None


# =====================================================================================================================
# 상영 예정작을 가져오기
def get_forthcomming_movies():
    # KOFIC API endpoint
    url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json"

    # Parameters for the API request
    params = {
        'key': KOFIC_API_KEY,
        'itemPerPage': 100,  # Maximum number of items per page
        'openStartDt': 2024,  # 시작년도. 일단 하드코딩함
        'openEndDt': 2025  # 종료년도. 일단 하드코딩함
    }

    # Send GET request
    response = requests.get(url, params=params)

    # Check if request was successful
    if response.status_code == 200:
        data = response.json()
        # Filter out movies where openDt is less than today
        today = datetime.today().strftime('%Y%m%d')
        filtered_movie_list = [movie for movie in data['movieListResult']['movieList'] if movie['openDt'] >= today]

        upcomming_movie = []
        for movie in filtered_movie_list:
            daily_movie = {
                "Name": movie['movieNm'],
                "Release Date": movie['openDt'],
                "Genre": movie['repGenreNm']
            }
            upcomming_movie.append(daily_movie)
        return upcomming_movie
    else:
        return None


# =====================================================================================================================
# 날씨 정보


# =====================================================================================================================
# 시간 정보
def get_time():
    now_utc = datetime.now()

    # KST 시간대는 UTC+9이므로 9시간을 더해줍니다.
    kst_offset = timedelta(hours=9)
    now_korea = now_utc + kst_offset

    # 날짜와 시간 포맷팅
    current_date = now_korea.strftime("%Y-%m-%d")
    current_time = now_korea.strftime("%H:%M:%S")

    return current_date, current_time


schema_func_name_dict = {
    "update_user_information": "update user's movie taste information.",
    "get_screen_movies": "Bring_the_movie_currently_playing",
    "get_forthcomming_movies": "Bring_the_movie_that_is_scheduled_to_be_shown",
    "get_temperature": "get_current_temperature",
    "get_movie_info": "get_details_about_specific_movie",
    "do_WebSearch": "do_websearch_about_characters_movie_etc"
}

session_times = {}


# 다미에게 대화할때마다 시간정보도 함께 알려주기 위해서
def get_time_for_session(assistant_id):
    if assistant_id not in session_times:
        session_times[assistant_id] = get_time()
    return session_times[assistant_id]


def submit_message(assistant_id, thread, user_message):
    logger.info("get time")
    now = get_time_for_session(assistant_id)
    # 사용자 입력 메시지를 스레드에 추가합니다.
    client.beta.threads.messages.create(
        thread_id=thread,
        role="user",
        content=user_message + str(now),
    )

    # 스레드에 메시지가 입력이 완료되었다면,
    # Assistant ID와 Thread ID를 사용하여 실행을 준비합니다.
    run = client.beta.threads.runs.create(
        thread_id=thread,
        assistant_id=assistant_id,
    )

    return run


def get_response(thread):
    # 스레드에서 메시지 목록을 가져옵니다.
    # 메시지를 오름차순으로 정렬할 수 있습니다. order="asc"로 지정합니다.
    return client.beta.threads.messages.list(thread_id=thread)


def wait_on_run(run, thread):
    while True:
        run_check = client.beta.threads.runs.retrieve(
            thread_id=thread,
            run_id=run.id
        )
        if run_check.status in ['queued', 'in_progress']:
            time.sleep(2)
        else:
            break
    return run_check
    
# filtering
def filter_response(response):
    # Only allows letters, punctuation, and spaces
    filtered_response = re.sub(r"[^a-zA-Z가-힣\s.,!?()\-0123456789]", "", response)
    return filtered_response
    

# main
def lambda_handler(event, context):
    # user_input 가져오기
    try:
        body = json.loads(event['body'])
        user_input = body['user_input']
    except (KeyError, TypeError, json.JSONDecodeError) as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid input format'})
        }

    try:
        run = submit_message(ASSISTANT_ID, THREAD_ID, user_input)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': '메세지 전달 실패'
        }

    try:
        run_check = wait_on_run(run, THREAD_ID)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': '잘못된 메세지 형식'
        }
    logger.info("함수 분석 시작")

    tool_outputs = []
    try:
        if run_check.status == "requires_action":
            tool_calls = run_check.required_action.submit_tool_outputs.tool_calls
            logger.info("실행할 함수 가져오기 성공")

            for tool in tool_calls:
                func_name = tool.function.name
                logger.info(f"함수 접근 시도: {func_name}")
                kwargs = json.loads(tool.function.arguments)

                # 함수를 직접 호출
                if func_name in globals() and callable(globals()[func_name]):
                    try:
                        output = globals()[func_name](**kwargs)
                    except Exception as e:
                        logger.info(e)
                        output = "Function Error"
                else:
                    raise Exception(f"Function {func_name} not found")

                tool_outputs.append(
                    {
                        "tool_call_id": tool.id,
                        "output": str(output)
                    }
                )

            run = client.beta.threads.runs.submit_tool_outputs(
                thread_id=THREAD_ID,
                run_id=run.id,
                tool_outputs=tool_outputs
            )
            run_check = wait_on_run(run, THREAD_ID)
            if run_check.status == "completed":
                answer = get_response(THREAD_ID).data[0].content[0].text.value
                filtered_answer=filter_response(answer)
                
            else:
                answer = get_response(THREAD_ID).data[0].content[0].text.value
                filtered_answer=filter_response(answer)
        else:
            answer = get_response(THREAD_ID).data[0].content[0].text.value
            filtered_answer=filter_response(answer)
           
    except Exception as e:
        return {
            'statusCode': 500,
            'body': "함수 분석 오류"
        }

    return {
        'statusCode': 200,
        'body': filtered_answer
    }
