from tkinter import *

def clear():
    val.set("")

def inputText(text):
    val.set(val.get() + text)

def result():
    val.set(eval(val.get()))
    
def main():
    root = Tk()
    global val
    val = StringVar()
    root.title("20210310")
    #root.geometry("200x200+0+0")
    w = 6
    h = 2

    label = Label(root, textvariable=val, width=w*4+4, height=h).grid(row=0, column=0, columnspan=4)



    
    
    Button(root, text="C", width=w*2+2, height=h, command=clear).grid(row=1, column=0, columnspan=2)
    #Button(root, text=" ", width=w, height=h).grid(row=1, column=1)
    Button(root, text="%", width=w, height=h, command=lambda: inputText("%")).grid(row=1, column=2)
    Button(root, text="/", width=w, height=h, command=lambda: inputText("/")).grid(row=1, column=3)

    Button(root, text="7", width=w, height=h, command=lambda: inputText("7")).grid(row=2, column=0)
    Button(root, text="8", width=w, height=h, command=lambda: inputText("8")).grid(row=2, column=1)
    Button(root, text="9", width=w, height=h, command=lambda: inputText("9")).grid(row=2, column=2)
    Button(root, text="*", width=w, height=h, command=lambda: inputText("*")).grid(row=2, column=3)

    Button(root, text="4", width=w, height=h, command=lambda: inputText("4")).grid(row=3, column=0)
    Button(root, text="5", width=w, height=h, command=lambda: inputText("5")).grid(row=3, column=1)
    Button(root, text="6", width=w, height=h, command=lambda: inputText("6")).grid(row=3, column=2)
    Button(root, text="-", width=w, height=h, command=lambda: inputText("-")).grid(row=3, column=3)

    Button(root, text="1", width=w, height=h, command=lambda: inputText("1")).grid(row=4, column=0)
    Button(root, text="2", width=w, height=h, command=lambda: inputText("2")).grid(row=4, column=1)
    Button(root, text="3", width=w, height=h, command=lambda: inputText("3")).grid(row=4, column=2)
    Button(root, text="+", width=w, height=h, command=lambda: inputText("+")).grid(row=4, column=3)

    Button(root, text="0", width=w*2+2, height=h, command=lambda: inputText("0")).grid(row=5, column=0, columnspan=2)
    #Button(root, text=" ", width=w, height=h).grid(row=5, column=1)
    Button(root, text=".", width=w, height=h, command=lambda: inputText(".")).grid(row=5, column=2)
    Button(root, text="=", width=w, height=h, command=result).grid(row=5, column=3)





    root.mainloop()

main()
