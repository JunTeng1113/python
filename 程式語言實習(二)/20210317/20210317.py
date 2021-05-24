from tkinter import *
import time
from random import randint
from random import choice



SIZE = 10 #設定大小
def main():
    global SIZE
    global array
    global pair
    root = Tk()
    root.title("20210317")

    ls = [randint(0, 9) for i in range(pair)]*2 #建立待生成清單
    print(ls)
    for y in range(SIZE):
        for x in range(SIZE):
            rand = choice(ls) ; ls.remove(rand) #從清單隨機取得一個值
            array[y][x] = Button(root, text=rand, width=2, height=1, bg="white", command=lambda i=x, j=y, r=rand: match(i, j, r))
            array[y][x].grid(row=y, column=x)
            
    global startTime ; startTime = time.time() #開始計時
    root.mainloop()


pair = SIZE**2//2
collect = 0
array = [[0 for j in range(SIZE)] for i in range(SIZE)]
tmp = [-1, -1, -1]
def match(x, y, num):
    global tmp
    global array
    global collect
    global pair
    
    print(tmp)
    array[y][x].config(state="disable", bg="yellow")
    if tmp[2] == -1:
        tmp = [x, y, num]
    elif tmp[2] != num:
        array[tmp[1]][tmp[0]].config(state="active", bg="white")
        array[y][x].config(state="active", bg="white")
        tmp = [-1, -1, -1]
    else:
        array[tmp[1]][tmp[0]].config(bg="black")
        array[y][x].config(bg="black")
        collect += 1
        if collect == pair:
            global startTime, endTime ; endTime = time.time() #結束計時
            print('經過時間(秒)：' + str(int((endTime - startTime) * 100)/100))
        tmp = [-1, -1, -1]

main()
