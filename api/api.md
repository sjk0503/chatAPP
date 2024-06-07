# api 정리
## 회원가입 api(POST)
### 요청 데이터
```python
data = {
    "userid": userid,
    "password": password,
    "name": name
}
```
### 회원 가입 성공 시
```python
return {
    'statusCode': 200,
    'body': json.dumps('sign up successful')
}
```
### 에러 메세지
1. 아이디 중복 시
```python
return {
    'statusCode': 400,
    'body': json.dumps('error: id exists')
}
```
2. 서버 에러
```python
return {
    'statusCode': 500,
    'body': json.dumps('server error')
}
```
