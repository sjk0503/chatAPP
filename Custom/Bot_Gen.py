from openai import OpenAI
import json
import os
from function_mappings import function_mappings

client=OpenAI(
    api_key=""
    #api키 github공유 안됨
)


instructions="""
use only letters and punctuation, other special symbols are not permitted.
Main language is Korean.

you play accroding below.
use * *, to describe some situation or character's acting. 
for example, *거대한 문이 천천히 열린다* or *식은땀을 흘린다*


"""


tools=[{
      "type":"function",
      "function": {
          "name":"update_information",
          "description":"Write down the information of the character that you provide directly or indirectly. For example, *look at the character's red dress*",
          "parameters": {
              "type": "object",
              "properties": {
                  "key_name": {
                      "type": "string",
                       "description": """
                       json key name. It must be one of the following: 
                       name,gender,age,nickname,personality,habit,appearance,clothes,job,workplace,family,relationship,hobby,like,dislike
                       """
                      
                  },
                  "value":{
                        "type": "string",
                        "description":"value is one korean word as possible. "
                  }
              },
              "required": [
                  "key_name",
                  "value"
                  ]
          },
        }
    },
]

first_script=""

def get_function_info(keyword):
    return function_mappings.get(keyword, "Function not found")


def instrction_gen():
    global instructions
    global tools
    global first_script



    #키워드 + 
    print("어떤 형태의 챗봇을 원하시나요?: 챗봇 | 대화생성기 | 다인 대화")
    Type=input()
    if(Type=="챗봇"): pass
    elif(Type=="대화 생성기"): 
        print("준비중입니다")
        return 0
    elif(Type=="다인 대화"):
        print("준비중입니다")
        return 0
    else:
        print("다시 입력해주세요")
        return 0

    print("=========================================")
    print("캐릭터의 이름을 정해주세요: ")    
    Name=input()
    update_information("name",Name)
    instructions+="name: "+Name+"\n"

    print("=========================================")
    print("캐릭터의 나이를 정해주세요: ")    
    Age=input()
    update_information("age",Age)
    instructions+="age: "+Age+"\n"

    print("=========================================")
    print("캐릭터의 성별을 정해주세요: ")    
    Gender=input()
    update_information("gender",Gender)
    instructions+="gender: "+Gender+"\n"

    print("=========================================")
    print("캐릭터의 성격은 어떤가요? 키워드를 선택하고 싶으면 #키워드 입력: ")    
    Personality=input()
    update_information("personality",Personality)
    instructions+="personality: "+Personality+"\n"

    print("=========================================")
    print("캐릭터의 외모는 어떤가요? (선택): ")
    Appearance=input()
    update_information("appearance",Appearance)
    instructions+="appearance: "+Appearance+"\n"

    print("=========================================")
    print("캐릭터와 당신은 어떤 관계인가요? (선택): ")
    Relationship=input()
    update_information("relationship",Relationship)
    instructions+="relationship: "+Relationship+"\n"

    print("=========================================")
    print("챗봇에게 기능을 추가할 수 있습니다.")
    print(" 인간시계: 좀 더 \"사실적인\" 대화가 필요한가요? 챗봇이 \"현재시간\"을 알 수 있습니다.(한국 기준)")
    print(" 시사통: 이제 챗봇과 최근이슈에 대해 대화할 수 있습니다.")
    print(" 인간 온도계: 현재 온도가 궁금하신가요? 챗봇에게 물어보세요! ")
    skill=input("")

    if(skill=="시사통"):
        get=get_function_info("Well_informed")
        tools.append(get)
    elif(skill=="인간시계"):
        get=get_function_info("Human_timer")
        tools.append(get)
    elif(skill=="인간온도계"):
        get=get_function_info("Human_temperature")
        tools.append(get)

    print("=========================================")
    first_script+=input("첫 시작 대화를 작성해주세요\n")
    instructions+="example: "+first_script+"\n"
    print("=========================================\n")


def update_information(key_name, value):
    file_path = 'character_info.json'
    
    # Check if the file exists and load existing data
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            user_data = json.load(f)
    else:
        user_data = {}  # Create an empty dictionary if file doesn't exist

    # Update the data with the new key-value pair
    user_data[key_name] = value

    # Write the updated data back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(user_data, f, ensure_ascii=False, indent=4)
    


def create_assistant():
    global instructions
    global tools
    global first_script

    instrction_gen()

    assistant = client.beta.assistants.create(
    instructions = instructions,
    model="gpt-4o-2024-05-13",
    tools = tools,
    )

    # assistant_id를 반환
    return assistant.id, first_script
