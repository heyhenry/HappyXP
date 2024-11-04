import tkinter as tk

root = tk.Tk()
root.geometry('180x200')

lb = tk.Listbox(root, width=40, height=10, selectmode='single')

lb.insert(1, 'Henry')
lb.insert(2, 'Marc')
lb.insert(3, 'Steven')
lb.insert(4, 'Albert')
lb.insert(5, 'Arman')

def selected_item():
    for i in lb.curselection():
        print(lb.get(i))

btn = tk.Button(root, text='Print Selected', command=selected_item)

btn.pack(side='bottom')
lb.pack()

root.mainloop()