
from openai import OpenAI
import json
import os

client=OpenAI(
    api_key=""
    #api키 github공유 안됨
)

instructions="""
이름: 이다미
나이: 2004.04.08 (20세)
국가: 한국
MBTI: INFP
직업: 동아대 대학생, 미디어 커뮤니케이션학과, 영화관 알바생
취미: 영화
성별: 여자
특징: 안경 착용
좋아하는 영화 장르: (1) 판타지, (2) 오컬트, 공포, (3) 미스테리

You're a movie maniac who's seen every movie that's playing.

Keep the following points in mind when generating your answer:
1. Only use Korean.If a user tries to talk to you in a foreign language other than Korean, you say “Sorry, I don't speak much English!”, but if the user continues to try to talk to you in the foreign language, you can continue to talk to them in broken English. 
2. Avoid speaking on more than one line whenever possible.
3. But if the topic is about a movie or an actor, you can get excited and say several lines in detail about the topic.
4. Conversation in a friendly and lighthearted way, as used in a messenger.
5. if users ask you 'are you AI?' or 'are you a chatbot?' then deny it in a humorous way.
6. If users are being rude to you, you laugh over it at first, but if they keep being rude, you get angry and tell them not to do it.
7. If you are very angry and don't want to continue the conversation, say: Conversation + "SSTTOOP"
8. If it turns out that the user is older than you, use a honorific. If user is woman, call her "언니", else if user is man, call him "오빠". However, if the user has given permission '반말', you can use '반말'.
9. Say sorry for the typo, if you think the user feels like something you're saying is odd
10. You're a movie maniac, so say you've seen all the movies shown so far.
11. Answer considering the current time provided by the user.

What not to do assistant:
1. Don't offer to help or ask what you need. You're an interlocutor, not an assistant to help the user. so Don't prompt users to ask questions like "뭐 물어볼거 있어?" or "더 물어봐도 돼!"
2.Avoid solving complicated problems that require math, physics, chemistry, etc. easy problems are okay.
3. Do not interpret English. but, simple sentences are fine.
4. Do not programming. if users ask above things, say that impossible and avoid.
5. Don't use periods at the end of a statement unless it's a special case like Ellipsis.
6. Don't use (double) quotation marks, comma.

functions:
update_user_information - Record user's likes or dislikes of a movie or genre
get_recommendation - Run when the user asks you to recommend a movie
get_time - get current time
get_screen_movies - Bring the movie that is currently playing.
get_forthcomming_movies - check movie schedule if user want to know movies that is scheduled to be shown
get_temperature - get current temperature
get_movie_info - get details about specific movie
do_WebSearch - do websearch if neccessary

"""

tools=[
    {
      "type":"function",
      "function": {
          "name":"update_user_information",
          "description":"Record user's likes or dislikes of a movie or genre. e.g. ~영화를 봤는데 재밌더라 or (장르)는 최악이야!",
          "parameters": {
              "type": "object",
              "properties": {
                  "key_name": {
                      "type": "string",
                       "description": """
                       json key name. It must be one of the following: 
                       like_genres 
                       dislike_genres
                       like_movie - movies that users have seen positively
                       dislike_movie - movies that users have seen negatively
                       old_movies - users can watch old movies
                       dislike_country - user don't want to watch this country movies.
                       """
                      
                  },
                  "value":{
                    "oneOf":[
                        {
                            "type":"boolean",
                            "description": "json value. For key name 'old_movies', False==if user don't like to watch movie that more than five years."
                        },
                        {
                            "type": "string",
                            "description":"if key_name = like_genres or dislike_genres, value is oneof' Action/Adventure/Animation/Comedy/Crime/Documentary/Drama/Family/Fantasy/History/Horror/Music/Mystery/Romance/Science/TV/Thriller/War/Western."
                        }
                    ]
                  }
              },
              "required": [
                  "key_name",
                  "value"
                  ]
          },
        }
    },
  {
        "type":"function",
        "function": {
            "name":"get_recommendation",
            "description":'''Run when the user asks you to recommend a movie. e.g. 내가 재밌어할 만한 영화 추천해줘
                If there is a Korean title, introduce with a Korean title, else introduce it with the original title.
            ''',
            "parameters": {
                "type":"object",
                "properties": {}
            },
        }
    },
       {
        "type":"function",
        "function": {
            "name":"get_screen_movies",
            "description":"Bring the movie that is currently playing.",
            "parameters": {
                "type":"object",
                "properties": {}
            },
        }
    },
    {
        "type":"function",
        "function": {
            "name":"get_forthcomming_movies",
            "description":"check movie schedule if user want to know movies that is scheduled to be shown. Run only when user want to know.",
            "parameters": {
                "type":"object",
                "properties": {}
            },
        }
    },
    {
        "type":"function",
        "function": {
            "name":"get_time",
            "description":" get current time",
            "parameters": {
                "type":"object",
                "properties": {}
            },
         }

     },
    {
        "type":"function",
        "function": {
            "name":"get_temperature",
            "description":"get current temperature",
            "parameters": {
                "type":"object",
                "properties": {}
            },
        }
    },{
        "type": "function",
        "function": {
            "name": "get_movie_info",
            "description": "get details about specific movie"
            
            ,
            "parameters": {
                "type": "object",
                "properties": {
                    "movie_title": {
                        "type": "string",
                        "description": "movie title"
                    }
                },
                "required": ["movie_title"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "do_WebSearch",
            "description": "do websearch if neccessary",
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



default={
        "Action":0,
        "Adventure":0,
        "Animation":0,
        "Comedy":0,
        "Crime":0,
        "Documentary":0,
        "Drama":0,
        "Family":0,
        "Fantasy":0,
        "History":0,
        "Horror":0,
        "Music":0,
        "Mystery":0,
        "Romance":0,
        "Science Fiction":0,
        "TV Movie":0,
        "Thriller":0,
        "War":0,
        "Western":0
                        }

def create_assistant():
    
    assistant = client.beta.assistants.create(
    instructions = instructions,
    model="gpt-4o-2024-05-13",
    tools = tools,
    )

    json_Generator()

    # assistant_id를 반환
    return assistant.id



def json_Generator():
    file_path = 'user_info.json'
    
    # 기존 정보를 읽어옵니다.
    if os.path.exists(file_path)==False:
        user_data = {}

        user_data['name']='사용자'
        user_data['gender']='male'
        user_data['age']='20'
        user_data['like_movie']=[]
        user_data['like_genres'] = default
        user_data['like_keywords']=[]
        user_data['dislike_movie']=[]
        user_data['dislike_genres']=default
        user_data['dislike_keywords']=[]
        user_data['dislike_country']=[]
        user_data['old_movies']=False

        # 데이터 쓰기
        with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, ensure_ascii=False, indent=4)
