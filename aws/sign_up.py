# RDS와 연동하여 아이디, 비밀번호와 이름을 DB에 저장하고,
# 쓰레드 아이디를 api를 통해 생성한 뒤, DB에 저장함

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
    password = body['password']
    name = body['name']
    threadid = body['threadid']

    try:
        with conn.cursor() as cur:
            # 아이디 중복 검사
            cur.execute("SELECT COUNT(*) FROM users WHERE userid = %s", (userid,))
            result = cur.fetchone()
            if result[0] > 0:
                logger.error("아이디 중복!")
                return {
                    'statusCode': 400,
                    'body': json.dumps('error: id exists')
                }

            # 새 사용자 삽입
            cur.execute("INSERT INTO users (userid, password, name) VALUES (%s, %s, %s)", (userid, password, name))
            logger.info(f"사용자 삽입 완료: {userid}")

            # 변경 사항 커밋
            conn.commit()
            logger.info("사용자 삽입 커밋 완료")

            # 쓰레드아이디와 유저아이디를 dami 테이블에 저장
            cur.execute("INSERT INTO dami (threadid, userid) VALUES (%s, %s)", (threadid, userid))
            logger.info(f"dami 테이블에 쓰레드아이디와 유저아이디 저장 완료: {threadid}, {userid}")

            # 변경 사항 커밋
            conn.commit()
            logger.info("변경 사항 커밋 완료")
        
        return {
            'statusCode': 200,
            'body': json.dumps('sign up successful')
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
