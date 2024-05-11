# import os
# from openai import OpenAI
# import requests
#
# # google search
# Google_SEARCH_ENGINE_ID = os.environ.get("GSE_ID")  # Search Engine ID
# Google_API_KEY = os.environ.get("GOOGLE_API_KEY")  # Custom Search Engine API KEY
# query = "쿵푸팬더4 개봉일"  # 검색할 쿼리
# start_page = "1"  # 검색할 페이지 설정. 한 페이지당 10개 가져올 수 있음
#
# url = f"https://www.googleapis.com/customsearch/v1?key={Google_API_KEY}&cx={Google_SEARCH_ENGINE_ID}&q={query}&start={start_page}"
#
# response = requests.get(url).json()
#
# output = response["items"]
#
# info = ""
#
# for out in output:
#     info += out["snippet"]
#
# client = OpenAI(
#     # This is the default and can be omitted
#     api_key=os.environ.get("OPENAI_API_KEY"),
# )
#
# system_message = {
#     "role": "system",
#     "content": "넌 영화에 대해서 알려주는 도우미야. 추가적으로 제공하는 정보를 바탕으로 알려줘"
# }
#
# user_message = {
#     "role": "user",
#     "content": "쿵푸팬더4 개봉일에 대해서 알려줘 정보: " + info,
# }
#
# chat_completion = client.chat.completions.create(
#     messages=[
#         system_message, user_message
#     ],
#     model="gpt-4-turbo",
# )
#
# print(chat_completion.choices[0].message.content)


import os
from openai import OpenAI
from konlpy.tag import Mecab

mecab = Mecab()
max_messages = 10  # 최대 메시지 수


# 문장에서 명사만 추출함
def summary_text(text):
    summary = mecab.nouns(text)
    output = ""
    for s in summary:
        output += s + " "
    return output


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

messages = [
    {
        "role": "system",
        "content": "너는 영화 도우미야"
    }
]

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

    # 메시지 리스트 전송하고 결과 받기
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-3.5-turbo"
    )

    # 메시지를 요약하고 다시 추가함
    messages.pop()

    user_message = {
        "role": "user",
        "content": summary_text(user_input)
    }
    # 요약한 내용 추가
    messages.append(user_message)

    # 모델의 응답 출력
    assistant_response = chat_completion.choices[0].message.content
    print("gpt\n", assistant_response)
    print()

    # 모델의 응답을 메시지 리스트에 추가
    assistant_message = {
        "role": "assistant",
        "content": summary_text(assistant_response)
    }
    messages.append(assistant_message)

    print(len(messages))

