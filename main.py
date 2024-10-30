import tkinter as tk
from user import UserInfo

# save data 
users = {}
entries = {}

class MainApp(tk.Tk):
    # initiate MainApp class
    def __init__(self, *args, **kwargs):
        # initiate Tk class
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.geometry('1200x800+350+100')

        # store the frames (pages)
        self.pages = {}

        # iterate through the various pages found in the app
        for P in (SetupPage, LoginPage, HomePage, NewEntryPage, EntriesPage, EditUserPage):
            page = P(container, self)
            # initialise frame of each page
            self.pages[P] = page
            page.grid(row=0, column=0, sticky='nswe')

        self.show_page(SetupPage)

    def show_page(self, cont):
        page = self.pages[cont]
        page.tkraise()


class SetupPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.display_name_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()

        self.password_privacy = False

        self.create_widgets()

    def create_widgets(self):
        setup_form = tk.Frame(self, highlightbackground='black', highlightthickness=2)
        setup_form.place(relx=0.5, rely=0.5, anchor='center')
        setup_form.propagate(0)
        setup_form.config(width=600, height=600)

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

class NewEntryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

class EntriesPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

class EditUserPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()