from time import sleep
from tkinter.ttk import Combobox
from pynput.mouse import Controller, Listener as mouse_listener, Button as mouse_button
from pynput.keyboard import KeyCode, Listener
from tkinter import *
from tkinter.messagebox import showerror
from threading import Thread

mouse : Controller = Controller()
clicking:bool = False
autoclicking:bool = True
redirect_input : bool = False
specified_positions_list:list[tuple[int]] = []

screen=Tk()
screen.geometry("400x400")
screen.resizable(False,False)
screen.title("Autoclicker")
click_position_determiner=IntVar()
click_repetition_determiner=IntVar()
label_dellay=Label(text="enter the dellay between clicks")
label_milliseconds=Label(text="milliseconds")
label_seconds=Label(text="seconds")
label_minutes=Label(text="minutes")
label_hours=Label(text="hours")
label_days=Label(text="days")
milliseconds=Entry(width=7)
seconds=Entry(width=7)
minutes=Entry(width=7)
hours=Entry(width=7)
days=Entry(width=7)
label_or=Label(text="or")
clicks_per_second=Entry(width=10)
clicks_per_second_label=Label(text="clicks/s")
mouse_button_options_label=Label(text="mouse button options")
mouse_button_label=Label(text="mouse button")
mouse_button_options=Combobox(state="readonly",
                              values=["Left click","Right click","Middle click"],
                              width=10)
click_type_label=Label(text="click type")
click_type_combobox=Combobox(state="readonly",
                    values=["single click","double click"],
                    width=10)
cursor_position_label=Label(text="cursor position")
specific_positions=Radiobutton(text="specific positions",
                               value=1,
                               variable=click_position_determiner)

def pick_position()->None:
    screen.withdraw()
    def on_click(x,y,button,pressed)->None:
        if pressed:
            specified_positions_list.append((x,y))
            screen.deiconify()
            return False
    mouse_listener(on_click=on_click).start()

pick_position_button=Button(text="pick position",
                            command=pick_position)
clear_positions_button=Button(text="clear configuration",
                              command=specified_positions_list.clear)
mouse_position=Radiobutton(text="mouse position",
                           value=0,
                           variable=click_position_determiner)
click_repetition_label=Label(text="click repetition")
repeat_forever=Radiobutton(text="repeat forever",
                           value=0,
                           variable=click_repetition_determiner)
repeat_specified_number_times=Radiobutton(text="repeat specified number of times",
                                          value=1,
                                          variable=click_repetition_determiner)
specified_number_times=Entry()
hotkey_label=Label(text="hotkey")
hotkey_entry=Entry(width=2)
def inputdirector()->None: redirect_input = not redirect_input
hotkey_entry.bind("FocusIn")
hotkey_entry.bind("FocusOut",)
def typing_mode()->None:
    global clicking,autoclicking
    autoclicking = not autoclicking
    clicking = False
    stop_button.configure(text="enable typing mode") if autoclicking else stop_button.configure(text="disable typing mode")
stop_button=Button(text="enable typing mode",
                   command=typing_mode)

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
click_type_combobox.place(relx=0.65,rely=0.36)
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

for widget in screen.winfo_children():
    widget.configure(font = ("Product Sans", 8))

hotkey_entry.insert(index="0",string=".")
clicks_per_second.insert(index="0",string="10")
mouse_button_options.set("Left click")
click_type_combobox.set("single click")

def keyboardmanager(key):
    global clicking
    if autoclicking and key == KeyCode(char=hotkey_entry.get()):
        clicking = not clicking
        if clicking:
            Thread(target=autoclicker).start()

def autoclicker():
    global clicking
    dellay:float=0.0
    for entry,multiplier in [(milliseconds,0.001),(seconds,1),(minutes,60),(hours,3600),(days,86400)]:
        try:
            dellay+=float(entry.get())*multiplier
        except ValueError:
            continue

    if not dellay:
        try:
            dellay+=1.0/float(clicks_per_second.get())
        except (ValueError,ZeroDivisionError):
            showerror("Error", "Enter a dellay") 
            clicking=False
            return None
    dict_options:dict={"Left click":mouse_button.left,"Right click":mouse_button.right,
                       "Middle click":mouse_button.middle,"single click":1,"double click":2}
    try:
        button:mouse_button=dict_options[mouse_button_options.get()]
        click_type:int=dict_options[click_type_combobox.get()]
    except KeyError:
        showerror("Error", "Fill the mouse button options") 
        clicking = False
        return None
    try:
        click_limit=int(specified_number_times) if click_repetition_determiner.get() else float("inf")      
    except ValueError:
        showerror("Error", "Enter the number of clicks") 
        clicking = False
        return None
    num_clicks:int=0
    specified_positions_list_loc = specified_positions_list
    if (click_position_determiner_get:=click_position_determiner.get()) and not specified_positions_list_loc :
        showerror("Error", "Specify the clicking positions")
        clicking = False
        return None
    while clicking and num_clicks < click_limit:
        if specified_positions_list_loc and click_position_determiner_get:
            for position in specified_positions_list_loc:
                mouse.position=position
                mouse.click(button,click_type)
                num_clicks+=1
                sleep(dellay)
        else:
            mouse.click(button,click_type)
            num_clicks+=1
            sleep(dellay)
            
Listener(on_press=keyboardmanager).start()
mainloop()