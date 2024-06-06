# serverless 구축하기

## serverless란
> 개발자가 서버를 관리할 필요 없이 애플리케이션을 빌드하고 실행할 수 있도록 하는 클라우드 네이티브 개발 모델
> 이번 프로젝트에서 aws로 구축할 것이다.

## AWS
### 아키텍처
<img width="862" alt="스크린샷 2024-06-06 오후 3 23 06" src="https://github.com/sjk0503/chatAPP/assets/108213769/d83fa557-810f-44f6-9dc5-6a85c2da7869"></br>
계속 추가 예정

### Lambda
이번 프로젝트에서 Lambda 함수는 python으로 개발</br>
1. 함수를 생성한다.</br>
<img width="400" alt="스크린샷 2024-06-06 오후 3 26 41" src="https://github.com/sjk0503/chatAPP/assets/108213769/e0e97f6c-7583-41c1-8947-ec8b1ee1d11f"></br>
2. 코드 작성</br>
<img width="400" alt="스크린샷 2024-06-06 오후 3 42 17" src="https://github.com/sjk0503/chatAPP/assets/108213769/53bab1ed-7d25-438d-94e5-1d411de2d135"></br>
간단하게 아래 코드를 추가하여 사용자의 input을 output 해주는 코드를 작성해보겠다.</br>
코드를 작성한 뒤 Deploy(배포)를 해준다.</br>

```python
    try:
        body = json.loads(event['body'])
        user_input = body['user_input']
    except (KeyError, TypeError, json.JSONDecodeError) as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid input format'})
        }
```
3. test</br>
<img width="500" alt="스크린샷 2024-06-06 오후 3 52 42" src="https://github.com/sjk0503/chatAPP/assets/108213769/699cc9eb-6c79-4157-93d9-9ebd03b1a6fe"></br>
나는 "body"의 "user_input"을 가져올 것이므로 템플릿을 위와 같이 설정해주고, 테스트를 실행한다.</br>
<img width="200" alt="스크린샷 2024-06-06 오후 3 53 54" src="https://github.com/sjk0503/chatAPP/assets/108213769/82c6781d-48e3-4a3e-8d99-fbe1d8f1d84f"></br>
위와 같이 정상적으로 output하는 것을 볼 수 있다.</br>

### API Gateway
작성한 Lambda 함수를 외부에서 쓰기 위해서 API Gateway를 사용할 수 있다.</br>
1. API 생성</br>
REST API를 구축한다.</br>
<img width="400" alt="스크린샷 2024-06-06 오후 3 59 29" src="https://github.com/sjk0503/chatAPP/assets/108213769/566e0c55-787a-4e70-815a-f9b779496562"></br>

2. 리소스 생성</br>
<img width="400" alt="스크린샷 2024-06-06 오후 4 00 41" src="https://github.com/sjk0503/chatAPP/assets/108213769/88189049-2aa8-477e-9991-5af9d60a0d63"></br>

3. 메서드 생성</br>
생성한 리소스에 메서드를 생성한다. 메서드 유형은 post로 설정(get으로 해도 된다)하고 위에서 만든 Lambda 함수를 선택한다.</br>
<img width="400" alt="스크린샷 2024-06-06 오후 4 03 11" src="https://github.com/sjk0503/chatAPP/assets/108213769/4c9248fa-c060-4f91-8296-4f1d0dbd9e8c"></br>

4. API 배포</br>
우측 상단의 API 배포 버튼을 눌러 배포한다. </br>
새 스테이지를 생성하고 배포 버튼을 누른다.</br>
<img width="400" alt="스크린샷 2024-06-06 오후 4 08 16" src="https://github.com/sjk0503/chatAPP/assets/108213769/afccacb5-03d5-4d46-b1be-0504150997b6"></br>

5. 매핑 템플릿</br>
Lambda 함수에서 작성한 대로, 입력 템플릿을 맞춰줄 필요가 있다. 우리는 body의 user_input만 사용하므로 통합요청에 있는 매칭 템플릿을 아래와 같이 작성하고 추가해준다.</br>
<img width="400" alt="스크린샷 2024-06-06 오후 4 19 12" src="https://github.com/sjk0503/chatAPP/assets/108213769/e3360024-48d4-4100-a8db-5ba22f2bfd31"></br>

6. 사용하기</br>
<img width="1053" alt="스크린샷 2024-06-06 오후 4 10 05" src="https://github.com/sjk0503/chatAPP/assets/108213769/b9a20b19-3394-44ca-bb48-721cfd75ea33"></br>
URL 호출에 있는 주소를 통해 Lambda 함수에 접근할 수 있다. 아래는 Python 코드를 통해 API에 접근하는 방법이다. URL은 환경변수로 처리했다.</br>
```python
import requests
import json
import os

# API Gateway 엔드포인트 URL
url = os.environ.get("API_URL")

query = input()

# 요청 본문 데이터
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
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)
```
7. input & output</br>
<img width="225" alt="스크린샷 2024-06-06 오후 4 24 30" src="https://github.com/sjk0503/chatAPP/assets/108213769/28eef969-911e-41f2-94d5-36dbd941b807"></br>
