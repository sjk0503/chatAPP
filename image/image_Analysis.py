from io import BytesIO
from openai import OpenAI
import os
import requests
import base64

# Your API key for OpenAI
api_key=os.environ.get('OPENAI_API_KEY')

# Open the image file in binary mode
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        # Read the image file content into a BytesIO stream
       return base64.b64encode(image_file.read()).decode("utf-8")


image_path="" //이미지 위치

base64_image=encode_image(image_path)

headers={
    "Content-Type":"application/json",
    "Authorization":f"Bearer {api_key}"
}

payload={
    "model":"gpt-4o",
    "messages":[
        {
            "role":"user",
            "content":[
                {
                    "type":"text",
                    "text":"이 사진을 한글로 설명해줘."
                },
                {
                    "type":"image_url",
                    "image_url":{
                        "url":f"data:image/png;base64,{base64_image}"
                    }
                }
            ]
        }
    ],
    "max_tokens":300
}

response=requests.post("https://api.openai.com/v1/chat/completions",headers=headers, json=payload)

print(response.json())
