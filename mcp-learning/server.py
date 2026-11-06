from mcp.server import MCPServer
mcp=MCPServer("learning-server")

@mcp.tool()
def add(a:int,b:int)->int:
    """计算两个整数的和"""
    return a+b

if __name__=='__main__':
    mcp.run(transport="stdio")
