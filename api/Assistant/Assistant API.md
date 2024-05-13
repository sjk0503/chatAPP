## Assistants API 개요
새로운 [Assistants API](https://platform.openai.com/docs/assistants/overview)는 [Chat Completions API](https://platform.openai.com/docs/guides/text-generation/chat-completions-api)를 발전시킨 것으로, 개발자가 어시스턴트와 유사한 경험을 간편하게 만들고 코드 해석기 및 검색과 같은 강력한 도구에 액세스할 수 있도록 하기 위한 것입니다.

### Assistants란?
Assistants는 OpenAI의 모델을 사용 하고 파일에 액세스하고 영구 스레드를 유지하며 도구를 호출할 수 있는 특수 목적 AI를 나타냅니다 .

### Assistants API의 기본 요소

![diagram-assistant](https://github.com/sjk0503/chatAPP/assets/100744515/67c1571d-a763-4c5e-8a32-b7ac8a6fbab8)

- Assistants: 모델(GPT-3.5, GPT-4, etc), instruction(지시문/프롬프트), tools(도구), files(업로드한 파일)를 캡슐화하는 역할입니다.
- Threads: 하나의 대화 채널입니다. 메시지(Message)를 담을 수 있으며, ChatGPT 기준 하나의 대화 스레드의 개념으로 생각하면 됩니다.
- Runs: Assistant + Thread 에서의 실행을 구동합니다. Run 단계에서 tools(도구) 의 활용 여부가 결정되기도 합니다. 또한, Run 을 수행한 후 Assistant 가 응답한 결과를 처리할 때도 사용할 수 있습니다.
위의 요소들이 유기적으로 동작하면서 결국 상태가 있는(stateful) 사용자 경험을 제공하게 됩니다.

## Assistants API

### Playground 에서 Assistants 생성
Assistants를 활용해보기 가장 쉬운 방법은 [Assistants Playground](https://platform.openai.com/playground)를 통하는 것입니다.
![assistant-create](https://github.com/sjk0503/chatAPP/assets/100744515/248ce798-d147-4d9c-a4aa-0cf0d0ccffb4)

### Assistants API로 생성
Assistants API를 통해 직접 Assistants를 생성할 수도 있습니다.

```python
import os
from openai import OpenAI

API_KEY = os.environ['OPENAI_API_KEY']

client = OpenAI(api_key=API_KEY)

# asst_0cxYrVKIqNqn8xfoqOYF05UX
# assistant = client.beta.assistants.create(
#   name="Math Tutor",
#   instructions="You are a personal math tutor. Write and run code to answer math questions.",
#   tools=[{"type": "code_interpreter"}],
#   model="gpt-4-turbo",
# )
# print(assistant) #JSON형태로 출력
```
