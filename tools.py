def read_file(path:str)->str:
    try:
        with open(path,"r",encoding="utf-8")as file:
            return file.read()
    except(OSError,UnicodeError)as e:
        return f"Error reading file:{e}"

if __name__=="__main__":
    print("测试一：读取现有文件")
    print(read_file("notes.txt"))

    print("测试二：读取不存在的文件")
    print(read_file("not_exist.txt"))