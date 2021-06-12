from tkinter import *

HEIGHT = 30 ; WIDTH = 30
FILE_NAME = "data.txt"

class dataBase:
    def __init__(self, data):
        self.list = dict()
        for key, value in data.items():
            self.add(key, value['姓名'], value['性別'], value['系所'], value['地址'], value['電話'])

    def add(self, number, name, sex, department, address, phoneNumber):
        if number not in self.list:
            self.list[number] = {
                '姓名': name, 
                '性別': sex, 
                '系所': department, 
                '地址': address, 
                '電話': phoneNumber
            }
        else:
            print(f"學號：{number} 資料已存在")

    def update(self, number, name=None, sex=None, department=None, address=None, phoneNumber=None):
        if number in self.list:
            self.list[number]['姓名'] = name if name != None else self.list[number]['姓名']
            self.list[number]['性別'] = sex if sex != None else self.list[number]['性別']
            self.list[number]['系所'] = department if department != None else self.list[number]['系所']
            self.list[number]['地址'] = address if address != None else self.list[number]['地址']
            self.list[number]['電話'] = phoneNumber if phoneNumber != None else self.list[number]['電話']
        elif all([name, sex, department, address, phoneNumber]):
                self.add(number, name, sex, department, address, phoneNumber)

    def delete(self, number):
        if number in self.list:
            self.list.pop(number)
        else:
            print(f"學號：{number} 資料不存在")

    def getData(self, number=None):
        if number == None:
            return self.list
        else:
            if number in self.list:
                return self.list[number]
            else:
                print(f"學號：{number} 資料不存在")


def readFile(fileName): # 回傳 dict, key為學號
    f = open(fileName, "r", encoding="utf8")
    data = {}
    for i in f:
        header = ['姓名', '性別', '系所', '地址', '電話']
        data[i.split()[0]] = dict(zip(header, i.split()[1:]))
    f.close()
    return data


v = None
def main():
    root = Tk()
    root.title("資料表單加強版")
    pixel = PhotoImage(height=1, width=1)
    global v ; v = {
        '學號': StringVar(),
        '姓名': StringVar(),
        '性別': StringVar(),
        '系所': StringVar(),
        '地址': StringVar(),
        '電話': StringVar()
    }
    
    database = dataBase(readFile(FILE_NAME))
    read(database, False)

    row = 0 ; col = 1 ; rowspan = 1 ; colspan = 2
    Label(root, text="學號", height=HEIGHT*rowspan, width=WIDTH*colspan, image=pixel, compound="c").grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)
    row = row ; col += colspan ; rowspan = 1 ; colspan = 4
    Entry(root, textvariable=v['學號']).grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)

    row += rowspan ; col = 1 ; rowspan = 1 ; colspan = 2
    Label(root, text="姓名", height=HEIGHT*rowspan, width=WIDTH*colspan, image=pixel, compound="c").grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)
    row = row ; col += colspan ; rowspan = 1 ; colspan = 4
    Entry(root, textvariable=v['姓名']).grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)

    row += rowspan ; col = 1 ; rowspan = 1 ; colspan = 2
    Label(root, text="性別", height=HEIGHT*rowspan, width=WIDTH*colspan, image=pixel, compound="c").grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)
    row = row ; col += colspan ; rowspan = 1 ; colspan = 2
    Radiobutton(root, text="男", variable=v['性別'], value="男").grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)
    row = row ; col += colspan ; rowspan = 1 ; colspan = 2
    Radiobutton(root, text="女", variable=v['性別'], value="女").grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)

    row += rowspan ; col = 1 ; rowspan = 1 ; colspan = 2
    Label(root, text="系所", height=HEIGHT*rowspan, width=WIDTH*colspan, image=pixel, compound="c").grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)
    row = row ; col += colspan ; rowspan = 1 ; colspan = 4
    Entry(root, textvariable=v['系所']).grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)

    row += rowspan ; col = 1 ; rowspan = 1 ; colspan = 2
    Label(root, text="地址", height=HEIGHT*rowspan, width=WIDTH*colspan, image=pixel, compound="c").grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)
    row = row ; col += colspan ; rowspan = 1 ; colspan = 4
    Entry(root, textvariable=v['地址']).grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)

    row += rowspan ; col = 1 ; rowspan = 1 ; colspan = 2
    Label(root, text="電話", height=HEIGHT*rowspan, width=WIDTH*colspan, image=pixel, compound="c").grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)
    row = row ; col += colspan ; rowspan = 1 ; colspan = 4
    Entry(root, textvariable=v['電話']).grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)

    row += rowspan ; col = 0 ; rowspan = 1 ; colspan = 1
    Button(root, text="<<", command=lambda : read(database, False), height=HEIGHT*rowspan, width=WIDTH*colspan, image=pixel, compound="c").grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)

    row = row ; col += colspan ; rowspan = 1 ; colspan = 2
    Button(root, text="更新", command=lambda : update(database), height=HEIGHT*rowspan, width=WIDTH*colspan, image=pixel, compound="c").grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)
    
    row = row ; col += colspan ; rowspan = 1 ; colspan = 2
    Button(root, text="刪除", command=lambda : delete(database, v['學號'].get()), height=HEIGHT*rowspan, width=WIDTH*colspan, image=pixel, compound="c").grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)

    row = row ; col += colspan ; rowspan = 1 ; colspan = 2
    Button(root, text="新增", command=clear, height=HEIGHT*rowspan, width=WIDTH*colspan, image=pixel, compound="c").grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)
    
    row = row ; col += colspan ; rowspan = 1 ; colspan = 1
    Button(root, text=">>", command=lambda : read(database, True), height=HEIGHT*rowspan, width=WIDTH*colspan, image=pixel, compound="c").grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)
    
    
    root.mainloop()

count = 0
def read(db, boolean=True):
    try:
        global count
        if boolean and count < len(db.getData())-1:
            count += 1
        elif boolean==False and count > 0:
            count -= 1
        data = db.getData()[list(db.getData().keys())[count]]
        v['學號'].set(list(db.getData().keys())[count])
        v['姓名'].set(data['姓名'])
        v['性別'].set(data['性別'])
        v['系所'].set(data['系所'])
        v['地址'].set(data['地址'])
        v['電話'].set(data['電話'])
    except IndexError:
        pass

def delete(db, number):
    db.delete(number)
    write(db)
    clear()
    read(db, False)
    
def clear():
    v['學號'].set("")
    v['姓名'].set("")
    v['性別'].set(" ")
    v['系所'].set("")
    v['地址'].set("")
    v['電話'].set("")

def update(db):
    number = v['學號'].get()
    name = v['姓名'].get()
    sex = v['性別'].get()
    department = v['系所'].get()
    address = v['地址'].get()
    phoneNumber = v['電話'].get()
    db.update(number, name, sex, department, address, phoneNumber)
    write(db)

def write(db):
    f = open(FILE_NAME, "w", encoding="utf8")
    for key, value in db.getData().items():
        f.write(f"{key} {value['姓名']} {value['性別']} {value['系所']} {value['地址']} {value['電話']}\n")
    f.close()

main()
