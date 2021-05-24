from tkinter import *
import time
from random import randint
from random import choice
from threading import Timer


SIZE = 4 #設定大小
def main():
    global SIZE
    global array
    global pair
    root = Tk()
    root.title("")
    MAX_WIDTH = 30
    MAX_HEIGHT = 30
    
    global output ; output = StringVar() ; output.set("配對成功" + str(collect) + "組")
    labF = Frame(root, width=MAX_WIDTH*SIZE, height=MAX_HEIGHT*2, bg="white")
    labF.pack_propagate(0)
    labF.grid(row=0, column=0, columnspan=SIZE, rowspan=2)
    Label(labF, textvariable=output, bg="white").pack(expand=1, fill=BOTH)
    
    ls = [randint(0, 9) for i in range(pair)]*2 #建立待生成清單
    for y in range(SIZE):
        for x in range(SIZE):
            rand = choice(ls) ; ls.remove(rand) #從清單隨機取得一個值
            btnF = Frame(root, width=MAX_WIDTH, height=MAX_HEIGHT, bg="white")
            btnF.pack_propagate(0)
            btnF.grid(row=y+2, column=x)
            array[y][x] = Button(btnF, text="", bg="white", command=lambda i=x, j=y, r=rand: match(i, j, r))
            array[y][x].pack(expand=1, fill=BOTH)
            
    root.mainloop()

output = None
pair = SIZE**2//2
collect = 0
array = [[0 for j in range(SIZE)] for i in range(SIZE)]
tmp = [-1, -1, -1]
time = None
def match(x, y, num):
    global tmp
    global array
    global collect
    global pair
    global step
    global time ; time = [[0 for j in range(SIZE)] for i in range(SIZE)]
    
    array[y][x].config(text=num, state="disable", bg="yellow")
    if tmp[2] == -1:
        tmp = [x, y, num]
    elif tmp[2] != num:
        array[tmp[1]][tmp[0]].config(state="active", bg="white")
        array[y][x].config(state="active", bg="white")
        
        time[tmp[1]][tmp[0]] = Timer(1, disable, [tmp[0], tmp[1]])
        time[tmp[1]][tmp[0]].start()
        time[y][x] = Timer(1, disable, [x, y])
        time[y][x].start()
        
        tmp = [-1, -1, -1]
    else:
        array[tmp[1]][tmp[0]].config(bg="black")
        array[y][x].config(bg="black")
        
        collect += 1
        global output ; output.set("配對成功" + str(collect) + "組")
        tmp = [-1, -1, -1]
    
def disable(x, y):
    global array ; array[y][x].config(text="")
    
main()
