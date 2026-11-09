import asyncio
import sys
from pathlib import Path

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

        for tool in tool_list.tools:
            print("工具名称:",tool.name)
            print("工具说明：",tool.description)
            print("参数要求：", tool.input_schema)

        result = await client.call_tool("get_alerts", {"state": "CA"})

        print("调用是否失败：", result.is_error)

        for block in result.content:
            if isinstance(block, TextContent):
                print("工具返回：", block.text)

    for block in result.content:
        if isinstance(block,TextContent):
            print("计算结果：",block.text)

if __name__ == "__main__":
    asyncio.run(main())
