from tkinter import *
import os
import json
import hashlib

class main:
    cwd=os.getcwd()
    path_=os.path.join(cwd,'user_data.json')
    screen=Tk()
    screen.attributes("-fullscreen",True)
    screen.title("place holder title")
    font_=("Product Sans",10)
    font_warning=("Product Sans",15,"bold")
    username=Entry(screen)
    password=Entry(screen)
    text_username=Label(text="enter your username")
    text_password=Label(text="enter your password")
    text_username.configure(font=font_)
    text_password.configure(font=font_)
    text_username.place(relx=0.5,rely=0.2,anchor="center")
    text_password.place(relx=0.5,rely=0.3,anchor="center")
    username.place(relx=0.5,rely=0.24,anchor="center")
    password.place(relx=0.5,rely=0.34,anchor="center")
    def throw_warning(text_):
        for widget in main.screen.winfo_children():
            widgets=['.!entry','.!entry2','.!label','.!label2','.!button','.!button2']
            if str(widget) not in widgets:
                widget.destroy()
            else:
                pass  
            warning_error=Label(text=text_)
            warning_error.configure(font=main.font_warning,fg="red")
            warning_error.place(relx=0.5,rely=0.45,anchor="center")
    def text_encrypter(string):
            string=string.encode("utf-8")
            return hashlib.sha256(string).hexdigest()
    def value_checker():
        username=main.username
        password=main.password
        username=str(username.get())
        password=str(password.get())
        path_=main.path_
        if len(username)==0:
            main.throw_warning("enter your username")
            return None
        else:
            pass

        for char in username:
            if char.isspace()==True:
                main.throw_warning("username cannot contain spaces")
                return None
            else:
                pass

        if len(username)<3:
            main.throw_warning("username cannot be shorter than three characters")
            return None
        else:
            pass

        if len(username)>15:
            main.throw_warning("username cannot be longer than fifteen characters")
            return None    
        else:
            pass

        if os.path.exists(path_)==True:
            with open(path_,'r') as file:
                file=json.load(file)
                if main.text_encrypter(username) in file:
                    main.throw_warning("username already exists")
                    return None
                else:
                    pass
        else:
            pass
        if len(password)==0:
            main.throw_warning("enter your password")
            return None
        else:
            pass
        for char in password:
            if char.isspace()==True:
                main.throw_warning("password cannot contain spaces")
                return None
            else:
                pass
        number_counter=0
        for char in password:
            if char.isnumeric()==True:
                number_counter+=1
                break
            else:
                pass
        if number_counter==0:
            main.throw_warning("password must contain atleast one number")
            return None
        else:
            pass  
        if len(password)<12:
            main.throw_warning("password cannot be shorter than twelve characters")
            return None
        else:
            pass
        sum_upper=0
        for i in password:
            if i.isupper()==True:
                sum_upper+=1
            else:
                pass
        if sum_upper==0:
            main.throw_warning("password must contain uppercase characters")
            return None
        else:
            pass
        sum_lower=0
        for i in password:
            if i.islower()==True:
                sum_lower+=1
            else:
                pass
        if sum_lower==0:
            main.throw_warning("password must contain lowercase characters")
            return None
        else:
            pass
        if os.path.exists(path_)==False:
            with open(path_,'w') as file:
                user_data={main.text_encrypter(username):main.text_encrypter(password)}
                file.write(json.dumps(user_data,indent=4))
                file.close()
        else:
            with open(path_,'r+b') as file:
                pass
    button=Button(command=value_checker,background="yellow",text="Create account",bd=0)
    button.configure(font=font_)
    button.place(relx=0.5,rely=0.4,anchor="center")
    def check():
        username=main.username
        password=main.password
        username=username.get()
        password=password.get()
        with open(main.path_,'r') as file:
            file=json.load(file)
            if main.text_encrypter(username) not in file:
                main.throw_warning("username doesn't exsist")
                return None
            else:
                pass
            if main.text_encrypter(password)!=file.get(main.text_encrypter(username)):
                main.throw_warning("iccorect password")
                return None
            else:
                print("logged in")
    def login():
        destroyed_widgets=['.!button','.!button2']
        for widget in main.screen.winfo_children():
            if str(widget) in destroyed_widgets:
                widget.destroy()
            else:
                pass
        button=Button(command=main.check,background="yellow",text="Login",bd=0)
        button.configure(font=main.font_)
        button.place(relx=0.5,rely=0.4,anchor="center")
    button_login=Button(command=login,background="yellow",text="Login",bd=0)
    button_login.configure(font=font_)
    button_login.place(relx=0.95,rely=0.04)
main.screen.mainloop()