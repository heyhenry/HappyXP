from tkcalendar import DateEntry
import tkinter as tk

save_data = {'status': '', 'start_date': '', 'end_date': ''}

def is_complete():
    save_data['status'] = status_choice.get()
    if status_choice.get() == 'Planned':
        save_data['start_date'] = 'N/A'
        save_data['end_date'] = 'N/A'
        print(f'Status: Planned')
        print(f'Start Date: {save_data['start_date']}\nEnd Date: {save_data['end_date']}')
    elif status_choice.get() == 'Finished':
        save_data['start_date'] = start_date.get()
        save_data['end_date'] = end_date.get()
        print('Status: Finished.')
        print(f'Start Date: {save_data['start_date']}\nEnd Date: {save_data['end_date']}')
    else:
        save_data['start_date'] = start_date.get()
        save_data['end_date'] = 'N/A'
        print('Status: Viewing.')
        print(f'Start Date: {save_data['start_date']}\nEnd Date: {save_data['end_date']}')

root = tk.Tk()
root.geometry('250x250')

status_choice = tk.StringVar(value='Select Status')

status_options = [
    'Planned',
    'Viewing',
    'Finished'
]

status_title = tk.Label(root, text='Status:')
status = tk.OptionMenu(root, status_choice, *status_options)

start_date_title = tk.Label(root, text='Start Date:')
start_date = DateEntry(root, date_pattern='dd-mm-yyyy')

end_date_title = tk.Label(root, text='End Date:')
end_date = DateEntry(root, date_pattern='dd-mm-yyyy')

submit = tk.Button(root, text='Submit', command=is_complete)

status_title.grid(row=0, column=0)
status.grid(row=0, column=1)

start_date_title.grid(row=1, column=0)
start_date.grid(row=1, column=1)

end_date_title.grid(row=2, column=0)
end_date.grid(row=2, column=1)

submit.grid(row=3, columnspan=2)

root.mainloop()

