# 모든 api url은 비공개

import os
import json
from openai import OpenAI
import logging
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

instructions = """
Do not ask users if they need help. Do not offer solutions to complex problems.
Refer to the given time information.
Please keep in mind, the information in ‘Your information’ is your identity. Generate an answer based on that information.
'Search' is information obtained by searching keywords about you on the Internet.
"""

tools = []

update_user_information = {
    "type": "function",
    "function": {
        "name": "update_user_information",
        "description": "Record or update the user's personal information such as name, age, gender, or their likes/dislikes regarding movies or genres. Use this function for statements like '내 이름은...', '나는 ... 살이야', or '나는 ... 영화를 싫어해/좋아해'",
        "parameters": {
            "type": "object",
            "properties": {
                "key_name": {
                    "type": "string",
                    "description": """
                       json key name. It must be one of the following:
                       like_genres
                       dislike_genres
                       like_movie - movies that users have seen positively
                       dislike_movie - movies that users have seen negatively
                       old_movies - users can watch old movies
                       dislike_country - user don't want to watch this country movies.
                       """
                },
                "value": {
                    "oneOf": [
                        {
                            "type": "boolean",
                            "description": "json value. For key name 'old_movies', False==if user don't like to watch movie that more than five years."
                        },
                        {
                            "type": "string",
                            "description": "if key_name = like_genres or dislike_genres, value is oneof' Action/Adventure/Animation/Comedy/Crime/Documentary/Drama/Family/Fantasy/History/Horror/Music/Mystery/Romance/Science/TV/Thriller/War/Western."
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
}

do_WebSearch = {
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
}


def create_assistant(instruction):
    logger.info(f"instruction: {instruction}")
    assistant = client.beta.assistants.create(
        instructions=instruction,
        model="gpt-4o-2024-05-13",
        tools=tools,
    )

    thread = client.beta.threads.create()
    return assistant.id, thread.id


def lambda_handler(event, context):
    init_info = "Your information \n"
    _characterName = "Name: "
    _selectedCategories = "Your Categories: "
    _shortDescription = "shortDescription: "
    _detailedDescription = "detailedDescription: "
    _prompt = "prompt: "
    _keyword = "Search: "
    # event에서 사용자 입력 가져오기
    try:
        body = json.loads(event['body'])
        characterName = body['characterName'] + '\n'
        selectedCategories = body['selectedCategories'] + '\n'
        shortDescription = body['shortDescription'] + '\n'
        detailedDescription = body['detailedDescription'] + '\n'
        prompt = body['prompt'] + '\n'
        isSearchingLatestInfo = body['isSearchingLatestInfo']
        isUpdatingUserInfo = body['isUpdatingUserInfo']
        characterImage = body['characterImage']
        keyword = body['keyword']
        logger.info(f"""receive data: {characterName}, {selectedCategories}, {shortDescription}, {detailedDescription},
                                        {prompt}, {isSearchingLatestInfo}, {isUpdatingUserInfo}, {characterImage}""")
    except (KeyError, TypeError, json.JSONDecodeError) as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid input format'})
        }

    # 키 만들기
    try:
        # 키워드에 대한 결과 가져오기
        url = ""
        data = {
            "user_input": keyword
        }
        headers = {
            "Content-Type": "application/json"
        }
        logger.info("API 호출 시도")
        response = requests.post(url, data=json.dumps(data), headers=headers)

        _characterName += characterName + '\n'
        _selectedCategories += selectedCategories + '\n'
        _shortDescription += shortDescription + '\n'
        _detailedDescription += detailedDescription + '\n'
        _prompt += prompt + '\n'
        _keyword += response.json()['body'] + '\n'
        init_info += _characterName + _selectedCategories + _shortDescription + _detailedDescription + _prompt + _keyword
        # 추가 기능
        if bool(isSearchingLatestInfo):
            tools.append(do_WebSearch)
        if bool(isUpdatingUserInfo):
            tools.append(update_user_information)
        # 키 생성
        assistant_ID, thread_ID = create_assistant(init_info + instructions)
        logger.info(f"thread, assistant: {thread_ID}, {assistant_ID}")
    except Exception as e:
        # 에러 처리
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

    # DB에 키 저장하기
    try:
        url = ""
        data = {
            "thread_ID": thread_ID,
            "assistant_ID": assistant_ID,
            "characterName": characterName,
            "selectedCategories": selectedCategories,
            "shortDescription": shortDescription,
            "detailedDescription": detailedDescription,
            "prompt": prompt,
            "isSearchingLatestInfo": isSearchingLatestInfo,
            "isUpdatingUserInfo": isUpdatingUserInfo,
            "characterImage": characterImage
        }
        headers = {
            "Content-Type": "application/json"
        }
        logger.info("API 호출 시도")
        response = requests.post(url, data=json.dumps(data), headers=headers)
        logger.info(f"ID 저장 완료: {response}")

        # 응답에서 JSON 내용을 추출
        response_json = response.json()  # JSON 형태로 변환
    except Exception as e:
        return {
            'statusCode': 500,
            'body': 'ID 저장 오류',
            'err': str(e)
        }

    if response_json.get('statusCode') == 200:
        return {
            'statusCode': 200,
            'thread_ID': thread_ID,
            'assistant_ID': assistant_ID
        }
    else:
        return {
            'statusCode': 400
        }
