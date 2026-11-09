import asyncio
import json
import os
import sys
from pathlib import Path

from openai import AsyncOpenAI
from mcp import Client, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp_types import TextContent


async def main():
    # 找到同目录下的服务器文件
    server_path = Path(__file__).resolve().with_name("server.py")

    # 配置服务器启动命令
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(server_path)],
    )

    # 启动 MCP 服务器并建立连接
    async with Client(stdio_client(params)) as client:
        # 获取服务器提供的工具
        tool_list = await client.list_tools()

        # 转换成模型接受的工具定义
        model_tools = []

        for tool in tool_list.tools:
            model_tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description or "",
                    "parameters": tool.input_schema,
                },
            })

        print("已连接，工具列表：")
        for tool in tool_list.tools:
            print("-", tool.name)

        # 创建 DeepSeek API 客户端
        async with AsyncOpenAI(
            api_key=os.environ["DEEPSEEK_API_KEY"],
            base_url="https://api.deepseek.com",
        ) as model_client:
            messages = [
                {
                    "role": "system",
                    "content": (
                        "你是一个助手，计算加法时请使用提供的工具。"
                        "根据工具实际返回的结果回答，调用失败时如实说明。"
                    ),
                },
                {
                    "role": "user",
                    "content": "请使用工具计算 12 加 30。",
                },
            ]

            # 最多请求模型 5 轮
            for round_number in range(1, 6):
                print(f"\n第 {round_number} 轮模型请求")

                response = await model_client.chat.completions.create(
                    model="deepseek-flash",
                    messages=messages,
                    tools=model_tools,
                    extra_body={"thinking": {"type": "disabled"}},
                )

                message = response.choices[0].message

                # 模型没有请求工具，输出回答并结束
                if not message.tool_calls:
                    print("最终回答：", message.content)
                    break

                # 保存模型的工具调用请求
                messages.append(
                    message.model_dump(
                        mode="json",
                        exclude_none=True,
                    )
                )

                # 执行这一轮的所有工具调用
                for call in message.tool_calls:
                    tool_name = call.function.name
                    arguments = json.loads(call.function.arguments)

                    print("调用工具：", tool_name)
                    print("工具参数：", arguments)

                    result = await client.call_tool(
                        tool_name,
                        arguments,
                    )

                    # 提取工具返回的文本
                    text_parts = []

                    for block in result.content:
                        if isinstance(block, TextContent):
                            text_parts.append(block.text)

                    tool_text = "\n".join(text_parts)

                    print("调用是否失败：", result.is_error)
                    print("工具结果：", tool_text)

                    # 把工具结果加入对话，供下一轮模型读取
                    messages.append({
                        "role": "tool",
                        "tool_call_id": call.id,
                        "content": json.dumps(
                            {
                                "is_error": result.is_error,
                                "result": tool_text,
                            },
                            ensure_ascii=False,
                        ),
                    })
            else:
                print("已达到 5 轮请求上限，停止执行。")


if __name__ == "__main__":
    asyncio.run(main())