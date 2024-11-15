import tkinter as tk
from user import UserInfo
import json
import os
from PIL import Image, ImageTk
from tkinter import filedialog
from tkcalendar import DateEntry
from entry import EntryInfo
from datetime import datetime
import requests
import random
from achievement import AchievementInfo

# save data 
users = {}
entries = {}
achievements = {}

# save file names
user_savefile = 'user_save.json'
entries_savefile = 'entries_save.json'
achievements_savefile = 'achievements_save.json'

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
        self.load_entries()
        self.load_achievements()

        self.login_status_var = tk.BooleanVar(value=users['user'].toggle_login)
        self.current_user_image_var = tk.StringVar(value='img/default_pic.png')

        # tracer to find changes to the current_user_image_var variable, if found - execute the update_profile_image function
        self.current_user_image_var.trace_add('write', self.update_profile_image)

        self.entry_id_var = tk.StringVar()

        # store the frames (pages)
        self.pages = {}

        # iterate through the various pages found in the app
        for P in (SetupPage, LoginPage, HomePage, NewEntryPage, EntriesPage, SettingsPage, DiscoverPage, UpdateEntryPage):
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
        if cont == EntriesPage:
            self.pages[EntriesPage].entries_lb.bind('<<ListboxSelect>>', lambda mouse_event: self.pages[EntriesPage].display_entry_details(mouse_event))
        else:
            self.pages[EntriesPage].entries_lb.unbind('<<ListboxSelect>>')
        page.tkraise()

    # json customised serializer
    def custom_serializer(self, obj):
        if isinstance(obj, UserInfo):
            return {
                'display_name': obj.display_name,
                'username': obj.username,
                'password': obj.password,
                'toggle_login': obj.toggle_login,
                'bio_message': obj.bio_message,
                'total_entries_count': obj.total_entries_count,
                'total_chapters_count': obj.total_chapters_count,
                'total_episodes_count': obj.total_episodes_count,
                'total_anime_count': obj.total_anime_count,
                'total_manga_count': obj.total_manga_count
            }
        elif isinstance(obj, EntryInfo):
            return {
                'title': obj.title,
                'content_type': obj.content_type,
                'rating': obj.rating,
                'current_progress': obj.current_progress,
                'total_progress': obj.total_progress,
                'status': obj.status,
                'start_date': obj.start_date,
                'end_date': obj.end_date
            }
        elif isinstance(obj, AchievementInfo):
            return {
                'name': obj.name,
                'date_unlocked': obj.date_unlocked
            }
        return obj

    # load the user saved data and update users dictionary
    def load_users(self):
        global users
        # checks if the save file can be located
        if os.path.exists(user_savefile):
            # opens the save file and reads its data
            with open(user_savefile, 'r') as file:
                # save the data into a dictionary 
                users_data = json.load(file)
                # populate the users dictionary with the save file's data
                for user, user_info in users_data.items():
                    users[user] = UserInfo(user_info['display_name'], user_info['username'], user_info['password'], user_info['toggle_login'], user_info['bio_message'], user_info['total_entries_count'], user_info['total_chapters_count'], user_info['total_episodes_count'], user_info['total_anime_count'], user_info['total_manga_count'])

    # load the user's entries' saved data and update entries dictionary
    def load_entries(self):
        global entries
        # check if the save file can be located
        if os.path.exists(entries_savefile):
            # open the save file and read its data
            with open(entries_savefile, 'r') as file:
                # save the data intoa dictionary
                entries_data = json.load(file)
                # populate the entries dictionary with the save file's data
                for entry, entry_info in entries_data.items():
                    entries[entry] = EntryInfo(entry_info['title'], entry_info['content_type'], entry_info['rating'], entry_info['current_progress'],
                                               entry_info['total_progress'], entry_info['status'], entry_info['start_date'], entry_info['end_date'])

    # load the users's achievements saved data and update achievements dictionary
    def load_achievements(self):
        global achievements
        if os.path.exists(achievements_savefile):
            with open(achievements_savefile, 'r') as file:
                achievements_data = json.load(file)
                for achievement, achievement_info in achievements_data.items():
                    achievements[achievement] = AchievementInfo(achievement_info['name'], achievement_info['date_unlocked'])

    # update the user save file
    def update_user_save(self):
        json_object = json.dumps(users, indent=4, default=self.custom_serializer)
        with open(user_savefile, 'w') as outfile:
            outfile.write(json_object)

    # update the entries save file
    def update_entries_save(self):
        json_object = json.dumps(entries, indent=4, default=self.custom_serializer)
        with open(entries_savefile, 'w') as outfile:
            outfile.write(json_object)

    # update the achievements save file
    def update_achievements_save(self):
        json_object = json.dumps(achievements, indent=4, default=self.custom_serializer)
        with open(achievements_savefile, 'w') as outfile:
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

        # specifically trigger the HomePage's func to update it's page's profile image display
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
        elif widget_name == self.pages[SettingsPage].login_status:
            if self.login_status_var.get():
                widget_name.config(foreground='green')
            else:
                widget_name.config(foreground='red')
        elif widget_name == self.pages[DiscoverPage].login_status:
            if self.login_status_var.get():
                widget_name.config(foreground='green')
            else:
                widget_name.config(foreground='red')
        elif widget_name == self.pages[EntriesPage].login_status:
            if self.login_status_var.get():
                widget_name.config(foreground='green')
            else:
                widget_name.config(foreground='red')
        # otherwise can assume original text's state colour is black (at this current time)
        else:
            widget_name.config(foreground='black')

    # fill in the entries listbox with all of the user's entries from the saved data
    def populate_entries(self, widget_name):
        # if the listbox is already populated, remove all items
        if widget_name.size():
            widget_name.delete(0, 'end')
        # loop through the entries dictionary's keys and add as the reference points for each entry
        for entry_name in entries.keys():
            widget_name.insert('end', entry_name)

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

        # region - navigation bar
        nav_bar = tk.Frame(home_window, highlightbackground='grey', highlightthickness=1)
        nav_bar.place(x=10, y=50)
        nav_bar.propagate(0)
        nav_bar.config(width=200, height=600)

        home_navtitle = tk.Label(nav_bar, text='Home', font=('helvetica', 18))
        discover_navtitle = tk.Label(nav_bar, text='Discover', font=('helvetica', 18))
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
        discover_navtitle.place(x=50, y=100)
        entries_navtitle.place(x=50, y=150)
        settings_navtitle.place(x=50, y=200)

        self.login_status.place(x=15, y=300)

        # when option is clicked in the navbar
        home_navtitle.bind("<Button-1>", lambda mouse_event: self.redirect_page(mouse_event, HomePage))
        discover_navtitle.bind("<Button-1>", lambda mouse_event: self.redirect_page(mouse_event, DiscoverPage))
        entries_navtitle.bind("<Button-1>", lambda mouse_event: self.redirect_page(mouse_event, EntriesPage))
        settings_navtitle.bind("<Button-1>", lambda mouse_event: self.redirect_page(mouse_event, SettingsPage))

        self.login_status.bind("<Button-1>", lambda mouse_event: self.toggle_login(mouse_event))

        # when option is hovered over in the navbar
        home_navtitle.bind("<Enter>", lambda mouse_event: self.controller.on_hover(mouse_event, home_navtitle))
        home_navtitle.bind("<Leave>", lambda mouse_event: self.controller.off_hover(mouse_event, home_navtitle))
        discover_navtitle.bind("<Enter>", lambda mouse_event: self.controller.on_hover(mouse_event, discover_navtitle))
        discover_navtitle.bind("<Leave>", lambda mouse_event: self.controller.off_hover(mouse_event, discover_navtitle))
        entries_navtitle.bind("<Enter>", lambda mouse_event: self.controller.on_hover(mouse_event, entries_navtitle))
        entries_navtitle.bind("<Leave>", lambda mouse_event: self.controller.off_hover(mouse_event, entries_navtitle))
        settings_navtitle.bind("<Enter>", lambda mouse_event: self.controller.on_hover(mouse_event, settings_navtitle))
        settings_navtitle.bind("<Leave>", lambda mouse_event: self.controller.off_hover(mouse_event, settings_navtitle))

        self.login_status.bind("<Enter>", lambda mouse_event: self.controller.on_hover(mouse_event, self.login_status))
        self.login_status.bind("<Leave>", lambda mouse_event: self.controller.off_hover(mouse_event, self.login_status))
        # endregion

        # region - bio and profile 
        user_info_section = tk.Frame(home_window, highlightbackground='black', highlightthickness=1)
        user_info_section.place(x=250, y=50)
        user_info_section.propagate(0)
        user_info_section.config(width=800, height=200)

        self.user_profile_pic = tk.Label(user_info_section, highlightbackground='black', highlightthickness=1)
        self.user_profile_pic.place(x=600, y=25)

        user_bio = tk.Label(user_info_section, highlightbackground='black', highlightthickness=1)
        user_bio.config(width=75, height=10)
        self.user_bio_info = tk.Text(user_info_section, width=39, height=4, font=('helvetica', 18), state='normal', background='#f0f0f0', relief='flat')
        self.user_bio_info.insert('1.0', users['user'].bio_message)
        self.user_bio_info.config(state='disabled')
        edit_bio = tk.Button(user_info_section, text='Edit', font=('helvetica', 9), command=self.edit_bio_info)
        self.confirm_bio = tk.Button(user_info_section, text='Confirm', font=('helvetica', 9), command=self.confirm_bio_info)

        user_bio.place(x=25, y=25)
        self.user_bio_info.place(x=30, y=30)
        edit_bio.place(x=445, y=150)
        self.confirm_bio.place(x=480, y=150)
        self.confirm_bio.place_forget()
        # endregion

        # region - favourite entries
        fav_entries_section = tk.Frame(home_window, highlightbackground='black', highlightthickness=1)
        fav_entries_section.place(x=250, y=260)
        fav_entries_section.propagate(0)
        fav_entries_section.config(width=800, height=200)
        # endregion

        # region - achievement badges
        achievement_badges_section = tk.Frame(home_window, highlightbackground='black', highlightthickness=1)
        achievement_badges_section.place(x=250, y=470)
        achievement_badges_section.propagate(0)
        achievement_badges_section.config(width=800, height=200)

        # display latest 4 achievement 
        
        # badge one display
        badge_one_img = Image.open('img/achievement_badges/first_entry.png')
        badge_one_img = ImageTk.PhotoImage(badge_one_img)

        badge_one_name = tk.Label(achievement_badges_section, text='Newcomer', font=('helvetica', 12))
        badge_one = tk.Label(achievement_badges_section, image=badge_one_img)
        badge_one.image = badge_one_img
        badge_one_date = tk.Label(achievement_badges_section, text='Unlocked: \n10/11/2024', font=('helvetica', 10))

        badge_one_name.place(x=30, y=10)
        badge_one.place(x=10, y=30)  
        badge_one_date.place(x=30, y=130)

        # badge two display
        badge_two_img = Image.open('img/achievement_badges/five_entries.png')
        badge_two_img = ImageTk.PhotoImage(badge_two_img)

        badge_two_name = tk.Label(achievement_badges_section, text='Moving Along', font=('helvetica', 12))
        badge_two = tk.Label(achievement_badges_section, image=badge_two_img)
        badge_two.image = badge_two_img
        badge_two_date = tk.Label(achievement_badges_section, text='Unlocked: \n24/11/2024', font=('helvetica', 10))

        badge_two_name.place(x=230, y=10)
        badge_two.place(x=210, y=30)
        badge_two_date.place(x=230, y=130)

        # badge three display
        badge_three_img = Image.open('img/achievement_badges/ten_anime.png')
        badge_three_img = ImageTk.PhotoImage(badge_three_img)

        badge_three_name = tk.Label(achievement_badges_section, text='Anime Star', font=('helvetica', 12))
        badge_three = tk.Label(achievement_badges_section, image=badge_three_img)
        badge_three.image = badge_three_img
        badge_three_date = tk.Label(achievement_badges_section, text='Unlocked: \n31/11/2024', font=('helvetica', 10))

        badge_three_name.place(x=430, y=10)
        badge_three.place(x=410, y=30)
        badge_three_date.place(x=430, y=130)

        # badge four display
        badge_four_img = Image.open('img/achievement_badges/hundred_chapters.png')
        badge_four_img = ImageTk.PhotoImage(badge_four_img)

        badge_four_name = tk.Label(achievement_badges_section, text='Manga Star', font=('helvetica', 12))
        badge_four = tk.Label(achievement_badges_section, image=badge_four_img)
        badge_four.image = badge_four_img
        badge_four_date = tk.Label(achievement_badges_section, text='Unlocked: \n14/12/2024', font=('helvetica', 10))

        badge_four_name.place(x=630, y=10)
        badge_four.place(x=610, y=30)
        badge_four_date.place(x=610, y=130)
        # endregion

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

    def edit_bio_info(self):
        self.user_bio_info.config(state='normal')
        self.confirm_bio.place(x=480, y=150)

    def confirm_bio_info(self):
        users['user'].bio_message = self.user_bio_info.get('1.0', 'end')
        self.controller.update_user_save()
        self.user_bio_info.config(state='disabled')
        self.confirm_bio.place_forget()

class NewEntryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.given_title = tk.StringVar()
        self.selected_ctype = tk.StringVar()
        self.selected_rating = tk.StringVar()
        self.current_progress = tk.StringVar()
        self.total_progress = tk.StringVar()
        self.selected_status = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        new_entry_window = tk.Frame(self, highlightbackground='black', highlightthickness=2)
        new_entry_window.place(relx=0.5, rely=0.5, anchor='center')
        new_entry_window.propagate(0)
        new_entry_window.config(width=1100, height=700)
    
        # region - new entry form
        new_entry_form = tk.Frame(new_entry_window, highlightbackground='black', highlightthickness=1)
        new_entry_form.place(x=250, y=50)
        new_entry_form.propagate(0)
        new_entry_form.config(width=800, height=600)

        new_entry_section_title = tk.Label(new_entry_form, text='New Entry', font=('helvetica', 18))

        new_entry_title = tk.Label(new_entry_form, text='Title:', font=('helvetica', 18))
        new_entry_ctype = tk.Label(new_entry_form, text='Content Type:', font=('helvetica', 18))
        new_entry_rating = tk.Label(new_entry_form, text='Rating:', font=('helvetica', 18))
        new_entry_progress = tk.Label(new_entry_form, text='Progress:', font=('helvetica', 18))
        new_entry_status = tk.Label(new_entry_form, text='Status:', font=('helvetica', 18))
        new_entry_start_date = tk.Label(new_entry_form, text='Start Date:', font=('helvetica', 18))
        new_entry_end_date = tk.Label(new_entry_form, text='End Date:', font=('helvetica', 18))

        new_entry_section_title.place(x=300, y=50)

        new_entry_title.place(x=150, y=100)
        new_entry_ctype.place(x=150, y=150)
        new_entry_rating.place(x=150, y=200)
        new_entry_progress.place(x=150, y=250)
        new_entry_status.place(x=150, y=300)
        new_entry_start_date.place(x=150, y=350)
        new_entry_end_date.place(x=150, y=400)

        new_entry_title_info = tk.Entry(new_entry_form, font=('helvetica', 18), textvariable=self.given_title)

        ctype_options = [
            "Book",
            "Anime",
            "Manga",
            "Manhwa",
            "TV Show",
            "Movie",
            "OVA"
        ]
        self.selected_ctype.set("Select Content Type")
        new_entry_ctype_info = tk.OptionMenu(new_entry_form, self.selected_ctype, *ctype_options)
        new_entry_ctype_info.config(font=('helvetica', 12), indicatoron=0)

        rating_options = [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10
        ]
        self.selected_rating.set('Select Rating')
        new_entry_rating_info = tk.OptionMenu(new_entry_form, self.selected_rating, *rating_options)
        new_entry_rating_info.config(font=('helvetica', 12), indicatoron=0)

        new_entry_progress_info_current = tk.Entry(new_entry_form, font=('helvetica', 18), textvariable=self.current_progress)
        new_entry_progress_info_current.config(width=5)
        new_entry_progress_info_divider = tk.Label(new_entry_form, text='/', font=('helvetica', 18))
        new_entry_progress_info_total = tk.Entry(new_entry_form, font=('helvetica', 18), textvariable=self.total_progress)
        new_entry_progress_info_total.config(width=5)
        new_entry_progress_metric = tk.Label(new_entry_form, text='Episodes/Chapters', font=('helvetica', 12))

        status_options = [
            'Planned',
            'Viewing', 
            'Paused',
            'Dropped',
            'Finished'
        ]
        self.selected_status.set('Select Status')
        new_entry_status_info = tk.OptionMenu(new_entry_form, self.selected_status, *status_options)
        new_entry_status_info.config(font=('helvetica', 12), indicatoron=0)

        self.new_entry_start_date_info = DateEntry(new_entry_form, date_pattern='dd-mm-yyyy')
        self.new_entry_start_date_info.config(font=('helvetica', 12))
        self.new_entry_end_date_info = DateEntry(new_entry_form, date_pattern='dd-mm-yyyy')
        self.new_entry_end_date_info.config(font=('helvetica', 12))

        new_entry_submit = tk.Button(new_entry_form, text='Submit Entry', font=('helvetica', 18), command=self.create_new_entry)
        new_entry_cancel = tk.Button(new_entry_form, text='Cancel Entry', font=('helvetica', 18), command=self.cancel_new_entry)

        new_entry_title_info.place(x=350, y=100)
        new_entry_ctype_info.place(x=350, y=150)
        new_entry_rating_info.place(x=350, y=200)
        new_entry_progress_info_current.place(x=350, y=250)
        new_entry_progress_info_divider.place(x=445, y=250)
        new_entry_progress_info_total.place(x=480, y=250)
        new_entry_progress_metric.place(x=580, y=250)
        new_entry_status_info.place(x=350, y=300)
        self.new_entry_start_date_info.place(x=350, y=350)
        self.new_entry_end_date_info.place(x=350, y=400)

        new_entry_submit.place(x=150, y=480)
        new_entry_cancel.place(x=350, y=480)

        self.error_message = tk.Label(new_entry_form, text='', font=('helvetica', 18), foreground='red')
        self.error_message.place(x=200, y=550)
        # endregion

    # create a new entry
    def create_new_entry(self):
        if not self.validate_entry():
            new_entry = EntryInfo(self.given_title.get(), self.selected_ctype.get(), self.selected_rating.get(), self.current_progress.get(),
                                self.total_progress.get(), self.selected_status.get(), self.new_entry_start_date_info.get(), self.new_entry_end_date_info.get())
            entries[self.given_title.get()] = new_entry
            # update the total count of entries
            users['user'].total_entries_count += 1
            # update the total count for episodes/chapters and anime/manga
            if self.selected_ctype.get() in ['Anime', 'TV Show', 'Movie', 'ONA']:
                users['user'].total_episodes_count += int(self.current_progress.get())
                users['user'].total_anime_count += 1
            else:
                users['user'].total_chapters_count += int(self.current_progress.get())
                users['user'].total_manga_count += 1
            # region - achievement tracking trigger

            # get date and format
            today = datetime.today()
            today = today.strftime("%d-%m-%Y")

            # achievement: first entry
            # achievement granted when first entry is saved
            # only trigger once (regardless of full entry page was cleared)
            if users['user'].total_entries_count == 1 and achievements['first_entry'].date_unlocked == "":
                # update the achievement with the date unlocked
                achievements['first_entry'].date_unlocked = today
                # update the achievements save file
                self.controller.update_achievements_save()

            # achievement: speedster
            if self.new_entry_start_date_info.get() == self.new_entry_end_date_info.get() and achievements['speedster'].date_unlocked == "":
                # update the achievement with the date unlocked
                achievements['speedster'].date_unlocked = today
                # update the achievements save file
                self.controller.update_achievements_save()

            # achievement: five entries
            if users['user'].total_entries_count == 5 and achievements['five_entries'].date_unlocked == "":
                # update the achievement with the date unlocked
                achievements['five_entries'].date_unlocked = today
                # update the achievements save file
                self.controller.update_achievements_save()

            # achievement: hundred chapters
            if users['user'].total_chapters_count >= 100 and achievements['hundred_chapters'].date_unlocked == "":
                # update the achievement with the date unlocked
                achievements['hundred_chapters'].date_unlocked = today
                # update the achievements save file
                self.controller.update_achievements_save()

            # achievement: hundred episodes
            if users['user'].total_episodes_count >= 100 and achievements['hundred_episodes'].date_unlocked == "":
                achievements['hundred_episodes'].date_unlocked = today
                self.controller.update_achievements_save()

            # achievement: ten mangas
            if users['user'].total_manga_count == 10 and achievements['ten_mangas'].date_unlocked == "":
                achievements['ten_mangas'].date_unlocked = today
                self.controller.update_achievements_save()

            # achievement: ten anime
            if users['user'].total_anime_count == 10 and achievements['ten_anime'].date_unlocked == "":
                achievements['ten_anime'].date_unlocked = today
                self.controller.update_achievements_save()

            # endregion
            self.controller.update_entries_save()
            self.controller.update_user_save()
            self.clear_entry_fields()
            self.controller.show_page(EntriesPage)
            # update the entries list with the addition of the new entry
            self.controller.populate_entries(self.controller.pages[EntriesPage].entries_lb)

    # validation checks for new entries
    def validate_entry(self):
        entry_titles = []
        for i in entries.keys():
            entry_titles.append(i.lower())
        if len(self.given_title.get()) < 1 or self.given_title.get() == len(self.given_title.get())*' ':
            self.error_message.config(text='Invalid Title Provided.')
        elif self.given_title.get().lower() in entry_titles:
            self.error_message.config(text='Entry Already Exists.')
        elif self.selected_ctype.get() == 'Select Content Type':
            self.error_message.config(text='Content Type Selection Required.')
        elif self.selected_rating.get() == 'Select Rating':
            self.error_message.config(text='Rating Selection Required.')
        elif not self.current_progress.get().isdigit() or not self.total_progress.get().isdigit():
            self.error_message.config(text='Progress Accepts Integers Only.')
        elif int(self.current_progress.get()) > int(self.total_progress.get()):
            self.error_message.config(text='Current Cannot Be More Than Total Progress.')
        elif self.selected_status.get() == 'Select Status':
            self.error_message.config(text='Status Selection Required.')
        else:
            return False
        self.error_message.after(1000, self.clear_error_message)
        return True
            
    # resets new entry's input fields
    def cancel_new_entry(self):
        self.clear_entry_fields()
        self.controller.show_page(EntriesPage)

    # clears the input fields for the entry form
    def clear_entry_fields(self):
        today = datetime.today().strftime('%d-%m-%Y')
        self.given_title.set('')
        self.selected_ctype.set('Select Content Type')
        self.selected_rating.set('Select Rating')
        self.current_progress.set('')
        self.total_progress.set('')
        self.selected_status.set('Select Status')
        self.new_entry_start_date_info.set_date(today)
        self.new_entry_end_date_info.set_date(today)

    # clears the error message
    def clear_error_message(self):
        self.error_message.config(text='')

class UpdateEntryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.given_title = tk.StringVar()
        self.selected_ctype = tk.StringVar()
        self.selected_rating = tk.IntVar()
        self.current_progress = tk.StringVar()
        self.total_progress = tk.StringVar()
        self.selected_status = tk.StringVar()

        self.create_widgets()

        self.controller.entry_id_var.trace_add('write', self.load_existing_entry_info)

    def create_widgets(self):
        update_entry_window = tk.Frame(self, highlightbackground='black', highlightthickness=2)
        update_entry_window.place(relx=0.5, rely=0.5, anchor='center')
        update_entry_window.propagate(0)
        update_entry_window.config(width=1100, height=700)

        # region - entry form for update
        update_entry_form = tk.Frame(update_entry_window, highlightbackground='black', highlightthickness=1)
        update_entry_form.place(relx=0.5, rely=0.5, anchor='center')
        update_entry_form.propagate(0)
        update_entry_form.config(width=800, height=600)

        update_entry_section_title = tk.Label(update_entry_form, text='Update Entry', font=('helvetica', 18))

        update_entry_title = tk.Label(update_entry_form, text='Title:', font=('helvetica', 18))
        update_entry_ctype = tk.Label(update_entry_form, text='Content Type:', font=('helvetica', 18))
        update_entry_rating = tk.Label(update_entry_form, text='Rating:', font=('helvetica', 18))
        update_entry_progress = tk.Label(update_entry_form, text='Progress:', font=('helvetica', 18))
        update_entry_status = tk.Label(update_entry_form, text='Status:', font=('helvetica', 18))
        update_entry_start_date = tk.Label(update_entry_form, text='Start Date:', font=('helvetica', 18))
        update_entry_end_date = tk.Label(update_entry_form, text='End Date:', font=('helvetica', 18))

        update_entry_section_title.place(x=300, y=50)

        update_entry_title.place(x=150, y=100)
        update_entry_ctype.place(x=150, y=150)
        update_entry_rating.place(x=150, y=200)
        update_entry_progress.place(x=150, y=250)
        update_entry_status.place(x=150, y=300)
        update_entry_start_date.place(x=150, y=350)
        update_entry_end_date.place(x=150, y=400)

        self.update_entry_title_info = tk.Entry(update_entry_form, font=('helvetica', 18), textvariable=self.given_title)

        ctype_options = [
            "Book",
            "Anime",
            "Manga",
            "Manhwa",
            "TV Show",
            "Movie",
            "OVA"
        ]
        self.selected_ctype.set("Select Content Type")
        self.update_entry_ctype_info = tk.OptionMenu(update_entry_form, self.selected_ctype, *ctype_options)
        self.update_entry_ctype_info.config(font=('helvetica', 12), indicatoron=0)

        rating_options = [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10
        ]
        self.selected_rating.set('Select Rating')
        self.update_entry_rating_info = tk.OptionMenu(update_entry_form, self.selected_rating, *rating_options)
        self.update_entry_rating_info.config(font=('helvetica', 12), indicatoron=0)

        self.update_entry_progress_info_current = tk.Entry(update_entry_form, font=('helvetica', 18), textvariable=self.current_progress)
        self.update_entry_progress_info_current.config(width=5)
        self.update_entry_progress_info_divider = tk.Label(update_entry_form, text='/', font=('helvetica', 18))
        self.update_entry_progress_info_total = tk.Entry(update_entry_form, font=('helvetica', 18), textvariable=self.total_progress)
        self.update_entry_progress_info_total.config(width=5)

        status_options = [
            'Planned',
            'Viewing', 
            'Paused',
            'Dropped',
            'Finished'
        ]
        self.selected_status.set('Select Status')
        self.update_entry_status_info = tk.OptionMenu(update_entry_form, self.selected_status, *status_options)
        self.update_entry_status_info.config(font=('helvetica', 12), indicatoron=0)

        self.update_entry_start_date_info = DateEntry(update_entry_form, date_pattern='dd-mm-yyyy')
        self.update_entry_start_date_info.config(font=('helvetica', 12))
        self.update_entry_end_date_info = DateEntry(update_entry_form, date_pattern='dd-mm-yyyy')
        self.update_entry_end_date_info.config(font=('helvetica', 12))

        update_entry_submit = tk.Button(update_entry_form, text='Update Entry', font=('helvetica', 18), command=self.update_entry)
        update_entry_cancel = tk.Button(update_entry_form, text='Cancel Entry', font=('helvetica', 18), command=lambda:self.controller.show_page(EntriesPage))

        self.update_entry_title_info.place(x=350, y=100)
        self.update_entry_ctype_info.place(x=350, y=150)
        self.update_entry_rating_info.place(x=350, y=200)
        self.update_entry_progress_info_current.place(x=350, y=250)
        self.update_entry_progress_info_divider.place(x=445, y=250)
        self.update_entry_progress_info_total.place(x=480, y=250)
        self.update_entry_status_info.place(x=350, y=300)
        self.update_entry_start_date_info.place(x=350, y=350)
        self.update_entry_end_date_info.place(x=350, y=400)

        update_entry_submit.place(x=150, y=480)
        update_entry_cancel.place(x=350, y=480)

        self.error_message = tk.Label(update_entry_form, text='', font=('helvetica', 18), foreground='red')
        self.error_message.place(x=200, y=550)
        # endregion

    # temp* check info retrieved
    def get_details(self):
        print(self.given_title.get())
        print(self.selected_ctype.get())
        print(self.selected_rating.get())
        print(self.current_progress.get())
        print(self.total_progress.get())
        print(self.selected_status.get())
        print(self.update_entry_start_date_info.get())
        print(self.update_entry_end_date_info.get())

        print(self.controller.entry_id_var.get())

    # load the existing entry's details as prefilled information and set relevant variables
    def load_existing_entry_info(self, *args):
        entry_id = self.controller.entry_id_var.get()
        self.given_title.set(entries[entry_id].title)
        self.selected_ctype.set(entries[entry_id].content_type)
        self.selected_rating.set(entries[entry_id].rating)
        self.current_progress.set(entries[entry_id].current_progress)
        self.total_progress.set(entries[entry_id].total_progress)
        self.selected_status.set(entries[entry_id].status)
        self.update_entry_start_date_info.set_date(entries[entry_id].start_date)
        self.update_entry_end_date_info.set_date(entries[entry_id].end_date)

    def update_entry(self):
        if not self.validate_entry():
            entry_id = self.controller.entry_id_var.get()

            # determine and update the total episodes/chapters counted from the given entry
            if self.selected_ctype.get() in ['Anime', 'TV Show', 'Movie', 'ONA']:
                users['user'].total_episodes_count -= int(entries[entry_id].current_progress)
                users['user'].total_episodes_count += int(self.current_progress.get())
            else:
                users['user'].total_chapters_count -= int(entries[entry_id].current_progress)
                users['user'].total_chapters_count += int(self.current_progress.get())
            self.controller.update_user_save()

            entries[entry_id].title = self.given_title.get()
            entries[entry_id].content_type = self.selected_ctype.get()
            entries[entry_id].rating = self.selected_rating.get()
            entries[entry_id].current_progress = self.current_progress.get()
            entries[entry_id].total_progress = self.total_progress.get()
            entries[entry_id].status = self.selected_status.get()
            entries[entry_id].start_date = self.update_entry_start_date_info.get()
            entries[entry_id].end_date = self.update_entry_end_date_info.get()

            # if the entry's title is updated, update the key name for the given entry
            if self.given_title.get() != entry_id:
                entries[self.given_title.get()] = entries.pop(entry_id)
            self.controller.update_entries_save()
            self.controller.populate_entries(self.controller.pages[EntriesPage].entries_lb)
            self.controller.show_page(EntriesPage)

            # region - achievement tracking trigger
            today = datetime.today()
            today = today.strftime('%d-%m-%Y')

            # achievement: speedster
            if entries[entry_id].start_date == entries[entry_id].end_date and achievements['speedster'].date_unlocked == "":
                achievements['speedster'].date_unlocked = entries[entry_id].end_date
                self.controller.update_achievements_save()
            
            # achievement: hundred chapters
            if users['user'].total_chapters_count >= 100 and achievements['hundred_chapters'].date_unlocked == "":
                achievements['hundred_chapters'].date_unlocked = today
                self.controller.update_achievements_save()

            # achievement: hundred episodes
            if users['user'].total_episodes_count >= 100 and achievements['hundred_episodes'].date_unlocked == "":
                achievements['hundred_episodes'].date_unlocked = today
                self.controller.update_achievements_save()

            # endregion

    # validation checks for entry updates
    def validate_entry(self):
        entry_id = self.controller.entry_id_var.get()
        entry_titles = []
        for i in entries.keys():
            entry_titles.append(i.lower())
        if len(self.given_title.get()) < 1 or self.given_title.get() == len(self.given_title.get())*' ':
            self.error_message.config(text='Invalid Title Provided.')
        elif self.given_title.get().lower() in entry_titles and self.given_title.get().lower() != entry_id.lower():
            self.error_message.config(text='Entry Already Exists.')
        elif not self.current_progress.get().isdigit() or not self.total_progress.get().isdigit():
            self.error_message.config(text='Progress Accepts Integers Only.')
        elif int(self.current_progress.get()) > int(self.total_progress.get()):
            self.error_message.config(text='Current Progress Cannot Exceed Total Progress.')
        else:
            return False
        self.error_message.after(1000, self.clear_error_message)
        return True
    
    # clear the error message
    def clear_error_message(self):
        self.error_message.config(text='')

class EntriesPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        
        self.create_widgets()

    def create_widgets(self):
        entries_window = tk.Frame(self, highlightbackground='black', highlightthickness=2)
        entries_window.place(relx=0.5, rely=0.5, anchor='center')
        entries_window.propagate(0)
        entries_window.config(width=1100, height=700)

        # region - navigation bar
        nav_bar = tk.Frame(entries_window, highlightbackground='grey', highlightthickness=1)
        nav_bar.place(x=10, y=50)
        nav_bar.propagate(0)
        nav_bar.config(width=200, height=600)

        home_navtitle = tk.Label(nav_bar, text='Home', font=('helvetica', 18))
        discover_navtitle = tk.Label(nav_bar, text='Discover', font=('helvetica', 18))
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
        discover_navtitle.place(x=50, y=100)
        entries_navtitle.place(x=50, y=150)
        settings_navtitle.place(x=50, y=200)

        self.login_status.place(x=15, y=300)

        # when option is clicked in the navbar
        home_navtitle.bind("<Button-1>", lambda mouse_event: self.redirect_page(mouse_event, HomePage))
        discover_navtitle.bind("<Button-1>", lambda mouse_event: self.redirect_page(mouse_event, DiscoverPage))
        entries_navtitle.bind("<Button-1>", lambda mouse_event: self.redirect_page(mouse_event, EntriesPage))
        settings_navtitle.bind("<Button-1>", lambda mouse_event: self.redirect_page(mouse_event, SettingsPage))

        self.login_status.bind("<Button-1>", lambda mouse_event: self.toggle_login(mouse_event))

        # when option is hovered over in the navbar
        home_navtitle.bind("<Enter>", lambda mouse_event: self.controller.on_hover(mouse_event, home_navtitle))
        home_navtitle.bind("<Leave>", lambda mouse_event: self.controller.off_hover(mouse_event, home_navtitle))
        discover_navtitle.bind("<Enter>", lambda mouse_event: self.controller.on_hover(mouse_event, discover_navtitle))
        discover_navtitle.bind("<Leave>", lambda mouse_event: self.controller.off_hover(mouse_event, discover_navtitle))
        entries_navtitle.bind("<Enter>", lambda mouse_event: self.controller.on_hover(mouse_event, entries_navtitle))
        entries_navtitle.bind("<Leave>", lambda mouse_event: self.controller.off_hover(mouse_event, entries_navtitle))
        settings_navtitle.bind("<Enter>", lambda mouse_event: self.controller.on_hover(mouse_event, settings_navtitle))
        settings_navtitle.bind("<Leave>", lambda mouse_event: self.controller.off_hover(mouse_event, settings_navtitle))

        self.login_status.bind("<Enter>", lambda mouse_event: self.controller.on_hover(mouse_event, self.login_status))
        self.login_status.bind("<Leave>", lambda mouse_event: self.controller.off_hover(mouse_event, self.login_status))
        # endregion

        # region - list of entries section (left side)
        entries_title = tk.Label(entries_window, text='List Of Entries', font=('helvetica', 18))
        entries_title.place(x=250, y=50)
        self.entries_lb = tk.Listbox(entries_window)
        self.entries_lb.place(x=250, y=100)
        entries_sb = tk.Scrollbar(entries_window)
        entries_sb.place(x=488, y=100, height=400)
        self.entries_lb.config(yscrollcommand=entries_sb.set, height=21, width=26, font=('helvetica', 12))
        entries_sb.config(command=self.entries_lb.yview, width=20)

        # populate the entries list with all of the user's entries
        self.controller.populate_entries(self.entries_lb)

        update_entries_btn = tk.Button(entries_window, text='Update An Entry', font=('helvetica', 18), command=self.load_update_entry)
        delete_entries_btn = tk.Button(entries_window, text='Delete An Entry', font=('helvetica', 18), command=self.delete_entry)

        update_entries_btn.place(x=250, y=530, width=250)
        delete_entries_btn.place(x=250, y=600, width=250)

        # endregion

        # region - entry details (right side)
        entries_details_title = tk.Label(entries_window, text='Entry Details', font=('helvetica', 18))
        entries_details_title.place(x=700, y=50)

        new_entries_btn = tk.Button(entries_window, text='+ Add New Entry', font=('helvetica', 10), command=lambda: self.controller.show_page(NewEntryPage))
        new_entries_btn.place(x=950, y=50)

        # entry details window
        edetails_window = tk.Frame(entries_window, highlightbackground='black', highlightthickness=1)
        edetails_window.place(x=550, y=100)
        edetails_window.propagate(0)
        edetails_window.config(width=500, height=550)

        # entry subtitles
        entry_title = tk.Label(edetails_window, text='Title:', font=('helvetica', 18))
        entry_ctype = tk.Label(edetails_window, text='Content Type:', font=('helvetica', 18))
        entry_rating = tk.Label(edetails_window, text='User Rating:', font=('helvetica', 18))
        entry_progress = tk.Label(edetails_window, text='User Progress:', font=('helvetica', 18))
        entry_status = tk.Label(edetails_window, text='Status:', font=('helvetica', 18))
        entry_start_date = tk.Label(edetails_window, text='Start Date:', font=('helvetica', 18))
        entry_end_date = tk.Label(edetails_window, text='End Date:', font=('helvetica', 18))

        entry_title.place(x=50, y=50)
        entry_ctype.place(x=50, y=100)
        entry_rating.place(x=50, y=150)
        entry_progress.place(x=50, y=200)
        entry_status.place(x=50, y=250)
        entry_start_date.place(x=50, y=300)
        entry_end_date.place(x=50, y=350)

        # entry information
        # current text is dummy text
        self.entry_title_info = tk.Label(edetails_window, text='', font=('helvetica', 18), width=16, anchor='w')
        self.entry_ctype_info = tk.Label(edetails_window, text='', font=('helvetica', 18))
        self.entry_rating_info = tk.Label(edetails_window, text='', font=('helvetica', 18))
        self.entry_progress_info = tk.Label(edetails_window, text='', font=('helvetica', 18))
        self.entry_status_info = tk.Label(edetails_window, text='', font=('helvetica', 18))
        self.entry_start_date_info = tk.Label(edetails_window, text='', font=('helvetica', 18))
        self.entry_end_date_info = tk.Label(edetails_window, text='', font=('helvetica', 18))

        self.entry_title_info.place(x=250, y=50)
        self.entry_ctype_info.place(x=250, y=100)
        self.entry_rating_info.place(x=250, y=150)
        self.entry_progress_info.place(x=250, y=200)
        self.entry_status_info.place(x=250, y=250)
        self.entry_start_date_info.place(x=250, y=300)
        self.entry_end_date_info.place(x=250, y=350) 
        # endregion

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

    # select and display entry details
    def display_entry_details(self, mouse_event):

        # selected entry's reference variable
        entry_id = ''

        # find user's selected item (otherwise known as entry)
        for i in self.entries_lb.curselection():
            entry_id = self.entries_lb.get(i)

        # display the selected entry's details on the right side of the entries page
        self.entry_title_info.config(text=entries[entry_id].title)
        self.entry_ctype_info.config(text=entries[entry_id].content_type)
        self.entry_rating_info.config(text=entries[entry_id].rating)
        # determine whether progress should show episodes or chapters based on content type of the entry
        if entries[entry_id].content_type in ['Anime', 'TV Show', 'Movie', 'ONA']:
            self.entry_progress_info.config(text=f'{entries[entry_id].current_progress} / {entries[entry_id].total_progress} Episodes')
        else:
            self.entry_progress_info.config(text=f'{entries[entry_id].current_progress} / {entries[entry_id].total_progress} Chapters')
        self.entry_status_info.config(text=entries[entry_id].status)
        self.entry_start_date_info.config(text=entries[entry_id].start_date)
        self.entry_end_date_info.config(text=entries[entry_id].end_date)

    # loads the details for the selected entry that will be getting updated
    # redirects to the update entry page
    def load_update_entry(self):
        entry_id = ''
        # get the selected entry's id
        for i in self.entries_lb.curselection():
            entry_id = self.entries_lb.get(i)

        if entry_id:
            # set the global variable for entry_id_var to the selected entry id
            self.controller.entry_id_var.set(entry_id)
            # redirect to the update entry page
            self.controller.show_page(UpdateEntryPage)

        # if the if statement is not triggered, just do nothing

    # delete the selected entry in the the entries list
    def delete_entry(self):
        entry_name = ''
        # get the selected entry's id
        for i in self.entries_lb.curselection():
            entry_name = self.entries_lb.get(i)
            # get selection item index
            entry_id = i
        
        if entry_name:
            # reference the currently selected entry to update it's user metric relevance
            if entries[entry_name].content_type in ['Anime', 'TV Show', 'Movie', 'ONA']:
                users['user'].total_episodes_count -= int(entries[entry_name].current_progress)
                users['user'].total_anime_count -= 1
            else:
                users['user'].total_chapters_count -= int(entries[entry_name].current_progress)
                users['user'].total_manga_count -= 1
            # delete the selectd entry from the dictionary and listbox
            del entries[entry_name]
            self.entries_lb.delete(entry_id)
            # reduce 'total_entries_count' by 1
            users['user'].total_entries_count -= 1
            self.controller.update_user_save()

        # update the entries save data
        self.controller.update_entries_save()

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
        discover_navtitle = tk.Label(nav_bar, text='Discover', font=('helvetica', 18))
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
        discover_navtitle.place(x=50, y=100)
        entries_navtitle.place(x=50, y=150)
        settings_navtitle.place(x=50, y=200)

        self.login_status.place(x=15, y=300)

        # when option is clicked in the navbar
        home_navtitle.bind("<Button-1>", lambda mouse_event: self.redirect_page(mouse_event, HomePage))
        discover_navtitle.bind("<Button-1>", lambda mouse_event: self.redirect_page(mouse_event, DiscoverPage))
        entries_navtitle.bind("<Button-1>", lambda mouse_event: self.redirect_page(mouse_event, EntriesPage))
        settings_navtitle.bind("<Button-1>", lambda mouse_event: self.redirect_page(mouse_event, SettingsPage))

        self.login_status.bind("<Button-1>", lambda mouse_event: self.toggle_login(mouse_event))

        # when option is hovered over in the navbar
        home_navtitle.bind("<Enter>", lambda mouse_event: self.controller.on_hover(mouse_event, home_navtitle))
        home_navtitle.bind("<Leave>", lambda mouse_event: self.controller.off_hover(mouse_event, home_navtitle))
        discover_navtitle.bind("<Enter>", lambda mouse_event: self.controller.on_hover(mouse_event, discover_navtitle))
        discover_navtitle.bind("<Leave>", lambda mouse_event: self.controller.off_hover(mouse_event, discover_navtitle))
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

    # open and discover for image file
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

class DiscoverPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.create_widgets()

    def create_widgets(self):
        discover_window = tk.Frame(self, highlightbackground='black', highlightthickness=2)
        discover_window.place(relx=0.5, rely=0.5, anchor='center')
        discover_window.propagate(0)
        discover_window.config(width=1100, height=700)

        # region - navigation bar
        nav_bar = tk.Frame(discover_window, highlightbackground='grey', highlightthickness=1)
        nav_bar.place(x=10, y=50)
        nav_bar.propagate(0)
        nav_bar.config(width=200, height=600)

        home_navtitle = tk.Label(nav_bar, text='Home', font=('helvetica', 18))
        discover_navtitle = tk.Label(nav_bar, text='Discover', font=('helvetica', 18))
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
        discover_navtitle.place(x=50, y=100)
        entries_navtitle.place(x=50, y=150)
        settings_navtitle.place(x=50, y=200)

        self.login_status.place(x=15, y=300)

        # when option is clicked in the navbar
        home_navtitle.bind("<Button-1>", lambda mouse_event: self.redirect_page(mouse_event, HomePage))
        discover_navtitle.bind("<Button-1>", lambda mouse_event: self.redirect_page(mouse_event, DiscoverPage))
        entries_navtitle.bind("<Button-1>", lambda mouse_event: self.redirect_page(mouse_event, EntriesPage))
        settings_navtitle.bind("<Button-1>", lambda mouse_event: self.redirect_page(mouse_event, SettingsPage))

        self.login_status.bind("<Button-1>", lambda mouse_event: self.toggle_login(mouse_event))

        # when option is hovered over in the navbar
        home_navtitle.bind("<Enter>", lambda mouse_event: self.controller.on_hover(mouse_event, home_navtitle))
        home_navtitle.bind("<Leave>", lambda mouse_event: self.controller.off_hover(mouse_event, home_navtitle))
        discover_navtitle.bind("<Enter>", lambda mouse_event: self.controller.on_hover(mouse_event, discover_navtitle))
        discover_navtitle.bind("<Leave>", lambda mouse_event: self.controller.off_hover(mouse_event, discover_navtitle))
        entries_navtitle.bind("<Enter>", lambda mouse_event: self.controller.on_hover(mouse_event, entries_navtitle))
        entries_navtitle.bind("<Leave>", lambda mouse_event: self.controller.off_hover(mouse_event, entries_navtitle))
        settings_navtitle.bind("<Enter>", lambda mouse_event: self.controller.on_hover(mouse_event, settings_navtitle))
        settings_navtitle.bind("<Leave>", lambda mouse_event: self.controller.off_hover(mouse_event, settings_navtitle))

        self.login_status.bind("<Enter>", lambda mouse_event: self.controller.on_hover(mouse_event, self.login_status))
        self.login_status.bind("<Leave>", lambda mouse_event: self.controller.off_hover(mouse_event, self.login_status))
        # endregion

        # region - discover content section
        search_animanga_title = tk.Label(discover_window, text='Search:', font=('helvetica', 18))
        self.search_animanga_entry = tk.Entry(discover_window, font=('helvetica', 18), foreground='grey', width=25)
        self.search_animanga_entry.insert(0, 'Search Anime or Manga')
        search_random_anime = tk.Button(discover_window, text='Random Anime', font=('helvetica', 12), command=self.process_random_anime)
        search_random_manga = tk.Button(discover_window, text='Random Manga', font=('helvetica', 12), command=self.process_random_manga)

        search_animanga_title.place(x=300, y=50)
        self.search_animanga_entry.place(x=400, y=50)
        search_random_anime.place(x=750, y=50)
        search_random_manga.place(x=900, y=50)

        self.error_message = tk.Label(discover_window, font=('helvetica', 18), foreground='red')

        self.title_result = tk.Label(discover_window, font=('helvetica', 14))
        self.genres_result = tk.Label(discover_window, font=('helvetica', 14))
        self.score_result = tk.Label(discover_window, font=('helvetica', 14))
        self.type_result = tk.Label(discover_window, font=('helvetica', 14))
        self.status_result = tk.Label(discover_window, font=('helvetica', 14))
        self.installment_result = tk.Label(discover_window, font=('helvetica', 14))

        self.cover_result = tk.Label(discover_window)

        self.error_message.place(x=500, y=100)

        self.title_result.place(x=300, y=150)
        self.genres_result.place(x=300, y=200)
        self.score_result.place(x=300, y=250)
        self.type_result.place(x=300, y=300)
        self.status_result.place(x=300, y=350)
        self.installment_result.place(x=300, y=400)

        self.cover_result.place(x=700, y=150)

        self.search_animanga_entry.bind('<Button-1>', lambda mouse_event: self.on_entry_mode_search(mouse_event))
        self.bind('<Button-1>', lambda mouse_event: self.off_entry_mode_search(mouse_event))
        nav_bar.bind('<Button-1>', lambda mouse_event: self.off_entry_mode_search(mouse_event))
        discover_window.bind('<Button-1>', lambda mouse_event: self.off_entry_mode_search(mouse_event))
        search_random_anime.bind('<Button-1>', lambda mouse_event: self.off_entry_mode_search(mouse_event))
        search_random_manga.bind('<Button-1>', lambda mouse_event: self.off_entry_mode_search(mouse_event))
        self.search_animanga_entry.bind('<Return>', lambda mouse_event: self.process_animanga(mouse_event, self.search_animanga_entry.get()))
        # endregion

    # redirects user to the selected page from the navbar
    def redirect_page(self, mouse_event, page_name):
        # reset the search field in the discover page
        self.off_entry_mode_search(mouse_event)
        self.controller.show_page(page_name)

    # toggling the status of the login's 'stay on' feature
    def toggle_login(self, mouse_event):
        # reset the search field in the discover page
        self.off_entry_mode_search(mouse_event)
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

    # when clicked inside the search field, remove prefilled text
    def on_entry_mode_search(self, mouse_event):
        self.search_animanga_entry.delete(0, 'end')
        self.search_animanga_entry.config(foreground='black')

    # reset the search field with prefilled text
    def off_entry_mode_search(self, mouse_event):
        if len(self.search_animanga_entry.get()) < 1:
            self.search_animanga_entry.insert(0, 'Search Anime or Manga')
            self.search_animanga_entry.config(foreground='grey')

    # search anime or manga in MAL database
    def search_animanga(self, search_value):
        url = f'https://api.jikan.moe/v4/anime?q={search_value}'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if 'data' in data:
                    content_data = data['data']
                    # tally the total results found
                    results_size = len(content_data)
                    # validate if no results were found
                    if results_size < 1:
                        return None
                    # select a random result from the tallied results
                    content_data = data['data'][random.randint(0, results_size)]
                    # proceed with rest of the details as normal
                    title = content_data['title']
                    genres = ', '.join(genre['name'] for genre in content_data['genres'])
                    score = content_data['score']
                    content_type = content_data['type']
                    status = content_data['status']
                    content_count = content_data['episodes'] or content_data['chapters']
                    image_url = content_data['images']['jpg']['image_url'] or content_data['images']['jpg']['small_image_url'] or content_data['images']['jpg']['large_image_url']
                    return [title, genres, score, content_type, status, content_count, image_url]
                else:
                    print(f'Data parameter not found')
                    return None
            else:
                print(f'Failed to fetch data. Status code: {response.status_code}')
                return None
        except requests.exceptions.RequestException as e:
            print(f'An error occurred: {e}')
            return None
        
    def process_animanga(self, mouse_event, search_value):
        self.error_message.config(text='')
        if self.search_animanga(search_value) is None:
            self.error_message.config(text=f'The search found no results for:\n{search_value}')
        else:
            content_info = self.search_animanga(search_value)
            
            if content_info[1] == '':
                content_info[1] = 'N/A'
            if content_info[2] == None:
                content_info[2] = 'N/A'

            content_img = Image.open(requests.get(content_info[6], stream='True').raw)
            content_img = ImageTk.PhotoImage(content_img)

            self.title_result.config(text=f'Title: {content_info[0][:35]}')
            self.genres_result.config(text=f'Genres: {content_info[1]}')
            self.score_result.config(text=f'Score: {content_info[2]} / 10.00')
            self.type_result.config(text=f'Content Type: {content_info[3]}')
            self.status_result.config(text=f'Status: {content_info[4]}')
            if content_info[3] in ['Manga', 'Novel', 'Light Novel', 'One-shot', 'Doujinshi', 'Manhua', 'Manhwa', 'OEL']:
                self.installment_result.config(text=f'Total Chapters: {content_info[5]}')
            else:
                self.installment_result.config(text=f'Total Episodes: {content_info[5]}')

            self.cover_result.config(image=content_img)
            self.cover_result.image = content_img

    # retrieve a random anime
    def fetch_random_anime(self):
        url = 'https://api.jikan.moe/v4/random/anime'
        try:
            # make a get request
            response = requests.get(url) 
            # check if the request is valid/successful (status code 200)
            if response.status_code == 200:
                # parse the response as json
                data = response.json()
                # check if 'data' parmeter is found in the json file
                if 'data' in data:
                    # access the 'data' field from the json response
                    anime_data = data['data']
                    # directly access the information via anime_data
                    title = anime_data['title']
                    genres = ', '.join(genre['name'] for genre in anime_data['genres'])
                    score = anime_data['score']
                    anime_type = anime_data['type']
                    status = anime_data['status']
                    episode_count = anime_data['episodes']
                    image_url = anime_data['images']['jpg']['image_url'] or anime_data['images']['jpg']['small_image_url'] or anime_data['images']['jpg']['large_image_url']
                    return [title, genres, score, anime_type, status, episode_count, image_url]
                else:
                    # provide error message and return None
                    print(f'Data parameter not found.')
                    return None
            else:
                # provide error message and return None
                print(f'Failed to fetch data. Status code: {response.status_code}')
                return None
        except requests.exceptions.RequestException as e:
            # provide error message and return None
            print(f'An error occurred: {e}')
            return None

    # process anime result
    def process_random_anime(self):
        # if an anime is not fetched
        if self.fetch_random_anime() is None:
            # re-run the process function (recursion)
            self.process_random_anime()
        else:
            # if all goes well, store returned data as a list
            anime_info = self.fetch_random_anime()

            # if there is no genre listed, result in 'N/A'
            if anime_info[1] == '':
                anime_info[1] = 'N/A'
            # if there is no score given, result in 'N/A'
            if anime_info[2] == None:
                anime_info[2] = 'N/A' 

            # get anime image cover
            anime_img = Image.open(requests.get(anime_info[6], stream='True').raw)
            # transform to be compatible with tkinter
            anime_img = ImageTk.PhotoImage(anime_img)

            # showcase the retrieved anime's details
            self.title_result.config(text=f'Title: {anime_info[0][:35]}')
            self.genres_result.config(text=f'Genres: {anime_info[1]}')
            self.score_result.config(text=f'Score: {anime_info[2]} / 10.00')
            self.type_result.config(text=f'Content Type: {anime_info[3]}')
            self.status_result.config(text=f'Status: {anime_info[4]}')
            self.installment_result.config(text=f'Total Episodes: {anime_info[5]}')

            self.cover_result.config(image=anime_img)
            self.cover_result.image = anime_img

    # retrieve a random manga
    def fetch_random_manga(self):
        url = 'https://api.jikan.moe/v4/random/manga'
        try: 
            # make a get request to the api
            response = requests.get(url)
            # check if the request is successful
            if response.status_code == 200:
                # parse the response as json
                data = response.json()
                # check if 'data' parameter is found in the data
                if 'data' in data:
                    # access the 'data' field from the json response
                    manga_data = data['data']
                    # directly access and retrieve information via anime_data
                    title = manga_data['title']
                    genres = ', '.join(genre['name'] for genre in manga_data['genres'])
                    score = manga_data['score']
                    manga_type = manga_data['type']
                    status = manga_data['status']
                    chapter_count = manga_data['chapters']
                    image_url = manga_data['images']['jpg']['image_url'] or manga_data['images']['jpg']['small_img_url'] or manga_data['images']['jpg']['large_img_url']
                    return [title, genres, score, manga_type, status, chapter_count, image_url]
                else:
                    print(f'Data parameter not found.')
                    return None
            else:
                print(f'Fetch data failed. Error status code: {response.status_code}')
                return None
        except requests.exceptions.RequestException as e:
            print(f'Exceptions error occurred: {e}')
            return None

    # process manga result 
    def process_random_manga(self):
        # check if fetch was successful
        if self.fetch_random_manga() is None:
            # fetch another manga result
            self.process_random_manga()
        else:
            manga_info = self.fetch_random_manga()

            # set default values when results are non-specifc
            if manga_info[1] == '':
                manga_info[1] = 'N/A'
            if manga_info[2] == None:
                manga_info[2] = 'N/A'
            if manga_info[5] == None:
                manga_info[5] = 'N/A'
            
            # process manga's image cover for display
            manga_img = Image.open(requests.get(manga_info[6], stream='True').raw)
            manga_img = ImageTk.PhotoImage(manga_img)

            # display the returned results
            self.title_result.config(text=f'Title: {manga_info[0][:35]}')
            self.genres_result.config(text=f'Genres: {manga_info[1]}')
            self.score_result.config(text=f'Score: {manga_info[2]} / 10.00')
            self.type_result.config(text=f'Content Type: {manga_info[3]}')
            self.status_result.config(text=f'Status: {manga_info[4]}')
            self.installment_result.config(text=f'Total Chapters: {manga_info[5]}')

            self.cover_result.config(image=manga_img)
            self.cover_result.image = manga_img

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()