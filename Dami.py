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
import json
import os
import pytz

from Dami_generator import create_assistant
from functions import *

client=OpenAI(
    api_key=""
    #api키 github공유 안됨
)


session_times={}

# 다미에게 대화할때마다 시간정보도 함께 알려주기 위해서
def get_time_for_session(assistant_id):
    if assistant_id not in session_times:
        session_times[assistant_id] = datetime.now()
    return session_times[assistant_id]


def submit_message(assistant_id,thread, user_message):
    now = get_time_for_session(assistant_id)
    # 사용자 입력 메시지를 스레드에 추가합니다.
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message+str(now)
    )
    
    # 스레드에 메시지가 입력이 완료되었다면,
    # Assistant ID와 Thread ID를 사용하여 실행을 준비합니다.
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

    return run
    

def get_response(thread):
    # 스레드에서 메시지 목록을 가져옵니다.
    # 메시지를 오름차순으로 정렬할 수 있습니다. order="asc"로 지정합니다.
    return client.beta.threads.messages.list(thread_id=thread.id)


def wait_on_run(run, thread):
    while True:
        run_check = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
        )
        if run_check.status in ['queued','in_progress']:
            time.sleep(2)
        else:
            break
    return run_check



def remove_emojis(text):
    answer=core.replace_emoji(text)
    return answer



if __name__=='__main__':
    assistant_id = create_assistant()
    thread = client.beta.threads.create()

    print("안녕! 이름이 뭐야?")
    # 하나의 스레드를 생성하여 유지합니다.
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
                print(func_name)
                
                kwargs = json.loads(tool.function.arguments)

                print(kwargs)
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
            else:
                print(cleaned_answer)
        
  
