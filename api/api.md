# API 정리 (10.19)
## API 리스트
1. Front-End 호출용
   1. [gptsAPI](#gptsAPI)
   2. [creat_ID](#creat_ID)
   3. [get_ID](#get_ID) - (부분적 사용)
2. Back-End 용
   1. [save_chat](#save_chat)
   2. [get_ID](#get_ID) - (부분적 사용)
   3. [save_ID](#save_ID)
   4. [search](#search)

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
isSearchingLatestInfo와 isUpdatingUserInfo은 1 또는 0으로 정수로 처리해야한다.
### 코드 링크
[creat_ID.py](../aws/creat_ID.py)
### 요청 데이터
```python
data = {
   "characterName": characterName,
   "selectedCategories": selectedCategories,
   "shortDescription": shortDescription,
   "detailedDescription": detailedDescription,
   "prompt": prompt,
   "isSearchingLatestInfo": isSearchingLatestInfo, 1 또는 0 ('1', '0' 하면 안됨)
   "isUpdatingUserInfo": isUpdatingUserInfo, 1 또는 0 ('1', '0' 하면 안됨)
   "characterImage": characterImage,
   "keyword": keyword
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
botNum에 맞는 thread ID와 assistant ID를 DB에서 가져오는 API<br>
case 데이터를 받아서 각 case 별로 리턴하는 데이터를 달리함
> case == 'all', 모든 정보 리턴 <br>
> case == 'id', thread, assistant id 리턴<br>
> case == '{cmd}', {cmd} 레코드 리턴<br>
### 코드 링크
[get_ID.py](../aws/get_ID.py)
### 요청 데이터
```python
data = {
   "botNum": int(botNum),
   "case": cmd # "all" or "id" or 원하는 레코드명
}
```
### 정상 메세지
case == 'all' 경우
```python
return {
   'statusCode': 200,
   'thread_id': thread_id,
   'assistant_id': assistant_id,
   'characterName': characterName,
   'selectedCategories': selectedCategories,
   'shortDescription': shortDescription,
   'detailedDescription': detailedDescription,
   'prompt': prompt,
   'isSearchingLatestInfo': isSearchingLatestInfo,
   'isUpdatingUserInfo': isUpdatingUserInfo,
   'characterImage': characterImage
}
```
case == 'id' 경우
```python
return {
   'statusCode': 200,
   'thread_id': thread_id,
   'assistant_id': assistant_id
}
```
case == cmd 경우 (ex. 'thread_id' or 'characterName' or 'prompt' 등)
```python
return {
   'statusCode': 200,
   case: case # 'thread_id': thread_id or 'characterName': characterName or 'prompt': prompt
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
   "assistant_ID": assistant_ID,
   "characterName": characterName,
   "selectedCategories": selectedCategories,
   "shortDescription": shortDescription,
   "detailedDescription": detailedDescription,
   "prompt": prompt,
   "isSearchingLatestInfo": isSearchingLatestInfo,
   "isUpdatingUserInfo": isUpdatingUserInfo,
   "characterImage": characterImage
}
```
### 정상 메세지
```python
return {
   'statusCode': 200,
   'body': json.dumps('save ID successful')
}
```

## search
사용자 쿼리에 대한 검색 결과를 리턴하는 API
create_ID api와 연동되어, 사용자가 입력한 keyword에 대한 검색 결과를 키를 생성할 때 포함하여 생성한다.
### 요청 데이터
```python
data = {
   "user_input": keyword
}
```
### 정상 메세지
```python
return {
   'statusCode': 200,
   'body': query # 검색 결과를 담은 내용
}
```
