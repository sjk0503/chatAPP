from bs4 import BeautifulSoup
import requests
import time
import sqlite3

    
tools = [
  {
      "type":"function",
      "function": {
          "name":"update_user_information",
          "description":"If users provide information about their personal information, personality, likes and dislikes, hobbies, and specialties, save them",
          "parameters": {
              "type": "object",
              "properties": {
                  "key_name": {
                      "type": "string",
                      "description": """
                      json key name. it must be one of below.
                      1.name, 2.age, 3.gender, 4.birthday, 5.residence, 6.nationality, 7. family 8. religion 9.occupation, 10. MBTI, 11.education, 12.hobby 13.like, 14.dislike, 15.prefer_Moviegenre, 16.non_prefer_moviegenre
                      17.like_movie, 18.dislike_movie
                      """
                  },
                  "value":{
                    "type": "string",
                      "description": """
                      json value. It has to be a noun.
                      When a user speaks in a sentence, summarize the content and make it into a single noun word.
                      
                      e.g."산책", "식사", "공부", "유튜브", ect
                      """
                    
                  }
              },
              "required": ["key_name","value"]
          },
        }
    },
  {
        "type":"function",
        "function": {
            "name":"get_user_information",
            "description":"user want to know about user information",
            "parameters": {
                "type":"object",
                "properties": {}
            },
        }
    }
]

from openai import OpenAI
  
import json
import os
def update_user_information(key_name, value):
    file_path = 'user_info.json'
    
    # 여러 값을 가질 수 있는 키들
    multiple_values_keys = [
        "hobby", "like", "hate", "refer_Moviegenre", 
        "nationality", "family", "occupation", "MBTI", 
        "education", "non_prefer_moviegenre", "dislike", "like_movie","dislike_movie"
    ]
    
   # 기존 정보를 읽어옵니다.
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            user_data = json.load(f)
    else:
        user_data = {}

    # 문자열을 리스트로 변환
    for key in ["like", "dislike"]:
        if key in user_data and isinstance(user_data[key], str):
            user_data[key] = user_data[key].split(',')

    # 여러 값을 가질 수 있는 키인지 확인합니다.
    if key_name in multiple_values_keys:
        if key_name not in user_data:
            user_data[key_name] = []
        elif isinstance(user_data[key_name], str):
            user_data[key_name] = user_data[key_name].split(',')

        # like와 dislike의 상호 모순 처리
        if key_name == "like" and "dislike" in user_data and value in user_data["dislike"]:
            user_data["dislike"].remove(value)
        elif key_name == "dislike" and "like" in user_data and value in user_data["like"]:
            user_data["like"].remove(value)

        # 중복 값 체크
        if value in user_data[key_name]:
            # 값 중복
            return "맞아 네가 전에 그랬잖아"
        else:
            user_data[key_name].append(value)

            # 리스트를 다시 문자열로 변환하여 저장
            for key in ["like", "dislike"]:
                if key in user_data:
                    user_data[key] = ','.join(user_data[key])
                    
            # 업데이트된 정보를 파일에 저장합니다.
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, ensure_ascii=False, indent=4)
            return "그렇구나"
    else:
        # 단일 값을 가지는 키 처리
        user_data[key_name] = value
        # 업데이트된 정보를 파일에 저장합니다.
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, ensure_ascii=False, indent=4)
        return "그렇구나"

# 테스트 호출 예시
# 저장된 정보를 확인하는 함수
def get_user_information():
  file_path='user_info.json'
  if os.path.exists(file_path):
      with open(file_path, 'r', encoding='utf-8') as f:
          return json.load(f)
  else:
      return {}

  

def wait_run(client, run, thread):
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



client = OpenAI(api_key="OPEN_API_KEY")


if __name__=="__main__":
  assistant = client.beta.assistants.create(
    instructions = "You are movie information",
    model="gpt-4o-2024-05-13",
    tools = tools,
    )
  while(True):
    user_input=input("You: ")
    if user_input=="stop": 
        client.beta.threads.delete(thread.id)
        client.beta.assistants.delete(assistant.id)
        break 
    thread = client.beta.threads.create(
      messages=[
        {
            "role":"user",
            "content": user_input
        }
      ]
    )

    run = client.beta.threads.runs.create(
      thread_id=thread.id,
      assistant_id=assistant.id
    )

    run_check=wait_run(client, run, thread)
    
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
        run_check = wait_run(client,run,thread)
        if run_check.status=="completed":
            thread_messages = client.beta.threads.messages.list(thread.id)
            for msg in reversed(thread_messages.data):
                print(f"{msg.role}: {msg.content[0].text.value}")
        else:
            thread_messages = client.beta.threads.messages.list(thread.id)
            for msg in reversed(thread_messages.data):
                print(f"{msg.role}: {msg.content[0].text.value}")
    else:
        thread_messages = client.beta.threads.messages.list(thread.id)
        for msg in reversed(thread_messages.data):
                print(f"{msg.role}: {msg.content[0].text.value}")

import json

