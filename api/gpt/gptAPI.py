import os
from openai import OpenAI
import requests

# google search
Google_SEARCH_ENGINE_ID = os.environ.get("GSE_ID")  # Search Engine ID
Google_API_KEY = os.environ.get("GOOGLE_API_KEY")  # Custom Search Engine API KEY
query = "쿵푸팬더4 개봉일"  # 검색할 쿼리
start_page = "1"  # 검색할 페이지 설정. 한 페이지당 10개 가져올 수 있음

url = f"https://www.googleapis.com/customsearch/v1?key={Google_API_KEY}&cx={Google_SEARCH_ENGINE_ID}&q={query}&start={start_page}"

response = requests.get(url).json()

output = response["items"]

info = ""

for out in output:
    info += out["snippet"]

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

system_message = {
    "role": "system",
    "content": "넌 영화에 대해서 알려주는 도우미야. 추가적으로 제공하는 정보를 바탕으로 알려줘"
}

user_message = {
    "role": "user",
    "content": "쿵푸팬더4 개봉일에 대해서 알려줘 정보: " + info,
}

chat_completion = client.chat.completions.create(
    messages=[
        system_message, user_message
    ],
    model="gpt-4-turbo",
)

print(chat_completion.choices[0].message.content)
