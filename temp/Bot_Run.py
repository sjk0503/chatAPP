from openai import OpenAI
from datetime import datetime
import time
import json
from bs4 import BeautifulSoup
import json

import Bot_Gen
from Bot_Func import *

client=OpenAI(
    api_key="sk-proj-DcDELsorAoQc7uJ3i8pgT3BlbkFJZITwPNm3ENbXMW24NBt0"
    #api키 github공유 안됨
)




def submit_message(assistant_id,thread, user_message):
    # 사용자 입력 메시지를 스레드에 추가합니다.
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message
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




if __name__=='__main__':
    assistant_id, first_script = Bot_Gen.create_assistant()
    thread = client.beta.threads.create()


    #시작메시지 출력
    print(first_script)



    while(True):
        #대충 20번 대화할때마다 character_info.json 한번씩 훑어서 확인해보기?
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
                print(answer)
            
        else:    
            answer=get_response(thread).data[0].content[0].text.value
            print(answer)#
        
  
