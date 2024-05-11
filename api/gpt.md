# GPT API

## GPT API Flow Chart
![flow chart](./flowChart/gptAPI.png)

## api 핵심
1. gpt 3.5와 gpt 4.0을 함께 사용
2. gpt 4.0의 검색 기능을 활용하여 최신 정보 확보

## gpt api 사용하기 - python
1. openAI에서 api key 발급
2. openAI 라이브러리 설치
3. api key는 환경변수로 처리
   
(사용예시)
```python
import os
from openai import OpenAI

client = OpenAI(
    # api key를 환경 변수로 설정
    api_key=os.environ.get("OPENAI_API_KEY"),
)

system_message = {
    "role": "system",
    "content": "넌 영화에 대해서 알려주는 도우미야."
}

user_message = {
    "role": "user",
    # 요청하는 정보
    "content": "영화 기생충에 대해서 알려줘"
}

chat_completion = client.chat.completions.create(
    messages=[
        system_message, user_message
    ],
    model="gpt-3.5-turbo",
)

print(chat_completion.choices[0].message.content)
```
(출력결과)
> "기생충"은 2019년 개봉한 대한민국의 영화로, 봉준호 감독이 연출하고 각본을 썼습니다. 이 영화는 한 가족이 빈곤한 가정의 다른 가족들을 기생충처럼 이용하면서 벌어지는 이야기를 다룹니다.
> 봉준호 감독의 유쾌하고 예리한 플롯 전개, 캐릭터의 복잡한 심리 묘사, 사회 비판적 요소 등이 매우 높은 평가를 받았으며, 수많은 시상식에서 수상을 기록하며 한국 영화 역사상 최고의 작품 중 하나로 꼽힙니다.
> "기생충"은 스릴러와 블랙 코미디의 요소를 혼합하여 관객들에게 긴장감과 웃음을 한꺼번에 선사하는 작품이라고 할 수 있습니다. 또한 사회적인 메시지와 섬세한 캐릭터들의 묘사로 많은 이들의 관심을 끌었습니다.
