from tkinter import *
from datetime import datetime
import time

win = Tk() # 창 생성
win.geometry("900x700")
win.title("Uptime Manager by 유주열")

label=Label(win,font=3,height=2,text="웹서비스 모니터링 매니져")
label.config(fg='blue',anchor=S)
label.pack()

def url_start():
    btn.config(text=datetime.now())

def setTextInput(text):
    global lastline
    listbox.insert(lastline, text+'\n')
    
def listbox_insert():
    global lastline
    for line in range(1,1001):
        listbox.insert(line, str(line) + "/1000")
        lastline = line
    
btn = Button(win) # 버튼 생성
btn.config(text="모니터링 시작")
btn.config(height=2)
btn.config(command=listbox_insert)
btn.pack(side='bottom') # 버튼 배치

#로그 출력 확인용
frame=Frame(win)
scrollbar=Scrollbar(frame)
scrollbar.pack(side="right", fill="y")
listbox=Listbox(frame, yscrollcommand = scrollbar.set)
listbox.config(width=700, height=40)
listbox.pack(side="left")
scrollbar["command"]=listbox.yview
frame.pack()

# textarea = Text(win, width=850, height=40)
# textarea.pack()

#빈줄
label=Label(win,font=3,height=2,text="")
label.config(fg='blue',anchor=S)
label.pack()


btnSet = Button(win, 
                height=1, 
                width=10, 
                text="Set", 
                command=lambda:setTextInput("new content"))
btnSet.pack()






win.mainloop() # 창 실행
