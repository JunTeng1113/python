from tkinter import *
from random import randint , choice

SIZE = 7 * 4
money = 100

'''
[V] 大小可自訂(最小7x7)
[V] 一個持有金錢的Label，預設100元
一個顯示目前指到的圖示為何的img
[V] 一個開始執行的Button
數個下注用的Button
[V] 數個下注目標圖示和下注數量的img和Label
[V] 數個顯示每個圖示倍率的Label

[V] 每個圖示至少出現一次
每個下注圖示下皆有加注和減注的Button
[V] 按下加注+1
[V] 按下減注-1
[V] 金額不足無法下注
[V] 開始執行後所有下注按鈕轉為Disabled
[V] 旋轉速度由快到慢
旋轉三圈才會開始減速
[V] 麻仔台停止後根據目標圖示將其下注數量與倍率相乘以獲取相對應的獎金
[V] 麻仔台停止後將所有下注數量重置
'''

IMAGE_BUTTON_SIZE = 50
OPTION_BUTTON_SIZE = IMAGE_BUTTON_SIZE / 2 - 5

image = {
    'apple': './Photos/apple.png',
    'betelnut': './Photos/betelnut.png',
    'double7': './Photos/double7.png',
    'grape': './Photos/grape.png',
    'orange': './Photos/orange.png',
    'ring': './Photos/ring.png',
    'star': './Photos/star.png',
    'watermelon': './Photos/watermelon.png'
}

iconAmount = None
oddset = None # 賠率
val = None
array = None
oddsetButton = None
pickButton = None
addButton = None
reduceButton = None 
myMoney = None # 持有金錢
winMoney = None # 贏得金錢
workAddButton = None
workReduceButton = None
displayLabel = None
photo = None
def main():
    global array
    array = [{"button": None, "image": None} for i in range(SIZE)]
    root = Tk()
    root.title("麻仔台_完整版")

    pixel = PhotoImage(height=1, width=1)
    global photo
    photo = dict()
    [photo.setdefault(key, PhotoImage(file=image[key])) for key in list(image.keys())]

    global val
    val = dict()
    [val.setdefault(key, IntVar()) for key in list(image.keys())]


    # 產生圖示清單
    iconList = list()
    [iconList.append(i) for i in list(image.keys())] # 每種至少一個
    [iconList.append(choice(iconList)) for i in range(SIZE-len(list(image.keys())))] # 從清單中隨機選一個出來
    
    # 賠率
    global iconAmount
    iconAmount = dict()
    [iconAmount.setdefault(key, iconList.count(key)) for key in list(image.keys())]
    setOddset()
    ''' 回型麻仔台 '''
    for i in range(0, SIZE):
        rowspan = 2 ; colspan = 2
        rnd = choice(iconList)
        iconList.remove(rnd)
        array[i]['button'] = Button(root, bd=0, height=IMAGE_BUTTON_SIZE*(rowspan/2), width=IMAGE_BUTTON_SIZE*(colspan/2), image=photo[rnd], compound="c")
        row = rectangular_ambulatory_plane(SIZE, i)[1]
        col = rectangular_ambulatory_plane(SIZE, i)[0]
        array[i]['button'].grid(row=row*2, column=col*2, rowspan=2, columnspan=2)
        array[i]['image'] = rnd
    
    ''' 分隔線 '''
    row = (SIZE//4+1)*2 ; col = 0 ; rowspan = 1 ; colspan = (SIZE//4+1)*2
    Label(root, height=15*rowspan, width=IMAGE_BUTTON_SIZE*(colspan/2), image=pixel, compound="c").grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)

    ''' 下注賠率 '''
    global oddsetButton
    oddsetButton = dict()
    row += 2 ; col = 0 ; rowspan = 1 ; colspan = 2
    for i in list(photo.keys()):
        oddsetButton[i] = Button(root, bd=0, text=oddset[i], background="#ffffff", height=IMAGE_BUTTON_SIZE*(rowspan/2), width=IMAGE_BUTTON_SIZE*(colspan/2), image=pixel, compound="c")
        oddsetButton[i].grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)
        row = row ; col += colspan

    ''' 下注圖示 '''
    global pickButton
    pickButton = dict()
    row += 2 ; col = 0 ; rowspan = 2 ; colspan = 2
    for i in list(photo.keys()):
        pickButton[i] = Button(root, command=lambda id=i : pick(id), background="#ffffff", height=IMAGE_BUTTON_SIZE*(rowspan/2), width=IMAGE_BUTTON_SIZE*(colspan/2), image=photo[i], compound="c")
        pickButton[i].grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)
        row = row ; col += colspan

    ''' 下注金額 '''
    row += 2 ; col = 0 ; rowspan = 2 ; colspan = 2
    for i in list(photo.keys()):
        Button(root, textvariable=val[i], bd=0, background="#ffffff", height=IMAGE_BUTTON_SIZE*(rowspan/2), width=IMAGE_BUTTON_SIZE*(colspan/2), image=pixel, compound="c").grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)
        row = row ; col += colspan

    ''' -----作業要求----- '''
    global workAddButton, workReduceButton
    workAddButton = dict()
    workReduceButton = dict()
    row += rowspan ; col = 0 ; rowspan = 1 ; colspan = 1
    for i in list(photo.keys()):
        workAddButton[i] = Button(root, text="+", command=lambda id=i: add(pick=id), bd=0, height=OPTION_BUTTON_SIZE, width=OPTION_BUTTON_SIZE, image=pixel, compound="c")
        workAddButton[i].grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)
        row = row ; col += colspan
        workReduceButton[i] = Button(root, text="-", command=lambda id=i: reduce(pick=id), bd=0, height=OPTION_BUTTON_SIZE, width=OPTION_BUTTON_SIZE, image=pixel, compound="c")
        workReduceButton[i].grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)
        row = row ; col += colspan

    global displayLabel
    row = 0 ; col = 99 ; rowspan = 1 ; colspan = 1
    displayLabel = Label(root)
    displayLabel.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)

    ''' 持有金錢 標籤'''
    row = 2*2+1 ; col = 1*2+1 ; rowspan = 1 ; colspan = 4
    Label(root, text="持有金錢", background="#eeeeee", height=IMAGE_BUTTON_SIZE*(rowspan/2), width=IMAGE_BUTTON_SIZE*(colspan/2), image=pixel, compound="c").grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)
    
    ''' 贏得金錢 標籤'''
    row = row ; col += colspan+1 ; rowspan = 1 ; colspan = 5
    Label(root, text="贏得金錢", background="#eeeeee", height=IMAGE_BUTTON_SIZE*(rowspan/2), width=IMAGE_BUTTON_SIZE*(colspan/2), image=pixel, compound="c").grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)
    
    ''' 持有金錢 欄位'''
    global myMoney, money
    myMoney = IntVar()
    myMoney.set(money)
    row = 3*2 ; col = 1*2+1 ; rowspan = 2 ; colspan = 4
    Label(root, textvariable=myMoney, background="#dddddd", height=IMAGE_BUTTON_SIZE*(rowspan/2), width=IMAGE_BUTTON_SIZE*(colspan/2), image=pixel, compound="c").grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)

    ''' 贏得金錢 欄位'''
    global winMoney
    winMoney = IntVar()
    winMoney.set(0)
    row = row ; col += colspan+1 ; rowspan = 2 ; colspan = 5
    Label(root, textvariable=winMoney, background="#dddddd", height=IMAGE_BUTTON_SIZE*(rowspan/2), width=IMAGE_BUTTON_SIZE*(colspan/2), image=pixel, compound="c").grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)

    ''' 加注 '''
    global addButton
    row = 5*2 ; col = 1*2+1 ; rowspan = 2 ; colspan = 2
    addButton = Button(root, text="加注", command=add, height=IMAGE_BUTTON_SIZE*(rowspan/2), width=IMAGE_BUTTON_SIZE*(colspan/2), image=pixel, compound="c")
    addButton.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)

    ''' 減注 '''
    global reduceButton
    row = row ; col += colspan ; rowspan = 2 ; colspan = 2
    reduceButton = Button(root, text="減注", command=reduce, height=IMAGE_BUTTON_SIZE*(rowspan/2), width=IMAGE_BUTTON_SIZE*(colspan/2), image=pixel, compound="c")
    reduceButton.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)

    ''' 全押 '''
    row = row ; col += colspan+1 ; rowspan = 2 ; colspan = 2
    Button(root, text="全押", command=selectAll, height=IMAGE_BUTTON_SIZE*(rowspan/2), width=IMAGE_BUTTON_SIZE*(colspan/2), image=pixel, compound="c").grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)

    ''' GO '''
    global GoButton
    row = row ; col += colspan+1 ; rowspan = 2 ; colspan = 2
    GoButton = Button(root, text="GO", command=start, height=IMAGE_BUTTON_SIZE*(rowspan/2), width=IMAGE_BUTTON_SIZE*(colspan/2), image=pixel, compound="c")
    GoButton.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan)
    
    disableAddButton()
    disableReduceButton()
    root.mainloop()
        
def rectangular_ambulatory_plane(size, number):
    if size % 4 == 0:
        if (number / (size // 4)) < 1: return [(number % (size // 4)), 0]
        elif (number / (size // 4)) < 2: return [(size // 4), (number % (size // 4))] 
        elif (number / (size // 4)) < 3: return [((size // 4) - (number % (size // 4))), (size // 4)]
        elif (number / (size // 4)) < 4: return [0, ((size // 4) - (number % (size // 4)))] 
    else:
        return 0

pickList = set()
def pick(id):
    global pickButton, pickList
    for i in pickList:
        pickButton[i].configure(background="#ffffff") 
    pickList.clear()
    pickList.add(id)
    pickButton[id].configure(background="#ffeecc") 

    if haveMoney():
        enableAddButton()

    if val[id].get() > 0: 
        enableReduceButton()

def selectAll():
    if len(pickList) < len(list(image.keys())):
        for id in list(image.keys()):
            pickList.add(id)
            pickButton[id].configure(background="#ffeecc") 
        if haveMoney():
            enableAddButton()
            
        disableReduceButton()
        for i in pickList:
            if val[i].get() > 0:
                enableReduceButton()
    else:
        for id in list(image.keys()):
            pickList.remove(id)
            pickButton[id].configure(background="white") 
        disableAddButton()
        disableReduceButton()

def haveMoney():
    global money
    if money > 0:
        return True
    else:
        return False

def isSelected():
    if len(pickList) == 0:
        return False
    else:
        return True

def enableAddButton():
    global addButton
    addButton.configure(state="active")

def disableAddButton():
    global addButton
    addButton.configure(state="disabled")

def enableReduceButton():
    global reduceButton
    reduceButton.configure(state="active")

def disableReduceButton():
    global reduceButton
    reduceButton.configure(state="disabled")

from threading import Timer
count = 0
displayLabel = None
GoButton = None
def countdown(sec):
    global GoButton ; GoButton.config(text="Playing", state="disabled")
    global array
    global count
    global winMoney, oddset, val, money
    print(sec)
    if sec > 0:
        array[(count+SIZE-1)%SIZE]['button'].config(bg="SystemButtonFace")
        array[(count+SIZE)%SIZE]['button'].config(bg="red")
        global photo
        global displayLabel ; displayLabel.config(image=photo[array[(count+SIZE)%SIZE]['image']])
        count = (count + 1) % SIZE
        return Timer(formula(sec), countdown, [sec-1]).start()
    else:
        result = array[(count+SIZE-1)%SIZE]['image']
        win = oddset[result] * val[result].get()
        winMoney.set(win) # 顯示贏得金錢
        money += win
        myMoney.set(money)
        [val[key].set(0) for key in val.keys()] # 重置下注
        end()
        return GoButton.config(text="GO", state='normal')
        
    
def formula(sec):
    return 1.5 * (1 - sec / (sec+20)) ** 5

def end():
    global pickButton, oddsetButton, workAddButton, workReduceButton
    for btn in list(pickButton.values()) + list(oddsetButton.values()) + list(workAddButton.values()) + list(workReduceButton.values()):
        btn.configure(background="SystemButtonFace", state="active")
    pickList.clear()

def start():
    global pickButton, oddsetButton, workAddButton, workReduceButton
    for btn in list(pickButton.values()) + list(oddsetButton.values()) + list(workAddButton.values()) + list(workReduceButton.values()):
        btn.configure(background="#dddddd", state="disabled")

    return countdown(randint(1, SIZE*2) + SIZE*4)
    
def add(amount=1, pick=None):
    global val, money, pickList, addButton, reduceButton, myMoney
    ''' 作業要求:( '''
    if pick != None:
        tmpAmount = amount
        if money < tmpAmount:
            tmpAmount = money
            disableAddButton()
        val[pick].set(val[pick].get() + tmpAmount)
        money -= tmpAmount
        myMoney.set(money)
        enableReduceButton()
    else:
        for i in pickList:
            tmpAmount = amount
            if money < tmpAmount:
                tmpAmount = money
                disableAddButton()
            val[i].set(val[i].get() + tmpAmount)
            money -= tmpAmount
            myMoney.set(money)
            enableReduceButton()
    
def reduce(amount=1, pick=None):
    global val, money, pickList, reduceButton, addButton, myMoney
    ''' 作業要求:( '''
    if pick != None:
        tmpAmount = amount
        if val[pick].get() <= tmpAmount:
            tmpAmount = val[pick].get()
        val[pick].set(val[pick].get() - tmpAmount)
        money += tmpAmount
        myMoney.set(money)
    else:
        for i in pickList:
            tmpAmount = amount
            if val[i].get() <= tmpAmount:
                tmpAmount = val[i].get()
            val[i].set(val[i].get() - tmpAmount)
            money += tmpAmount
            myMoney.set(money)
    
    if haveMoney():
        enableAddButton()

    disableReduceButton()
    for i in pickList:
        if val[i].get() > 0:
            enableReduceButton()

def setOddset():
    global iconAmount, oddset
    oddset = dict()
    oddsetTable = {
        '0.04': 50, 
        '0.08': 20,
        '0.11': 10,
        '0.15': 7,
        '0.18': 5,
        '0.22': 3,
        '0.30': 2,
        '1.00': 1
    }
    for key in list(iconAmount.keys()):
        occupancy = iconAmount[key] / SIZE
        for rate, value in oddsetTable.items():
            if occupancy < float(rate):
                oddset.setdefault(key, value)

main()