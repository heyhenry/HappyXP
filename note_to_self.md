# notes to help me remember how i made my code work the way it does.


1. Ensuring the realtime change of the user's profile pic in the homepage based on the change made in the settings page
    - I created an update_image function inside the HomePage class to update the user's profile (when there was a change)
    - I also had to create a trace_add call in the MainApp class to see if my shared variable that denotes the image's file path had changed
        - If the shared variable's value had changed, that meant that i had decided to use a different picture.
        - Even though there has been a change in the shared variable's value for the profile pic, I am still ensuring that I am saving the new user profile pic under the same name 'default_pic.png' (a completely different thing to the shared variable)
    - Based on the trace_add, if triggered.. it will run a function founded in the MainApp called 'update_profile_image'
        - This aforementiond function create the profile image instance and then sends the updated image configuration to the label founded in the HomePage via 'update_image' function which is founded in the HomePage's class, however is called in the mainapp by referencing the homepage page(frame)
    - tl;dr: 
        - shared variable that denotes the changes in the user profile's file path (new image or not) created in mainapp so it can be accessed in multiple pages
        - trace_add is used to find the changes in the user profile's image
        - function to update the profile image as well as create the image instance is founded in the mainapp to ensure access to multiple pages
        - function within the HomePage class has been created to update the label that will be storing and displaying the user profile's image

2. Ensuring that the display preview image does revert back to the default_pic.png if no new updates were made post previewing a different image in the settings page
    - The usage of a mainapp founded function called 'load_initial_image' was required to ensure that an initial image instance was created and then pushed to the HomePage via the same update portal
    - The settings page's display image that was not used in the update would revert to the old one based on a checkpoint created in the <Button-1> bind when user chooses to the leave the settings page
        - Said checkpoint would assess the current selected_file_path's value against the shared file path value (current_user_image_var) to see if the updated was confirmed, if not it will re-set the selected_file_path's value to the original filepath in use and also call the display_image function and display the current user profile's image