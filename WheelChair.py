from tkinter import *
import tkinter
from PIL import ImageTk, Image
import os
from subprocess import call
import serial
import pyautogui 

kb = tkinter.Tk()

button_small = [
'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p','7','8','9','<--',
'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l','?','4','5','6','CAPS',
'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.','!','1','2','3','\___/',
]
button_caps = [
'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O','P','7','8','9','<--',
'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L','?','4','5','6','CAPS',
'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.','!','1','2','3','\___/',
]


class globals():
    caps=False

def select(value):
    if value == "<--":
        entry.delete(len(entry.get())-1,tkinter.END)
    elif value == "\___/":
        entry.insert(tkinter.END, ' ')
    elif value == "CAPS":
        if globals.caps==True:
            AllSmall()
        else:
            AllCaps()
    elif value == "Say it out loud":
        ToSpeech(entry.get())
        entry.delete(0,END)
    elif value == "Clear all":
        entry.delete(0,END)
    else :
        entry.insert(tkinter.END,value)
    print (kb.winfo_pointerxy())
   # print(pyautogui.position())



def ToSpeech(value):
    print (kb.winfo_pointerxy())
    tospeech = 'echo "'+str(value)+'" | festival --tts' 
    os.system(tospeech)  


def AllCaps():
    varRow = CurrentRow+1
    varColumn = 0

    for button in button_caps:

        command = lambda x=button: select(x)
        
        if button == "SPACE" or button == "SHIFT" or button == "< Del":
            tkinter.Button(kb,text= button,width=7, bg="#3c4987", fg="#ffffff",
                activebackground = "#ffffff", activeforeground="#3c4987", relief='raised', padx=0,
                pady=0, bd=1,command=command,font=("Courier", 12)).grid(row=varRow,column=varColumn)

        else:
            tkinter.Button(kb,text= button,width=5, bg="#3c4987", fg="#ffffff",
                activebackground = "#ffffff", activeforeground="#3c4987", relief='raised', padx=0,
                pady=0, bd=1,command=command,font=("Courier", 12)).grid(row=varRow,column=varColumn)


        varColumn +=1 

        if varColumn > 13:
            varColumn = 0
            varRow+=1
    globals.caps=True

def AllSmall():
    tkinter.Label(kb,text=" ",bg="black",fg="black").grid(column=2,row=CurrentRow+1,rowspan=6)
    varRow = CurrentRow+1
    varColumn = 0

    for button in button_small:
        command = lambda x=button: select(x)
        
        if button == "SPACE" or button == "SHIFT" or button == "< Del":
            tkinter.Button(kb,text= button,width=7, bg="#3c4987", fg="#ffffff",
                activebackground = "#ffffff", activeforeground="#3c4987", relief='raised', padx=0,
                pady=0, bd=1,command=command,font=("Courier", 12)).grid(row=varRow,column=varColumn)

        else:
            tkinter.Button(kb,text= button,width=5, bg="#3c4987", fg="#ffffff",
                activebackground = "#ffffff", activeforeground="#3c4987", relief='raised', padx=0,
                pady=0, bd=1,command=command,font=("Courier", 12)).grid(row=varRow,column=varColumn)


        varColumn +=1 
        if varColumn > 13:
            varColumn = 0
            varRow+=1
    globals.caps=False

def Phrase():
    varRow = CurrentRow+1
    varColumn = 0
    phrases = ['Hello!', 'Yes', 'No', 'What?', 'Thank you', 'Bye','Help me!']
    for button in phrases:
        command = lambda x=button: ToSpeech(x)
        tkinter.Button(kb,text= button, bg="#3c4987", fg="#ffffff",
                activebackground = "#ffffff", activeforeground="#3c4987", relief='raised', padx=0,
                pady=0, bd=1,command=command,font=("Courier", 12)).grid(row=varRow,column=varColumn,columnspan=2,sticky='we')   
        varColumn +=2

def OtherButtons():
    varRow = CurrentRow+1
    varColumn = 0
    options=['Say it out loud','Clear all']
    for button in options:
        command = lambda x=button: select(x)
        tkinter.Button(kb,text= button, bg="#3c4987", fg="#ffffff",
                activebackground = "#ffffff", activeforeground="#3c4987", relief='raised', padx=0,
                pady=0, bd=1,command=command,font=("Courier", 12)).grid(row=varRow,column=varColumn,columnspan=7,sticky='we')
        varColumn +=7

AttenLvl=0
MedLvl=0
Blink=True
def UpdateLvls():
    global AttenLvl
    global MedLvl
    global Blink
    c=0
    values=[]
    ser = serial.Serial('/dev/ttyACM0', 57600)
    while 1:
        string_data = ser.readline()
        for char in string_data:
            c = c+1
            if (char == '$'):
                for i in range(3):
                    values.append(string_data[c+i])
    def sum(values):
        val=""
        for value in values:
            val = val+value
        return val
    AttenLvl = int(sum(values[0:3]))
    MedLvl = int(sum(values[3:6]))
    Blink = int(sum(values[6:9]))
	# global AttenLvl
	# AttenLvl+=1
	# global MedLvl
	# MedLvl+=1
	# global Blink
	# Blink=not Blink
    global Green
    global Red
    MedLvlLab['text']=MedLvl
    AttenLvlLab['text']=AttenLvl
    kb.after(1000,UpdateLvls)
    if(Blink==True):
        pyautogui.click()
        BlinkIndi['image']=Green
    else:
        BlinkIndi['image']=Red

def main():
    kb.title("BCI_WheelChair")
    kb.configure(background='black')
    kb.resizable(0,0)
    global CurrentRow
    global CurrentCol
    CurrentRow=-1
    CurrentCol=-1
    Title=ImageTk.PhotoImage(Image.open("BCI-WheelChair.png"))
    tkinter.Label(kb,image=Title,bg="black").grid(row=CurrentRow+1,column=CurrentCol+1,columnspan=14)
    CurrentRow+=1
    tkinter.Label(kb,height=1,bg="black",fg="black").grid(column=CurrentCol+1,row=CurrentRow+1,columnspan=14)
    CurrentRow+=1
    img2 = ImageTk.PhotoImage(Image.open("ATTENTION.png"))
    tkinter.Label(kb,image=img2,bg="black").grid(row=CurrentRow+1,column=CurrentCol+1,columnspan=6)
    global AttenLvlLab
    AttenLvlLab=tkinter.Label(kb,text="0",bg="black",fg="white",font=("Courier", 16))
    AttenLvlLab.grid(row=CurrentRow+1,column=6)
    img3 = ImageTk.PhotoImage(Image.open("CALMNESS.png"))
    tkinter.Label(kb,image=img3,bg="black").grid(row=CurrentRow+1,column=8,columnspan=4)
    global MedLvlLab
    MedLvlLab=tkinter.Label(kb,text="0",bg="black",fg="white",font=("Courier", 16))
    MedLvlLab.grid(row=CurrentRow+1,column=12,columnspan=2)
    CurrentRow+=1
    tkinter.Label(kb,text="",bg="black",fg="black").grid(column=CurrentCol+1,row=CurrentRow+1,columnspan=14)
    CurrentRow+=1
    img1 = ImageTk.PhotoImage(Image.open("BLINK.png"))
    tkinter.Label(kb,image=img1,bg="black").grid(row=CurrentRow+1,column=4,columnspan=7)
    CurrentRow+=1
    global Red
    global Green
    Red = ImageTk.PhotoImage(Image.open("Red.png"))
    Green = ImageTk.PhotoImage(Image.open("Green.png"))
    global BlinkIndi
    BlinkIndi=tkinter.Label(kb,image=Green,bg="black")
    BlinkIndi.grid(row=CurrentRow+1,column=4,columnspan=7)
    CurrentRow+=1
    tkinter.Label(kb,text="",bg="black",fg="black").grid(column=CurrentCol+1,row=CurrentRow+1,columnspan=14)
    CurrentRow+=1
    your_text = ImageTk.PhotoImage(Image.open("Your-text.png"))
    tkinter.Label(kb,image=your_text,bg="black").grid(column=CurrentCol+1,row=CurrentRow+1,columnspan=3)
    CurrentCol+=3
    global entry
    entry = Entry(kb)
    entry.grid(row=CurrentRow+1,column=CurrentCol+1,columnspan=11,sticky='we',padx=10)
    CurrentRow+=1
    tkinter.Label(kb,text="  ",bg="black",fg="black").grid(column=CurrentCol+1,row=CurrentRow+1,columnspan=17)
    CurrentRow+=1
    Phrase()
    CurrentRow+=1
    AllSmall()
    CurrentRow+=3
    OtherButtons()
    CurrentRow=9
    UpdateLvls()
    kb.mainloop()
main()