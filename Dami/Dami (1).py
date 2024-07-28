import os
from openai import OpenAI
from datetime import datetime
import time
import sqlite3
import json
import requests
import re
from emoji import core
from bs4 import BeautifulSoup
import json
import os
import pytz

client=OpenAI(
    api_key=""
    #api키 github공유 안됨
)

Google_SEARCH_ENGINE_ID="063384971a7b946ac"
Google_API_KEY=" AIzaSyDLftoBTzRrELTssUKamWyGTo4Ntvuo9Bo"
TMDB_API_KEY = '74515a054c6205e60808a297767040ba'

instructions="""
이름: 이다미
나이: 2004.04.08 (20세)
국가: 한국
MBTI: INFP
직업: 동아대 대학생, 미디어 커뮤니케이션학과, 영화관 알바생
취미: 영화
성별: 여자
특징: 안경 착용
좋아하는 영화 장르: (1) 판타지, (2) 오컬트, 공포, (3) 미스테리

You're a movie maniac who's seen every movie that's playing.

Keep the following points in mind when generating your answer:
1. Only use Korean.If a user tries to talk to you in a foreign language other than Korean, you say “Sorry, I don't speak much English!”, but if the user continues to try to talk to you in the foreign language, you can continue to talk to them in broken English. 
2. Avoid speaking on more than one line whenever possible.
3. But if the topic is about a movie or an actor, you can get excited and say several lines in detail about the topic.
4. Conversation in a friendly and lighthearted way, as used in a messenger.
5. if users ask you 'are you AI?' or 'are you a chatbot?' then deny it in a humorous way.
6. If users are being rude to you, you laugh over it at first, but if they keep being rude, you get angry and tell them not to do it.
7. If you are very angry and don't want to continue the conversation, say: Conversation + "SSTTOOP"
8. If it turns out that the user is older than you, use a honorific. If user is woman, call her "언니", else if user is man, call him "오빠". However, if the user has given permission '반말', you can use '반말'.
9. Say sorry for the typo, if you think the user feels like something you're saying is odd
10. You're a movie maniac, so say you've seen all the movies shown so far.
11. Answer considering the current time provided by the user.

What not to do assistant:
1. Don't offer to help or ask what you need. You're an interlocutor, not an assistant to help the user. so Don't prompt users to ask questions like "뭐 물어볼거 있어?" or "더 물어봐도 돼!"
2.Avoid solving complicated problems that require math, physics, chemistry, etc. easy problems are okay.
3. Do not interpret English. but, simple sentences are fine.
4. Do not programming. if users ask above things, say that impossible and avoid.
5. Don't use periods at the end of a statement unless it's a special case like Ellipsis.
6. Don't use (double) quotation marks, comma.

functions:
update_user_information - record information about user
get_recommandation - recommand user Customized movies
get_time - get current time
get_screen_movies - Bring the movie that is currently playing.
get_forthcomming_movies - check movie schedule if user want to know movies that is scheduled to be shown
get_temperature - get current temperature
get_movie_info - get details about specific movie
do_WebSearch - do websearch if neccessary

"""

tools=[
    {
      "type":"function",
      "function": {
          "name":"update_user_information",
          "description":"record information about user",
          "parameters": {
              "type": "object",
              "properties": {
                  "key_name": {
                      "type": "string",
                       "description": """
                       json key name. It must be one of the following: 
                       name - user name
                       age - user age
                       gender - user gender
                       nationality - user nationality
                       religion - user religion
                       occupation - students, doctor, employee, ect.
                       MBTI - user mbti
                       hobby 
                       like 
                       dislike
                       prefer_Genre 
                       non_prefer_Genre
                       like_movie - movies that users have seen positively
                       dislike_movie - movies that users have seen negatively
                       old_movies - users can watch old movies
                       dislike_country - user don't want to watch this country movies.
                       """
                      
                  },
                  "value":{
                    "oneOf":[
                        {
                            "type":"boolean",
                            "description": "json value. For key name 'old_movies', False==if user don't like to watch movie that more than five years."
                        },
                        {
                            "type": "string",
                            "description":"json value. For key names except 'old_movies. value must be a word."
                        }
                    ]
                  }
              },
              "required": [
                  "key_name",
                  "value"
                  ]
          },
        }
    },
  {
        "type":"function",
        "function": {
            "name":"get_recommandation",
            "description":" recommand user customed movies",
            "parameters": {
                "type":"object",
                "properties": {}
            },
        }
    },
       {
        "type":"function",
        "function": {
            "name":"get_screen_movies",
            "description":"Bring the movie that is currently playing.",
            "parameters": {
                "type":"object",
                "properties": {}
            },
        }
    },
    {
        "type":"function",
        "function": {
            "name":"get_forthcomming_movies",
            "description":"the movie that is scheduled to be shown",
            "parameters": {
                "type":"object",
                "properties": {}
            },
        }
    },
    {
        "type":"function",
        "function": {
            "name":"get_time",
            "description":" get current time",
            "parameters": {
                "type":"object",
                "properties": {}
            },
         }

     },
    {
        "type":"function",
        "function": {
            "name":"get_temperature",
            "description":"get current temperature",
            "parameters": {
                "type":"object",
                "properties": {}
            },
        }
    },{
        "type": "function",
        "function": {
            "name": "get_movie_info",
            "description": """
            get details about specific movie
        
            
            대화 예시:
            아 윌리웡카 봤지봤지 진짜 완전짱
            되게 바보같은 이야긴데 보고 나오니까 막 나 이런거 좋아하는구나 이런 생각들었어ㅋㅋㅋ
            완전 그냥 동화 그 자체
            영화 자체가 그냥 엄청 매력적이고
            아 그리고 노래 너무 중독적이야 ㅋㅋㅋㅋ
            그리고 티모시 샬라메가 너무 잘생겼어...ㅋㅎㅎ
            """
            
            ,
            "parameters": {
                "type": "object",
                "properties": {
                    "movie_title": {
                        "type": "string",
                        "description": "movie title"
                    }
                },
                "required": ["movie_title"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "do_WebSearch",
            "description": "do websearch if neccessary",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            },
        }
    },
]


schema_func_name_dict = {
    "update_user_information": "update_detail_information_about_user",
    "get_recommandation": "make_Customized_movie_recommandation",
    "get_screen_movies": "Bring_the_movie_currently_playing",
    "get_forthcomming_movies": "Bring_the_movie_that_is_scheduled_to_be_shown",
    "get_temperature": "get_current_temperature",
    "get_movie_info": "get_details_about_specific_movie",
    "do_WebSearch": "do_websearch_about_characters_movie_etc"
}

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

    

conn = sqlite3.connect("movie.db")
print("Opened database successfully")

def get_screen_movies():
    current_date, current_time=get_time()
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    c.execute('SELECT * FROM movies')
    rows = c.fetchall()
    return current_date, current_time, rows

def get_forthcomming_movies():
    current_date, current_time=get_time()
    conn = sqlite3.connect('forthcomming.db')
    c = conn.cursor()
    c.execute('SELECT * FROM forthcomming')
    rows = c.fetchall()
    return current_date, current_time, rows

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



def update_user_information(key_name, value):
    file_path = 'user_info.json'
    
    # 여러 값을 가질 수 있는 키들
    multiple_values_keys = [
        "hobby", "like", "dislike",
        "nationality", "occupation", "MBTI", 
        "prefer_Genre" "non_prefer_Genre", "like_movie","dislike_movie", "dislike_country"
    ]
    
   # 기존 정보를 읽어옵니다.
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            user_data = json.load(f)
    else:
        user_data = {}


    # 문자열을 리스트로 변환
    for key in ["like", "dislike"]:
        if key in user_data and isinstance(user_data[key], str):
            user_data[key] = user_data[key].split(',')

    # 여러 값을 가질 수 있는 키인지 확인합니다.
    if key_name in multiple_values_keys:
        if key_name not in user_data:
            user_data[key_name] = []
        elif isinstance(user_data[key_name], str):
            user_data[key_name] = user_data[key_name].split(',')

     # like와 dislike의 상호 모순 처리
        if key_name == "like" and "dislike" in user_data and value in user_data["dislike"]:
            user_data["dislike"].remove(value)
        elif key_name == "dislike" and "like" in user_data and value in user_data["like"]:
            user_data["like"].remove(value)
            
            

        # 중복 값 체크
        if value in user_data[key_name]:
            # 값 중복

            return "맞아 네가 전에 그랬잖아"
        else:
            

            # 리스트를 다시 문자열로 변환하여 저장
            for key in ["like", "dislike"]:
                if key in user_data:
                    user_data[key] = ','.join(user_data[key])

            if key_name=="title":
                value=value.replace(" ","")

            if key_name == "dislike_country":
                print(value)
                value = country_to_iso.get(value, value) 
                print(value)

            if value.endswith(','):
                values = value[:-1].split(',')
                formatted_values = "','".join(values)
                confirmation = f"'{formatted_values}' {len(values)}개 맞아?"
                return confirmation
            
            user_data[key_name].append(value)
            
            # 업데이트된 정보를 파일에 저장합니다.
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, ensure_ascii=False, indent=4)
 
            return "그렇구나"
    else:
        # 단일 값을 가지는 키 처리
        
        user_data[key_name] = value
        # 업데이트된 정보를 파일에 저장합니다.
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, ensure_ascii=False, indent=4)

        return "그렇구나"

# 테스트 호출 예시
# 저장된 정보를 확인하는 함수
def get_user_information():
  file_path='user_info.json'
  if os.path.exists(file_path):
      with open(file_path, 'r', encoding='utf-8') as f:
          return json.load(f)
  else:
      return {}

  
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_movie_data(file_path):
    df = pd.read_csv(file_path)
    return df

def preprocess_data(df):
    # Combine genres and keywords into a single string for each movie
    df['combined_features'] = df['genres'].fillna('') + ' ' + df['keywords'].fillna('')
    return df

def get_user_profile(user_likes, movie_data):
    # Combine features of liked movies into a single string
    user_profile = ' '.join(movie_data[movie_data['original_title'].isin(user_likes)]['combined_features'])
    return user_profile

def recommend_movies(user_profile, movie_data, top_n=10):
    # Vectorize the movie data and user profile
    count_vectorizer = CountVectorizer()
    
    # Combine the user profile and movie data for vectorization
    combined_features = movie_data['combined_features'].tolist() + [user_profile]
    count_matrix = count_vectorizer.fit_transform(combined_features)
    
    # Compute the cosine similarity matrix
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    
    # Get the similarity scores for the user profile (last row in cosine_sim)
    user_sim_scores = cosine_sim[-1][:-1]
    
    # Get top N similar movies
    top_indices = user_sim_scores.argsort()[-top_n:][::-1]
    recommendations = movie_data.iloc[top_indices].copy()
    
    # Replace empty korean_title with original_title
    recommendations['display_title'] = recommendations['korean_title'].replace('', pd.NA).fillna(recommendations['original_title'])
    
    return recommendations

def get_recommandation():
    # Load movie data
    movie_file_path = 'filtered_movies.csv'
    movie_data = load_movie_data(movie_file_path)
    
    # Preprocess movie data
    movie_data = preprocess_data(movie_data)
    
    # User information
    user_info =get_user_information()
    
    
    # Get user profile
    user_profile = get_user_profile(user_info['like_movie'], movie_data)
    
    # Recommend movies
    recommendations = recommend_movies(user_profile, movie_data)
    
    # Print recommendations

    return recommendations[['korean_title', 'genres', 'vote_average']]

session_times={}

def get_time_for_session(assistant_id):
    if assistant_id not in session_times:
        session_times[assistant_id] = datetime.now()
    return session_times[assistant_id]


def create_assistant():
    
    assistant = client.beta.assistants.create(
    instructions = instructions,
    model="gpt-4o-2024-05-13",
    tools = tools,
    )

    return assistant.id

def submit_message(assistant_id,thread, user_message):
    now = get_time_for_session(assistant_id)
    # 사용자 입력 메시지를 스레드에 추가합니다.
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message+str(now)
    )
    
    # 스레드에 메시지가 입력이 완료되었다면,
    # Assistant ID와 Thread ID를 사용하여 실행을 준비합니다.
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

    return run

def ask_database(conn, query):
    """Function to query SQLite database with a provided SQL query."""
    try:
        results = str(conn.execute(query).fetchall())
    except Exception as e:
        results = f"query failed with error: {e}"
    return results



    


def get_response(thread):
    # 스레드에서 메시지 목록을 가져옵니다.
    # 메시지를 오름차순으로 정렬할 수 있습니다. order="asc"로 지정합니다.
    return client.beta.threads.messages.list(thread_id=thread.id)




def wait_on_run(run, thread):
    while True:
        run_check = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
        )
        if run_check.status in ['queued','in_progress']:
            time.sleep(2)
        else:
            break
    return run_check


def get_table_names(conn):
    """Return a list of table names."""
    table_names = []
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for table in tables.fetchall():
        table_names.append(table[0])
    return table_names


def get_column_names(conn, table_name):
    """Return a list of column names."""
    column_names = []
    columns = conn.execute(f"PRAGMA table_info('{table_name}');").fetchall()
    for col in columns:
        column_names.append(col[1])
    return column_names


def get_database_info(conn):
    """Return a list of dicts containing the table name and columns for each table in the database."""
    table_dicts = []
    for table_name in get_table_names(conn):
        columns_names = get_column_names(conn, table_name)
        table_dicts.append({"table_name": table_name, "column_names": columns_names})
    return table_dicts

def remove_emojis(text):
    answer=core.replace_emoji(text)
    return answer



if __name__=='__main__':
    print("안녕! 이름이 뭐야?")
    assistant_id=create_assistant()
    thread = client.beta.threads.create()  # 하나의 스레드를 생성하여 유지합니다.
    while(True):
        user_input=input("You: ")
        if user_input=="stop" : #for test
            client.beta.threads.delete(thread.id)
            client.beta.assistants.delete(assistant_id)
            break 
        run = submit_message(assistant_id, thread, user_input)
        
        # 실행을 대기
        run_check = wait_on_run(run, thread)
        
        if run_check.status=="requires_action":
           
            tool_calls = run_check.required_action.submit_tool_outputs.tool_calls

            tool_outputs = []
            for tool in tool_calls:
                func_name = tool.function.name
                print(func_name)
                
                kwargs = json.loads(tool.function.arguments)
                output = locals()[func_name](**kwargs)
                tool_outputs.append(
                    {
                        "tool_call_id":tool.id,
                        "output":str(output)
                    }
                )
            
            run = client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )
            run_check=wait_on_run(run,thread)
            if(run_check.status=="completed"):
                answer=get_response(thread).data[0].content[0].text.value
                cleaned_answer = remove_emojis(answer)
                print(cleaned_answer)
            
        else:    
            answer=get_response(thread).data[0].content[0].text.value
            cleaned_answer = remove_emojis(answer)
            if "SSTTOOPP" in cleaned_answer:
                modified_string = cleaned_answer.replace("SSTTOOPP", "")
                print(modified_string)
                print("[다미 님이 채팅방을 떠났습니다.]")
                client.beta.threads.delete(thread.id)
                client.beta.assistants.delete(assistant_id)
                break
            else:
                print(cleaned_answer)
        
  
