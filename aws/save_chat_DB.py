# 사용자의 input과 gpt의 output을 rds(MySQL)에 저장하는 api


import sys
import logging
import pymysql
import json
import os
    

rds_host = os.environ.get("rds_host")
user_name = os.environ.get("user_name")
password = os.environ.get("password")
db_name = os.environ.get("db_name")

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(host=rds_host, user=user_name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("연결 실패!")
    logger.error(e)
    sys.exit()

logger.info("연결 성공!")

def lambda_handler(event, context):
    body = json.loads(event['body'])
    
    userid = body['userid']
    user_input = body['user_input']
    gpt_input = body['gpt_input']

    try:
        with conn.cursor() as cur:
            # 사용자의 입력을 저
            cur.execute("INSERT INTO chats (userid, chat, issend, time) VALUES (%s, %s, %s, NOW())", 
                        (userid, user_input, True))
            logger.info(f"사용자 입력 저장 완료: {user_input}")

            # GPT의 응답을 저장
            cur.execute("INSERT INTO chats (userid, chat, issend, time) VALUES (%s, %s, %s, NOW())", 
                        (userid, gpt_input, False))
            logger.info(f"GPT 응답 저장 완료: {gpt_input}")

            # 변경 사항 커밋
            conn.commit()
            logger.info("변경 사항 커밋 완료")
        
        return {
            'statusCode': 200,
            'body': json.dumps('save chat successful')
        }
    except pymysql.MySQLError as e:
        logger.error("데이터베이스 오류 발생!")
        logger.error(e)
        return {
            'statusCode': 500,
            'body': json.dumps('database error')
        }
    except Exception as e:
        logger.error("오류 발생!")
        logger.error(e)
        return {
            'statusCode': 500,
            'body': json.dumps('server error')
        }
