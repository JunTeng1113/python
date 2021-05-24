from tkinter import *
from random import randint
import os

size = 24 #4的倍數

array = None
displayLabel = None
GoButton = None
root = Tk()
print(os.path.dirname(__file__) + "\Photos")
image_path = os.path.join(os.path.dirname(__file__), 'apple.png')
photo = [PhotoImage(file=os.path.join(os.path.dirname(__file__) + "\Photos", 'apple.png')),
         PhotoImage(file=os.path.join(os.path.dirname(__file__) + "\Photos", 'betelnut.png')),
         PhotoImage(file=os.path.join(os.path.dirname(__file__) + "\Photos", 'double7.png')),
         PhotoImage(file=os.path.join(os.path.dirname(__file__) + "\Photos", 'grape.png')),
         PhotoImage(file=os.path.join(os.path.dirname(__file__) + "\Photos", 'orange.png')),
         PhotoImage(file=os.path.join(os.path.dirname(__file__) + "\Photos", 'ring.png')),
         PhotoImage(file=os.path.join(os.path.dirname(__file__) + "\Photos", 'star.png')),
         PhotoImage(file=os.path.join(os.path.dirname(__file__) + "\Photos", 'watermelon.png'))]
def main():
    global array ;array = [0 for i in range(size)]
    global root
    root.title("麻仔台")
    MAX_WIDTH = 60
    MAX_HEIGHT = 60


    '''
    建立BUTTON
    '''
    for i in range(0, size):
        btnF = Frame(root, width=MAX_WIDTH, height=MAX_HEIGHT, bg="white")
        btnF.pack_propagate(0)
        print(rectangular_ambulatory_plane(size, i))
        btnF.grid(row=rectangular_ambulatory_plane(size, i)[1], column=rectangular_ambulatory_plane(size, i)[0])
        array[i] = Button(btnF, text=str(i+1), bg="white", image=photo[randint(0, len(photo)-1)])
        array[i].pack(expand=1, fill=BOTH)
        
    '''
    建立GO BUTTON
    '''
    btnF = Frame(root, width=MAX_WIDTH, height=MAX_HEIGHT, bg="white")
    btnF.pack_propagate(0)
    btnF.grid(row=size // 4 // 2, column=size // 4 // 2)
    global GoButton
    GoButton = Button(btnF, text="GO", bg="white", command=start)
    GoButton.pack(expand=1, fill=BOTH)
    
    '''
    建立LABEL
    '''
    btnF = Frame(root, width=MAX_WIDTH, height=MAX_HEIGHT, bg="white")
    btnF.pack_propagate(0)
    btnF.grid(row=size // 4 // 2+1, column=size // 4 // 2)
    global displayLabel
    displayLabel = Label(btnF, text="TEST", bg="white")
    displayLabel.pack(expand=1, fill=BOTH)
    
    
    root.mainloop()
    
def formula(sec):
    return 1.5 * (1 - sec / (sec+20)) ** 5

def start():
    return countdown(randint(1, size*2) + size*4)

from threading import Timer
count = 0
def countdown(sec):
    global GoButton ; GoButton.config(text="Playing", state="disable")
    global array
    global count
    print(sec)
    if sec > 0:
        array[(count+size-1)%size].config(bg="white")
        array[(count+size)%size].config(bg="red")
        global displayLabel ; displayLabel.config(image=array[(count+size)%size]['image'])
        count = (count + 1) % size
        if sec > 5:
            return Timer(formula(sec), countdown, [sec-1]).start()
        else:
            return Timer(formula(sec), countdown, [sec-1]).start()
    else:
        return GoButton.config(text="GO", state='normal')
    
def rectangular_ambulatory_plane(size, number):
    if size % 4 == 0:
        if (number / (size // 4)) < 1: return [(number % (size // 4)), 0]
        elif (number / (size // 4)) < 2: return [(size // 4), (number % (size // 4))] 
        elif (number / (size // 4)) < 3: return [((size // 4) - (number % (size // 4))), (size // 4)]
        elif (number / (size // 4)) < 4: return [0, ((size // 4) - (number % (size // 4)))] 
    else:
        return 0
    
main()

