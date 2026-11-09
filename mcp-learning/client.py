import asyncio
import sys
import os
import json

from pathlib import Path
from mcp import Client,StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import AsyncOpenAI

async def main():

    #算路径
    server_path=Path(__file__).resolve().with_name("server.py")
    params=StdioServerParameters(
        command=sys.executable,
        args=[str(server_path)],
    )
    #异步
    async with Client(stdio_client(params)) as client:
        tool_list=await client.list_tools()

        model_tools=[]

        for tool in tool_list.tools:
            model_tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description or "",
                    "parameters": tool.input_schema,
                },
            })

        async with AsyncOpenAI(
            api_key=os.environ["DEEPSEEK_API_KEY"],
            base_url="https://api.deepseek.com",
        ) as model_client:

            response=await model_client.chat.completions.create(
                model="deepseek-flash",
                messages=[
                    {
                        "role":"system",
                        "content":"你是一个助手，计算加法时请使用提供的工具。"
                    },
                    {
                        "role":"user",
                        "content":"请使用工具计算12加30"
                    },
            ],
            tools=model_tools,
                extra_body={"thinking":{"type":"disabled"}},
            )

        message = response.choices[0].message

        print("模型文字：", message.content)

        if message.tool_calls:
            for call in message.tool_calls:
                print("调用编号：", call.id)
                print("工具名称：", call.function.name)

                arguments = json.loads(call.function.arguments)
                print("工具参数：", arguments)
        else:
            print("模型没有请求调用工具。")
if __name__ == "__main__":
    asyncio.run(main())
