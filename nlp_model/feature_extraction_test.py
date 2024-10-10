from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# 코드 실행 전 해야 할것. 

# 1) pip install transformers datasets torch sentencepiece gdown
# 2) gdown --id '1VAq7Dtjmom1HosuE4KkVWPz9IkTmPSw0' -> model.zip
# 3) checkpoint_path  모델 경로 넣어주기

# 1. 저장된 체크포인트에서 모델과 토크나이저 로드
checkpoint_path = "./results/checkpoint-1575"
tokenizer = AutoTokenizer.from_pretrained(checkpoint_path)
model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint_path)

# 2. validation 데이터셋의 첫 번째 항목 가져오기
# first_eval_example = eval_dataset[1]

a =     ["나는 20대 남자입니다. 그쪽은요?",
          "오늘은 집에 있어요. 거북이 한마리 키우는데 집 청소 해줄려고 해요.",
          "오, 저는 어류를 싫어해요.ㅠㅠ 대단하시네요. 집에서 혼자 있어요?",
          "저는 자취하고 있어서 혼자 살아요. ㅎㅎ 거북이 꽤 귀여워요.",
          "혼자서 안심심해요? 저는 혼자 있는것을 못참거든요. ㅎㅎ.",
          "저는 책을 많이 읽어요. 제가 지리학과 부전공 하면서 측량사가 됐거든요. 그래서 지리학과 관련된 서적을 많이 읽어요.",
          "어쩌다보니 제가 재밌게 느껴져서 그런지 자주 읽어요.ㅎㅎ.",
          "대화 재밌네요. ㅎㅎ 전 친구들 만나서 다음에 또 이야기 해요!",
          "네! 저도 재밌었어요. 또 연락해요^^",
]

# 3. 입력 대화 가져오기 (원본 데이터에서)
# input_dialogue = first_eval_example['session_dialog']
# print(type(input_dialogue))
input_dialogue = str(a)
# 4. 입력 대화 토큰화
inputs = tokenizer(input_dialogue, return_tensors="pt", max_length=512, truncation=True)

# 5. 모델에 입력하여 페르소나 추출
output_ids = model.generate(inputs['input_ids'], max_length=128, num_beams=4, early_stopping=True)

# 6. 추출된 페르소나 디코딩
extracted_persona = tokenizer.decode(output_ids[0], skip_special_tokens=True)

# 7. 결과 출력
print("Input Dialogue:", input_dialogue)
print("Extracted Persona:", extracted_persona)
