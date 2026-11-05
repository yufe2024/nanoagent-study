import os
import json
from tool_definitions import TOOLS
from openai import OpenAI
from tools import call_tool


client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)
messages=[
        {
            "role": "system",
            "content": "请用简短中文回答。涉及本地文件内容时，先调用工具读取，不要猜测。",
        },
        {
            "role": "user",
            "content": "请调用工具读取 notes.txt，然后总结文件内容。",
        },
    ]
response=client.chat.completions.create(
    model="deepseek-flash",
    messages=messages,
    tools=TOOLS,
)

message=response.choices[0].message

if message.tool_calls:
    messages.append(message.model_dump(exclude_none=True))

    for tool_call in message.tool_calls:
        name=tool_call.function.name
        arguments=json.loads(tool_call.function.arguments)

        result = call_tool(name,arguments)
        print("工具执行结果",result)

        messages.append({
            "role":"tool",
            "tool_call_id":tool_call.id,
            "content":result,
        })

    final_response=client.chat.completions.create(
        model="deepseek-flash",
        messages=messages,
    )
    print("模型总结:")
    print(final_response.choices[0].message.content)
else:
    print("模型回复：",message.content)
