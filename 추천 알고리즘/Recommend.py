from bs4 import BeautifulSoup
import requests
import time
import sqlite3

    
tools = [
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
    },{
        "type":"function",
        "function": {
            "name":"recommandtion",
            "description":"""사용자에게 사용자 맞춤형 영화를 최대 3개 추천해줍니다.
            
            출력예시1: 
            평점 좀 괜찮은 영화라면... 
            A라는 영화는 어때? a' 장르의 영화야! B라는 영화도 괜찮거든? 이건 b'장르야. C도 괜찮아! 이건 c' 장르야. 
            
            출력 예시2:
            A라는 영화 재밌는데 어떄? 대충 ~~ 하는 내용이야! 
            아니면 B도 괜찮아! 이건 ~~ 하는 영화거든? 평점도 좋다?
            아니면 C도 재밌어! 니 취향에 맞을것같아!
            
            잘못된 출력 예시1:
            1. A 어때? 2. B 어때? 3.C 어때?
            
            잘못된 출력 예시2:
            -**A** -**B** -**C**
            
            """,
            "parameters": {
                "type":"object",
                "properties": {}
            },
        }
    },
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
    


# 테스트 호출 예시
# 저장된 정보를 확인하는 함수
def get_user_information():
  file_path='user_info.json'
  if os.path.exists(file_path):
      with open(file_path, 'r', encoding='utf-8') as f:
          return json.load(f)
  else:
      return {}

  
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_movie_data(file_path):
    df = pd.read_csv(file_path)
    return df

def preprocess_data(df):
    # Combine genres and keywords into a single string for each movie
    df['combined_features'] = df['genres'].fillna('') + ' ' + df['keywords'].fillna('')
    return df

def get_user_profile(user_likes, movie_data):
    # Combine features of liked movies into a single string
    user_profile = ' '.join(movie_data[movie_data['original_title'].isin(user_likes)]['combined_features'])
    return user_profile

def recommend_movies(user_profile, movie_data, top_n=10):
    # Vectorize the movie data and user profile
    count_vectorizer = CountVectorizer()
    
    # Combine the user profile and movie data for vectorization
    combined_features = movie_data['combined_features'].tolist() + [user_profile]
    count_matrix = count_vectorizer.fit_transform(combined_features)
    
    # Compute the cosine similarity matrix
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    
    # Get the similarity scores for the user profile (last row in cosine_sim)
    user_sim_scores = cosine_sim[-1][:-1]
    
    # Get top N similar movies
    top_indices = user_sim_scores.argsort()[-top_n:][::-1]
    recommendations = movie_data.iloc[top_indices]
    
    return recommendations

def recommandtion():
    # Load movie data
    movie_file_path = 'filtered_movies.csv'
    movie_data = load_movie_data(movie_file_path)
    
    # Preprocess movie data
    movie_data = preprocess_data(movie_data)
    
    # User information
    user_info =get_user_information()
    
    
    # Get user profile
    user_profile = get_user_profile(user_info['like_movie'], movie_data)
    
    # Recommend movies
    recommendations = recommend_movies(user_profile, movie_data)
    
    # Print recommendations

    return recommendations[['korean_title', 'genres', 'vote_average']]


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

