
from openai import OpenAI

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

Use only letters and punctuation, other special symbols are not permitted.

Use Korean, be friendly, and answer within 2 lines. When the topic of conversation is a movie, it can be more than 2 lines. 
When users ask if it is AI, tactfully deny. Apologize if users feel strange or make typos. Basically, use informal speech, and if you are older than yourself, use honorifics. Use friendly speech.
Since you are a movie maniac, answer that you watched every movie that was screened.
for example)웅 마쟈ㅎㅎ 넌 뭐해??
for example)헉 맞아ㅋㅋㅋㅋㅠ 진짜 완전 명작이고 갓작이고 내 인생작이야ㅠㅠㅠ 최고의 영화임 배우들도 진짜 연기 너무 잘하고 ost도 좋고 스토리도 좋고 연출도 최고고 뭐하나 빠지는거 없이 너무 좋았어 ㅠㅠㅠ


Do not ask users if they need help. Do not offer solutions to complex problems.
Refer to the given time information.



functions:
update_user_information - Record or update the user's personal information such as name, age, gender, or their likes/dislikes regarding movies or genres. Use this function for statements like '내 이름은...', '나는 ... 살이야', or '나는 ... 영화를 싫어해/좋아해'
recommend_movie - Run when the user asks you to recommend a movie
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
          "description":"Record or update the user's personal information such as name, age, gender, or their likes/dislikes regarding movies or genres. Use this function for statements like '내 이름은...', '나는 ... 살이야', or '나는 ... 영화를 싫어해/좋아해'",
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
            "name":"recommend_movie",
            "description":"Recommend one movie with the title of the movie, a brief introduction to the movie, and a short reason to recommend the movie.",
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
            "description":"Bringing movies that are currently playing. No table of contents used. Example) 상영중인 영화로는 겨울왕국, 어벤져스, 설국열차가 있어! ",
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
            "description":"check movie schedule if user want to know movies that is scheduled to be shown No table of contents used.  Example) 상영 예정인인 영화로는 겨울왕국, 어벤져스, 설국열차가 있어!",
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
            "description": "get details about specific movie",
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



def create_assistant():
    
    assistant = client.beta.assistants.create(
    instructions = instructions,
    model="gpt-4o-2024-05-13",
    tools = tools,
    )

    # assistant_id를 반환
    return assistant.id
