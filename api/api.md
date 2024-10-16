# API 정리 (10.8)
## API 리스트
1. Front-End 호출용
   1. [gptsAPI](#gptsAPI)
   2. [creat_ID](#creat_ID)
2. Back-End 용
   1. [save_chat](save_chat)
   2. [get_ID](get_ID)
   3. [save_ID](save_ID)

## gptsAPI
gpt 대화 생성 api <br>
get_ID, save_chat API와 연동되어, 원하는 bot number의 ID를 DB에서 가져오고, 생성한 대화 내용을 자동으로 DB에 저장한다.
### 코드 링크
[gptsAPI.py](../aws/gptsAPI.py)
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

## creat_ID
사용자가 원하는 쿼리에 기반한 gpt 모델 ID 생성 API<br>
save_ID API와 연동되어, 생성한 ID를 DB에 저장한다.
### 코드 링크
[creat_ID.py](../aws/creat_ID.py)
### 요청 데이터
```python
data = {
    "instructions": instructions # 사용자가 원하는 쿼리
}
```
### 정상 메세지 (ID도 리턴되지만, Front에서 따로 처리할 필요는 없음)
```python
return {
   'statusCode': 200,
   'thread_ID': thread_ID,
   'assistant_ID': assistant_ID
}
```

## save_chat
gptsAPI에서 호출하는 API <br>
대화 내용을 DB에 저장한다.
### 코드 링크
[save_chat.py](../aws/save_chat.py)
### 요청 데이터
```python
data = {
   "botNum": botNum, # 대화한 bot 번호
   "user_input": user_input, # 사용자 대화
   "gpt_input": gpt_input # gpt가 생성한 대화
}
```
### 정상 메세지
```python
return {
   'statusCode': 200,
   'body': json.dumps('save chat successful')
}
```

## get_ID
botNum에 맞는 thread ID와 assistant ID를 DB에서 가져오는 API
### 코드 링크
[get_ID.py](../aws/get_ID.py)
### 요청 데이터
```python
data = {
   "botNum": botNum
}
```
### 정상 메세지
```python
return {
   'statusCode': 200,
   'thread_id': thread_id,
   'assistant_id': assistant_id
}
```

## save_ID
사용자 요청 쿼리에 맞게 생성한 GPT ID를 DB에 저장하는 API
### 코드 링크
[save_ID.py](../aws/save_ID.py)
### 요청 데이터
```python
data = {
   "thread_ID": thread_ID,
   "assistant_ID": assistant_ID
}
```
### 정상 메세지
```python
return {
   'statusCode': 200,
   'body': json.dumps('save ID successful')
}
```
