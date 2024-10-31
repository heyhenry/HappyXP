import tkinter as tk

root = tk.Tk()

something = tk.Text(root, height=10)
something.insert('1.0', 'water')

something.pack()

root.mainloop()