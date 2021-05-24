from tkinter import *

size = 10

output = None
def main():
    global array ;array = [0 for i in range(size)]
    global root ; root = Tk()
    root.title("")
    MAX_WIDTH = 40
    MAX_HEIGHT = 40

    '''
    建立BUTTON
    '''
    for i in range(size):
        btnF = Frame(root, width=MAX_WIDTH, height=MAX_HEIGHT, bg="white")
        btnF.pack_propagate(0)
        btnF.grid(row=0, column=i)
        array[i] = Button(btnF, text=str(i+1), bg="yellow", command= lambda x=i+1: display(x))
        array[i].pack(expand=1, fill=BOTH)
        
    '''
    輸出視窗
    '''
    global output ; output = StringVar()
    labF = Frame(root, width=MAX_WIDTH*10, height=MAX_HEIGHT*10, bg="white")
    labF.pack_propagate(0)
    labF.grid(row=1, column=0, columnspan=10, rowspan=10)
    array[i] = Label(labF, textvariable=output, bg="white")
    array[i].pack(expand=1, fill=BOTH)
    
    root.mainloop()
    
def display(x):
    s = ""
    for i in range(0, x+1):
        s += "＊" * i + "　" * (x-i) + "\n"
    global output; output.set(s)

main()
