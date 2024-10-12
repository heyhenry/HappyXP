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
        
        self.check_user_exists()

        self.frames = {}

        self.geometry('1000x1000')

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

    def check_user_exists(self):
        if not users:
            user = UserInfo('', '')
            users['user'] = user
            self.update_user_save()

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
        submit = tk.Button(setup_window, text='Create', font=('Kozuka Mincho Pro M', 24))

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
        

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        lbl = tk.Label(self, text='yo')
        lbl.place(relx=0.5, rely=0.5, anchor='center')

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