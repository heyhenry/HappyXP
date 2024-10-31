import tkinter as tk
from user import UserInfo
import json
import os
from PIL import Image, ImageTk
from tkinter import filedialog

# save data 
users = {}
entries = {}

# save file names
user_savefile = 'user_save.json'

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

        self.load_users()

        self.login_status_var = tk.BooleanVar(value=users['user'].toggle_login)
        self.current_user_image_var = tk.StringVar(value='img/default_pic.png')

        # tracer to find changes to the current_user_image_var variable, if found - execute the update_profile_image function
        self.current_user_image_var.trace_add('write', self.update_profile_image)

        # store the frames (pages)
        self.pages = {}

        # iterate through the various pages found in the app
        for P in (SetupPage, LoginPage, HomePage, NewEntryPage, EntriesPage, SettingsPage, SearchPage):
            page = P(container, self)
            # initialise frame of each page
            self.pages[P] = page
            page.grid(row=0, column=0, sticky='nswe')

        self.load_initial_profile_image()

        # initial startup page alogrithm
        # if a username is not found in the user save file, then it indicates the account hasnt been created
        if not users['user'].username:
            self.show_page(SetupPage)
        # check if the toggle_login was toggled on
        elif users['user'].toggle_login:
            self.show_page(HomePage)
        # otherwise, go to login page
        else:
            self.show_page(LoginPage)

    def show_page(self, cont):
        page = self.pages[cont]
        page.tkraise()

    # load the user saved data and update users dictionary
    def load_users(self):
        global users
        # checks if the save file can be located
        if os.path.exists(user_savefile):
            # opens the save file and reads its data
            with open(user_savefile, 'r') as file:
                # save the data into a dictionary variable
                users_data = json.load(file)
                # populate the users dictionary with the save file data
                for user, user_info in users_data.items():
                    users[user] = UserInfo(user_info['display_name'], user_info['username'], user_info['password'], user_info['toggle_login'])

    # json customised serializer
    def custom_serializer(self, obj):
        if isinstance(obj, UserInfo):
            return {
                'display_name': obj.display_name,
                'username': obj.username,
                'password': obj.password,
                'toggle_login': obj.toggle_login
            }
        return obj

    # update the user save file
    def update_user_save(self):

        json_object = json.dumps(users, indent=4, default=self.custom_serializer)

        with open(user_savefile, 'w') as outfile:
            outfile.write(json_object)

    # updates the login toggle status
    def update_login(self, widget_name, *args):
        if self.login_status_var.get():
            widget_name.config(foreground='green')
        else:
            widget_name.config(foreground='red')

    # intial loading of the user's profile image (curently just to the homepage)
    def load_initial_profile_image(self):
        self.user_profile_img = Image.open(self.current_user_image_var.get())
        self.user_profile_img.thumbnail((150, 150))
        self.user_profile_img = ImageTk.PhotoImage(self.user_profile_img)

        self.pages[HomePage].update_image(self.user_profile_img)

    # updates the user's profile image
    def update_profile_image(self, *args):
        # create the image based on the current given file path
        self.user_profile_img = Image.open(self.current_user_image_var.get())
        self.user_profile_img.thumbnail((150, 150))
        self.user_profile_img = ImageTk.PhotoImage(self.user_profile_img)
        self.user_profile_img.image = self.user_profile_img

        # specifically trigge the HomePage's func to update it's page's profile image display
        self.pages[HomePage].update_image(self.user_profile_img)

    # highlight nav options upon hover
    def on_hover(self, mouse_event, widget_name):
        widget_name.config(foreground='lightblue')

    # return nav option text colour to original state found
    def off_hover(self, mouse_event, widget_name):
        # if the widget in question is the login_status toggle text, then chnage to original state based on current status colour
        if widget_name == self.pages[HomePage].login_status:
            if self.login_status_var.get():
                widget_name.config(foreground='green')
            else:
                widget_name.config(foreground='red')
        # otherwise can assume original text's state colour is black (at this current time)
        else:
            widget_name.config(foreground='black')

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

        submit_btn = tk.Button(setup_form, text='Create', font=('helvetica', 18), command=self.process_account)

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

    # check for errors in the input fields
    def check_errors(self):
        # clean error messages
        self.clear_errors()
        # display name related
        if ' ' in self.display_name_var.get():
            self.display_name_error.config(text='Display Name Must Not Contain Spaces.') 
        elif len(self.display_name_var.get()) < 3:
            self.display_name_error.config(text='Display Name Must Be Longer Than 2 Characters.')
        elif len(self.display_name_var.get()) > 12:
            self.display_name_error.config(text='Display Name Must Be Less Than 13 Characters.')
        # username related
        elif ' ' in self.username_var.get():
            self.username_error.config(text='Username Must Not Contain Spaces.')
        elif len(self.username_var.get()) < 3:
            self.username_error.config(text='Username Must Be Longer Than 2 Characters.')
        elif len(self.username_var.get()) > 12:
            self.username_error.config(text='Username Must Be Less Than 13 Characters.')
        # password related
        elif ' ' in self.password_var.get():
            self.password_error.config(text='Password Must Not Contain Spaces.')
        elif len(self.password_var.get()) < 8:
            self.password_error.config(text='Password Must Be Longer Than 7 Characters.')
        elif len(self.password_var.get()) > 12:
            self.password_error.config(text='Password Must Be Less Than 13 Characters.')
        elif self.password_var.get() != self.confirm_password_var.get():
            self.confirm_password_error.config(text='Passwords Do Not Match.')
        else:
            return False
        return True

    # processes valid account creation and saves data
    def process_account(self):
        if not self.check_errors():
            # updates the users dictionary
            users['user'].display_name = self.display_name_var.get()
            users['user'].username = self.username_var.get()
            users['user'].password = self.password_var.get()

            # updates save data            
            self.controller.update_user_save()
            # redirect to the login page
            self.controller.show_page(LoginPage)

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        login_form = tk.Frame(self, highlightbackground='black', highlightthickness=2)
        login_form.place(relx=0.5, rely=0.5, anchor='center')
        login_form.propagate(0)
        login_form.config(width=600, height=600)

        login_title = tk.Label(login_form, text='Login to HappyXP', font=('helvetica', 32))

        username_subtitle = tk.Label(login_form, text='Username:', font=('helvetica', 12))
        username_entry = tk.Entry(login_form, textvariable=self.username_var, font=('helvetica', 18))
        self.username_error = tk.Label(login_form, text='', foreground='red', font=('helvetica', 10))

        password_subtitle = tk.Label(login_form, text='Password:', font=('helvetica', 12))
        password_entry = tk.Entry(login_form, textvariable=self.password_var, font=('helvetica', 18))
        self.password_error = tk.Label(login_form, text='', foreground='red', font=('helvetica', 10))

        login_btn = tk.Button(login_form, text='Login', font=('helvetica', 18), command=self.process_login)

        login_title.place(x=130, y=50)

        username_subtitle.place(x=130, y=150)
        username_entry.place(x=130, y=180)
        self.username_error.place(x=130, y=210)

        password_subtitle.place(x=130, y=260)
        password_entry.place(x=130, y=290)
        self.password_error.place(x=130, y=320)

        login_btn.place(x=130, y=380)

    # clear error messages
    def clear_errors(self):
        self.username_error.config(text='')
        self.password_error.config(text='')

    # check for errors in user input
    def check_errors(self):
        self.clear_errors()
        if self.username_var.get() != users['user'].username:
            self.username_error.config(text='Incorrect Username.')
        elif self.password_var.get() != users['user'].password:
            self.password_error.config(text='Incorrect Password.')
        else:
            return False
        return True

    # process login details
    def process_login(self):
        if not self.check_errors():
            self.controller.show_page(HomePage)

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.create_widgets()

    def create_widgets(self):
        home_window = tk.Frame(self, highlightbackground='black', highlightthickness=2)
        home_window.place(relx=0.5, rely=0.5, anchor='center')
        home_window.propagate(0)
        home_window.config(width=1100, height=700)

        # navigation bar
        nav_bar = tk.Frame(home_window, highlightbackground='grey', highlightthickness=1)
        nav_bar.place(x=10, y=50)
        nav_bar.propagate(0)
        nav_bar.config(width=200, height=600)

        home_navtitle = tk.Label(nav_bar, text='Home', font=('helvetica', 18))
        search_navtitle = tk.Label(nav_bar, text='Search', font=('helvetica', 18))
        entries_navtitle = tk.Label(nav_bar, text='Entries', font=('helvetica', 18))
        settings_navtitle = tk.Label(nav_bar, text='Settings', font=('helvetica', 18))

        self.login_status = tk.Label(nav_bar, text='Stay Logged In', font=('helvetica', 18))

        # determines which colour should be showcasing the toggled or not login text 
        if self.controller.login_status_var.get():
            self.login_status.config(foreground='green')
        else:
            self.login_status.config(foreground='red')

        self.controller.login_status_var.trace_add('write', lambda *args: self.controller.update_login(self.login_status))

        home_navtitle.place(x=50, y=50)
        search_navtitle.place(x=50, y=100)
        entries_navtitle.place(x=50, y=150)
        settings_navtitle.place(x=50, y=200)

        self.login_status.place(x=15, y=300)

        # when option is clicked in the navbar
        home_navtitle.bind("<Button-1>", lambda mouse_event: self.redirect_page(mouse_event, HomePage))
        search_navtitle.bind("<Button-1>", lambda mouse_event: self.redirect_page(mouse_event, SearchPage))
        entries_navtitle.bind("<Button-1>", lambda mouse_event: self.redirect_page(mouse_event, EntriesPage))
        settings_navtitle.bind("<Button-1>", lambda mouse_event: self.redirect_page(mouse_event, SettingsPage))

        self.login_status.bind("<Button-1>", lambda mouse_event: self.toggle_login(mouse_event))

        # when option is hovered over in the navbar
        home_navtitle.bind("<Enter>", lambda mouse_event: self.controller.on_hover(mouse_event, home_navtitle))
        home_navtitle.bind("<Leave>", lambda mouse_event: self.controller.off_hover(mouse_event, home_navtitle))
        search_navtitle.bind("<Enter>", lambda mouse_event: self.controller.on_hover(mouse_event, search_navtitle))
        search_navtitle.bind("<Leave>", lambda mouse_event: self.controller.off_hover(mouse_event, search_navtitle))
        entries_navtitle.bind("<Enter>", lambda mouse_event: self.controller.on_hover(mouse_event, entries_navtitle))
        entries_navtitle.bind("<Leave>", lambda mouse_event: self.controller.off_hover(mouse_event, entries_navtitle))
        settings_navtitle.bind("<Enter>", lambda mouse_event: self.controller.on_hover(mouse_event, settings_navtitle))
        settings_navtitle.bind("<Leave>", lambda mouse_event: self.controller.off_hover(mouse_event, settings_navtitle))

        self.login_status.bind("<Enter>", lambda mouse_event: self.controller.on_hover(mouse_event, self.login_status))
        self.login_status.bind("<Leave>", lambda mouse_event: self.controller.off_hover(mouse_event, self.login_status))

        # bio and profile 
        user_info_section = tk.Frame(home_window, highlightbackground='black', highlightthickness=1)
        user_info_section.place(x=250, y=50)
        user_info_section.propagate(0)
        user_info_section.config(width=800, height=200)

        self.user_profile_pic = tk.Label(user_info_section, highlightbackground='black', highlightthickness=1)

        user_bio = tk.Label(user_info_section, highlightbackground='black', highlightthickness=1)
        user_bio.config(width=75, height=10)

        self.user_profile_pic.place(x=600, y=25)

        user_bio.place(x=25, y=25)

        # favourite entries
        fav_entries_section = tk.Frame(home_window, highlightbackground='black', highlightthickness=1)
        fav_entries_section.place(x=250, y=260)
        fav_entries_section.propagate(0)
        fav_entries_section.config(width=800, height=200)

        # achievement badges
        achievement_badges_section = tk.Frame(home_window, highlightbackground='black', highlightthickness=1)
        achievement_badges_section.place(x=250, y=470)
        achievement_badges_section.propagate(0)
        achievement_badges_section.config(width=800, height=200)

    # redirects user to the selected page from the navbar
    def redirect_page(self, mouse_event, page_name):
        self.controller.show_page(page_name)

    # toggling the status of the login's 'stay on' feature 
    def toggle_login(self, mouse_event):
        if self.controller.login_status_var.get():
            users['user'].toggle_login = False
            self.login_status.config(foreground='red')
            self.controller.update_user_save()
            self.controller.login_status_var.set(False)
        else:
            users['user'].toggle_login = True
            self.login_status.config(foreground='green')
            self.controller.update_user_save()
            self.controller.login_status_var.set(True)

    # update the user's profile image
    def update_image(self, new_image):
        self.user_profile_pic.config(image=new_image)
        self.user_profile_pic.image = new_image

class NewEntryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

class EntriesPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.display_name_var = tk.StringVar(value=users['user'].display_name)
        self.username_var = tk.StringVar(value=users['user'].username)
        self.password_var = tk.StringVar(value=users['user'].password)

        self.selected_file_path = tk.StringVar(value='img/default_pic.png')

        self.create_widgets()

    def create_widgets(self):
        settings_window = tk.Frame(self, highlightbackground='black', highlightthickness=2)
        settings_window.place(relx=0.5, rely=0.5, anchor='center')
        settings_window.propagate(0)
        settings_window.config(width=1100, height=700)

        # navigation bar
        nav_bar = tk.Frame(settings_window, highlightbackground='grey', highlightthickness=1)
        nav_bar.place(x=10, y=50)
        nav_bar.propagate(0)
        nav_bar.config(width=200, height=600)

        home_navtitle = tk.Label(nav_bar, text='Home', font=('helvetica', 18))
        search_navtitle = tk.Label(nav_bar, text='Search', font=('helvetica', 18))
        entries_navtitle = tk.Label(nav_bar, text='Entries', font=('helvetica', 18))
        settings_navtitle = tk.Label(nav_bar, text='Settings', font=('helvetica', 18))

        self.login_status = tk.Label(nav_bar, text='Stay Logged In', font=('helvetica', 18))

        # determines which colour should be showcaseing the toggled or not login text
        if self.controller.login_status_var.get():
            self.login_status.config(foreground='green')
        else:
            self.login_status.config(foreground='red')

        # updates the toggle status in real time
        self.controller.login_status_var.trace_add('write', lambda *args: self.controller.update_login(self.login_status))

        home_navtitle.place(x=50, y=50)
        search_navtitle.place(x=50, y=100)
        entries_navtitle.place(x=50, y=150)
        settings_navtitle.place(x=50, y=200)

        self.login_status.place(x=15, y=300)

        # when option is clicked in the navbar
        home_navtitle.bind("<Button-1>", lambda mouse_event: self.redirect_page(mouse_event, HomePage))
        search_navtitle.bind("<Button-1>", lambda mouse_event: self.redirect_page(mouse_event, SearchPage))
        entries_navtitle.bind("<Button-1>", lambda mouse_event: self.redirect_page(mouse_event, EntriesPage))
        settings_navtitle.bind("<Button-1>", lambda mouse_event: self.redirect_page(mouse_event, SettingsPage))

        self.login_status.bind("<Button-1>", lambda mouse_event: self.toggle_login(mouse_event))

        # when option is hovered over in the navbar
        home_navtitle.bind("<Enter>", lambda mouse_event: self.controller.on_hover(mouse_event, home_navtitle))
        home_navtitle.bind("<Leave>", lambda mouse_event: self.controller.off_hover(mouse_event, home_navtitle))
        search_navtitle.bind("<Enter>", lambda mouse_event: self.controller.on_hover(mouse_event, search_navtitle))
        search_navtitle.bind("<Leave>", lambda mouse_event: self.controller.off_hover(mouse_event, search_navtitle))
        entries_navtitle.bind("<Enter>", lambda mouse_event: self.controller.on_hover(mouse_event, entries_navtitle))
        entries_navtitle.bind("<Leave>", lambda mouse_event: self.controller.off_hover(mouse_event, entries_navtitle))
        settings_navtitle.bind("<Enter>", lambda mouse_event: self.controller.on_hover(mouse_event, settings_navtitle))
        settings_navtitle.bind("<Leave>", lambda mouse_event: self.controller.off_hover(mouse_event, settings_navtitle))

        self.login_status.bind("<Enter>", lambda mouse_event: self.controller.on_hover(mouse_event, self.login_status))
        self.login_status.bind("<Leave>", lambda mouse_event: self.controller.off_hover(mouse_event, self.login_status))

        # edit section
        edit_section = tk.Frame(settings_window, highlightbackground='black', highlightthickness=1)
        edit_section.place(x=250, y=50)
        edit_section.propagate(0)
        edit_section.config(width=800, height=600)

        update_display_name_subtitle = tk.Label(edit_section, text='Change Display Name:', font=('helvetica', 12))
        update_display_name_entry = tk.Entry(edit_section, textvariable=self.display_name_var, font=('helvetica', 18))
        self.update_display_name_error = tk.Label(edit_section, text='', foreground='red', font=('helvetica', 10))

        update_username_subtitle = tk.Label(edit_section, text='Change Username:', font=('helvetica', 12))
        update_username_entry = tk.Entry(edit_section, textvariable=self.username_var, font=('helvetica', 18))
        self.update_username_error = tk.Label(edit_section, text='', foreground='red', font=('helvetica', 10))

        update_password_subtitle = tk.Label(edit_section, text='Change Password:', font=('helvetica', 12))
        update_password_entry = tk.Entry(edit_section, textvariable=self.password_var, font=('helvetica', 18))
        self.update_password_error = tk.Label(edit_section, text='', foreground='red', font=('helvetica', 10))

        # display preview of the current user's profile image
        current_user_image = Image.open('img/default_pic.png')
        current_user_image.thumbnail((150, 150))
        current_user_image = ImageTk.PhotoImage(current_user_image)
        current_user_image.image = current_user_image

        self.display_image_preview = tk.Label(edit_section, image=current_user_image)
        update_user_profile_image = tk.Button(edit_section, text='Upload New User Image', command=self.open_image)

        edit_btn = tk.Button(edit_section, text='Update Details', font=('helvetica', 18), command=self.process_edit)

        self.success_message = tk.Label(edit_section, text='', font=('helvetica', 12), foreground='green')

        update_display_name_subtitle.place(x=100, y=50)
        update_display_name_entry.place(x=100, y=80)
        self.update_display_name_error.place(x=100, y=110)

        update_username_subtitle.place(x=100, y=140)
        update_username_entry.place(x=100, y=170)
        self.update_username_error.place(x=100, y=200)

        update_password_subtitle.place(x=100, y=230)
        update_password_entry.place(x=100, y=260)
        self.update_password_error.place(x=100, y=290)

        self.display_image_preview.place(x=500, y=100)
        update_user_profile_image.place(x=500, y=300)

        edit_btn.place(x=100, y=340)

        self.success_message.place(x=100, y=410)

    # redirect to a different page
    def redirect_page(self, mouse_event, page_name):
        # if the selected display image was not updated, then revert the file path for selected_file_path
        # and display the current user's profile image for the display preview next time settings page is opened
        if self.selected_file_path.get() != self.controller.current_user_image_var.get():
            self.selected_file_path.set(self.controller.current_user_image_var.get())
            self.display_image(self.controller.current_user_image_var.get())
        self.controller.show_page(page_name)

    # update and toggle the stay logged in status
    def toggle_login(self, mouse_event):
        if self.controller.login_status_var.get():
            users['user'].toggle_login = False
            self.login_status.config(foreground='red')
            self.controller.update_user_save()
            self.controller.login_status_var.set(False)
        else:
            users['user'].toggle_login = True
            self.login_status.config(foreground='green')
            self.controller.update_user_save()
            self.controller.login_status_var.set(True)

    # checks the login status's curent value
    def update_login(self, *args):
        if self.controller.login_status_var.get():
            self.login_status.config(foreground='green')
        else:
            self.login_status.config(foreground='red')

    # clear the error messages
    def clear_errors(self):
        self.update_display_name_error.config(text='')
        self.update_username_error.config(text='')
        self.update_password_error.config(text='')

    # check for errors in user input fields
    def check_errors(self):
        # clear error messages
        self.clear_errors()
        # display name related
        if ' ' in self.display_name_var.get():
            self.update_display_name_error.config(text='Display Name Must Not Contain Spaces.')
        elif len(self.display_name_var.get()) < 3:
            self.update_display_name_error.config(text='Display Name Must Be Longer Than 2 Characters.')
        elif len(self.display_name_var.get()) > 12:
            self.update_display_name_error.config(text='Display Name Must Be Less Than 13 Characters.')
        # username related
        elif ' ' in self.username_var.get():
            self.update_username_error.config(text='Username Must Not Contain Spaces.')
        elif len(self.username_var.get()) < 3:
            self.update_username_error.config(text='Username Must Be Longer Than 2 Characters.')
        elif len(self.username_var.get()) > 12:
            self.update_username_error.config(text='Username Must be Less Than 13 Characters.')
        # password related
        elif ' ' in self.password_var.get():
            self.update_password_error.config(text='Password Must Not Contain Spaces.')
        elif len(self.password_var.get()) < 8:
            self.update_password_error.config(text='Password Must Be Longer Than 7 Characters.')
        elif len(self.password_var.get()) > 12:
            self.update_password_error.config(text='Password Must Be Less Than 13 Characters.')
        else:
            return False
        return True

    # clear the success message
    def clear_success_message(self):
        self.success_message.config(text='')

    # process to information in the edit section
    def process_edit(self):
        if not self.check_errors():
            users['user'].display_name = self.display_name_var.get()
            users['user'].username = self.username_var.get()
            users['user'].password = self.password_var.get()

            self.controller.update_user_save()

            self.controller.current_user_image_var.set(self.selected_file_path.get())
            self.save_image()

            self.success_message.config(text='Successfully Updated!')
            self.success_message.after(1000, self.clear_success_message)

    # open and search for image file
    def open_image(self):
        file_path = filedialog.askopenfilename(title='Update User Image File', filetypes=[('Image Files', '*.png *.jpg *jpeg')])
        # if image file is valid, save the image as the new profile pic
        # if file_path:
        #     self.save_image(file_path)
        if file_path:
            self.display_image(file_path)

    # save image file to img folder for user profile pic
    def save_image(self):
        user_image = Image.open(self.selected_file_path.get())
        user_image.save('img/default_pic.png')

    # display the selected image onto the settings page
    def display_image(self, file_path):
        profile_image = Image.open(file_path)
        profile_image.thumbnail((150, 150))
        profile_image = ImageTk.PhotoImage(profile_image)
        self.display_image_preview.config(image=profile_image)
        self.display_image_preview.image = profile_image
        self.selected_file_path.set(file_path)

class SearchPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()