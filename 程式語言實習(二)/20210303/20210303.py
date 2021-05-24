from tkinter import *

def gt(number):
    if number < 1: return 0
    if number == 1: return 1
    return gt(number-1) * number

def easy():
    file = open("input.txt", "r")
    value = int(file.read())
    file.close()
    for n in range(value+1):
        for k in range(n+1):

            a = 1
            for i in range(1, 1 + n):
                a *= i

            b = 1
            for i in range(1, 1 + n-k):
                b *= i
                
            c = 1
            for i in range(1, 1 + k):
                c *= i

            print(a // (b * c), end=" ")
        print()

def normal():
    root = Tk()
    root.title("20210303")
    #root.geometry("200x200+0+0")


    file = open("input.txt", "r")
    value = int(file.read())
    file.close()

    for n in range(value+1):
        for k in range(n+1):
            if (gt(n-k) * gt(k)) == 0:
                Label(root, text=1).place(x=15 * (value - n) + 30 * k, y=20 * n)
            else:
                Label(root, text=(gt(n) // (gt(n-k) * gt(k)))).place(x=15 * (value - n) + 30 * k, y=20 * n)

    root.mainloop()

easy()
normal()
