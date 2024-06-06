# Lambda 함수로 작성됨
# 검색어와 함께 요청 시, google search api를 통해 정보를 가져온 뒤,
# gpt에게 정보를 전달, gpt output

import json
import os
import requests
from openai import OpenAI
from datetime import datetime

# google search init
Google_SEARCH_ENGINE_ID = os.environ.get("GSE_ID")  # Search Engine ID
Google_API_KEY = os.environ.get("GOOGLE_API_KEY")  # Custom Search Engine API KEY
start_page = "1"  # 검색할 페이지 설정. 한 페이지당 10개 가져올 수 있음

# openai init
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)


def googleInfo(query):
    url = f"https://www.googleapis.com/customsearch/v1?key={Google_API_KEY}&cx={Google_SEARCH_ENGINE_ID}&q={query}&start={start_page}"
    response = requests.get(url).json()
    output = response["items"]
    info = ""
    for out in output:
        info += out["snippet"]
        info += "\n"
    return info


def gptInfo(query, info):
    currentTime = datetime.today()
    messages = [
        {
            "role": "system",
            "content": f"Considering the current time, please provide the requested information based on the given details. / Current time: {currentTime} / Requested information: {query}"
        },
        {
            "role": "user",
            "content": info
        }
    ]
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-3.5-turbo"
    )
    return chat_completion.choices[0].message.content


def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        user_input = body['user_input']
    except (KeyError, TypeError, json.JSONDecodeError) as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid input format'})
        }
    
    search_info = ""
    try:
        search_info = googleInfo(user_input)
    except Exception as e:
        # 에러 처리
        return {
            'statusCode': 500,
            'body': json.dumps({'google search api Error': str(e)})
        }
    
    gpt_info = ""
    try:
        gpt_info = gptInfo(user_input, search_info)
    except Exception as e:
        # 에러 처리
        return {
            'statusCode': 500,
            'body': json.dumps({'gpt api Error': str(e)})
        }
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(gpt_info, ensure_ascii=False)
    }
