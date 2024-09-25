from tkinter import *
from os import getenv
from os.path import join,exists
from json import load,dumps
from hashlib import sha256

class main:
    path_=join(getenv('APPDATA'),'user_data.json')
    screen=Tk()
    screen.attributes("-fullscreen",True)
    screen.title("place holder title")
    font_=("Product Sans",10)
    font_warning=("Product Sans",15,"bold")

    show_password=False
    def show_password_func():
        main.show_password=not main.show_password
        if main.show_password:
            main.show_password_button.configure(text="hide password")
            main.password.configure(show="")
        else:
            main.show_password_button.configure(text="show password")
            main.password.configure(show="x")

    def throw_warning(text_):
        for widget in main.screen.winfo_children():
            if widget not in main.widgets:
                widget.destroy()
            else:
                pass
        warning_error=Label(text=f'error: {text_}')
        warning_error.configure(font=main.font_warning,fg="red")
        warning_error.place(relx=0.5,rely=0.45,anchor="center")

    def text_encrypter(string):
        string=string.encode("utf-8")
        return sha256(string).hexdigest()
    
    username=Entry(screen)
    password=Entry(screen,show='x')
    show_password_button=Button(bg='yellow',text='show password',command=show_password_func,border=0)
    text_username=Label(text="enter your username")
    text_password=Label(text="enter your password")

    #this function checks input when the user tries to sign up
    def signup_check():
        username=main.username
        password=main.password
        username=username.get()
        password=password.get()
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

        if exists(path_)==True:
            with open(path_,'r') as file:
                file=load(file)
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
        
        if len(password)<12:
            main.throw_warning("password cannot be shorter than twelve characters")
            return None
        else:
            pass

        number_counter=0
        for char in password:
            if char.isnumeric()==True:
                number_counter+=1
            else:
                pass
        if number_counter==0:
            main.throw_warning("password must contain atleast one number")
            return None
        else:
            pass

        sum_upper=0
        for char in password:
            if char.isupper()==True:
                sum_upper+=1
            else:
                pass
        if sum_upper==0:
            main.throw_warning("password must contain uppercase characters")
            return None
        else:
            pass

        sum_lower=0
        for char in password:
            if char.islower()==True:
                sum_lower+=1
            else:
                pass
        if sum_lower==0:
            main.throw_warning("password must contain lowercase characters")
            return None
        else:
            pass
        
        sum_special=0
        special_characters = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
    		                  ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|',
		                      '}', '~']
        for char in password:
            if char in special_characters:
                sum_special+=1
            else:
                pass
        if sum_special==0:
            main.throw_warning("password must contain a special character")
            return None

        if exists(path_)==False:
            user_data={main.text_encrypter(username):main.text_encrypter(password)}
            with open(path_,'w') as file:
                file.write(dumps(user_data,indent=4))
        else:
            with open(path_,'r') as file:
                file_data=load(file)
                file_data[main.text_encrypter(username)]=main.text_encrypter(password)
            with open(path_,'w') as file:
                file.write(dumps(file_data,indent=4)) 
        print("Signed in")

    #this is the signup button which appears on the first screen
    button=Button(command=signup_check,background="yellow",text="Sign up",bd=0)

    #the function bellow checks input when
    #the user tries to login
    def login_check():
        username=main.username
        password=main.password
        username=username.get()
        password=password.get()
        if len(username)==0:
            main.throw_warning("enter your username")
            return None  
        with open(main.path_,'r') as file:
            file=load(file)
            if main.text_encrypter(username) not in file:
                main.throw_warning("username doesn't exsist")
                return None
            else:
                pass
            if len(password)==0:
                main.throw_warning("enter your password")
                return None
            if main.text_encrypter(password)!=file.get(main.text_encrypter(username)):
                main.throw_warning("iccorect password")
                return None
            else:
                print("logged in")

    #this function is used when you press the login button 
    def login():
        if exists(main.path_)==True:
            main.button.configure(text='Login',command=main.login_check)
            #this function is called when you press the sign up buttton in the login screen
            def logintosignup():
                main.button.configure(text='Signup',command=main.signup_check)
                main.button_login.configure(text='Login',command=main.login)
            main.button_login.configure(text='signup',command=logintosignup)
        else:
            main.throw_warning("No accounts exists")

    #this is the login button which appears at the top right corner of the screen
    button_login=Button(command=login,background="yellow",text="Login",bd=0)

    text_username.place(relx=0.5,rely=0.2,anchor="center")
    text_password.place(relx=0.5,rely=0.3,anchor="center")
    username.place(relx=0.5,rely=0.24,anchor="center")
    password.place(relx=0.5,rely=0.34,anchor="center")
    show_password_button.place(relx=0.6,rely=0.34,anchor="center")
    button.place(relx=0.5,rely=0.4,anchor="center")
    button_login.place(relx=0.95,rely=0.04)

    widgets=screen.winfo_children()
    for widget in widgets:
        widget.configure(font=font_)
    
main.screen.mainloop()