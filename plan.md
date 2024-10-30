# HappyXP (Happy Experiences): Log your entertainment
# Disclaimer: currently this app will be only targetting the entry logging of mangas, manhwa and similar + anime


1. Create a barebones aethetic but heavy functioning application first.

1.1 Features
    1.1.0 Setup Page (Create Account)
        1.1.0.0 username, password, confirm password input fields x 
        1.1.0.1 validation check user input for standard protection/security x
        1.1.0.2 error messages based on validation x
        1.1.0.3 save to a user save file (json file storage) x
    1.1.1 Login Page
        1.1.1.0 username, password input fields x
        1.1.1.1 validation check for correct account details x
        1.1.1.2 error messages based on validation x
        1.1.1.3 redirect to the homepage x
    1.1.2 Home Page
        1.1.2.0 display top 5 favourite anime
        1.1.2.1 display top 5 mangas/manhwas
        1.1.2.3 display user profile
        1.1.2.4 small section for personal bio
        1.1.2.5 option to stay logged in toggle 
        1.1.2.6 display some achivement badges
        1.1.2.7 navigation bar (home, entries)
        1.1.2.8 edit user account option button
    1.1.3 Entries Page
        1.1.3.0 List of entries
        1.1.3.1 Tab feature to filter entry list to either mangas or anime
        1.1.3.2 Search bar feature for entries
        1.1.3.3 Display information of entry on the side (title, content type, rating, progress, status, start date, end start)
        1.1.3.4 Provide edit options (update, delete)
        1.1.3.5 create a new entry option
    1.1.4 User Details Page
        1.1.4.0 edit username, password, profile picture
    1.1.5 New Entry Page
        1.1.5.0 userinput = title, content type, rating, progress, status, start date, end date
        1.1.5.1 mandatory input validation for title, content type
        1.1.5.2 if other input fields aside from mandatory fields left blank, then add entry day's date for start date, status set to watching/reading, everything else set to 0 or n/a
        1.1.5.3 validation check to ensure no duplicate entries are created based on title and content type
