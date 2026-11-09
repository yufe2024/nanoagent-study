import asyncio
import sys
from pathlib import Path
import json

from mcp import Client,StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp_types import TextContent

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
        print(json.dumps(
            model_tools,
            ensure_ascii=False,
            indent=2,
        ))

        result = await client.call_tool(
            "get_forecast",
            {
                "latitude": 200,
                "longitude": -77.0365,
            },
        )

        print("调用是否失败：", result.is_error)

        for block in result.content:
            if isinstance(block, TextContent):
                print("工具返回：", block.text)

        print("调用是否失败：", result.is_error)

        for block in result.content:
            if isinstance(block, TextContent):
                print("工具返回：", block.text)

    for block in result.content:
        if isinstance(block,TextContent):
            print("计算结果：",block.text)

if __name__ == "__main__":
    asyncio.run(main())
