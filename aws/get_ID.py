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

    botNum = body['botNum']

    try:
        # bot 테이블에서 bot_number 키의 값이 botNum인 레코드를 찾고
        # 해당 레코드의 thread_id와 assistant_id 값을 가져오는 부분
        with conn.cursor() as cur:
            cur.execute("SELECT thread_id, assistant_id FROM bot WHERE bot_number = %s", (botNum,))
            result = cur.fetchone()

            if result:
                thread_id, assistant_id = result
                logger.info(f"id 가져오기 완료 + {thread_id}, {assistant_id}")
            else:
                logger.error("해당 bot_number에 대한 레코드가 없습니다.")
                return {
                    'statusCode': 404,
                    'body': json.dumps('not found')
                }

        return {
            'statusCode': 200,
            'thread_id': thread_id,
            'assistant_id': assistant_id
        }
    except Exception as e:
        logger.error("오류 발생!")
        logger.error(e)
        return {
            'statusCode': 500,
            'body': json.dumps('server error')
        }
