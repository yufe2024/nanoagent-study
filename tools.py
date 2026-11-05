import subprocess


def read_file(path:str)->str:
    try:
        with open(path,"r",encoding="utf-8")as file:
            return file.read()
    except(OSError,UnicodeError)as e:
        return f"Error reading file:{e}"

def write_file(path:str,content:str)->str:
    try:
        with open(path,"w",encoding="utf-8")as file:
            file.write(content)
        return f"Successfully wrote to{path}"
    except(OSError,UnicodeError) as e:
        return f"Error writing file:{e}"

#执行命令
def execute_command(command:str)->str:
    try:
        result =subprocess.run(
            command,
            shell=True,#交给系统的解释器
            capture_output=True,#收集输出
            text=True,#解码为字符串
            errors="replace",#遇到无法解码的就替换，避免解码报错
            timeout=30,
        )

        output=result.stdout + result.stderr

        if result.returncode!=0:
            return f"Command failed (exit code {result.returncode}):\n{output}"

        return output if output else "(Command executed with no output)"
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds."
    except OSError as e:
        return f"Error executing command: {e}"



FUNCTIONS={
    "read_file":read_file,
    "write_file":write_file,
    "execute_command": execute_command,
}



def call_tool(name:str,arguments:dict)->str:
    function = FUNCTIONS.get(name)

    if function is None:
        return f"Error: Unknown tool '{name}'"

    return function(**arguments)




#只有作为main调用是才会执行，其他导入时不执行，这个__的作用
if __name__=="__main__":
    print("测试一：读取现有文件")
    print(read_file("notes.txt"))

    print("测试二：读取不存在的文件")
    print(read_file("not_exist.txt"))

    print("测试三，写入文件")
    result=write_file("output.txt","你好，这是写入测试")
    print(result)

    print("读回检查:")
    print(read_file("output.txt"))

    print("测试四：覆盖已有内容")
    print(write_file("output.txt", "这是覆盖后的内容。"))
    print(read_file("output.txt"))

    print("测试五：父文件夹不存在")
    print(write_file("missing_folder/output.txt", "测试"))

    print("测试六：执行正常命令")
    print(execute_command("echo Hello Agent"))

    print("测试七：列出当前目录")
    print(execute_command("dir /b"))

    print("测试八：执行不存在的命令")
    print(execute_command("this_command_does_not_exist_123"))

    #print("测试九：验证超时")
    #print(execute_command('powershell.exe -NoProfile -Command "Start-Sleep -Seconds 35"'))

    print("测试十：通过名称调用读取工具")
    name = "read_file"
    arguments = {"path": "notes.txt"}
    print(call_tool(name, arguments))

    print("测试十一：调用不存在的工具")
    print(call_tool("unknown_tool", {}))