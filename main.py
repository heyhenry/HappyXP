import tkinter as tk

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (SetupPage, LoginPage, EntryPage, HomePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nswe')

    # 
    def show_page(self, page):
        frame = self.frames[page]
        frame.tkraise()

class SetupPage:
    pass

class LoginPage:
    pass

class EntryPage:  
    pass

class HomePage:
    pass