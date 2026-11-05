import os
import json
from tool_definitions import TOOLS
from openai import OpenAI
from tools import call_tool


client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)
def run_agent(task:str,max_iterations:int=5)->str:
    messages=[
        {
            "role":"system",
            "content":"请用简短中文回答。涉及本地文件内容时，先调用工具读取，不要猜测。",
        },
        {
            "role":"user",
            "content":task,
        },
    ]

    for iteration in range(max_iterations):
        print(f"\n第 {iteration + 1} 轮模型请求")

        response=client.chat.completions.create(
            model="deepseek-flash",
            messages=messages,
            tools=TOOLS,
        )

        message=response.choices[0].message
        print(message.content)
        messages.append(message.model_dump(exclude_none=True))

        if not message.tool_calls:
            return message.content or "(模型为返回文本)"

        for tool_call in message.tool_calls:
            name=tool_call.function.name
            arguments=json.loads(tool_call.function.arguments)

            print(f"调用工具：{name}，参数：{arguments}")

            result=call_tool(name,arguments)
            print("工具结果：",result)

            messages.append({
                "role":"tool",
                "tool_call_id":tool_call.id,
                "content":result,
            })
    return f"已达到最大请求轮数 {max_iterations}，任务可能尚未完成。"

# messages=[
#         {
#             "role": "system",
#             "content": "请用简短中文回答。涉及本地文件内容时，先调用工具读取，不要猜测。",
#         },
#         {
#             "role": "user",
#             "content": "请调用工具读取 notes.txt，然后总结文件内容。",
#         },
#     ]
# response=client.chat.completions.create(
#     model="deepseek-flash",
#     messages=messages,
#     tools=TOOLS,
# )
#
# message=response.choices[0].message
#
# if message.tool_calls:
#     messages.append(message.model_dump(exclude_none=True))
#
#     for tool_call in message.tool_calls:
#         name=tool_call.function.name
#         arguments=json.loads(tool_call.function.arguments)
#
#         result = call_tool(name,arguments)
#         print("工具执行结果",result)
#
#         messages.append({
#             "role":"tool",
#             "tool_call_id":tool_call.id,
#             "content":result,
#         })
#
#     final_response=client.chat.completions.create(
#         model="deepseek-flash",
#         messages=messages,
#     )
#     print("模型总结:")
#     print(final_response.choices[0].message.content)
# else:
#     print("模型回复：",message.content)
if __name__ == "__main__":
    result = run_agent(
        "先读取 notes.txt，再读取其中指定的项目详情文件。"
        "根据文件内容生成简短总结，并调用 write_file 保存到 summary.txt。"
        "保存成功后告诉我文件路径。"
    )
    print("\n最终结果：")
    print(result)