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

        create_account_title = tk.Label(setup_form, text='Create Account', font=('helvetica', 32))

        display_name_subtitle = tk.Label(setup_form, text='Display Name:', font=('helvetica', 12))
        display_name_entry = tk.Entry(setup_form, textvariable=self.display_name_var, font=('helvetica', 18))
        self.display_name_error = tk.Label(setup_form, text='', foreground='red', font=('helvetica', 10))

        username_subtitle = tk.Label(setup_form, text='Username:', font=('helvetica', 12))
        username_entry = tk.Entry(setup_form, textvariable=self.username_var, font=('helvetica', 18))
        self.username_error = tk.Label(setup_form, text='', foreground='red', font=('helvetica', 10))

        password_subtitle = tk.Label(setup_form, text='Password:', font=('helvetica', 12))
        password_entry = tk.Entry(setup_form, textvariable=self.password_var, font=('helvetica', 18))
        self.password_error = tk.Label(setup_form, text='', foreground='red', font=('helvetica', 10))

        confirm_password_subtitle = tk.Label(setup_form, text='Confirm Password:', font=('helvetica', 12))
        confirm_password_entry = tk.Entry(setup_form, textvariable=self.confirm_password_var, font=('helvetica', 18))
        self.confirm_password_error = tk.Label(setup_form, text='', foreground='red', font=('helvetica', 10))

        submit_btn = tk.Button(setup_form, text='Create', font=('helvetica', 18))

        create_account_title.place(x=150, y=50)

        display_name_subtitle.place(x=150, y=150)
        display_name_entry.place(x=150, y=180)
        self.display_name_error.place(x=150, y=210)

        username_subtitle.place(x=150, y=250) # +40
        username_entry.place(x=150, y=280)
        self.username_error.place(x=150, y=310)

        password_subtitle.place(x=150, y=350)
        password_entry.place(x=150, y=380)
        self.password_error.place(x=150, y=410)

        confirm_password_subtitle.place(x=150, y=450)
        confirm_password_entry.place(x=150, y=480)
        self.confirm_password_error.place(x=150, y=510)

        submit_btn.place(x=240, y=535)

    # clear error messages
    def clear_errors(self):
        self.display_name_error.config(text='')
        self.username_error.config(text='')
        self.password_error.config(text='')
        self.confirm_password_error.config(text='')

    

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