from tkinter import *
from threading import Timer
from random import choice, choices, randint
import string

COUNT = 10 ; SPEED = 1
SIZE = {'x': 10, 'y': 10}

array = []
root = None
entry = None
question = None
answer = None
gameTime = None
score = 0
counter = 0
def main():
    maxHeight = 30
    maxWidth = 30
    global array ; array = [[None for i in range(SIZE['y'])] for j in range(SIZE['x'])]

    global root ; root = Tk()
    root.title("打字遊戲")
    for y in range(SIZE['y']):
        for x in range(SIZE['x']):
            btnF = Frame(root, height=maxHeight, width=maxWidth)
            btnF.propagate(0)
            btnF.grid(row=y, column=x)
            array[y][x] = Button(btnF)
            array[y][x].pack(expand=1, fill=BOTH)

    x = 0 ; y += 1 ; w = 3
    frame = Frame(root, height=maxHeight, width=maxWidth*w)
    frame.propagate(0)
    frame.grid(row=y, column=x, columnspan=w)
    global question ; question = StringVar() ; question.set(getQuestion())
    Label(frame, textvariable=question).pack(expand=1, fill=BOTH)
    
    x = w; w = 4
    frame = Frame(root, height=maxHeight, width=maxWidth*w)
    frame.propagate(0)
    frame.grid(row=y, column=x, columnspan=w)
    global answer ; answer = StringVar()
    global entry ; entry = Entry(frame, textvariable=answer)
    entry.pack(expand=1, fill=BOTH)
    entry.focus()
    entry.bind("<Return>", enter)

    x += w ; w = 3
    frame = Frame(root, height=maxHeight, width=maxWidth*w)
    frame.propagate(0)
    frame.grid(row=y, column=x, columnspan=w)
    global score ; score = StringVar() ; score.set("得分：" + str(0))
    Label(frame, textvariable=score).pack(expand=1, fill=BOTH)

    global gameTime ; gameTime = Timer(SPEED, startGame)
    gameTime.start()
    root.mainloop()

def enter(event):
    if entry.get() == question.get():
        question.set(getQuestion())
        score.set("得分：" + str(int("".join(filter(lambda x : x in string.digits, score.get()))) + 1))
        removeChar()
    answer.set("")

def getQuestion():
    return "".join(choices(string.ascii_letters, k=randint(5, 7))) #從a-zA-Z中取5~7個

def charFall():
    for y in range((SIZE['y']-1)-1, -1, -1):
        for x in range(SIZE['x']): 
            array[y+1][x]['bitmap'] = array[y][x]['bitmap']

    for x in range(SIZE['x']):
        array[0][x]['bitmap'] = ""

    if counter < COUNT:
        addChar()
    else:
        if len(list(filter(lambda i : i['bitmap'] != '', [x for y in array for x in y]))) == 0:
            stopGame()

def addChar():
    choice(list(filter(lambda i : i['bitmap'] == '', array[0])))['bitmap'] = 'hourglass' # 新增一個(不是字符的)字符
    global counter ; counter += 1

def removeChar():
    y = SIZE['y']
    bottomList = []
    while True:
        y -= 1
        bottomList += list(filter(lambda i : i['bitmap'] != '', array[y]))
        if bottomList != [] or y == 0:
            break

    choice(bottomList)['bitmap'] = ''

        
def startGame():
    global gameTime ; gameTime = Timer(SPEED, startGame)
    gameTime.start()
    charFall()

def stopGame():
    global gameTime ; gameTime.cancel()
    question.set("GAME OVER")
    entry['state'] = 'disabled'

main()
