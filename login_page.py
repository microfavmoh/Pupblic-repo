from tkinter import *
from os import getenv
from os.path import join,exists
from json import load,dumps
from hashlib import sha256

path_:str=join(getenv('APPDATA'),'user_data.json')
screen=Tk()
screen.attributes("-fullscreen",True)
screen.title("place holder title")
font=("Product Sans",10)
font_warning=("Product Sans",15,"bold")
show_password:bool=False

def show_password_func()->None:
    global show_password
    show_password=not show_password
    if show_password:
        show_password_button.configure(text="hide password")
        password_entry.configure(show="")
    else:
        show_password_button.configure(text="show password")
        password_entry.configure(show="x")

def throw_warning(text_:str)->None:
    for widget in screen.winfo_children():
        if widget not in widgets:
            widget.destroy()
    warning_error=Label(text=f'error: {text_}')
    warning_error.configure(font=font_warning,fg="red")
    warning_error.place(relx=0.5,rely=0.45,anchor="center")

def text_encrypter(string:str)->str:
    return sha256(string.encode("utf-8")).hexdigest()
    
username_entry=Entry(screen)
password_entry=Entry(screen,show='x')
show_password_button=Button(bg='yellow',text='show password',command=show_password_func,border=0)
text_username=Label(text="enter your username")
text_password=Label(text="enter your password")

#this function checks input when the user tries to sign up
def signup_check()->None:
    global username_entry,password_entry,path_
    username=username_entry.get()
    password=password_entry.get()
    if not len(username):
        throw_warning("enter your username")
        return None

    for char in username:
        if char.isspace():
            throw_warning("username cannot contain spaces")
            return None

    if len(username)<3:
        throw_warning("username cannot be shorter than three characters")
        return None

    if len(username)>15:
        throw_warning("username cannot be longer than fifteen characters")
        return None    

    if exists(path_):
        with open(path_,'r') as file:
            file=load(file)
            if text_encrypter(username) in file:
                throw_warning("username already exists")
                return None

    if not len(password):
        throw_warning("enter your password")
        return None
        
    for char in password:
        if char.isspace():
            throw_warning("password cannot contain spaces")
            return None
        
    if len(password)<12:
        throw_warning("password cannot be shorter than twelve characters")
        return None

    num_exsitis:bool=False
    for char in password:
        if char.isnumeric():
            num_exsitis=True
            break

    if not num_exsitis:
        throw_warning("password must contain atleast one number")
        return None

    sum_upper:bool=False
    for char in password:
        if char.isupper():
            sum_upper=True
            break

    if not sum_upper:
        throw_warning("password must contain uppercase characters")
        return None

    sum_lower:bool=False
    for char in password:
        if char.islower():
            sum_lower=True
            break

    if not sum_lower:
        throw_warning("password must contain lowercase characters")
        return None
        
    sum_special:bool=False
    special_characters =['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
    		            ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|',
		                '}', '~']
    for char in password:
        if char in special_characters:
            sum_special=True
            break

    if not sum_special:
        throw_warning("password must contain a special character")
        return None

    if not exists(path_):
        user_data={text_encrypter(username):text_encrypter(password)}
        with open(path_,'w') as file:
            file.write(dumps(user_data,indent=4))
    else:
        with open(path_,'r') as file:
            file_data=load(file)
            file_data[text_encrypter(username)]=text_encrypter(password)
        with open(path_,'w') as file:
            file.write(dumps(file_data,indent=4)) 
    print("Signed in")

#this is the signup button which appears on the first screen
button=Button(command=signup_check,background="yellow",text="Sign up",bd=0)

#the function bellow checks input when
#the user tries to login
def login_check()->None:
    username=username.get()
    password=password.get()
    if not len(username):
        throw_warning("enter your username")
        return None
    if not len(password):
        throw_warning("enter your password")
        return None
    with open(path_,'r') as file:
        file=load(file)
        if text_encrypter(username) not in file:
            throw_warning("username doesn't exsist")
            return None
        if text_encrypter(password)!=file.get(text_encrypter(username)):
            throw_warning("iccorect password")
            return None
        else:
            print("logged in")

#this function is used when you press the login button 
def login()->None:
    if exists(path_):
        button.configure(text='Login',command=login_check)
        #this function is called when you press the sign up buttton in the login screen
        def logintosignup()->None:
            button.configure(text='Signup',command=signup_check)
            button_login.configure(text='Login',command=login)
        button_login.configure(text='signup',command=logintosignup)
    else:
        throw_warning("No accounts exists")

#this is the login button which appears at the top right corner of the screen
button_login=Button(command=login,background="yellow",text="Login",bd=0)

text_username.place(relx=0.5,rely=0.2,anchor="center")
text_password.place(relx=0.5,rely=0.3,anchor="center")
username_entry.place(relx=0.5,rely=0.24,anchor="center")
password_entry.place(relx=0.5,rely=0.34,anchor="center")
show_password_button.place(relx=0.6,rely=0.34,anchor="center")
button.place(relx=0.5,rely=0.4,anchor="center")
button_login.place(relx=0.95,rely=0.04)

widgets=screen.winfo_children()
for widget in widgets:
    widget.configure(font=font)
    
screen.mainloop()