# api 정리
## api 리스트
1. [회원가입 api](##-회원가입-api(POST))
2. thread id, assistant id 생성 api (회원가입 api와 연결)
3. dami api
4. save chat api (dami api와 연결)
## 회원가입 api(POST)
아이디, 비밀번호와 이름을 받아서 db에 저장하고 동시에 openAI thread id 를 생성하여 db에 저장한다.
### 요청 데이터
```python
data = {
    "userid": userid,
    "password": password,
    "name": name
}
```
### 정상 메세지
>'statusCode': 200
### 에러 메세지
1. 아이디 중복 시
    >'statusCode': 400
3. 서버 에러
    >'statusCode': 500

## thread id, assistant id 생성 api (회원가입 api와 연결)
id 생성 후, db에 저장한다.
### 요청 데이터
```python
data = {
    "userid": userid
}
```
### 정상 메세지
>'statusCode': 200
### 에러 메세지
1. thread id 발급 에러
   >'statusCode': 400
2. assistant id 발급 에러
   >'statusCode': 400
3. 서버 에러
   >'statusCode': 500
4. db 접근 에러
   >'statusCode': 300
