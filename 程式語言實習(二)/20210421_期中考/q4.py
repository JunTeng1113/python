from tkinter import *
from random import randint

count = 0
array = []
label1 = 0
label2 = 0
nextBtn = 0
def main():
    global root ; root = Tk()
    root.geometry("350x100+400+200")
    root.title("")
    MAX_WIDTH = 30
    MAX_HEIGHT = 30

    r = 0
    global label2 ; label2 = StringVar()
    label2.set("")
    labF = Frame(root, width=MAX_WIDTH * 3, height=MAX_HEIGHT, bg="white")
    labF.pack_propagate(0)
    labF.grid(row=r, column=0, columnspan=3)
    Label(labF, textvariable=label2, bg="white").pack(expand=1, fill=BOTH)
    
    global label1 ; label1 = StringVar()
    label1.set("答對題數：" + str(count))
    labF = Frame(root, width=MAX_WIDTH * 3, height=MAX_HEIGHT, bg="white")
    labF.pack_propagate(0)
    labF.grid(row=r, column=3, columnspan=3)
    Label(labF, textvariable=label1, bg="white").pack(expand=1, fill=BOTH)

    btnF = Frame(root, width=MAX_WIDTH * 3, height=MAX_HEIGHT, bg="white")
    btnF.pack_propagate(0)
    btnF.grid(row=r, column=6, columnspan=3)
    global nextBtn ; nextBtn = Button(btnF, text="Next", bg="white", command=nextStage, state="disabled")
    nextBtn.pack(expand=1, fill=BOTH)
    r += 1
    
    default = 2
    global array ; array = [0 for i in range(4)]
    rand = randint(0, 2)
    
    btnF = Frame(root, width=MAX_WIDTH * 2, height=MAX_HEIGHT, bg="white")
    btnF.pack_propagate(0)
    btnF.grid(row=r, column=0, columnspan=3)
    array[0] = Button(btnF, text="", bg="white", bitmap="question", command= lambda i=rand: play(0, i))
    array[0].pack(expand=1, fill=BOTH)

    btnF = Frame(root, width=MAX_WIDTH * 2, height=MAX_HEIGHT, bg="white")
    btnF.pack_propagate(0)
    btnF.grid(row=r, column=3, columnspan=3)
    array[1] = Button(btnF, text="", bg="white", bitmap="question", command= lambda i=rand: play(1, i))
    array[1].pack(expand=1, fill=BOTH)
    
    btnF = Frame(root, width=MAX_WIDTH * 2, height=MAX_HEIGHT, bg="white")
    btnF.pack_propagate(0)
    btnF.grid(row=r, column=6, columnspan=3)
    array[2] = Button(btnF, text="", bg="white", bitmap="question", command= lambda i=rand: play(2, i))
    array[2].pack(expand=1, fill=BOTH)
    
    
    root.mainloop()

def nextStage():
    root.destroy()
    main()

def play(i, answer):
    global array
    for j in range(3):
        array[j].config(bitmap="")
        array[j].config(state="disabled")
        array[j].config(text="X")
    array[answer].config(text="O")
    global nextBtn ; nextBtn.config(state="normal")
    global label2
    if i == answer:
        global count ; count += 1
        global label1 ; label1.set("答對題數：" + str(count))
        label2.set("正確")
    else:
        label2.set("錯誤")

main()
