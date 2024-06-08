from openai import OpenAI
import time
import json
from emoji import core
import requests
import datetime


client=OpenAI(
    api_key=""
    #api키 github공유 안됨
)

Google_SEARCH_ENGINE_ID="063384971a7b946ac"
Google_API_KEY=" AIzaSyDLftoBTzRrELTssUKamWyGTo4Ntvuo9Bo"
ASSISTANT_ID=""
THREAD_ID=""


#스레드에 대화 입력하는 함수
def submit_message(assistant_id,thread, user_message):
    
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message,
    )
    

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

    return run


#대화분석 실행대기
def wait_on_run(run, thread_id):
    while True:
        run_check = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run.id
        )
        print(run_check.status)
        if run_check.status in ['queued','in_progress']:
            time.sleep(2)
        else:
            break
    return run_check


# 어시스턴트 답변 가져오기
def get_response(thread_id):
    return client.beta.threads.messages.list(thread_id)

# 이모지 삭제
def remove_emojis(text):
    answer=core.replace_emoji(text)
    return answer



##======================함수==============
    
# 시간 체크용
def timer():
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")
    return current_date, current_time


# 검색함수
def WebSearch(query):
    current_date, current_time=timer()
    api_key = Google_API_KEY  # 여기에 실제 API 키를 넣으세요
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx":Google_SEARCH_ENGINE_ID,
        "q": query,
        "lowRange":0,
        "highRange":20
    }
    response = requests.get(search_url, params=params)
    results = response.json()

    return current_date, current_time,results


##======================main
if __name__=='__main__':
    print("앗...! 안녕..? 이름이 어떻게 돼..?!")
    while(True):
        user_input=input("You: ")
        if user_input=="stop" : #for test
            client.beta.threads.delete(THREAD_ID)
            client.beta.assistants.delete(ASSISTANT_ID)
            break 
        run = submit_message(ASSISTANT_ID, THREAD_ID, user_input)
        
        # 실행을 대기
        run_check = wait_on_run(run, THREAD_ID)
        
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
                thread_id=THREAD_ID,
                run_id=run.id,
                tool_outputs=tool_outputs
            )
            run_check=wait_on_run(run,THREAD_ID)
            if(run_check.status=="completed"):
                answer=get_response(THREAD_ID).data[0].content[0].text.value
                cleaned_answer = remove_emojis(answer)
                print(cleaned_answer)
            
        else:    
            answer=get_response(THREAD_ID).data[0].content[0].text.value
            cleaned_answer = remove_emojis(answer)
            if "SSTTOOPP" in cleaned_answer:
                modified_string = cleaned_answer.replace("SSTTOOPP", "")
                print(modified_string)
                print("[다미 님이 채팅방을 떠났습니다.]")
                client.beta.threads.delete(THREAD_ID)
                client.beta.assistants.delete(ASSISTANT_ID)
                break
            else:
                print(cleaned_answer)
