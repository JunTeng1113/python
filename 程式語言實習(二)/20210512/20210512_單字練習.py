from tkinter import *
from random import choice
import os

FILEPATH = "/english.txt"

root = None
questionEnglish = None
questionChinese = None
score = None
answer = None
english = None
entry = None
f = open(os.path.dirname(os.path.abspath(__file__)) + FILEPATH, "r", encoding="utf8")
englishList = f.readlines()
def main():
    global root ; root = Tk()
    createScreen(root)

    choiceQuestion()

    root.mainloop()

def choiceQuestion():
    global english
    english, chinese = choice(englishList).strip().split()
    questionEnglish.set(hideChar(english))
    questionChinese.set(chinese)

def hideChar(char):
    if len(char) > 2:
        return char[0] + "*" * (len(char)-2) + char[-1]
    return char


def createScreen(window):
    window.title("單字練習")
    maxHeight = 30 ; maxWidth = 30

    x = 0 ; y = 0 ; w = 3
    frame = Frame(window, height=maxHeight, width=maxWidth*w)
    frame.propagate(0)
    frame.grid(row=y, column=x, columnspan=w)
    Label(frame, text="英文：").pack(expand=1, fill=BOTH)

    x += w ; w = 3
    frame = Frame(window, height=maxHeight, width=maxWidth*w)
    frame.propagate(0)
    frame.grid(row=y, column=x, columnspan=w)
    global questionEnglish ; questionEnglish = StringVar()
    Label(frame, textvariable=questionEnglish).pack(expand=1, fill=BOTH)

    x = 0 ; y += 1 ; w = 3
    frame = Frame(window, height=maxHeight, width=maxWidth*w)
    frame.propagate(0)
    frame.grid(row=y, column=x, columnspan=w)
    Label(frame, text="中文：").pack(expand=1, fill=BOTH)
    x += w ; w = 3
    frame = Frame(window, height=maxHeight, width=maxWidth*w)
    frame.propagate(0)
    frame.grid(row=y, column=x, columnspan=w)
    global questionChinese ; questionChinese = StringVar()
    Label(frame, textvariable=questionChinese).pack(expand=1, fill=BOTH)

    x = 0 ; y += 1 ; w = 3
    frame = Frame(window, height=maxHeight, width=maxWidth*w)
    frame.propagate(0)
    frame.grid(row=y, column=x, columnspan=w)
    Label(frame, text="答對題數：").pack(expand=1, fill=BOTH)
    x = w ; w = 3
    frame = Frame(window, height=maxHeight, width=maxWidth*w)
    frame.propagate(0)
    frame.grid(row=y, column=x, columnspan=w)
    global score ; score = IntVar()
    Label(frame, textvariable=score).pack(expand=1, fill=BOTH)


    x = 0 ; y += 1 ; w = 6
    frame = Frame(window, height=maxHeight, width=maxWidth*w)
    frame.propagate(0)
    frame.grid(row=y, column=x, columnspan=w)
    global answer ; answer = StringVar()
    global entry ; entry = Entry(frame, textvariable=answer)
    entry.pack(expand=1, fill=BOTH)

    x = 0 ; y += 1 ; w = 6
    frame = Frame(window, height=maxHeight, width=maxWidth*w)
    frame.propagate(0)
    frame.grid(row=y, column=x, columnspan=w)
    Button(frame, text="送出", command=enter).pack(expand=1, fill=BOTH)

def enter():
    if entry.get() == english:
        score.set(score.get() + 1)
        choiceQuestion()
        answer.set("")

main()