# RDS와 연동한 lambda 함수는 쓰레드ID를 생성할 수 없음(보안상 문제)
# 아이디, 비밀번호와 이름을 요청 데이터로 받고,
# 쓰레드ID를 생성한 뒤에,
# DB에 저장하는 API를 호출하여 DB에 저장한다.

import json
import os
import logging
import sys
import requests
from openai import OpenAI

def lambda_handler(event, context):
    body = json.loads(event['body'])
    
    userid = body['userid']
    password = body['password']
    name = body['name']
    
    try:
        API_KEY = os.environ['OPENAI_API_KEY']
        client = OpenAI(api_key=API_KEY)
        thread = client.beta.threads.create()
        threadid = thread.id
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps('thread err')
        }

    try:
        url = "https://ayt27rgcse.execute-api.eu-north-1.amazonaws.com/sign_up/sign_up_save_db"
        data = {
            "userid": userid,
            "password": password,
            "name": name,
            "threadid": threadid
        }
        headers = {
            "Content-Type": "application/json"
        }
        try:
            # POST 요청 보내기
            response = requests.post(url, data=json.dumps(data), headers=headers)
            return json.dumps(response)
        except Exception as e:
            logger.info("회원가입 요청 실패")
        
    except Exception as e:
        logger.error("오류 발생!")
        logger.error(e)
        return {
            'statusCode': 500,
            'body': json.dumps('server error')
        }
