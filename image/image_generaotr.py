from openai import OpenAI
client = OpenAI(api_key="")

response = client.images.generate(
  model="dall-e-3",
  prompt="a happy brown dog, wear glassess and red hat", //생성될 그림 설명
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url

print(image_url) //url 형식으로 반환함. 
