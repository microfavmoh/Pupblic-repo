import os
import json
import time


class username_password:
    username=None
    password=None


def create_account():
    username=None
    while username==None:
        username=str(input('please enter your username(note:username mustbe loger than 3 character but shorter than 15)'))
    while len(username)<3 or len(username)>15:
        username=str(input('please enter your username(note:username mustbe loger than 3 character but shorter than 15)'))
    if os.path.exists("C:/Users/Arabtech/Desktop/Coding/users_data.json")==False:
            pass
    elif os.path.exists("C:/Users/Arabtech/Desktop/Coding/users_data.json")==True:
        with open('users_data.json','r') as file:
            file=json.load(file)
            while username in file:
                username=str(input("username already exists please try again"))
            while len(username)<3 and len(username)>15:
                username=str(input('please enter your username(note:username mustbe loger than 3 character but shorter than 15)'))

    username_password.username=username
    password=None
    while password==None:
        print('password must be atleast eight characters')
        password=str(input('please enter a strong password'))
    while len(password)<7:
        password=str(input('please enter a strong password'))
    with open('users_data.json',mode='a') as file:
        user_data={username:password}
        user_data=json.dumps(user_data,indent=4)
        file.write(user_data)
        file.close()


def login():
    if os.path.exists("C:/Users/Arabtech/Desktop/Coding/users_data.json")==True:
        pass
    else:
        print('no accounts available please create an account')
        time.sleep(2)
        create_account()
        return None
    username_login=None
    while username_login==None:
        username_login=str(input('please enter your username'))
    with open('users_data.json',mode='r') as file:
        file=file.read()
        if username_login in file:
            pass
        else:
            while username_login not in file:
                username_login=str(input('please enter your username'))
    username_password.username=username_login
    password_login=None
    while password_login==None:
        password_login=str(input('please enter your password'))
    with open('users_data.json',mode='r') as file:
        file=file.read()
        if password_login in file:
            pass
        else:
            while password_login not in file:
                password_login=str(input('please enter your password'))


user_input_create_account_login=None
print("would you like to crete an account or login")
time.sleep(2)
while user_input_create_account_login not in ['account','login']:
    user_input_create_account_login=input("if you want to create an account type 'account' and if you want to log in type 'login'.")
if user_input_create_account_login=='account':
    create_account()
if user_input_create_account_login=='login':
    login()