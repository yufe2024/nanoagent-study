import httpx2
from mcp.server import MCPServer

mcp=MCPServer("learning-server")

@mcp.tool()
def add(a:int,b:int)->int:
    """计算两个整数的和"""
    return a+b

@mcp.tool()
async def get_alerts(state : str)->str:
    """查询美国某个州的天气预警。

    Args:
        state: 两位美国州代码，例如 CA、NY。
    """
    state = state.strip().upper()
    url = f"https://api.weather.gov/alerts/active/area/{state}"

    async with httpx2.AsyncClient() as client:
        response = await client.get(
            url,
            headers={
                "User-Agent":"mcp-learning/1.0",
                "Accept":"application/get+json"
            },
            timeout=30.0
        )
        response.raise_for_status()
        data=response.json()

    alerts=data.get("features",[])

    if not alerts:
        return  f"{state} 当前没有生效的天气预警。"

    messages = []

    for alert in alerts[:5]:
        props = alert["properties"]
        messages.append(
            f"事件：{props.get('event', '未知')}\n"
            f"区域：{props.get('areaDesc', '未知')}\n"
            f"级别：{props.get('severity', '未知')}\n"
            f"说明：{props.get('headline', '无')}"
        )

    return "\n\n".join(messages)


if __name__=='__main__':
    mcp.run(transport="stdio")
