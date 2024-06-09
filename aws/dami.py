# 학습시킨 gpt를 서버에 배포하는 코드
# 다양한 api(검색 api, tmdb api, gpt api 등)와 다양한 함수를 조합하여 구현


import json
import os
from openai import OpenAI
import requests
import datetime
import time
from bs4 import BeautifulSoup
import sys
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

ASSISTANT_ID = ""
THREAD_ID = ""
TMDB_API_KEY = ''

# 스레드에 대화 입력하는 함수
def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread,
        role="user",
        content=user_message,
    )

    run = client.beta.threads.runs.create(
        thread_id=thread,
        assistant_id=assistant_id,
    )

    return run


# 대화분석 실행대기
def wait_on_run(run, thread_id):
    while True:
        run_check = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        if run_check.status in ['queued', 'in_progress']:
            time.sleep(2)
        else:
            break
    return run_check


# 어시스턴트 답변 가져오기
def get_response(thread_id):
    return client.beta.threads.messages.list(thread_id)


# 시간 체크용
def timer():
    now = datetime.datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")
    return current_date, current_time

#온도체크
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


# 검색함수
def WebSearch(query):
    logger.info("함수 접근 성공")
    url = "https://flnptw3076.execute-api.eu-north-1.amazonaws.com/gpt/searchGPT"
    data = {
        "user_input": query
    }
    headers = {
        "Content-Type": "application/json"
    }
    # POST 요청 보내기
    logger.info("search api 호출 시도")
    response = requests.post(url, data=json.dumps(data), headers=headers)
    logger.info("search api 호출 성공")
    response_json = response.json()
    results = response_json['body']
    current_date, current_time = timer()

    return current_date, current_time, results


# 검색함수
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
            WebSearch(movie_title)
    else:
        WebSearch(movie_title)

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

    try:
        if run_check.status == "requires_action":
            tool_calls = run_check.required_action.submit_tool_outputs.tool_calls
            logger.info("실행할 함수 가져오기 성공")

            tool_outputs = []
            for tool in tool_calls:
                func_name = tool.function.name
                logger.info(f"함수 접근 시도: {func_name}")
                kwargs = json.loads(tool.function.arguments)

                # 함수를 직접 호출
                if func_name in globals() and callable(globals()[func_name]):
                    output = globals()[func_name](**kwargs)
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
        else:
            answer = get_response(THREAD_ID).data[0].content[0].text.value
    except Exception as e:
        return {
            'statusCode': 500,
            'body': '함수 분석 오류'
        }
    
    # 채팅 db 저장
    try:
        url = "https://ayt27rgcse.execute-api.eu-north-1.amazonaws.com/sign_up/save_chat"
        data = {
            "userid": "jkelly",
            "user_input": user_input,
            "gpt_input": answer
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, data=json.dumps(data), headers=headers)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': '대화 내용 저장 오류'
        }

    return {
        'statusCode': 200,
        'body': answer
    }
