from tkinter import *
from random import randint

string = ["剪刀", "石頭", "布"]
output = None
def main():
    global array ; array = [0 for i in range(3)]
    global root ; root = Tk()
    root.geometry("280x120+400+200")
    root.title("")
    MAX_WIDTH = 40
    MAX_HEIGHT = 40
    length = 7

    global output ; output = StringVar()
    labF = Frame(root, width=MAX_WIDTH*length, height=MAX_HEIGHT*2, bg="white")
    labF.pack_propagate(0)
    labF.grid(row=0, column=0, columnspan=length, rowspan=2)
    Label(labF, textvariable=output, bg="white").pack(expand=1, fill=BOTH)

    for i in range(3):
        btnF = Frame(root, width=MAX_WIDTH, height=MAX_HEIGHT, bg="white")
        btnF.pack_propagate(0)
        btnF.grid(row=3, column=1 + i * 2)
        Button(btnF, text=string[i], bg="lightyellow", command= lambda x=i: play(x)).pack(expand=1, fill=BOTH)
        
        
    root.mainloop()
    
play_count = 0
player_win = 0
player_lose = 0
def play(player):
    computer = randint(0, 2)
    global play_count; play_count += 1
    
    s = ""
    s += "玩家出" + string[player] + "，"
    s += "電腦出" + string[computer] + "，"
    
    if player == (computer + 1) % 3:
        s += "玩家獲勝" + "\n"
        global player_win ; player_win += 1
        
    elif (player + 1) % 3 == computer:
        s += "電腦獲勝" + "\n"
        global player_lose ; player_lose += 1
        
    else:
        s += "平手" + "\n"
        
    s += "玩家現已" + str(player_win) + "勝" + str(player_lose) + "負"
    
    global output ; output.set(s)

main()
