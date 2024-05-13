## GPTs의 이해

### GPTs 란?

[GPTs](https://chatgpt.com/gpts)는 챗GPT를 특정 목적에 맞게 커스터마이징한 챗봇입니다.  
이는 기업이나 개인이 자신들의 특정한 요구사항에 맞춰 챗GPT를 조정할 수 있게 해줍니다.  

예를 들어, 특정 언어나 전문성을 이해하고 사용하는 챗봇을 만들 수 있습니다.  

### GPTs 생성 방법

GPTs는 OpenAI에서 제공하는 GPT 빌더 대화창에서 간단한 채팅을 통해 생성할 수 있습니다.  
복잡한 코딩없이 쉬운 접근성으로 다양한 사용자들이 GPTs를 만들고 사용할 수 있습니다.

![GPTs Create](https://github.com/sjk0503/chatAPP/assets/100744515/513834f1-0302-4731-a2dd-a7f9978a63ea)

Create 창에서 빌더와의 대화를 통해 입력하는 내용을 기반으로 커스텀 GPT를 생성합니다.
빌더는 내가 입력한 설명을 기준으로 챗봇을 만들기 때문에 최대한 상세하게 작성해야합니다.

![gpts create 2](https://github.com/sjk0503/chatAPP/assets/100744515/cff7bb36-e878-4959-9a53-b74645a2cf22)

Configure창에서 대표 이미지, 이름(Name), 간단한 소개(Description), 역할 설명(Instructions) 수정할 수 있습니다.  
각 항목에는 내가 입력한 설명이 입력되어 있고, Conversation starters도 수정할 수 있습니다.

![gpts configure](https://github.com/sjk0503/chatAPP/assets/100744515/3c0c1fc5-7d8a-413b-9fc4-7e308814bdd7)

- Knowledge에는 자료를 업로드하여 GPT가 해당 자료를 참고하여 답변을 제공할 수 있습니다.
- Capabilities에는 GPT 자체 기능의 사용 여부를 설정할 수 있습니다.

  - Web Browsing: 실시간으로 인터넷을 검색하여 최신 정보 제공
  - DALL-E Image Generation: DALL-E로 AI 이미지 생성
  - Code Interpreter: 입력한 정보를 파이썬으로 분석하여 답변 제공

## GPTs Action

### GPTs Action이란?

GPTs Action은 간단하게 사용자가 자신의 API를 GPT에 연결하여 외부 데이터를 사용 할수 있게 하는 기능 입니다. 플랫폼 내에서 사용자가 자신의 API를 GPT에 연결하여 외부 데이터에 접근하거나 상호작용할 수 있게 할 수 있도록 하는 역할을 합니다.

### GPTs Action 생성 방법

![gpts action](https://github.com/sjk0503/chatAPP/assets/100744515/177ff416-e178-462f-ab1d-9d4274220723)

##### 인증 방법 선택(Authentication)

- API 접근을 위한 인증 방법을 설정할 수 있습니다.
None(없음), API Key(API 키), OAuth(OAuth 인증) 중에서 선택하여 설정할 수 있습니다.

##### 스키마(Schema)입력

- GPT가 API에 접근을 정의하는 스키마를 입력합니다. (스키마는 OpenAPI 형식을 따릅니다.)

GPTs에서 제공하는 ActionsGPT를 이용하여 스키마를 생성할 수 있습니다.

##### 개인정보 정책 URL 설정

- 사용자가 GPT를 열었을 때 보게되는 개인정보 정책의 URL을 설정할 수 있습니다.

## GPTs 예상 문제점

GPTs 모델로 자체 API를 만들어 Flutter와 같이 사용하는게 가능한가?  
정교한 파인튜닝보다 더 좋은 결과물을 보여줄 수 있는사황  

## 진행 예정 사항

- 예상 문제점 해결방안 찾기
- GPTs에 활용할 정교한 데이터셋과 스키마 만들기
