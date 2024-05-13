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

# OpenAI API를 사용하기 위한 클라이언트 객체 생성
client = OpenAI(api_key=API_KEY)

# asst_0cxYrVKIqNqn8xfoqOYF05UX
assistant = client.beta.assistants.create(
   name="Math Tutor",
   instructions="You are a personal math tutor. Write and run code to answer math questions.",
   tools=[{"type": "code_interpreter"}],
   model="gpt-4-turbo",
 )
print(assistant) #JSON형태로 출력
```

##### 출력 예
Assistant(id='asst_yWNa4jwdfun1OJmCS4KHGYlx', created_at=1715568546, description=None, instructions='You are a personal math tutor. Write and run code to answer math questions.', metadata={}, model='gpt-4-turbo', name='Math Tutor', object='assistant', tools=[CodeInterpreterTool(type='code_interpreter')], response_format='auto', temperature=1.0, tool_resources=ToolResources(code_interpreter=ToolResourcesCodeInterpreter(file_ids=[]), file_search=None), top_p=1.0)

### Threads란?
스레드는 어시스턴트와 사용자 간의 대화 세션입니다. 스레드는 메시지 기록을 저장하고 모델의 컨텍스트 길이에 비해 대화가 너무 길어지면 이를 잘라 애플리케이션 개발을 단순화합니다.

### Threads
다음으로, 새로운 Thread를 생성하고 그 안에 Message를 추가합니다.
Thread 는 우리 대화의 상태를 유지해 주는 역할을 합니다.
이전 까지의 대화내용을 기억하고 있기 때문에, 매번 전체 메시지 기록을 다시 보내지 않아도 됩니다.

##### 정리
1. Threads: Message 풀을 관리하는 집합체. Message 의 상태 관리도 포함입니다.
2. Message: 단일 메시지 이며, 각 Message 는 역할(role) 과 컨텐츠(content) 로 구성되어 있습니다.
즉, 1개의 Thread 는 여러 개의 순차적으로 연결된 Message 들을 가지고 있습니다. Thread 에 새로운 Message 를 추가할 수 있습니다.

새로운 대화 스레드를 생성해 보겠습니다.

```python
# 새로운 스레드를 생성
thread = client.beta.threads.create()

print(thread)
```
##### 출력 예시
Thread(id='thread_4PeKxu4NS69G5p1OuPwOojUo', created_at=1715568904, metadata={}, object='thread', tool_resources=ToolResources(code_interpreter=None, file_search=None))

다음은 스레드에 메세지를 추가해 보겠습니다.

```python
message = client.beta.threads.messages.create(
  thread_id="thread_Ead7OoHZX3VBKBRA2pYJNmD6", # 스레드 아이디 입력
  role="user",
  content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
)
print(message)
```

##### 출력 예시
Message(id='msg_MkJDG8GmNlrvaDxPDtCFKCeD', assistant_id=None, attachments=[], completed_at=None, content=[TextContentBlock(text=Text(annotations=[], value='I need to solve the equation `3x + 11 = 14`. Can you help me?'), type='text')], created_at=1715569080, incomplete_at=None, incomplete_details=None, metadata={}, object='thread.message', role='user', run_id=None, status=None, thread_id='thread_Ead7OoHZX3VBKBRA2pYJNmD6')

### Run(실행)

![structures](https://github.com/sjk0503/chatAPP/assets/100744515/fbde0cbd-7a5e-4670-af01-ac5b0190935f)

이전에 만든 Assistant와 Thread는 서로 연결되어 있지 않다는 것을 생각해야합니다!

Thread는 Assistant와 독립적으로 존재합니다.

Run 이 수행되기 위해서는 2가지 전제 조건이 존재합니다.
누가(Assistant), 어떤 대화(Thread) 를 실행할 것인가! 입니다.

즉, Run 이 수행되기 위한 조건에는 Assistant ID 와 Thread ID 가 지정되어야 합니다.

```python
run = client.beta.threads.runs.create_and_poll(
  thread_id="thread_Ead7OoHZX3VBKBRA2pYJNmD6", # 스레드 아이디
  assistant_id="asst_0cxYrVKIqNqn8xfoqOYF05UX", # 어시스턴트 아이디

  instructions="Please address the user as Jane Doe. The user has a premium account." # 역할 추가 부여
)
print(run)
```
##### 출력 예시

{'id': 'run_KCb5HKRwoQwXOCO8srw0Ydq8',
 'assistant_id': 'asst_0cxYrVKIqNqn8xfoqOYF05UX',
 'cancelled_at': None,
 'completed_at': None,
 'created_at': 1707908868,
 'expires_at': 1707909468,
 'failed_at': None,
 'file_ids': [],
 'instructions': 'You are a personal math tutor. Answer questions briefly, in a sentence or less.',
 'last_error': None,
 'metadata': {},
 'model': 'gpt-4-turbo-preview',
 'object': 'thread.run',
 'required_action': None,
 'started_at': None,
 'status': 'queued',
 'thread_id': 'thread_Ead7OoHZX3VBKBRA2pYJNmD6',
 'tools': [],
 'usage': None}
