from tkinter import *

special = [0]
def main():
    global root ; root = Tk()
    root.title("")
    MAX_WIDTH = 30
    MAX_HEIGHT = 30

    r = 0
    labF = Frame(root, width=MAX_WIDTH * 2, height=MAX_HEIGHT, bg="white")
    labF.pack_propagate(0)
    labF.grid(row=r, column=0, columnspan=2)
    Label(labF, text="2021年5月", bg="white").pack(expand=1, fill=BOTH)
    r += 1
    
    date = "日一二三四五六"
    for i in range(0, 7):
        labF = Frame(root, width=MAX_WIDTH, height=MAX_HEIGHT, bg="white")
        labF.pack_propagate(0)
        labF.grid(row=r, column=i%7)
        Label(labF, text=date[i], bg="white").pack(expand=1, fill=BOTH)
    r += 1
    
    start = 6
    for i in range(start, 31+start):
        labF = Frame(root, width=MAX_WIDTH, height=MAX_HEIGHT, bg="white")
        labF.pack_propagate(0)
        labF.grid(row=i//7 + r, column=i%7)
        if i - start in special:
            Label(labF, text=i-start+1, bg="orange").pack(expand=1, fill=BOTH)
        else:
            Label(labF, text=i-start+1, bg="white").pack(expand=1, fill=BOTH)
        
    root.mainloop()
    
main()
