from tkinter import *

string = list("abcdefghijklmnopqrstuvwxyz") + ["清除"]
def main():
    global array ; array = [0 for i in range(1)]
    global root ; root = Tk()
    root.title("")
    MAX_WIDTH = 40
    MAX_HEIGHT = 40
    length = 9

    global output ; output = StringVar()
    labF = Frame(root, width=MAX_WIDTH*length, height=MAX_HEIGHT*2, bg="white")
    labF.pack_propagate(0)
    labF.grid(row=0, column=0, columnspan=length, rowspan=2)
    array[0] = Label(labF, textvariable=output, bg="white")
    array[0].pack(expand=1, fill=BOTH)
        
    for i in range(26+1):
        btnF = Frame(root, width=MAX_WIDTH, height=MAX_HEIGHT, bg="white")
        btnF.pack_propagate(0)
        btnF.grid(row=2 + i//length, column=i%length)
        Button(btnF, text=string[i], bg="lightyellow", command= lambda x=i: input_(x)).pack(expand=1, fill=BOTH)
        
    root.mainloop()

def input_(x):
    global output
    if string[x] == "清除":
        output.set("")
    else:
        output.set(output.get() + string[x])
    
main()
