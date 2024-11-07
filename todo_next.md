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




