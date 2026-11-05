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
    {
        "type":"function",
        "function":{
            "name":"execute_command",
            #这里加括号的作用是将长串分行写，最后仍得到一个字符串
            "description":(
                "在 Windows 上通过 cmd.exe 执行命令，返回命令输出或错误信息。"
                "工作目录是程序当前工作目录，等待超时为 30 秒。"
                "使用 CMD 命令语法，不要使用 Bash 或 PowerShell 专属语法。"
            ),
            "parameters":{
                "type":"object",
                "properties":{
                    "command":{
                        "type":"string",
                        "description":"要执行的cmd命令例如die/b *.txt",
                    },
                },
                "required":["command"]
            },
        },

    },
]


if __name__ == "__main__":
    import json

    print(json.dumps(TOOLS, ensure_ascii=False, indent=2))