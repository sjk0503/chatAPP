# GPT 이전 대화 기억
gpt api를 사용하면서 가장 문제점은 지속적인 대화가 불가능하다는 것이다.
이를 해결하기 위해서는 매번 api를 호출할 때 마다 이전 대화를 함께 보내야한다.

## 단순 저장 방식
### 구현 방법
첫 번째 방법은 단순히 지금까지의 대화내용을 계속 저장하여 api를 호출할때 같이 보내는 것이다.

(첫 번째 방법 알고리즘)
```python
user_message = {
    "role": "user",
    "content": user_input
}

messages.append(user_message)  # 사용자 메시지 추가

# 메시지 리스트 전송하고 결과 받기
chat_completion = client.chat.completions.create(
    messages=messages,
    model="gpt-3.5-turbo"
)

# 모델의 응답 출력
assistant_response = chat_completion.choices[0].message.content
print("gpt\n", assistant_response)
print()

# 모델의 응답을 메시지 리스트에 추가
assistant_message = {
    "role": "assistant",
    "content": assistant_response
}
messages.append(assistant_message)
```

위 방식은 사용자가 입력한 대화내용과 응답 메시지를 계속해서 리스트에 추가하는 방식이다.

### 문제점
계속해서 대화를 이어나갈 경우 최대 허용 토큰 갯수를 초과할 수 있다는 문제점이다.

## 최근 대화만 기억하는 방식
### 구현 방법
말 그대로 최근 대화만 기억하는 방식이다.
최대 저장할 대화 갯수를 정하고, 해당 대화 갯수를 넘을 경우 과거 대화는 삭제하는 방식으로 구현한다.

(두번째 방법 알고리즘)
```python
max_messages = 5  # 최대 메시지 수

while True:
    user_input = input("user\n")  # 사용자 입력 받기
    if user_input.lower() in ["quit", "exit", "stop"]:  # 종료 조건
        print("대화를 종료합니다.")
        break
    print()
    user_message = {
        "role": "user",
        "content": user_input
    }
    messages.append(user_message)

    if len(messages) > max_messages:
        messages = messages[-max_messages:]

    # GPT-3 모델에 메시지 리스트 전송하고 결과 받기
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-3.5-turbo"
    )

    # 모델의 응답 출력
    assistant_response = chat_completion.choices[0].message.content
    print("gpt\n", assistant_response)
    print()
    # 모델의 응답을 메시지 리스트에 추가
    assistant_message = {
        "role": "assistant",
        "content": assistant_response
    }
    messages.append(assistant_message)
```

### 문제점
효율적으로 토큰을 관리할 수 있지만, 오래된 대화를 기억하지 못한다. 이는 사용자의 만족도를 감소시킬 수 있다.

## 내용을 요약하여 저장
### 구현 방법
매번 입력한 내용과 답변을 요약하여 저장하는 것이고, 요약 알고리즘을 따로 구현해야한다.
요약하는 방법을 두가지 정도 생각해보았다.
1. 파이썬의 KoNLPy 라이브러리를 사용하여 명사만 추출하기
2. 문서 요약 api(naver) 사용하기

#### KoNLPy 라이브러리 사용
일단 KoNLPy의 품사 태깅 클래스 중 가장 빠른 Mecab을 사용하였다.
명사만 추출하는 이유는 명사만 보더라도 어느정도 내용 추측이 가능하기 때문이다.

> 직업도 없이 허름한 반지하에 사는 기택 가족에게 돈을 벌 기회가 찾아온다. 친구의 소개로 부잣집 딸 다혜의 과외 선생님을 맡게 된 기택의 아들, 기우는 기대감에 부푼 채 글로벌 IT기업을 이 끄는 박 사장의 저택에 들어간다. 극과 극의 삶을 사는 두 가족의 예측 불가능한 만남이 시작된다.

위 글을 명사만 추출할 경우 아래와 같다.

> 직업 반지하 기택 가족 돈 기회 친구 소개 부잣집 딸 혜의 과외 선생 기택 아들 친구 소개 부잣집 딸 혜의 과외 선생 기택 아들 기대감 채 글로벌 기업 박 사장 저택 극 극 삶 가족 예측 가능 만남 시작

167토큰에서 120토큰으로 어느정도 줄여지긴 하지만, 미약한 수준이다.

(코드)
```python
from konlpy.tag import Mecab

mecab = Mecab()

text = "직업도 없이 허름한 반지하에 사는 기택 가족에게 돈을 벌 기회가 찾아온다. 친구의 소개로 부잣집 딸 다혜의 과외 선생님을 맡게 된 기택의 아들."
text += "친구의 소개로 부잣집 딸 다혜의 과외 선생님을 맡게 된 기택의 아들, 기우는 기대감에 부푼 채 글로벌 IT기업을 이끄는 박 사장의 저택에 들어간다."
text += "극과 극의 삶을 사는 두 가족의 예측 불가능한 만남이 시작된다."

summary = mecab.nouns(text)

for s in summary:
    print(s, end=' ')
```

### 문서 요약 api 사용하기
