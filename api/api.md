# API 정리
## API 리스트
1. [회원가입 api](#회원가입-api)
2. [사용자 정보 저장 api (회원가입 api와 연결)](#thread-id-assistant-id-생성-api)
3. [dami api](#dami-api)
4. [save chat api (dami api와 연결)](#save-chat-api)
5. [search api(dami api와 연결)](#search-api)
## 회원가입 api
아이디, 비밀번호와 이름을 받아서 쓰레드ID를 생성하고, DB에 저장하는 API를 호출한 뒤, 사용자 정보를 DB에 저장한다.</br>
DB에 저장하는 API와 분리하는 이유는 rds와 연결한 lambda 함수는 보안상 문제로 쓰레드ID를 생성할 수 없기 때문.
### 코드 링크
[sign_up.py](https://github.com/sjk0503/chatAPP/blob/main/aws/sign_up.py)
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

## 사용자 정보 저장 api
요청받은 데이터들을 db에 저장한다.
### 코드 링크
[save_userData_DB.py](https://github.com/sjk0503/chatAPP/blob/main/aws/save_userData_DB.py)
### 요청 데이터
```python
data = {
    "userid": userid,
    "password": password,
    "name": name,
    "threadid": threadid
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

## dami api
사용자의 input에 맞는 답변을 생성하여 return, 대화 내용은 save chat api를 통해 저장한다.
### 코드 링크
[dami.py](https://github.com/sjk0503/chatAPP/blob/main/aws/dami.py)
### 요청 데이터
```python
data = {
    "user_input": user_input
}
```
### 정상 메세지
>'statusCode': 200
### 에러 메세지
1. gpt 에러
   >'statusCode':400
2. db 에러
   >'statusCode': 300
3. 서버 에러
   >'statusCode': 500

## save chat api
dami api에서 요청 받은 사용자 input과 반환할 gpt output을 db에 저장한다.
### 코드 링크
[save_chat_DB.py](https://github.com/sjk0503/chatAPP/blob/main/aws/save_chat_DB.py)
### 요청 데이터
```python
data = {
    "userid": userid,
    "user_input": user_input,
    "gpt_input": gpt_input
}
```
### 정상 메세지
>'statusCode': 200
### 에러 메세지
1. db 에러
   >'statusCode': 300
2. 서버 에러
   >'statusCode': 500

## search api
dami api에서 요청하는 api, 검색할 쿼리에 맞는 정보를 output한다.
### 코드 링크
[search_GPT.py](https://github.com/sjk0503/chatAPP/blob/main/aws/search_GPT.py)
### 요청 데이터
```python
data = {
    "query": query
}
```
### 정상 메세지
>'statusCode': 200
### 에러 메세지
1. 답변 생성 에러
   >'statusCode': 400
2. 서버 에러
   >'statusCode': 500
