# from tkcalendar import DateEntry
# import tkinter as tk

# save_data = {'status': '', 'start_date': '', 'end_date': ''}

# def is_complete():
#     # save_data['status'] = status_choice.get()
#     if status_choice.get() == 'Planned':
#         save_data['start_date'] = 'N/A'
#         save_data['end_date'] = 'N/A'
#         print(f'Status: Planned')
#         print(f'Start Date: {save_data['start_date']}\nEnd Date: {save_data['end_date']}')
#         print(save_data)
#     elif status_choice.get() == 'Finished':
#         save_data['start_date'] = start_date.get()
#         save_data['end_date'] = end_date.get()
#         print('Status: Finished.')
#         print(f'Start Date: {save_data['start_date']}\nEnd Date: {save_data['end_date']}')
#         print(save_data)
#     else:
#         save_data['start_date'] = start_date.get()
#         save_data['end_date'] = 'N/A'
#         print('Status: Viewing.')
#         print(f'Start Date: {save_data['start_date']}\nEnd Date: {save_data['end_date']}')
#         print(save_data)

# root = tk.Tk()
# root.geometry('250x250')

# status_choice = tk.StringVar(value='Select Status')

# status_options = [
#     'Planned',
#     'Viewing',
#     'Finished'
# ]

# status_title = tk.Label(root, text='Status:')
# status = tk.OptionMenu(root, status_choice, *status_options)

# start_date_title = tk.Label(root, text='Start Date:')
# start_date = DateEntry(root, date_pattern='dd-mm-yyyy')

# end_date_title = tk.Label(root, text='End Date:')
# end_date = DateEntry(root, date_pattern='dd-mm-yyyy')

# submit = tk.Button(root, text='Submit', command=is_complete)

# status_title.grid(row=0, column=0)
# status.grid(row=0, column=1)

# start_date_title.grid(row=1, column=0)
# start_date.grid(row=1, column=1)

# end_date_title.grid(row=2, column=0)
# end_date.grid(row=2, column=1)

# submit.grid(row=3, columnspan=2)

# root.mainloop()

import tkinter as tk
from tkcalendar import DateEntry

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Trace OptionMenu Example")
        
        # Create a StringVar to store the selected value from the OptionMenu
        self.selected_status = tk.StringVar()
        
        # Create an OptionMenu with a list of options
        self.status_options = ["Viewing", "Paused", "Dropped", "Finished", "Planned"]
        self.selected_status.set(self.status_options[0])  # Default value
        
        self.status_menu = tk.OptionMenu(self.root, self.selected_status, *self.status_options)
        self.status_menu.pack(padx=10, pady=10)
        
        # Add a trace to the StringVar that tracks changes to the selected value
        self.selected_status.trace_add("write", self.on_status_change)
        
        # Label to display selected status
        self.status_label = tk.Label(self.root, text="Selected Status: " + self.selected_status.get())
        self.status_label.pack(padx=10, pady=10)

        # Date Entry Display
        self.status_date = DateEntry(self.root, date_pattern='dd-mm-yyyy')
        self.status_date.pack()
        self.status_date.pack_forget()
    
    def on_status_change(self, *args):
        # This function will be called whenever the value in selected_status changes
        new_status = self.selected_status.get()
        print(f"Status changed to: {new_status}")
        
        # Update the label to reflect the change
        self.status_label.config(text="Selected Status: " + new_status)

        if self.selected_status.get() == 'Finished' or self.selected_status.get() == 'Dropped':
            self.status_date.pack()
        else:
            self.status_date.pack_forget()

# Create the main window
root = tk.Tk()

# Create the app instance
app = App(root)

# Start the Tkinter event loop
root.mainloop()


