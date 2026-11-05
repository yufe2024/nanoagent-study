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
    },
    {
        "type":"function",
        "function":{
            "name":"write_file",
            "description":"将文本写入本地UTF-8文件。文件不存在时创建，同时覆盖原内容",
            "parameters":{
                "type":"object",
                "properties":{
                    "path":{
                        "type":"string",
                        "description":"要写入的文件路径",
                    },
                    "content":{
                        "type":"string",
                        "description":"要保存到文件中的完整文本",
                    }
                },
                "requeried":["path","content"],

            }
        },
    },
]


if __name__ == "__main__":
    import json

    print(json.dumps(TOOLS, ensure_ascii=False, indent=2))