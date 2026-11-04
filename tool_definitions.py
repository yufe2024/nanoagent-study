TOOLS=[
    {
        #类型是函数
        "type":"function",
        "function":{
            "name":"read_file",
            "description":"读取本地UTF-8文本文件，返回文件的完整内容",
            "parameters":{
                #所需参数格式是object
                "type":"object",
                "properties":{
                    "path":{
                        "type":"string",
                        "description":"文件路径，基于程序当前工作目录。",
                    }
                },
            "required":["path"],
            },
        },
    }
]


if __name__ == "__main__":
    import json

    print(json.dumps(TOOLS, ensure_ascii=False, indent=2))