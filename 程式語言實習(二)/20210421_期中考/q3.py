from tkinter import *


state = 4

array = []
player = 0
v = 0
root = 0
def main():
    global array ;array = [[0 for i in range(state)] for j in range(state)]
    global root ; root = Tk()
    root.title("20210324")
    global v ; v = StringVar()

    MAX_WIDTH = 100
    MAX_HEIGHT = 100

    
    topF = Frame(root, width=MAX_WIDTH, height=MAX_HEIGHT)
    topF.pack_propagate(0)
    topF.grid(row=0, column=0, columnspan=state)
    
    v.set("輪到Player1")
    Label(topF, textvariable=v, bg="yellow").pack(expand=1, fill=BOTH)

    for y in range(state):
        for x in range(state):
            btnF = Frame(root, width=MAX_WIDTH, height=MAX_HEIGHT, bg="white")
            btnF.pack_propagate(0)
            btnF.grid(row=y+1, column=x)
            array[y][x] = Button(btnF, text="", bg="white", command= lambda tmpX=x, tmpY=y : play(tmpX, tmpY))
            array[y][x].pack(expand=1, fill=BOTH)
            
    btnF = Frame(root, width=MAX_WIDTH, height=MAX_HEIGHT, bg="white")
    btnF.pack_propagate(0)
    btnF.grid(row=state+1, column=0)
    Button(btnF, text="Restart", bg="white", command= restart).pack(expand=1, fill=BOTH)

    '''
    btnF = Frame(root, width=MAX_WIDTH, height=MAX_HEIGHT, bg="white")
    btnF.pack_propagate(0)
    btnF.grid(row=state+1, column=1)
    Button(btnF, text="Next State", bg="white", command= nextState).pack(expand=1, fill=BOTH)
    '''
    
    root.mainloop()

def restart():
    global over
    global count
    global player
    root.destroy()
    over = False
    count = 0
    player = 0
    main()
    
'''
def nextState():
    global state
    state += 1
    restart()
'''

over = False
def play(locX, locY):
    global player, array, over
    if array[locY][locX]['text'] != "" or over: return 0 #按過的按鈕不能再按

    playerName = ["Player1", "Player2", "Player3"]
    content = ["O", "X", "!"]
    array[locY][locX].config(text=content[player])
    status = getStatus(locX, locY)
    if status == "WIN":
        v.set(playerName[player] + "獲勝")
        over = True
    elif status == "Tie":
        v.set("平手")
        over = True
    else:
        player = (player+1) % len(playerName)
        v.set("輪到" + playerName[player])

count = 0
def getStatus(locX, locY):
    global count ; count += 1
    for i in range(1, state):
        if array[locY][i]['text'] != array[locY][i-1]['text']:
            break
        else:
            if i == state - 1: return "WIN"
            continue

    for i in range(1, state):
        if array[i][locX]['text'] != array[i-1][locX]['text']:
            break
        else:
            if i == state - 1: return "WIN"
            continue
    
    if locX == locY:
        for i in range(1, state):
            if array[i][i]['text'] != array[i-1][i-1]['text']:
                break
            else:
                if i == state - 1:
                    return "WIN"
                continue
    
    if locX != locY and (locX + state-1) % (state-1) == (locY + state-1) % (state-1):
        for i in range(1, state):
            if array[i][(state-1)-i]['text'] != array[i-1][(state-1)-(i-1)]['text']:
                break
            else:
                if i == state - 1: return "WIN"
                continue
            
    if count == state * state: return "Tie"
    return "Playing"

main()
