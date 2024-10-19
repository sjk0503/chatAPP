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
    # case == 'all', 모든 정보 리턴
    # case == 'id', thread, assistant id 리턴
    # case == '{cmd}', {cmd} 레코드 리턴
    case = body['case']


    try:
        # bot 테이블에서 bot_number 키의 값이 botNum인 레코드를 찾고
        # 해당 레코드의 thread_id와 assistant_id 값을 가져오는 부분
        data = {}
        with conn.cursor() as cur:
            if case == 'all':
                cur.execute("SELECT * FROM bot WHERE bot_number = %s", (botNum))
                result = cur.fetchone()
                logger.info(result)

                if result:
                    logger.info("가져오기 완료")
                    data = {
                        'statusCode': 200,
                        'thread_id': result[1],
                        'assistant_id': result[2],
                        'characterName': result[3],
                        'selectedCategories': result[4],
                        'shortDescription': result[5],
                        'detailedDescription': result[6],
                        'prompt': result[7],
                        'isSearchingLatestInfo': result[8],
                        'isUpdatingUserInfo': result[9],
                        'characterImage': result[10]
                    }
                else:
                    logger.error("레코드가 없습니다.")
                    return {
                        'statusCode': 404,
                        'body': json.dumps('not found')
                    }

            elif case == 'id':
                cur.execute("SELECT thread_id, assistant_id FROM bot WHERE bot_number = %s", (botNum))
                result = cur.fetchone()
                logger.info(result)

                if result:
                    thread_id, assistant_id = result
                    logger.info("가져오기 완료")
                    data = {
                        'statusCode': 200,
                        'thread_id': thread_id,
                        'assistant_id': assistant_id
                    }
                else:
                    logger.error("해당 bot_number에 대한 레코드가 없습니다.")
                    return {
                        'statusCode': 404,
                        'body': json.dumps('not found')
                    }
            else: # cass == '{cmd}' 특정 레코드
                cur.execute(f"SELECT {case} FROM bot WHERE bot_number = %s", (botNum))
                result = cur.fetchone()
                logger.info(result)

                if result:
                    logger.info("가져오기 완료")
                    data = {
                        'statusCode': 200,
                        case: result[0]
                    }
                else:
                    logger.error("해당 bot_number에 대한 레코드가 없습니다.")
                    return {
                        'statusCode': 404,
                        'body': json.dumps('not found')
                    }
        return data
    except Exception as e:
        logger.error("오류 발생!")
        logger.error(e)
        return {
            'statusCode': 500,
            'body': json.dumps('server error')
        }
