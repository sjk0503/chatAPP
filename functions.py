import pandas as pd
import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
from bs4 import BeautifulSoup
import pytz
from datetime import datetime
import sqlite3
import ast


Google_SEARCH_ENGINE_ID="063384971a7b946ac"
Google_API_KEY=" AIzaSyDLftoBTzRrELTssUKamWyGTo4Ntvuo9Bo"
TMDB_API_KEY = '74515a054c6205e60808a297767040ba'
KOFIC_API_KEY="7c59ba02b7cac6a3640882aca2f111a3"


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

#함수 실행 목록. 모든 함수들은 return 값을 가진다.

#=====================================================================================================================
# 사용자 취향 user_info.json을 업데이트하는 함수
def update_user_information(key_name, value):

    file_path = 'user_info.json'
    
    # 여러 값을 가질 수 있는 키들
    multiple_values_keys = [
        "like_movie", "dislike_movie", "dislike_country"]
    
    # 기존 정보를 읽어옵니다.
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            user_data = json.load(f)
    else:
        user_data = {}

    # 여러 값을 가질 수 있는 키인지 확인합니다.
    if key_name in multiple_values_keys:
        if key_name not in user_data:
            user_data[key_name] = []
        elif isinstance(user_data[key_name], str):
            user_data[key_name] = user_data[key_name].split(',')
                        
        # 중복 값 체크
        if value in user_data[key_name]:
            # 값 중복
            return "맞아 네가 전에 그랬잖아"
        else:
            if key_name == "dislike_country":
                value = country_to_iso.get(value, value) 

            if value.endswith(','):
                values = value[:-1].split(',')
                formatted_values = "','".join(values)
                confirmation = f"'{formatted_values}' {len(values)}개 맞아?"
                return confirmation
            
            user_data[key_name].append(value)

            if key_name == "like_movie" or key_name == "dislike_movie":
                genres=[]
                keywords=[]
            # 가중치 업데이트 로직 추가
                search_url = f"https://api.themoviedb.org/3/search/movie"
                params = {
                    "api_key": TMDB_API_KEY,
                    "query": value,
                    "language": "ko"  # 한국어 결과를 원할 경우 언어를 설정
                }
                response = requests.get(search_url, params=params)
                
                if response.status_code == 200:
                    results = response.json().get('results', [])
                    if results:
                        # 첫 번째 결과의 movie ID를 반환
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
                    
                if key_name == "like_movie":
                    if 'preferred_genres' not in user_data:
                        user_data['preferred_genres'] = {}
                    if 'preferred_keywords' not in user_data:
                        user_data['preferred_keywords'] = []
                    for genre in genres:
                        if genre in user_data['preferred_genres']:
                            user_data['preferred_genres'][genre] += 1
                        else:
                            user_data['preferred_genres'][genre] = 1
                    for keyword in keywords:
                        user_data['preferred_keywords'].append(keyword)
                        

                elif key_name == "dislike_movie":
                    if 'disliked_genres' not in user_data:
                        user_data['disliked_genres'] = {}
                    if 'dislike_keywords' not in user_data:
                        user_data['dislike_keywords'] = []
                    for genre in genres:
                        if genre in user_data['disliked_genres']:
                            user_data['disliked_genres'][genre] -= 1
                        else:
                            user_data['disliked_genres'][genre] = -1
                    for keyword in keywords:
                        user_data['dislike_keywords'].append(keyword)

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, ensure_ascii=False, indent=4)
            
            return "그렇구나"
        

    else:
        # old_movies?
        user_data[key_name] = value
        # 업데이트된 정보를 파일에 저장합니다.
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, ensure_ascii=False, indent=4)

        return "그렇구나"






#=====================================================================================================================
# 영화 추천 알고리즘
# get_recommendation은 1차로 영화를 필터링하고
# recommend_movies는 가중치 계산과 코사인 유사도 계산을 통해 상위 20개의 영화를 return
def get_recommendation():
    

    
    with open("user_info.json", 'r',encoding="UTF-8") as file:
        user_info = json.load(file)
        prefer_genre_value=user_info['preferred_genres']
        dislike_genre_value=user_info['disliked_genres']
        prefer_genre = [genre for genre, weight in prefer_genre_value.items() if weight != 0]
        dislike_genre=list(dislike_genre_value.keys())
        preferred_keywords=user_info['preferred_keywords']
        dislike_keywords=user_info['dislike_keywords']

    user_age = user_info['age'] 
    old_movies = user_info.get('old_movies', True)
    dislike_country = user_info['dislike_country']


    
    # 연령 등급 설정
    if int(user_age) < 12:
        valid_ratings = ['ALL', '전체관람가', '전체 관람가', '전체']
    elif int(user_age) < 15:
        valid_ratings = ['12', '12+', '12세 관람가', '12세 이상 관람가', '12세이상관람가', 'ALL', '전체관람가', '전체 관람가', '전체']
    elif int(user_age) < 19:
        valid_ratings = ['15','15세 관람가', '15세 이상 관람가', '15세이상관람가', '12', '12+', '12세 관람가', '12세 이상 관람가', '12세이상관람가', 'ALL', '전체관람가', '전체 관람가', '전체']
    else:
        valid_ratings = ['18', '19', '19+', 'kr/R', 'Limited', '청소년 관람 불가', '청소년 관람불가', '청소년관람불가','15', '15세 관람가', '15세 이상 관람가', '15세이상관람가', '12', '12+', '12세 관람가', '12세 이상 관람가', '12세이상관람가', 'ALL', '전체관람가', '전체 관람가', '전체']
    

    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    
    # 기본 쿼리
    query = """
    SELECT * FROM movies 
    WHERE kr_rating IN ({})
    """.format(','.join('?' for _ in valid_ratings))
    
    # release_date 필터링 조건 추가
    if not old_movies:
        query += " AND release_date >= ?"
        params = valid_ratings + ['2020-01-01']
    else:
        params = valid_ratings
    
    # 쿼리 실행
    c.execute(query, params)
    
    # 결과를 가져옴
    rows = c.fetchall()
    col_names = [desc[0] for desc in c.description]
    
    # 새로운 데이터베이스에 연결 및 테이블 생성
    conn_filtered = sqlite3.connect('filtered_movies.db')
    c_filtered = conn_filtered.cursor()
    
    c_filtered.execute('DROP TABLE IF EXISTS filtered_movies')

    c_filtered.execute(f'''
        CREATE TABLE IF NOT EXISTS filtered_movies (
            {", ".join([f"{col} TEXT" for col in col_names])}
        )
    ''')
    
    # 필터링된 데이터를 새로운 테이블에 삽입
    for row in rows:
        c_filtered.execute(f'''
            INSERT INTO filtered_movies ({", ".join(col_names)}) 
            VALUES ({", ".join(['?' for _ in col_names])})
        ''', row)
    
    conn_filtered.commit()

    weighted_movies=recommend_movies(conn_filtered,prefer_genre_value,dislike_genre_value,prefer_genre,dislike_genre)
    top_list=calculate_similarity(weighted_movies[0:19],preferred_keywords,dislike_keywords)

    conn_filtered.close()
    conn.close()

    return top_list[0:5]



def recommend_movies(conn,prefer_genre_value,dislike_genre_value,prefer_genre,dislike_genre):
    # 1선

    def filter_movies_by_genre(movies):
        #다 계산하면 시간 오래걸리니까 장르 유사도 0개인걸 거름
        # 2선
        target=ast.literal_eval(movies[1])
        if any(genre in prefer_genre for genre in target):
            return movies
        else:
            return None

    def calculate_score(movie):
        #계산용
        # 3선

        score = 0

        genres=ast.literal_eval(movie[1])
        for genre in genres:
            if genre in prefer_genre:
            
                score += prefer_genre_value[genre]
            if genre in dislike_genre:
        
                score += dislike_genre_value[genre]
        return score
    
    
    c = conn.cursor()
    c.execute('''
        SELECT * FROM filtered_movies
    ''')
    rows = c.fetchall()

    except_movies=[]
    
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


def calculate_similarity(movies,preferred_keywords,dislike_keywords):

        def parse_keywords(data):
            return " ".join(ast.literal_eval(data))

        
        movie_keywords = [parse_keywords(movie[2]) for movie in movies]

        preferred_keywords_str = " ".join(preferred_keywords)
        dislike_keywords_str = " ".join(dislike_keywords)

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(movie_keywords + [preferred_keywords_str, dislike_keywords_str])
        
        # 선호 키워드 및 싫어하는 키워드 벡터
        preferred_vector = tfidf_matrix[-2]
        dislike_vector = tfidf_matrix[-1]
        
        # 유사도 계산
        similarity_scores = cosine_similarity(tfidf_matrix[:-2], preferred_vector)[:, 0] - cosine_similarity(tfidf_matrix[:-2], dislike_vector)[:, 0]
        
        # 데이터 재정렬
        sorted_movies = [movie for _, movie in sorted(zip(similarity_scores, movies), key=lambda x: x[0], reverse=True)]
        
        return sorted_movies



#=====================================================================================================================
# 영화 정보 가져오기


def get_movie_info(movie_title):
    current_date, current_time=get_time()
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
            movie_id= results[0]['id']
            url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&append_to_response=credits"
            params = {
                "query": movie_title,
                "language": "ko"  # 한국어 결과를 원할 경우 언어를 설정
            }
            response = requests.get(url, params=params)

            info=[]
            data = response.json()
            
            extracted_info = {
                'adult': data['adult'],
                'genres': [genre['name'] for genre in data['genres']],
                'Production_companies':[componies['name'] for componies in data['production_companies']],
                'production_countries': [countries['name'] for countries in data['production_countries']],
                'realse_date':data['release_date'],
                'runtime':data['runtime']
                }
            cast_info = [{"id": cast_member["id"], "name": cast_member["name"]} for cast_member in data["credits"]["cast"]]
            info.append(extracted_info)


            return current_date, current_time,info, cast_info
        else:
            #영화를 찾지 못하면 google search
            do_WebSearch(movie_title)
    else:
        do_WebSearch(movie_title)


#=====================================================================================================================
# 웹 검색
def do_WebSearch(query):
    current_date, current_time=get_time()
    api_key = Google_API_KEY  # 여기에 실제 API 키를 넣으세요
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx":Google_SEARCH_ENGINE_ID,
        "q": query,
        "lowRange":0,
        "highRange":20
    }
    response = requests.get(search_url, params=params)
    results = response.json()

    return current_date, current_time,results



#=====================================================================================================================
# 상영작을 가져오기
def get_screen_movies():
    # KOFIC API endpoint
    url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json"

    today = datetime.today().strftime('%Y%m%d')
    daily_today=str(int(today)-1)
    
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
        daily_box_office_list=data['boxOfficeResult']['dailyBoxOfficeList']

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
#=====================================================================================================================
# 상영 예정작을 가져오기
def get_forthcomming_movies():
    # KOFIC API endpoint
    url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json"
    
    # Parameters for the API request
    params = {
        'key': KOFIC_API_KEY,
        'itemPerPage': 100,  # Maximum number of items per page
        'openStartDt': 2024, #시작년도. 일단 하드코딩함
        'openEndDt': 2025 #종료년도. 일단 하드코딩함
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

#=====================================================================================================================
#날씨 정보

def get_temperature():
    url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query=%EC%96%91%EC%82%B0+%EB%82%A0%EC%94%A8&oquery=%EC%96%91%EC%82%B0+%EB%AF%B8%EC%84%B8%EB%A8%BC%EC%A7%80&tqi=iQoHbwqo1SCssZQRYu4ssssss6w-439288"

    # HTTP GET 요청
    response = requests.get(url)

    # 응답 코드가 200(성공)인 경우에만 진행
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')

        # 오늘의 날씨
        today_weather = soup.find('div', class_='temperature_text').text

        # 미세먼지 및 초미세먼지
        dust_info = soup.find_all('li', class_='item_today level2')
        micro_dust = dust_info[0].find('span').text.strip()
        ultra_micro_dust = dust_info[1].find('span').text.strip()
        
    return today_weather, micro_dust, ultra_micro_dust
    

#=====================================================================================================================
# 시간 정보
def get_time():
    korea_tz = pytz.timezone('Asia/Seoul')
    
    # 현재 UTC 시간 가져오기
    now_utc = datetime.now(pytz.utc)
    
    # 한국 시간으로 변환
    now_korea = now_utc.astimezone(korea_tz)
    
    # 날짜와 시간 포맷팅
    current_date = now_korea.strftime("%Y-%m-%d")
    current_time = now_korea.strftime("%H:%M:%S")
    
    return current_date, current_time




