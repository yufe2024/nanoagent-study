import os
import json
from tool_definitions import TOOLS
from openai import OpenAI

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
    for tool_call in message.tool_calls:
        name=tool_call.function.name
        raw_arguments=tool_call.function.arguments
        arguments=json.loads(raw_arguments)

        print("调用编号：", tool_call.id)
        print("工具名称：", name)
        print("原始参数：", raw_arguments)
        print("解析后的参数：", arguments)
        print("参数类型：", type(arguments))
else:
    print("模型没有调用工具，回复为：", message.content)