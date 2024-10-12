import tkinter as tk
from user import UserInfo
import json
import os

users = {}
user_savefile = 'user_save.json'

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.geometry('1000x1000')

        self.load_user()

        # loop that puts all the pages (aka frames) into a dictionary called frames
        for F in (SetupPage, LoginPage, EntryPage, HomePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nswe')
     
        self.show_page(SetupPage)

    def show_page(self, page):
        frame = self.frames[page]
        frame.tkraise()

    def custom_serializer(self, obj):
        if isinstance(obj, UserInfo):
            return {
                'username': obj.username,
                'password': obj.password
            }
        return obj

    def load_user(self):
        if os.path.exists(user_savefile):
            with open(user_savefile, 'r') as file:
                user_data = json.load(file)
                for user, user_value in user_data.items():
                    users[user] = UserInfo(user_value['username'], user_value['password'])

    def update_user_save(self):
        json_object = json.dumps(users, indent=4, default=self.custom_serializer)
        with open(user_savefile, 'w') as outfile:
            outfile.write(json_object)

class SetupPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self.create_page()

    def create_page(self):
        setup_window = tk.Frame(self, highlightbackground='black', highlightthickness=2)
        page_title = tk.Label(setup_window, text='Create Account', font=('Kozuka Mincho Pro M', 48))
        username_title = tk.Label(setup_window, text='Username:', font=('Kozuka Mincho Pro M', 24))
        username = tk.Entry(setup_window, textvariable=self.username_var, font=('Kozuka Mincho Pro M', 24))
        password_title = tk.Label(setup_window, text='Password:', font=('Kozuka Mincho Pro M', 24))
        password = tk.Entry(setup_window, textvariable=self.password_var, font=('Kozuka Mincho Pro M', 24))
        submit = tk.Button(setup_window, text='Create', font=('Kozuka Mincho Pro M', 24), command=self.process_details)

        setup_window.place(relx=0.5, rely=0.5, anchor='center')
        setup_window.propagate(0)
        setup_window.config(width=800, height=800)
        page_title.place(x=200, y=100)
        username_title.place(x=225, y=250)
        username.place(x=225, y=300)
        password_title.place(x=225, y=450)
        password.place(x=225, y=500)
        submit.place(x=300, y=600, width=200)
    
    # no need for restrictions on input data as its personal use (atleast for now)
    
    def process_details(self):
        users['user'].username = self.username_var.get()
        users['user'].password = self.password_var.get()
        self.controller.update_user_save()
        self.controller.show_page(LoginPage)

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self.create_page()

    def create_page(self):
        login_window = tk.Frame(self, highlightbackground='black', highlightthickness=2)
        page_title = tk.Label(login_window, text='Login To HappyXP', font=('Kozuka Mincho Pro M', 48))
        username_title = tk.Label(login_window, text='Username:', font=('Kozuka Mincho Pro M', 24))
        username = tk.Entry(login_window, textvariable=self.username_var, font=('Kozuka Mincho Pro M', 24))
        password_title = tk.Label(login_window, text='Password:', font=('Kozuka Mincho Pro M', 24))
        password = tk.Entry(login_window, textvariable=self.password_var, font=('Kozuka Mincho Pro M', 24))
        submit = tk.Button(login_window, text='Create', font=('Kozuka Mincho Pro M', 24), command=self.process_login)
        self.error_message = tk.Label(login_window, font=('Kozuka Mincho Pro M', 24), foreground='red')

        login_window.place(relx=0.5, rely=0.5, anchor='center')
        login_window.propagate(0)
        login_window.config(width=800, height=800)
        page_title.place(x=150, y=100)
        username_title.place(x=225, y=250)
        username.place(x=225, y=300)
        password_title.place(x=225, y=450)
        password.place(x=225, y=500)
        submit.place(x=300, y=600, width=200)
        self.error_message.place(x=250, y=650)

    def process_login(self):
        self.error_message.config(text='')
        
        if self.username_var.get() == users['user'].username and self.password_var.get() == users['user'].password:
            self.controller.show_page(HomePage)
        else:
            self.error_message.config(text='Incorrect Username or Password. Try again.')

class EntryPage(tk.Frame):  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        lbl = tk.Label(self, text='yo')
        lbl.pack()

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        lbl = tk.Label(self, text='yo')
        lbl.pack()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()