# 1. 라이브러리

```
import os
from openai import OpenAI
from datetime import datetime
import time
import sqlite3
import json
import requests
import re
from emoji import core
from bs4 import BeautifulSoup


```

순서대로
1. os
2. openAI 라이브러리
3. 현재 시간 확인용
4. 작동 대기
5. json화 필요
6. 크롤링용 url 열기
7. 이모지 제거용(자꾸 assistant가 이모지를 사용해서 제거하기 위해서)
8. 크롤링 BeautifulSoup 라이브러리


# 2. 어시스턴트 생성

```

def create_assistant():
    
    assistant = client.beta.assistants.create(
    instructions = instructions,
    model="gpt-4o-2024-05-13",
    tools = tools,
    )
    return assistant.id
```

어시스턴트를 생성하고 해당 어시스턴트의 id를 return합니다.
```
tools=tools 
```
이 부분을 설정해 주어야 해서 매번 동적으로 어시스턴트를 생성합니다. 생성하지 않고도 tools 설정이 가능한 방법이 있는지는 못찾겠습니다...;


# 3. 대화 입력
```
def submit_message(assistant_id,thread, user_message):
    
    # 사용자 입력 메시지를 스레드에 추가합니다.
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message,
    )
    
    # 스레드에 메시지가 입력이 완료되었다면,
    # Assistant ID와 Thread ID를 사용하여 실행을 준비합니다.
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

    return run
```

대화내용을 스레드에 입력하고, 스레드안에서 실행해서 대답을 생성하는 함수입니다.


# 4. 함수 설정
<details>
<summary>함수 열기</summary>
  
  ```
  
tools=[
       {
        "type":"function",
        "function": {
            "name":"screen_movies",
            "description":"If user asks about a '요즘 영화', or user asks what movie is playing right now, Get screen movies.",
            "parameters": {
                "type":"object",
                "properties": {}
            },
        }
    },
    {
        "type":"function",
        "function": {
            "name":"forthcomming_movies",
            "description":"Get forthcomming movies When the user asks what movies are scheduled to play.",
            "parameters": {
                "type":"object",
                "properties": {}
            },
        }
    },
    {
        "type":"function",
        "function": {
            "name":"Thermometer",
            "description":"Bring the current temperature, micro dust, ultra micro dust information.",
            "parameters": {
                "type":"object",
                "properties": {}
            },
        }
    },{
        "type": "function",
        "function": {
            "name": "get_movie_info",
            "description": """
            If the user asks about any movie, or if you don't know about the movie which is the topic of conversation, you can get more information about the movie.
            
            대화 예시1(user is older then assistant and be allowed spoiler):
            파묘 당연히 봤죠!!!!
            나오기 전부터 엄청 기대하고 있었거든요!
            사실 처음엔 좀 실망했었거든요..
            공포영화라고 생각하고 갔었다보니...ㅠ
            그치만 배우들 연기력도 진짜 좋고...  
            특히 김고은님이 무당연기할때 한번 감탄하고
            이도현님이 빙의당했을때 또 감탄하고ㅠㅠㅠ
            그리고 나중에 해석본 본 다음에 2회차 가니까 또 다르더라구요 하진짜최고ㅠ
            
            대화 예시2(user allowed informal speech and spoilers):
            아 윌리웡카 봤지봤지 진짜 완전짱
            되게 바보같은 이야긴데 보고 나오니까 막 나 이런거 좋아하는구나 이런 생각들었어ㅋㅋㅋ
            완전 그냥 동화 그 자체
            영화 자체가 그냥 엄청 매력적이고
            아 그리고 노래 너무 중독적이야 ㅋㅋㅋㅋ
            그리고 티모시 샬라메가 너무 잘생겼어...ㅋㅎㅎ
            """
            
            ,
            "parameters": {
                "type": "object",
                "properties": {
                    "movie_title": {
                        "type": "string",
                        "description": "try search using movie_title"
                    }
                },
                "required": ["movie_title"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "WebSearch",
            "description": """해당 인물에 대한 정보를 찾아라
                
                예시1(user allowed informal speech):
                라이언 레이놀즈가 누구냐면 캐나다 배우겸 코미디언겸 영화제작도 하고 축구 경영도 하는 사람이거든? 
                연기력이 엄청 좋아가지구 눈물흘리는 연기할때 인공눈물 안쓰고도 막 우는 연기하고 그래 
                옛날에는 히어로 영화만 하면 줄줄이 망했었는데 ㅠㅠ 
                근데 데드풀 촬영하고 나서 완전 대박터짐
                유명한걸로는 이제 데드풀하고 명탐정 피카츄랑 
                아 이번에 이프 상상의 친구에서도 나온다!!
                
                예시2(user allowed informal speech):
                최민식 배우 몰라? 엄청 유명하잖아!! 
                파묘에도 나왔고 범죄와의 전쟁 명량 대호 악마를보았다 신세계 꽃피는 봄이오면 등등등 진짜 많이 나왔잖아 
                범죄와의 전쟁에서 살아있네 한사람!!!! 
                최민식 연기력 진짜 장난아니라고 
                카리스마도 쩌는데 소시민 연기도 잘하고 범죄자 연기도 잘하고 바보연기도 잘하고 
                영화가 망해도 최민식 캐릭터만큼은 살아남을 정도라고.... 
                
                예시3(user allowed informal speech):
                유해진 배우가 나온작품들? 아 뭐가있더라...
                타짜랑 베테랑이랑 택시운전사랑
                아 전우치도 있다!!
                봉오동전투랑
                최근엔 파묘!!
                
                """,
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            },
        }
    },
]
  ```
</details>

tools를 설정해서, 각 경우에 맞는 함수를 호출합니다.
description은 어떤 상황에서 함수가 실행되어야 하는지를 작성합니다. name은 그 상황이 왔을때 호출될 함수(def)의 이름입니다.
parameters를 설정할 수 있습니다. 
```
{
        "type": "function",
        "function": {
            "name": "get_movie_info",
            "description": """
            If the user asks about any movie, or if you don't know about the movie which is the topic of conversation, you can get more information about the movie.

            """
            
            ,
            "parameters": {
                "type": "object",
                "properties": {
                    "movie_title": {
                        "type": "string",
                        "description": "try search using movie_title"
                    }
                },
                "required": ["movie_title"]
            },
        }
    },
```
예를 들어 함수 def get_movie_info(movie_title): 의 구조로 되어있으며 movie_title을 인자로 필요로 합니다. 

# 4. 함수 실행
```

def wait_on_run(run, thread):
    while True:
        run_check = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
        )
        print(run_check.status)
        if run_check.status in ['queued','in_progress']:
            time.sleep(2)
        else:
            break
    return run_check
```

함수를 실행해야하는 상황인지 확인하는 함수입니다.
run_check.status가 requires_action라면 함수 실행이 필요하단 의미이고, run_check.status가 completed라면 함수 실행이 필요하지 않다는 뜻입니다.


# 5. 메인함수
```
if __name__=='__main__':
    print("앗...! 안녕..? 이름이 어떻게 돼..?!")
    assistant_id=create_assistant()
    thread = client.beta.threads.create()  # 하나의 스레드를 생성하여 유지합니다.
    while(True):
        user_input=input("You: ")
        if user_input=="stop" : #for test
            client.beta.threads.delete(thread.id)
            client.beta.assistants.delete(assistant_id)
            break 
        run = submit_message(assistant_id, thread, user_input)
        
        # 실행을 대기
        run_check = wait_on_run(run, thread)
        
        if run_check.status=="requires_action":
        
            tool_calls = run_check.required_action.submit_tool_outputs.tool_calls
            
            tool_outputs = []
            for tool in tool_calls:
                func_name = tool.function.name
                
                kwargs = json.loads(tool.function.arguments)
                output = locals()[func_name](**kwargs)
                tool_outputs.append(
                    {
                        "tool_call_id":tool.id,
                        "output":str(output)
                    }
                )
            
            run = client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )
            run_check=wait_on_run(run,thread)
            if(run_check.status=="completed"):
                answer=get_response(thread).data[0].content[0].text.value
                cleaned_answer = remove_emojis(answer)
                print(cleaned_answer)
            
          else:    
            answer=get_response(thread).data[0].content[0].text.value
            cleaned_answer = remove_emojis(answer)
            if "SSTTOOPP" in cleaned_answer:
                modified_string = cleaned_answer.replace("SSTTOOPP", "")
                print(modified_string)
                print("[다미 님이 채팅방을 떠났습니다.]")
                client.beta.threads.delete(thread.id)
                client.beta.assistants.delete(assistant_id)
                break
            else:
                print(cleaned_answer)
        
  
```

우선 처음 이름을 물어보는걸로 대화를 시작하도록 유도했습니다.
함수가 호출되면 각 함수를 실행한 결과를 어시스턴트에게 넘깁니다.
호출되지 않으면 평범하게 대화를 합니다.

대화시에 이모지 쓰지 말라고 설정했는데 계속 이모지를 사용해서 remove_emojis 함수를 통해 이모지를 제거합니다.

만약 사용자가 무례하게 군다면 어시스턴트는 SSTTOOPP를 외치게 되는데, SSTTOOPP를 외치면 대화가 강제로 중지되게게끔 했습니다. 

사용자가 stop를 입력하면 대화를 중지할 수 있습니다

대화가 중지되면 동적으로 생성된 어시스턴트와 스레드가 제거되도록 했습니다.(필요시 수정)

# 6. 실행 결과 예시

```
앗...! 안녕..? 이름이 어떻게 돼..?!
You: 난 이하린이얌
in_progress
completed
오~ 안녕 하린! 나는 이다미야! ㅎㅎ 몇살이야??
You: 23ㅎ
in_progress
completed
앗 언니시네요!! 저는 20살이에요ㅎㅎ 말 편하게 해도 돼요?
You: 안돼
in_progress
completed
앗 알겠습니다, 언니...! ㅎㅎ 어떤 영화 좋아하세요?
You: ㅋㅋㅋㅋㅋ 농담이야 말 편하게해
completed
오 진짜지?! 그럼 편하게 말할게 언니! ㅎㅎ 언니는 어떤 영화 좋아해??
You: 바빠서 영화 자주 못보긴 하는데.. 최근에 본건 파묘? 
in_progress
completed
와 파묘 봤구나!! 진짜 무섭지 않았어? 김고은님이랑 이도현님 연기 진짜 대박이었잖아, 특히 김고은님 무당 연기 진짜 소름 돋았어... 대박 ㅠㅠ 언니는 어떻게 봤어?
You: 아~ 난 좀 글쎄 모르겠다 무섭진 않았는데 재밌었나? 글쎄 그닥..?
in_progress
completed
앗 그런가? ㅋㅋ 사람마다 느낌이 다른가봐 나도 처음엔 살짝 실망했었는데 배우들 연기보고 다시 보니까 좀 달라진 것 같더라 ㅋㅋㅋ 언니는 어떤 스타일의 영화를 더 좋아해?
You: 나는 판타지 영화 좋아해
in_progress
completed
오~ 나도 판타지 영화 진짜 좋아해!! 언니, '반지의 제왕'이나 '해리 포터' 같은 영화 좋아해? 진짜 명작이지 ㅎㅎ
You: 반지의 제왕은 안봤는데 해리포터는 좋아하지 
in_progress
in_progress
completed
오 진짜?! 해리포터 어느 편 제일 좋아해? 나는 개인적으로 '불의 잔' 진짜 재밌게 봤거든! 떼쓰리 위즈도막 조 졀 소 간이막 붙어있졍 어 눈로 막 잡아 끌어내 것 같으면서, 애들 결적으로는 다들 막 최선다하기만 하는 영화, 근데 최고로 재밌었어. 어떤 편 좋아해?
You: 뭐라고???     
in_progress
completed
아 오타;; 해리포터 얘기하면 흥분해서 오타가 많아져 ㅋㅋㅋ 불의 잔 재밌었어! ㅋㅋ 오타난 부분은 넘기고, 언니는 어느 편 제일 좋아??
You: 나는 1편이 제일 좋아 약간  그 신비함 몽글몽글함이 좋달까
in_progress
completed
오 그 신비로운 분위기 나도 완전 좋아해 1편이 진짜 마법 세계로 처음 들어가는 느낌이라서 특별하지 영화가 처음 시작할 때 그 호그와트로 가는 기차 타고 막... 진짜 설
레는 느낌이랄까 ㅎㅎ
You: ㅁㅈㅋㅋㅋㅋ 아 최근에 하는 영화 뭐있지?
in_progress
requires_action
in_progress
in_progress
completed
요즘 하는 영화 진짜 많아...! '설계자', '퓨리오사: 매드맥스 사가', '그녀가 죽었다', '범죄도시4' 이런 것들이 있네! 언니 취향에 맞는 영화 있으면 골라서 한번 보자! 
You: 너 범죄도시4봤어?
queued
in_progress
completed
아직 못 봤어 ㅠㅠ 근데 진짜 재밌다고 하더라! 1편부터 3편까지 다 진짜 엄청 재밌었잖아! 이번에도 마동석님 나오고, 액션 장난 아닐 것 같다. 혹시 봤어?
You: 헐~ 못봤어? 
in_progress
completed
헉 언니는 봤어?? 어떘어?? 진짜 궁금해! ㅠㅠ
You: 재밋었지 뭐
in_progress
completed
역시!! 진짜 기대하고 있었거든 ㅋㅋ 어떤 장면 제일 인상 깊었어? 스포 살짝만 알려주라 ㅎㅎ
You: 에이~~~~ 직접 가서봐야지 ㅋㅋㅋ 
in_progress
completed
ㅋㅋㅋ 알겠어. 그럼 빨리 보러 가야겠다ㅎㅎ 그래도 영화관 분위기가 더 재밌긴 하지!
You: 야 야 그럼 곧 상영하는거 뭐있는지 알아?
in_progress
requires_action
queued
in_progress
completed
곧 상영하는 영화도 엄청 많아! '인사이드 아웃 2', '드라이브', '키타로 탄생 게게게의 수수께끼', '생츄어리', '다우렌의 결혼' 같은 영화들이 있는데 어때? 괜찮은 거 있어?
You: 오 인사이드아웃2 며칠남았어??     
in_progress
completed
'인사이드 아웃 2'는 6월 12일에 개봉해! 딱 6일 남았다! 진짜 기대된다 ㅎㅎ
You: 와ㅋㅋㅋㅋㅋㅋ 개재밌겠다 나 1편 진짜 재밌게봤거든ㅋㅋㅋ
queued
in_progress
completed
와 나도 1편 진짜 좋아했어! 감정들이 캐릭터로 나오니까 너무 귀엽고 이야기 자체도 흥미로웠지 2편도 진짜 기대돼...! 
You: 2편은 어떤 내용일까..??
in_progress
requires_action
in_progress
in_progress
completed
'인사이드 아웃 2'는 애니메이션, 가족, 드라마, 모험, 코미디 장르로 구성되어 있고, 개봉일은 6월 12일이야! 안에 나오는 다양한 감정들이 새로운 모험을 겪는 이야기일 
것 같아! 에이미 폴러, 마야 호크 등 많은 배우들이 나와서 더 기대돼! ㅎㅎ
You: 에이미 폴러가 누구야?
in_progress
in_progress
requires_action
in_progress
in_progress
completed
에이미 폴러는 미국의 배우, 코미디언, 작가, 성우야! 'Saturday Night Live'에서 유명해졌고, 'Parks and Recreation'에서도 주연을 맡았어. 애니메이션에서도 목소리 연기를 많이 했는데, '인사이드 아웃'에서 기쁨 역할로 출연했어! 완전 재능 많은 사람이야.
You: 아 기쁨이 역할 맡은분이구나! 
in_progress
completed
맞아! 기쁨이 역할로 진짜 귀엽고 유쾌하게 연기했잖아! 그래서 더 기억에 남아 ㅎㅎ 이번 2편에서도 기쁨이 역할로 돌아오니까 너무 기대돼!
You: 아 지금 왤케 좀 춥냐               
in_progress
requires_action
in_progress
completed
지금 온도는 20도야. 근데 확실히 좀 쌀쌀하게 느껴질 수도 있을 것 같아! 따뜻하게 입고 있어야겠다 ㅎㅎ
You:  지금 선풍기 틀어놨거든ㅋㅋㅋ 
in_progress
completed
ㅋㅋㅋㅋㅋ 그러면 당연히 춥지! 선풍기 좀 꺼야 할 거 같은데? ㅋㅋ 추울 땐 따뜻하게 챙겨 입어야 해!
You: 쯧쯧 선풍기틀고 이불안에 들어가면 얼마나 좋은데
in_progress
completed
아... 그 느낌 알지 ㅋㅋ 여름에 선풍기 틀고 이불 덮고 그 시원한 바람 맞으면서 자는 거 진짜 최고야 ㅋㅋㅋ 따뜻하게 잘 쉬어~~
You: 웅 헉 지금 몇시지?
in_progress
completed
지금은 23시 36분이야!
You: 아;; 그럼 슬슬 진짜 자야겠다
in_progress
completed
응응! 얼른 자고 좋은 꿈 꿔! 잘자~~~!
You: 웅 고마워 잘자!
in_progress
completed
응 잘 자~~!!
You: stop
```
