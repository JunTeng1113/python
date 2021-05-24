from tkinter import *
v = 0
array = [[0 for i in range(3)] for j in range(3)]
def main():
    root = Tk()
    root.title("標題名稱")
    global v
    v = StringVar()
    v.set("輪到 " + str(name[r]))
    topFrame = Frame(root, width=300, height=100)
    topFrame.pack_propagate(False)
    topFrame.grid(row=0, column=0, columnspan=3)
    Label(topFrame, textvariable=v).pack(expand=True, fill=BOTH)
    for y in range(3):
        for x in range(3):
            btnFrame = Frame(root, width=100, height=100)
            btnFrame.pack_propagate(False)
            btnFrame.grid(row=y+1, column=x)
            array[y][x] = Button(btnFrame, text="", 
                 command= lambda tmpX=x, tmpY=y : play(tmpX, tmpY))
            array[y][x].pack(expand=True, fill=BOTH)
    root.mainloop()


name = ["player1", "player2"]
player = ["O", "X"]
status = "playing"
r = 0
count = 0 
def play(x, y):
    global r, status, count
    if array[y][x]['text'] == "" and status == "playing": 
        array[y][x].config(text=player[r])
        count += 1
        status = getStatus(x, y)
        if status == "WIN": v.set(str(name[r]) + " 獲勝")
        elif status == "Tie": v.set("平手")
        else:
            if r == 0: r = 1
            else: r = 0
            v.set("輪到 " + str(name[r]))

def getStatus(x, y):
    if array[y][x]['text'] == array[y][(x+1) % 3]['text'] == array[y][(x+2) % 3]['text']:
        return "WIN"
    if array[y][x]['text'] == array[(y+1) % 3][x]['text'] == array[(y+2) % 3][x]['text']:
        return "WIN"
    if (x == 0 and y == 0) or (x == 2 and y == 2) or (x == 1 and y == 1):
        if array[y][x]['text'] == array[(y+1) % 3][(x+1) % 3]['text'] == array[(y+2) % 3][(x+2) % 3]['text']:
            return "WIN"
    if (x == 2 and y == 0) or (x == 1 and y == 1) or (x == 0 and y == 2):
        if array[y][x]['text'] == array[(y+1) % 3][(x+2) % 3]['text'] == array[y][x]['text']:
            return "WIN"
    if count == 9: return "Tie"
    return "playing"

main()
