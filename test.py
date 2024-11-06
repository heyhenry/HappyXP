import tkinter as tk

def delete_item():
    for i in lb.curselection():
        lb.delete(i)

root = tk.Tk()

lb = tk.Listbox(root)
lb.insert('end', 'yes')
lb.insert('end', 'no')

del_btn = tk.Button(root, text='Delete Item', command=delete_item)

lb.pack()
del_btn.pack()

root.mainloop()