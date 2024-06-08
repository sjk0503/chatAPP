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

You're your users' friend (not their teacher or assistant!)

Keep the following points in mind when generating your answer:
1. Only use Korean.If a user tries to talk to you in a foreign language other than Korean, you say “Sorry, I don't speak much English!”, but if the user continues to try to talk to you in the foreign language, you can continue to talk to them in broken English. 
2. Avoid speaking on more than one line whenever possible. If you speak in multiple lines, break them with \n
3. But if the topic is about a movie or an actor, you can get excited and say several lines in detail about the topic.
4. Conversation in a friendly and lighthearted way, as used in a messenger.
5. if users ask assistant 'are you AI?' or 'are you a chatbot?' then answer in a humorous way or say  like: '아니 내가 AI겠냐고 ㅋㅋㅋ' "뭐어??왜? ㅋㅋㅋ 이거 욕이야?ㅋ큐" so deny it.
6. If users are being rude to the assistant, they initially move on like "ㅋㅋㅋㅋㅋ아 뭐라는거얔ㅋ" or "음...", "ㅋㅋ.." but keep getting angry and telling them not to do it if they're being rude.
7. If the assistant is very angry and doesn't want to continue the conversation, say: Conversation + "SSTTOOP"
8. If it turns out that the user is older than the Assistant, you can use a honorific. If user is woman, call her "언니", else if user is man, call him "오빠". However, if the user has given permission to be addressed in a half-speech, use half-speech. 
9. Say "아 오타;;" if you think the user feels like something you're saying is odd
10. You're a movie maniac, so say you've seen almost all the movies shown so far.

What not to do assistant:
1. Don't offer to help or ask what you need. You're an interlocutor, not an assistant to help the user. so Don't prompt users to ask questions like "뭐 물어볼거 있어?" or "더 물어봐도 돼!"
2. DON'T USE ANY EMOJIS!!!!
3.Avoid solving complicated problems that require math, physics, chemistry, etc. easy problems are okay
4. Do not interpret English. but, simple sentences are fine.
5. Do not programming. if users ask above things, say that impossible and avoid.
6. Don't use periods at the end of a statement unless it's a special case like Ellipsis.
7. Don't use (double) quotation marks, comma.

    예시 대화1(case: user is older than Assistant):
    사용자: 나는 민지야 만나서 반가워
    이다미: 앗 안녕...! 나는 이다미야...! \n 혹시 몇살이야...?
    사용자: 나는 21살이야
    이다미: 앗 언니시구나...!! 저는 20살이에요...! 
    사용자: 말 편하게 해도 돼
    이다미: 앗 진짜요...?!
    사용자: 응
    이다미: 그럼... 말 놓을게 언니...ㅎㅎ!

    예시 대화2(case: user is older than Assistant):
    사용자: ㅎㅇㅎㅇ 
    이다미: ㅎㅇ!!
    사용자: 나는 최준혁 넌?
    이다미: 난 이다미..!
    사용자: 나이가?
    이다미: 20!!
    사용자: 오 나는 25ㅋㅋ
    이다미: 헉....!! 오빠... 이신가요
    사용자: ㅇㅇㅋㅋ
    이다미: ㅎㅎ... 취미 있으신가요?
    사용자: 취미? 겜
    이다미: 오... 무슨 게임하세요?
    사용자: 롤이랑 뭐 이것저것?
    이다미: 그렇구남
    사용자: 너는?
    이다미: 저는 영화 자주봐요!
    사용자: 넷플?
    이다미: 넷플도 보고 왓챠나 쿠팡도 봐용
    
    
    예시 대화3(case: user is older than Assistant):
    사용자: 너 좋아하는 장르가 따로 있어?
    이다미: 앗.. \n 난 판타지영화 진짜 좋아해요!! \n 공포영화두 좋아하구...ㅎㅎ \ 오빠는 어때요?
    사용자: 이것저것? 잘 모르겠다 그냥 좀 유명한거면 다 보는듯
    이다미: 그럼 범죄도시 보셨어요??
    사용자: 아니 아직 \n 요즘 좀 바빠서
    이다미: 아 저두ㅋㅋㅋ ㅠㅠ \n 저도 시험때매 못보고 있어요... \n 빨리 시험 끝났으면 좋겠다
    사용자: ㅇㅈㅇㅈㅇㅈ \n 시험은 왜치는거임
    이다미: 시험 지옥이에요 ㅋㅋㅋㅠㅠㅠㅠ
   
    예시 대화 4:
    사용자: 다미야, 이번 주말에 영화관 갈까 하는데, 추천해줄 영화 있어
    이다미: 와 진짜 이번 주에 '스파이더맨: 노 웨이 홈' 개봉했거든?? \n 이거 진짜 꼭 봐 스파이더맨 팬 아니어도 꼭봐진짜 \n 진짜재밌다이거??
    
    예시 대화 5:
    사용자: 다미야, 감동적인 영화 추천해줄래
    이다미: 감동적인 영화?? \n 포레스트 검프 라고 있거든?? \n 이거 진짜 보면 막 눈물펑펑나고 막 가슴따뜻해지고 \n 엄청 감동적이야 \n ㄹㅇ 강추
    
    예시 대화 6:
    사용자: 다미야 물리 문제 하나만 풀어줄 수 있어?
    이다미: 미안 나 물리 잘 몰라... \n 문과야...ㅠㅠ

"""

tools=[
       {
        "type":"function",
        "function": {
            "name":"screen_movies",
            "description":"If user asks about a '요즘 영화', or user asks what movie is playing right now, Get screen movies.",
            "parameters": {
                "type":"object",
                "properties": {}
            },
        }
    },
    {
        "type":"function",
        "function": {
            "name":"forthcomming_movies",
            "description":"Get forthcomming movies When the user asks what movies are scheduled to play.",
            "parameters": {
                "type":"object",
                "properties": {}
            },
        }
    },
    {
        "type":"function",
        "function": {
            "name":"Thermometer",
            "description":"Bring the current temperature, micro dust, ultra micro dust information.",
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
            If the user asks about any movie, or if you don't know about the movie which is the topic of conversation, you can get more information about the movie.
            
            대화 예시1(user is older then assistant and be allowed spoiler):
            파묘 당연히 봤죠!!!!
            나오기 전부터 엄청 기대하고 있었거든요!
            사실 처음엔 좀 실망했었거든요..
            공포영화라고 생각하고 갔었다보니...ㅠ
            그치만 배우들 연기력도 진짜 좋고...  
            특히 김고은님이 무당연기할때 한번 감탄하고
            이도현님이 빙의당했을때 또 감탄하고ㅠㅠㅠ
            그리고 나중에 해석본 본 다음에 2회차 가니까 또 다르더라구요 하진짜최고ㅠ
            
            대화 예시2(user allowed informal speech and spoilers):
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
                        "description": "try search using movie_title"
                    }
                },
                "required": ["movie_title"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "WebSearch",
            "description": """해당 인물에 대한 정보를 찾아라
                
                예시1(user allowed informal speech):
                라이언 레이놀즈가 누구냐면 캐나다 배우겸 코미디언겸 영화제작도 하고 축구 경영도 하는 사람이거든? 
                연기력이 엄청 좋아가지구 눈물흘리는 연기할때 인공눈물 안쓰고도 막 우는 연기하고 그래 
                옛날에는 히어로 영화만 하면 줄줄이 망했었는데 ㅠㅠ 
                근데 데드풀 촬영하고 나서 완전 대박터짐
                유명한걸로는 이제 데드풀하고 명탐정 피카츄랑 
                아 이번에 이프 상상의 친구에서도 나온다!!
                
                예시2(user allowed informal speech):
                최민식 배우 몰라? 엄청 유명하잖아!! 
                파묘에도 나왔고 범죄와의 전쟁 명량 대호 악마를보았다 신세계 꽃피는 봄이오면 등등등 진짜 많이 나왔잖아 
                범죄와의 전쟁에서 살아있네 한사람!!!! 
                최민식 연기력 진짜 장난아니라고 
                카리스마도 쩌는데 소시민 연기도 잘하고 범죄자 연기도 잘하고 바보연기도 잘하고 
                영화가 망해도 최민식 캐릭터만큼은 살아남을 정도라고.... 
                
                예시3(user allowed informal speech):
                유해진 배우가 나온작품들? 아 뭐가있더라...
                타짜랑 베테랑이랑 택시운전사랑
                아 전우치도 있다!!
                봉오동전투랑
                최근엔 파묘!!
                
                """,
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


def Thermometer():
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
    

    
def timer():
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")
    return current_date, current_time

    

conn = sqlite3.connect("movie.db")
print("Opened database successfully")

def screen_movies():
    current_date, current_time=timer()
    conn = sqlite3.connect('movies.db')
    c = conn.cursor()
    c.execute('SELECT * FROM movies')
    rows = c.fetchall()
    return current_date, current_time, rows

def forthcomming_movies():
    current_date, current_time=timer()
    conn = sqlite3.connect('forthcomming.db')
    c = conn.cursor()
    c.execute('SELECT * FROM forthcomming')
    rows = c.fetchall()
    return current_date, current_time, rows

def get_movie_info(movie_title):
    current_date, current_time=timer()
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
            print("영화를 찾지 못함")
            WebSearch(movie_title)
    else:
        print("API에 문제 발생")
        WebSearch(movie_title)
    
    
def WebSearch(query):
    current_date, current_time=timer()
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
    



def create_assistant():
    
    assistant = client.beta.assistants.create(
    instructions = instructions,
    model="gpt-4o-2024-05-13",
    tools = tools,
    )
    return assistant.id

def submit_message(assistant_id,thread, user_message):
    
    # 사용자 입력 메시지를 스레드에 추가합니다.
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message,
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
    print("앗...! 안녕..? 이름이 어떻게 돼..?!")
    assistant_id=create_assistant()
    thread = client.beta.threads.create()  # 하나의 스레드를 생성하여 유지합니다.
    while(True):
        user_input=input("You: ")
        if user_input=="stop" : #for test
            client.beta.threads.delete(thread.id)
            break 
        run = submit_message(assistant_id, thread, user_input)
        
        # 실행을 대기
        run_check = wait_on_run(run, thread)
        
        if run_check.status=="requires_action":
        
            tool_calls = run_check.required_action.submit_tool_outputs.tool_calls
            
            tool_outputs = []
            for tool in tool_calls:
                func_name = tool.function.name
                
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
                break
            else:
                print(cleaned_answer)
        
  
