from tkinter import *
from threading import Timer
from random import choice
from random import randint

size = 10
ratAmount = None

t = None
counter = 0
def updateTime():
    global counter
    global time ; time.set("時間：" + str(counter))
    global t ; t = Timer(1, updateTime)
    if counter // 5 == 3:
        pause()
        clear()
    elif counter % 5 == 0:
        clear()
        global ratAmount ; ratAmount = randint(5, 15)
        global r ; r.set("地鼠：" + str(ratAmount))
        print("階段" + str(counter // 5 + 1))
        ratJump(ratAmount)
        
    counter += 1
    t.start()
        
def clear():
    [[array[y][x].config(bitmap="") for x in range(size)] for y in range(size)]

def pause():
    global t ; t.cancel()

def end():
    global root ; root.destroy()
    global t ; t.cancel()
    
#t2 = None
def ratJump(amount = 1):
    if amount <= 0:
        return 0
    else:
        global array ; rand = choice(choice(array))
        if rand['bitmap'] == "":
            rand.config(bitmap="warning")
            return ratJump(amount - 1)
        else:
            return ratJump(amount)


scoreCounter = 0
def attack(x, y):
    if array[y][x]['bitmap'] == "warning":
        array[y][x].config(bitmap="")
        global scoreCounter ; scoreCounter += 1
        global score ; score.set("得分：" + str(scoreCounter))
        print("打中: [" +str(x) + ", " + str(y) + "]")

def main():
    global array ;array = [[0 for i in range(size)] for j in range(size)]
    global root ; root = Tk()
    root.title("")
    MAX_WIDTH = 30
    MAX_HEIGHT = 30
    '''==============='''
    global time ; time = StringVar()
    topF = Frame(root, width=MAX_WIDTH * 2, height=MAX_HEIGHT)
    topF.pack_propagate(0)
    topF.grid(row=0, column=0, columnspan=2)
    
    time.set("時間：0")
    Label(topF, textvariable=time, bg="white").pack(expand=1, fill=BOTH)

    '''==============='''
    global score ; score = StringVar()
    topF = Frame(root, width=MAX_WIDTH * 3, height=MAX_HEIGHT)
    topF.pack_propagate(0)
    topF.grid(row=0, column=2, columnspan=3)
    
    score.set("得分：0")
    Label(topF, textvariable=score, bg="white").pack(expand=1, fill=BOTH)
    
    '''==============='''
    topF = Frame(root, width=MAX_WIDTH * 3, height=MAX_HEIGHT)
    topF.pack_propagate(0)
    topF.grid(row=0, column=5, columnspan=3)
    
    global r ; r = StringVar()
    global ratAmount ; r.set("地鼠：" + str(ratAmount))
    Label(topF, textvariable=r, bg="white").pack(expand=1, fill=BOTH)

    
    '''==============='''
    topF = Frame(root, width=MAX_WIDTH * 2, height=MAX_HEIGHT)
    topF.pack_propagate(0)
    topF.grid(row=0, column=8, columnspan=2)
    
    Button(topF, text="EXIT", bg="white", command=end).pack(expand=1, fill=BOTH)



    for y in range(size):
        for x in range(size):
            btnF = Frame(root, width=MAX_WIDTH, height=MAX_HEIGHT, bg="white")
            btnF.pack_propagate(0)
            btnF.grid(row=y+1, column=x)
            array[y][x] = Button(btnF, text="", bg="white", command= lambda tmpX=x, tmpY=y : attack(tmpX, tmpY))
            array[y][x].pack(expand=1, fill=BOTH)

    updateTime()
    root.mainloop()
main()
