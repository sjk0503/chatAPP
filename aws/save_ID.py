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

    thread_ID = body['thread_ID']
    assistant_ID = body['assistant_ID']

    try:
        with conn.cursor() as cur:
            # 사용자의 입력을 저장
            cur.execute("INSERT INTO bot (thread_id, assistant_id) VALUES (%s, %s)",
                        (thread_ID, assistant_ID))
            logger.info(f"ID 저장 완료: {thread_ID}, {assistant_ID}")

            # 변경 사항 커밋
            conn.commit()
            logger.info("변경 사항 커밋 완료")
        return {
            'statusCode': 200,
            'body': json.dumps('save ID successful')
        }
    except Exception as e:
        logger.error("오류 발생!")
        logger.error(e)
        return {
            'statusCode': 500,
            'body': json.dumps('server error')
        }
