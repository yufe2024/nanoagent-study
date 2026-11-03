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