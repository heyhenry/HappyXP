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
    - Cancel or Go Back(?) button
- Link Entry Page with the '+ New Entry' button
- Create the Entry Object Class
- Implement Entry Object to the existing functions i.e. custom_serializer
- Create entries save file
- Populate the entries_listbox with the submitted entries
- Create the update entry button and related stuff
- Create the delete entry function
- Create the Search bar in the SearchPage
- Link up the Jikan API to the SearchPage for Results (or atleast look at its viability)
