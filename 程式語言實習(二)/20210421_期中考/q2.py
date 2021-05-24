from tkinter import *

size = 10
def main():
    global array ;array = [[0 for i in range(size)] for j in range(size)]
    global root ; root = Tk()
    root.title("")
    MAX_WIDTH = 40
    MAX_HEIGHT = 40

    
    for i in range(size ** 2):
        btnF = Frame(root, width=MAX_WIDTH, height=MAX_HEIGHT, bg="white")
        btnF.pack_propagate(0)
        btnF.grid(row=i//size, column=i%size)
        array[i//size][i%size] = Button(btnF, text=str(i//size+1) + ", " + str(i%size+1), bg="yellow", command= lambda y=i//size+1, x=i%size+1: display(y, x))
        array[i//size][i%size].pack(expand=1, fill=BOTH)
        
    root.mainloop()

def display(y, x):
    print("第" + str(y) +  "列, 第" + str(x) + "行")
main()
