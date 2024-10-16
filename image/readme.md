1. image_generator.py
- 실행 결과: 링크
- 예시: https://oaidalleapiprodscus.blob.core.windows.net/private/org-hPHgS0ydcxTNUqYrGOqCMDnD/user-H4eLkMigXIF4XhhnkXkGx135/img-YZ8mS2Sw8ujjwRb2hTTA1i5r.png?st=2024-10-16T01%3A49%3A09Z&se=2024-10-16T03%3A49%3A09Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-10-15T18%3A24%3A35Z&ske=2024-10-16T18%3A24%3A35Z&sks=b&skv=2024-08-04&sig=zPm4GgA6utUZojMMgnfjoQ9gtEAcOtSD8ky/SQ6F1Hs%3D

2. image_Analysis.py
- 실행 결과: string
- 예시: 사용 이미지:
- ![스크린샷 2024-10-15 221543](https://github.com/user-attachments/assets/2bf2a434-191e-4bef-b771-610dbd303f48)
- 예시: 결과: {'id': 'chatcmpl-AIoQTpFiXGHskPf6Ozr4k0DiTSdcT', 'object': 'chat.completion', 'created': 1729047105, 'model': 'gpt-4o-2024-08-06', 'choices': [{'index': 0, 'message': {'role': 'assistant', 'content': '이 사진은 게임 개발 엔진에서 사용되는 스크립트 설정 화면입니다. \n\n1. **Zombie Script**:\n   - Hp: 100\n   - 걷는 속도: 2\n   - 뛰는 속도: 5\n   - 회전 속도: 10\n   - 걷는 시간: 10\n   - 대기 시간: 5\n   - 실행 시간: 5\n   - 애니메이션, 물리, 충돌체 설정이 포함되어 있습니다.\n   - 소리 설정으로 일반, 다친 소리 등이 포함되어 있습니다.\n   - 웨이포인트(Element 0~3) 설정이 있습니다.\n\n2. **Field Of View Angle Script**:\n   - 시야각: 120도\n   - 시야 거리: 10\n   - 타겟 마스크: 플레이어\n\n3. **Nav Mesh Agent**:\n   - 에이전트 유형: Humanoid\n   - 속도, 각속도, 가속도 등의 조향 및 장애물 회피 설정이 포함되어 있습니다.', 'refusal': None}, 'logprobs': None, 'finish_reason': 'stop'}], 'usage': {'prompt_tokens': 442, 'completion_tokens': 229, 'total_tokens': 671, 'prompt_tokens_details': {'cached_tokens': 0}, 'completion_tokens_details': {'reasoning_tokens': 0}}, 'system_fingerprint': 'fp_a20a4ee344'}
