# API 정리 (10.8)
## API 리스트
1. Front-End 호출용
   1. gptsAPI
   2. creat_ID
2. Back-End 용
   1. save_chat
   2. get_ID
   3. save_ID
  

1. [회원가입 api](#회원가입-api)
2. [사용자 정보 저장 api (회원가입 api와 연결)](#thread-id-assistant-id-생성-api)
3. [dami api](#dami-api)
4. [save chat api (dami api와 연결)](#save-chat-api)
5. [search api(dami api와 연결)](#search-api)


## gptsAPI
gpt 대화 생성 api <br>
get_ID, save_chat API와 연동되어, 원하는 bot number의 ID를 DB에서 가져오고, 생성한 대화 내용을 자동으로 DB에 저장한다.
### 코드 링크
[sign_up.py](https://github.com/sjk0503/chatAPP/blob/main/aws/sign_up.py)
### 요청 데이터
```python
data = {
   "botNum": botNum, # ex) 1 or 2 or 3 ...
   "user_input": user_input
}
```
### 정상 메세지
```python
return {
   "statusCode": 200,
   "body": answer # gpt 응답
}
```

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
