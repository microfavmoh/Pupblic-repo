from time import sleep
from tkinter.ttk import Combobox
from pynput.mouse import Controller,Listener as mouse_listener,Button
from pynput.keyboard import Listener,KeyCode
import tkinter
from threading import Thread

clicking:bool=False
auto_clicking:bool=True
mouse=Controller()
font:tuple=("Product Sans",8)
specified_positions_set:set[tuple[int]]={}

def clear_config()->None:
    specified_positions_set.clear()

def stop_auto_clicker()->None:
    global auto_clicking,clicking
    auto_clicking=not auto_clicking
    clicking=False
    if auto_clicking:
        stop_button.configure(text="enable typing mode")
    else:
        stop_button.configure(text="disable typing mode") 

def x_y_graber()->None:
    screen.withdraw()
    def on_click(x,y,pressed,button):
        if pressed:
            specified_positions_set.add((x,y))
            screen.deiconify()
            return False
    listener=mouse_listener(on_click=on_click)
    listener.start()
    
screen=tkinter.Tk()
screen.geometry("400x400")
screen.resizable(False,False)
screen.title("Autoclicker")
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
click_type_label=tkinter.Label(text="click type")
click_type_options=Combobox(state="readonly",values=["single click","double click"],width=10)
cursor_position_label=tkinter.Label(text="cursor position")
specific_positions=tkinter.Radiobutton(text="specific positions",value=1,variable=click_position_determiner,command=x_y_graber)
pick_position_button=tkinter.Button(text="pick position",command=x_y_graber)
clear_positions_button=tkinter.Button(text="clear configuration",command=clear_config)
mouse_position=tkinter.Radiobutton(text="mouse position",value=0,variable=click_position_determiner)
click_repetition_label=tkinter.Label(text="click repetition")
repeat_forever=tkinter.Radiobutton(text="repeat forever",value=0,variable=click_repetition_determiner)
repeat_specified_number_times=tkinter.Radiobutton(text="repeat specified number of times",value=1,variable=click_repetition_determiner)
specified_number_times=tkinter.Entry()
hotkey_label=tkinter.Label(text="hotkey")
hotkey_entry=tkinter.Entry(width=2)
stop_button=tkinter.Button(text="enable typing mode",command=stop_auto_clicker)

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
specific_positions.place(relx=0.07,rely=0.51)
pick_position_button.place(relx=0.34,rely=0.51)
clear_positions_button.place(relx=0.55,rely=0.51)
click_repetition_label.place(relx=0.07,rely=0.61)
repeat_forever.place(relx=0.07,rely=0.66)
repeat_specified_number_times.place(relx=0.07,rely=0.71)
specified_number_times.place(relx=0.08,rely=0.76)
hotkey_label.place(relx=0.07,rely=0.84)
hotkey_entry.place(relx=0.19,rely=0.84)
stop_button.place(relx=0.47,rely=0.84)

mouse_button_options.current("0")
click_type_options.current("0")
clicks_per_second.insert("0",10)
hotkey_entry.insert("0",".")
hotkey_entry.bind("<FocusIn>")
for widget in screen.winfo_children():
    widget.configure(font=font)
    if isinstance(widget,tkinter.Entry) and not widget.get():
        widget.insert("0",0)

def on_press(key)->None:
    if auto_clicking:
        start_key=KeyCode(char=hotkey_entry.get())
        global clicking
        if key==start_key:
            clicking=not clicking
        if clicking:
            auto_clicker_thread=Thread(target=auto_clicker)
            auto_clicker_thread.start()

def auto_clicker()->None:
    global clicking
    for entry in {milliseconds,seconds,minutes,hours,days,clicks_per_second}:
        if not entry.get() or entry.get().isspace():
            entry.delete("0","end")
            entry.insert("0",0)
    try:
        dellay:float=float(milliseconds.get())*0.001
        dellay+=float(seconds.get())
        dellay+=float(minutes.get())*60
        dellay+=float(hours.get())*3600
        dellay+=float(days.get())*86400
    except ValueError:
        pass

    if dellay not in locals() or not dellay:
        try:
            dellay:float=1/float(clicks_per_second.get())
        except ValueError:
            clicking=False
            return None

    dict_options:dict={"left click":Button.left,"right click":Button.right,"middle click":Button.middle,
                       "single click":1,"double click":2}
    mouse_button:Button=dict_options.get(mouse_button_options.get())
    click_type:int=dict_options.get(click_type_options.get())

    if click_repetition_determiner.get()==1:
        try:
            click_limit=int(specified_number_times.get())
        except ValueError:
            clicking=False
            return None
    else:
        click_limit=float("inf")

    specified_positions_set_local=specified_positions_set
    click_position_determiner_local=click_position_determiner

    number_clicks=0
    while clicking and number_clicks<click_limit:
        if click_position_determiner_local or not specified_positions_set_local:
            mouse.click(mouse_button,count=click_type)
        else:
            for position in specified_positions_set_local:
                mouse.position=position
                mouse.click(mouse_button,count=click_type)
        sleep(dellay)
        number_clicks+=1
    else:
        clicking=False
        return None
            
listener=Listener(on_press=on_press)
listener.start()
print(screen.focus_get())