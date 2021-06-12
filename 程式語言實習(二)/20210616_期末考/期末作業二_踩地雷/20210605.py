from tkinter import *
from random import randint, sample
from threading import Timer
import os

''' 功能要求－－－－－
    [V] 產生隨機數量的地雷
    [V] 按下按鈕後變更為 Disabled
    [V] 踩到地雷後將所有按鈕變更為 Disabled
    [V] 踩到地雷後顯示所有地雷
    [V] 若不是地雷，則顯示周圍地雷數量
    [V] 若不是地雷，將旁邊同樣不是地雷的按鈕變更為 Disabled
    [V] 當所有不是地雷的按鈕都呈現 Disabled，則遊戲結束，並將計時器暫停

    額外功能－－－－－
    [V] 首次點擊不會踩到地雷，且周圍八格無地雷
'''

''' BOMB_AMOUNT 設定 None 則隨機產生 5 ~ 15 個地雷  '''

''' －－－－－　操作區　－－－－－ '''
BOMB_AMOUNT = None
SIZE = 10
''' －－－－－　操作區　－－－－－ '''

'''－像素－'''
HEIGHT = 15 ; WIDTH = 15


root = Tk()
pixel = PhotoImage(width=1, height=1)  
bombImage = PhotoImage(file=os.path.join(os.path.dirname(__file__), 'images.png')).subsample(15, 15)
startImage = PhotoImage(file=os.path.join(os.path.dirname(__file__), 'happy.png')).subsample(15, 15)
failImage = PhotoImage(file=os.path.join(os.path.dirname(__file__), 'dead.png')).subsample(15, 15)
endImage = PhotoImage(file=os.path.join(os.path.dirname(__file__), 'shocked.png')).subsample(15, 15)
array = dict()
restartButton = None
time = StringVar()
amount = StringVar()
def main():
    root.title('踩地雷')

    row = 0 ; col = 0 ; rowspan = 3 ; columnspan = 3
    lab = Label(root, textvariable=amount, height=HEIGHT * rowspan, width=WIDTH * columnspan, image=pixel, compound="c")
    lab.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan)
    
    row = row ; col += columnspan ; rowspan = 3 ; columnspan = 4
    global restartButton
    restartButton = Button(root, command=clear, height=HEIGHT * rowspan, width=WIDTH * columnspan, image=startImage, compound="c")
    restartButton.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan)

    row = row ; col += columnspan ; rowspan = 3 ; columnspan = 3
    lab = Label(root, textvariable=time, height=HEIGHT * rowspan, width=WIDTH * columnspan, image=pixel, compound="c")
    lab.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan)

    global array
    row += rowspan ; col += columnspan
    for y in range(SIZE):
        for x in range(SIZE):
            btn = Button(root, text=" ", height=HEIGHT, width=WIDTH, command=btnCmd(x, y).onClick, image=pixel, compound="c")
            array[f'({x}, {y})'] = bombBtn(btn, x, y)
            array[f'({x}, {y})'].btn.grid(row=(row+y), column=x)

    clear()
    root.mainloop()

class btnCmd:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def onClick(self):
        '''－－－－－　首次點擊　－－－－－'''
        if array['(0, 0)'].state == None:
            restart(self.x, self.y)

        def test(x, y):
            for ele in getAround(x, y):
                if ele.btn['text'] == " ":
                    btnCmd(ele.x, ele.y).onClick()
        global timer
        '''－－－－－　遊戲失敗　－－－－－'''
        if array[f'({self.x}, {self.y})'].bomb:
            for i in list(filter(lambda a : a.bomb, array.values())):
                i.btn['image'] = bombImage
            
            for i in array.values():
                i.btn['state'] = "disabled"

            restartButton['image'] = failImage
            timer.cancel()

        else:
            bombAmount = array[f'({self.x}, {self.y})'].state
            array[f'({self.x}, {self.y})'].setText(bombAmount)
            array[f'({self.x}, {self.y})'].btn['state'] = "disabled"
            array[f'({self.x}, {self.y})'].btn['bg'] = "white"
            if bombAmount == 0:
                delay(lambda x=self.x, y=self.y : test(x, y), 0.02)
            
            '''－－－－－　成功完成遊戲　－－－－－'''
            if list(filter(lambda a : a.bomb==False and a.btn['state'] != "disabled", list(array.values()))) == []:
                for i in array.values():
                    i.btn['state'] = "disabled"
                restartButton['image'] = endImage
                timer.cancel()


def getAround(x, y, haveSelf=False):
    s = list()    
    if y > 0:
        if x > 0:
            s.append(array[f"({x-1}, {y-1})"])

        s.append(array[f"({x}, {y-1})"])
        if x < SIZE-1:
            s.append(array[f"({x+1}, {y-1})"])

    if x > 0:
        s.append(array[f"({x-1}, {y})"])

    if haveSelf:
        s.append(array[f"({x}, {y})"])

    if x < SIZE-1:
        s.append(array[f"({x+1}, {y})"])

    if y < SIZE-1:
        if x > 0:
            s.append(array[f"({x-1}, {y+1})"])

        s.append(array[f"({x}, {y+1})"])
        if x < SIZE-1:
            s.append(array[f"({x+1}, {y+1})"])

    return s

class bombBtn:
    def __init__(self, btn, x, y, state=None, bomb=False):
        self.btn = btn
        self.x = x
        self.y = y
        self.state = state
        self.bomb = bomb

    def setText(self, number):
        foreColor = ['light gray', 'blue', 'dark green', 'coral', 'red', 'dark red', 'indian red', 'purple', 'dim gray']
        self.btn['text'] = number
        self.btn['disabledforeground'] = foreColor[number]

def delay(func, sec):
    t = Timer(sec, func)
    t.start()
    return t


def add():
    m = int(time.get().split(":")[0])
    s = int(time.get().split(":")[1])
    if s < 59:
        s += 1
    else:
        m += 1 ; s = 0 

    time.set(f"{str(m).rjust(2, '0')}:{str(s).rjust(2, '0')}")

    global timer
    timer = Timer(1, add)
    timer.start()
    return timer

timer = Timer(1, add)
bombAmount = 0
def clear():
    global bombAmount ; bombAmount = BOMB_AMOUNT if BOMB_AMOUNT else randint(5, 15)
    global amount ; amount.set(str(bombAmount).rjust(3, "0"))
    global time ; time.set("00:00")
    for btn in array.values(): 
        btn.btn['text'] = " "
        btn.btn['state'] = "normal"
        btn.btn['bg'] = "light gray"
        btn.btn['image'] = pixel
        btn.bomb = False
        btn.state = None
        global restartButton
        restartButton['image'] = startImage

    global timer ; timer.cancel()
    timer = Timer(1, add)
    timer.start()

def restart(x=None, y=None):
    # 設定bomb
    configList = list(array.values())
    '''－－－－－　首次點擊不會踩到地雷，且周圍八格無地雷　－－－－－'''
    if (x != None) and (y != None):
        configList = list(filter(lambda ele : ele not in list(getAround(x, y, haveSelf=True)), configList))

    for btn in sample(configList, bombAmount):
        btn.bomb = True

    # 設定state
    for value in array.values():
        if value.bomb:
            value.state = "B"

        else:
            value.state = len(list(filter(lambda ele: ele.bomb==True, getAround(value.x, value.y))))

main()



