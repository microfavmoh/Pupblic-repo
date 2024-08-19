from tkinter.ttk import Combobox
from pynput import mouse
from pynput.keyboard import Listener, KeyCode
import tkinter
import threading
from time import sleep

clicking=False
Mouse=mouse.Controller()
check_dellay=0.00000000000000000000000000000000000000000000001
font_=("Product Sans",8)

screen=tkinter.Tk()
screen.geometry("400x400")
screen.resizable(False,False)
screen.title("autoclicker")
click_position_determiner=tkinter.IntVar()
click_repetition_determiner=tkinter.IntVar()
label_dellay=tkinter.Label(text="enter the dellay between clicks")
label_milliseconds=tkinter.Label(text="milliseconds")
label_seconds=tkinter.Label(text="seconds")
label_minutes=tkinter.Label(text="minutes")
label_hours=tkinter.Label(text="hours")
label_days=tkinter.Label(text="days")
milliseconds=tkinter.Entry(width=7)
seconds=tkinter.Entry(width=7)
minutes=tkinter.Entry(width=7)
hours=tkinter.Entry(width=7)
days=tkinter.Entry(width=7)
label_or=tkinter.Label(text="or")
clicks_per_second=tkinter.Entry(width=10)
clicks_per_second_label=tkinter.Label(text="clicks/s")
mouse_button_options_label=tkinter.Label(text="mouse button options")
mouse_button_label=tkinter.Label(text="mouse button")
mouse_button_options=Combobox(state="readonly",values=["left click","right click","middle click"],width=10)
mouse_button_options.current("0")
click_type_label=tkinter.Label(text="click type")
click_type_options=Combobox(state="readonly",values=["single click","double click"],width=10)
click_type_options.current("0")
cursor_position_label=tkinter.Label(text="cursor position")

def x_y_graber():
    screen.withdraw()
    def on_click(x,y,pressed,button):
        if pressed:
            x_value.delete(0,"end")
            y_value.delete(0,"end")
            x_value.insert("0",x)
            y_value.insert("0",y)
            screen.deiconify()
            return False
    listener=mouse.Listener(on_click=on_click)
    listener.start()
    
pick_position_button=tkinter.Button(text="pick position",command=x_y_graber)
x_label=tkinter.Label(text="X")
y_label=tkinter.Label(text="Y")
x_value=tkinter.Entry(width=4)
y_value=tkinter.Entry(width=4)
specific_position=tkinter.Radiobutton(text="specific position",value=1,variable=click_position_determiner)
mouse_position=tkinter.Radiobutton(text="mouse position",value=0,variable=click_position_determiner)
click_repetition_label=tkinter.Label(text="click repetition")
repeat_forever=tkinter.Radiobutton(text="repeat forever",value=0,variable=click_repetition_determiner)
repeat_specified_number_times=tkinter.Radiobutton(text="repeat specified number of times",value=1,variable=click_repetition_determiner)
specified_number_times=tkinter.Entry()
start_key_label=tkinter.Label(text="start key")
start_key=tkinter.Entry(width=2)
end_key_label=tkinter.Label(text="end key")
end_key=tkinter.Entry(width=2)

label_dellay.place(relx=0.3,rely=0.05)
label_milliseconds.place(relx=0.07,rely=0.1)
label_seconds.place(relx=0.275,rely=0.1)
label_minutes.place(relx=0.45,rely=0.1)
label_hours.place(relx=0.65,rely=0.1)
label_days.place(relx=0.85,rely=0.1)
milliseconds.place(relx=0.07,rely=0.15)
seconds.place(relx=0.275,rely=0.15)
minutes.place(relx=0.45,rely=0.15)
hours.place(relx=0.65,rely=0.15)
days.place(relx=0.85,rely=0.15)
label_or.place(relx=0.2,rely=0.2)
clicks_per_second.place(relx=0.07,rely=0.25)
clicks_per_second_label.place(relx=0.24,rely=0.25)
mouse_button_options_label.place(relx=0.65,rely=0.25)
mouse_button_label.place(relx=0.46,rely=0.3)
mouse_button_options.place(relx=0.65,rely=0.3)
click_type_label.place(relx=0.46,rely=0.36)
click_type_options.place(relx=0.65,rely=0.36)
cursor_position_label.place(relx=0.07,rely=0.41)
mouse_position.place(relx=0.07,rely=0.46)
specific_position.place(relx=0.07,rely=0.51)
pick_position_button.place(relx=0.34,rely=0.51)
x_label.place(relx=0.52,rely=0.51)
x_value.place(relx=0.56,rely=0.51)
y_label.place(relx=0.635,rely=0.51)
y_value.place(relx=0.675,rely=0.51)
click_repetition_label.place(relx=0.07,rely=0.59)
repeat_forever.place(relx=0.07,rely=0.64)
repeat_specified_number_times.place(relx=0.07,rely=0.69)
specified_number_times.place(relx=0.08,rely=0.74)
start_key_label.place(relx=0.07,rely=0.84)
start_key.place(relx=0.19,rely=0.84)
end_key_label.place(relx=0.25,rely=0.84)
end_key.place(relx=0.37,rely=0.84)
for widget in screen.winfo_children():
    widget.configure(font=font_)
    if str(widget).startswith(".!entry"):
        if widget["width"]==10:
            widget.insert("0",100)
        if widget["width"]==2:
            widget.insert("0","h")
        else:
            if widget["width"]!=10:
                widget.insert("0",0)

def on_press(key):
    global clicking,dellay,mouse_button,click_type,x,y,n
    start_key_=KeyCode(char=start_key.get())
    end_key_=KeyCode(char=end_key.get())
    if key==start_key_:
        for entry in [milliseconds,seconds,minutes,hours,days,clicks_per_second]:
            if entry.get()=='':
                entry.insert("0",0)

        try:
            dellay=int(milliseconds.get())/1000
            dellay+=int(seconds.get())
            dellay+=int(minutes.get())*60
            dellay+=int(hours.get())*3600
            dellay+=int(days.get())*86400
        except ValueError:
            return None
        
        if clicks_per_second.get()!="0" and dellay!=0:
            return None
        elif clicks_per_second.get()!="0":
            dellay=1/int(clicks_per_second.get())

        if dellay==0:
            return None

        mouse_button=mouse_button_options.get()
        if mouse_button=="left click":
            mouse_button=mouse.Button.left
        elif mouse_button=="right click":
            mouse_button=mouse.Button.right
        else:
            mouse_button=mouse.Button.middle

        if click_type_options.get()=="single click":
            click_type=1
        else:
            click_type=2
        if click_position_determiner.get()==1:
            try:
                x=int(x_value.get())
                y=int(y_value.get())
            except ValueError:
                return None
        else:
            x="mouse"

        if click_repetition_determiner.get()==1:
            try:
                n=int(specified_number_times.get())
            except ValueError:
                return None
        else:
            n=float("inf")

        if start_key_==end_key_:
            clicking=not clicking
    if start_key_!=end_key_:
        if key==start_key_:
            clicking=True
        elif key==end_key_:
            clicking=False

def auto_clicker():
    number_clicks=0
    global clicking
    while True:
        if clicking and number_clicks<n:
            if x=="mouse":
                Mouse.click(mouse_button,count=click_type)
            else:
                Mouse.position=(x,y)
                Mouse.click(mouse_button,count=click_type)
            sleep(dellay)
            number_clicks+=1
        else:
            clicking=False
            number_clicks=0
        sleep(check_dellay)

auto_clicker_thread=threading.Thread(target=auto_clicker)
auto_clicker_thread.start()
listener=Listener(on_press=on_press)
listener.start()
screen.mainloop()