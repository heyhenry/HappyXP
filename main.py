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

        if users['user'].username:
            self.show_page(HomePage)
        else:
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
        global users
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

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.create_page()

    def create_page(self):
        top_section = tk.Frame(self, background='red', height=100, width=1000)
        entries_section = tk.Frame(self, background='blue', height=450, width=500)
        statistics_section = tk.Frame(self, background='green', height=450, width=500)
        graphs_section = tk.Frame(self, background='magenta', height=900, width=500)

        top_section.grid(row=0, columnspan=2, sticky='nswe')
        entries_section.grid(row=1, column=0, sticky='nswe')
        statistics_section.grid(row=2, column=0, sticky='nswe')
        graphs_section.grid(row=1, column=1, rowspan=2, sticky='nswe')

        # entries section
        entry_listbox = tk.Listbox(entries_section)
        scrollbar = tk.Scrollbar(entries_section)
        entry_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=entry_listbox.yview)

        entry_listbox.place(x=165, y=20, width=300, height=400)
        scrollbar.place(x=465, y=20, width=30, height=400)

        add_entry = tk.Button(entries_section, text='Add Entry', font=('Kozuka Mincho Pro M', 14))
        update_entry = tk.Button(entries_section, text='Update Entry', font=('Kozuka Mincho Pro M', 14))
        delete_entry = tk.Button(entries_section, text='Delete Entry', font=('Kozuka Mincho Pro M', 14))

        add_entry.place(x=10, y=50, width=150)
        update_entry.place(x=10, y=150, width=150)
        delete_entry.place(x=10, y=250, width=150)

class EntryPage(tk.Frame):  
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        lbl = tk.Label(self, text='yo')
        lbl.pack()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()