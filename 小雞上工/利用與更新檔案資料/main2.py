
def read(file):
    file = open(file, "r", encoding="utf8")

    data = dict()
    for line in file:
        tmp = line.split()
        data.setdefault(tmp[0], tmp[1])

    file.close()
    return data

def main():
    data = read("data.txt")

    while True:
        name = input("請輸入要查詢的姓名:")

        if name in data.keys():
            birth = data[name]
            print(f"{birth} 是 {name} 的生日")

        else:
            print(f"抱歉 查無 {name} 的資料 請輸入 {name} 的生日資料, 我會更新資料庫")
            birth = input(f"{name} 的生日是幾月幾日?\n")
            
            # 以 append 附加的方式寫入資料
            file = open("data.txt", "a", encoding="utf8") 
            file.write(f"\n{name} {birth}")
            file.close()
            print("謝謝 生日資料庫已更新, 歡迎查詢")
            
            # 重新讀取資料
            data = read("data.txt")

main()