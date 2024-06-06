import requests
import json
import os

# API Gateway 엔드포인트 URL
url = os.environ.get("API_URL")

query = input()

# 요청 본문 데이터
# 요청 입력
data = {
    "user_input": query
}

# 요청 헤더 설정
headers = {
    "Content-Type": "application/json"
}

# POST 요청 보내기
response = requests.post(url, data=json.dumps(data), headers=headers)

# 응답 확인
if response.status_code == 200:
    print("Response:")
    # 실제로 리턴 될 값
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)
