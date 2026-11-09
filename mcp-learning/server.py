import httpx2
from mcp.server import MCPServer

mcp=MCPServer("learning-server")

async def request_weather(url:str)->dict:
    """请求天气接口并返回解析后的 JSON 数据。"""
    async with httpx2.AsyncClient() as client:
        response = await client.get(
            url,
            headers={
                "User-agent":"mcp-learning/1.0",
                "Accept":"application/geo+json"
            },
            timeout=30.0
        )
        response.raise_for_status()
        return response.json()

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

    data = await request_weather(url)

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


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """根据经纬度查询美国境内地点的天气预报。

    Args:
        latitude: 纬度，例如 38.8977。
        longitude: 经度，例如 -77.0365。
    """
    if not -90 <= latitude <= 90:
        raise ValueError("纬度必须在 -90 到 90 之间")

    if not -180 <= longitude <= 180:
        raise ValueError("经度必须在 -180 到 180 之间")

    # 第一次请求：获取这个地点的天气预报地址
    points_url = (
        f"https://api.weather.gov/points/{latitude},{longitude}"
    )
    points_data = await request_weather(points_url)

    forecast_url = points_data["properties"]["forecast"]

    # 第二次请求：获取具体预报
    forecast_data = await request_weather(forecast_url)

    periods = forecast_data["properties"]["periods"]
    messages = []

    for period in periods[:5]:
        messages.append(
            f"时段：{period['name']}\n"
            f"温度：{period['temperature']}°"
            f"{period['temperatureUnit']}\n"
            f"风：{period['windSpeed']} "
            f"{period['windDirection']}\n"
            f"预报：{period['detailedForecast']}"
        )

    return "\n\n".join(messages)





if __name__=='__main__':
    mcp.run(transport="stdio")
