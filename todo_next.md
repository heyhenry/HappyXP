# To do next, based on previous coding session.

1. Highlight on hover for navbar options x
2. Editable text area for profile bio x/v (Make it better, better formatting and ui.)
    - Save the message in a save file. maybe user save file? x
3. Start on Search Page
    - Create Search Bar
    - Gain access to Jikan API for retrieving results
    - Showcase retrieved results
4. See if there is a way to make the text widget's presentation more natural like a label
5. Find 5-10 badge images for showcase


# This the updated one
- Create the Entry Page x
    - Title x
    - Content type (Drop Down Limited Options) x
        - Book
        - Anime
        - Manga
        - Manhwa
        - TV Show
        - Movie
    - Rating (Drop Down Limited Options) x
        - 1 - 10
    - Progress (text setup like [[]/[]]) x
        - If content type is books, manga or manhwa - automatically attach chapters to progress
        - If content type is movie, tv show or anime - automatically attach episodes to progress
    - Status (Drop Down Limited Options) x
        - Planned
        - Viewing
        - Paused
        - Dropped
        - Finished
    - Start Date x
        - [[dd]-[mm]-[yyyy]] (Temporary method)
    - End Date x
        - [[dd]-[mm]-[yyyy]]
    - Submit button x
    - Cancel or Go Back(?) button x
- Link Entry Page with the '+ New Entry' button x
- Create the Entry Object Class x
- Implement Entry Object to the existing functions i.e. custom_serializer x
- Create entries save file x
- Populate the entries_listbox with the submitted entries x
- Display the information as per selected entry x
- Make sure that the displayed information does not go past the borders
- Ensure to add in the type of metric is being used to measure the progress i.e. book = chapters, anime = episodes (preset during the new entry creation(?)) -
- Create the update entry button and related stuff x
- Create the delete entry function x
- Create the Search bar in the SearchPage
- Link up the Jikan API to the SearchPage for Results (or atleast look at its viability)
- Create validations for the user input for the new entry page x
    - valid user inputs
    - ensure all fields are filed
    - else if there are some fields that don't require filling, have a preset default value that will take its place
    - error message to go along with the validation checking


# Do these today (5th nov), when you come back from a break
- Display the new entries in the entries list right after a new entry has been created
- Actually update the selected entry's details
- Display updated entry information when selected upon in the entries list

So.. 
1. In the EntriesPage class, go and make sure the changes are shown in real time on relevant pages (i.e. Displays on the Entries Listbox) x
2. In the UpdateEntryPage class, save/update the new entry information to the entries_savefile and existing variables (?) x
3. In the EntriesPage class, make sure the updated entry's information is being shown in realtime when user decides to browse through the entries listbox post-update of an entry x

# If all is good after those 3 points...
(Priority)
- Create the delete entry functionality/feature x

(FlowingPriority)
- Implement validation related features to the new entries and entries that are going to get update aka (NewEntryPage & UpdateEntryPage) x/o

# TO THINK ABOUT THROUGHOUT THE PROCESSES OF THE ABOVE
- What metrics do I want to implement and have shown automatically based on the users decisions during the new entry creation? I.e
    - If its a book, manga or manhwa, have the metric as chapters
    - If its a tv show or anime, have the metric as episodes
    - If its a movie have the total_progress at 1
    - Should you allow the total_progress to be editable when the user is updating an entry
    - Should i bother creating a function to automatically change the status of an entry to completed/finished when current_progress == total_progress?

# completed nov 7th

# After completing nov 5ths points of work..
- Implement validation to the update entry page akin to new entry page x
- Find a way to stop title from cutting into the border on the details section of the entries page x
- Debugged the error trigger related to the the binding of the listboxselection x
- Proper cleaning/resetting of the entry field post entry creation x

# Bugs to debug and take note of
- When selecting an item from the entries listbox and then going to say.. the add_new_entry button, bind trigger gets error x
    - It pops up in terminal, almost always when i click in the progress entry boxes... but the error does show that it gets triggerd from the start aka entry_title x

# nov 7th todo next

Discuss and potentially overhaul search feature and replace with Discover?
- Create the search bar on the search page
- Look at using the jikan api? Should I even bother having a search page?

Potential of the Discover Page:
- Provide maybe ... 1 - 3 'fun' buttons for search results i.e. [Random Anime] [Random Manga] [Random Anything]
- Maybe provide an allowance to search based on genre [Action] [Adventure] [Romance] <--- Maybe its better to do this later as an expansion post creation of a working model and code
- For the time being maybe just have a discover feature using the MyAnimeList's database i.e. Jikan API

# nov 10th

Played around with the anilist graphql api and was able to get it to retrieve and display what I wanted for the most part, however, at some point I recieved a status_code of 403 which in HTTP means 'Forbidden', the server understood the request but refused to authorise it. Most likely in my case it is to do with rate-limiting. Will need to get it out further.

- Through playing around and testing, I was able to achieve what I wanted but need to confirm if I can still continue with anilist or require a different api that doesnt have finicky rate limit issues. (fyi, anilist notes it allows up to 90 requests per hour or something)

    # Tasks for today: 
        - Confirm anilist api's stability
        - Proceed with its usage if its stable and create the first randomised anime results component


# 11 Nov going onto 12... (all below done on the 12th)
- Create random manga functionality x
- Add additional information for random anime/manga results x
    - Type (i.e. manga, manhua, anime, ona, movie) x
    - Status (i.e. Finished, Hiatus, On-going) x
    - Desc?
    - Episodes/Chapters x
- Provide better ui for the discover page x
    - Have the anime/manga image display on the right side meanwhile details are displayed on the left side x
- Potentially create a search page for simple anime, manga searches x
- Ensure only animes and mangas are shown, no music?

What I accomplished today: 
- Full implementation of the random manga recommendation feature
- Updated the UI of the Discover Page
- Full implementation of the search feature for anime and mangas (amongst other content)

This lead me to create the following (deeper dive) all done on the discover page:
- implemented fetch random manga function
- implemented process random manga function
- updated the layout of information
- added additional result information to the display/showcase
- implemented search_animanga function
- implemented process_animanga function
- implemented bind events for the search feature (Pressing 'Enter' to execute search)
- learning more about data manipulation within confines of an api
- implemented error message for unfounded search results from manual searching
- implemented additional event bindings related to the search feature
- implemented on_search_entry function
- implemented off_search_entry function
- bunch of tweaking code throughout + testings


# Nov 12th todo list for tomorrow (maybe later today included)
- create achievement badges
    - find 5-7 images for badges x
    - figure out 5-7 achievements x
    - need for an edit page.....? maybe not so.. just show 5 recent badges. but store all of them with a date attached (hidden or otherwise)
- add additional user competitive metrics like:
    - total episodes watched
    - total chapters read
    - other metrics required to confirm achievements
- ability to showcase top ... 5? favourite entries (for now its just anime/manga content)
    - need for a edit page for favourites? (EditFavouritesPage?)
    - search query for anime/manga that will also confirm its in their list? or maybe dont bother confirming. ppl like to exasperate.
- App colour scheme (i.e. like kandayo)


# Nov 13th Log --- (pushed to 14th.)
# updated todo list for today... going on tomorrow probably
- 1.0 Achievement Section
    - Find 5-7 images for the achievement badges x
    - Figure out 5-7 achivements to associate with the badges ^ x
        - first_entry
        - five_entries
        - hundred_chapters
        - hundred_episodes
        - speedster (finished an entry in a day)
        - ten_mangas
        - ten_anime
    - Link the achievements to the badges
    - Display top 5 latest badge icons
    - Provide a popup window via button in the achievement section, to see list of all achievements and date achieved
    - Implement User Metrics for Achievement Tracking x
        - first_entry --> total_entries_count : int x
        - five_entries --> total_entries_count : int x
        - hundred_chapters --> total_chapters_count : int x
        - hundred_episodes --> total_episodes_count : int x
        - speedster (finished an entry in a day) --> entry_start_date == entry_end_date x
        - ten_mangas --> total_mangas_count : int x
        - ten_anime --> total_anime_count : int  x
    - Implement achievement triggers:
        - first_entry x
        - five_entries x
        - hundred_chapters x
        - hundred episodes x
        - speedster x
        - ten_mangas x
        - ten_anime x

- 2.0 Navigation Bar Section
    - Update UI
        - Include profile image
        - Include Username
        - Redesign 
- 3.0 Profile Image Section
    - Set fixed user profile image dimensions and fill with selected image


# 14Nov notes for tomorrow.

- Still use the above list to work on next stuff.

- What i've done tonight to help future me know whats up.
    - follow similar structure to the workout logic in my betterlife project.
        - have a separate dict/save file that contains the achievements
        - have the metrics for achievements in the user obj/save file
        - based on the user's metrics, update the achievements save file with new achievement badges when achieved

# 15th Nov
- Prevent user from clicking the update entry or delet entry buttons if they have no selected an entry x
- Prevent ability to create a new entry that has more current_progress > than total_progress x


# 16th Nov.

- BIG NOTE: Ignore everything above for a moment.

- Latest completion: 
    - Implementing the display update based on achievement for imagery.
    - Implemented to all code logics that trigger an achievement.
    - Added a variable toggler (var_name = 'achievement_unlocked') to notify the trace_add to update the badge display
    - Implemented update to the achievement name and date display based on the given achievement and its position in the display section

- TODO NEXT TIME:
    - Need to update text alignment for the name and date that is shown with the achievement badge icon
    - Need to save the state of the achievements that are being displayed x
    - There's probably more for the above ^ (code reductions, small test cases to consider - none coming up off the top of my head)
    - Implementation of the favourite manga/anime section...
        - Things to consider: 
            - How are we going to display an image? Or do we just not bother. considering manual entries wont have image input nor is there anywhere that images are being displayed for entries in this current version
            - ^ adding on to the above - maybe just have a full overhaul and only showcase anime/mangas based on the MAL database so i can showcase stuff better.
                - kind of defeats the purpose of not being able to put in entries of content that isnt not recorded in the MAL Database tho... like certain manhwas.
                    - maybe just have an option for manual entry as well.
# ----------------------------------------------------------------------------------- #

# 18th Nov.  TODO:
- Adopt the algorithm created yesterday in test2.py in NewEntryPage and UpdateEntryPage.
	- TLDR Algorithm Logic: Update the entry's dictionary, save it and then reference it's start date, end date so that we can have a 'N/A' value based on the status of the entry. x
	- Cont. Algorithm Logic: Displays of the entry details will always be referenced from the saved data in lieu of tkinter get() variables. x
	- Suggestion for Implementation: Potentially having some sort of trace action of the status selected in an entry in real time that will hide the end date or just a simple checkbox next to both start and end dates to let the user know whether the date has been taken or a null (N/A) value will be given once they submit the entry. x
- Remove all mention of Book, TV Show, Movies, Ona and ensure only Manga, Manhua, Manhwa, Comic, Anime, Donghua, Hanguk Aeni and Animation are present.
- Update the UpdateEntryPage's fields:
	- Non-Editable: Title, Content Type and Total Progress Count x 
	- Include the Chapters/Episodes text next to progress except, only one of the two based on the content type given
- Allow the discover page to be used to help search for entries
	- This would include new functions on said page: 
		- Create Entry: This will open up a New Entry Style Page except, relevant data that can be sourced from the api will be prefilled (non-editable). This will require a new page class.
# Low Priority
- Update text alignment for displayed achievement badge's name and date unlocked
- Change the profile bio message's Edit and Confirm buttons to highlighted texts (highlight colour based on action performed/performing)
- Button or label widget that opens up a pop-up window to list out all unlocked achievements
	- Maybe also those that haven't been unlocked yet (Similar setup to steam achievements)
- Create the favourite entry section
	- Consider imagery and name text display
		- For manual entries have a nice default image for the time being (something like... numba one best show gold medal ambiguous imagery?)
- Navbar Update
	- Include display name
	- Include user's profile image
	- Include mini social media/community/contact icons with dummy references (temp, but real redirects later)
- General UI update
	- removing the borderlines
	- adjusting the locaiton of the bordered boxed content

# Bug Found (required fix)
- when deleting the entries via the app, the user_save's data for said entry information still resides and gets scuffed... i.e. negative numbers. (saved state/clearing state? issue)
- disallow the ability to choose a earlier end date than that of the start date in new entry and update entry (validation issue)