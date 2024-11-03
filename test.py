import tkinter as tk
from tkcalendar import DateEntry

def get_date():
    selected_date = cal.get()
    print(f'Selected date: {selected_date}')


root = tk.Tk()
cal = DateEntry(root, date_pattern='dd-mm-yyyy')
cal.pack()
btn = tk.Button(root, text='Click Here To Return a Date', command=get_date)
btn.pack()
root.mainloop()