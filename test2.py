import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()

achievement_name = tk.StringVar()
achievements_queue = ['default_pic', 'default_pic', 'default_pic']

def unlock_achievement(name):
    achievements_queue[0] = achievements_queue[1]
    achievements_queue[1] = achievements_queue[2]
    achievements_queue[2] = name

    update_images()

achievements_title = tk.Label(root, text='Achievements Hall:')

def update_images():
    first_img = Image.open('img/achievement_badges/'+achievements_queue[0]+'.png')
    first_img.thumbnail((100, 100))
    first_img = ImageTk.PhotoImage(first_img)
    first_image.config(image=first_img)
    first_image.image = first_img

    second_img = Image.open('img/achievement_badges/'+achievements_queue[1]+'.png')
    second_img.thumbnail((100, 100))
    second_img = ImageTk.PhotoImage(second_img)
    second_image.config(image=second_img)
    second_image.image = second_img

    third_img = Image.open('img/achievement_badges/'+achievements_queue[2]+'.png')
    third_img.thumbnail((100, 100))
    third_img = ImageTk.PhotoImage(third_img)
    third_image.config(image=third_img)
    third_image.image = third_img

first_achievement_title = tk.Label(root, text='')
first_image = tk.Label(root)
first_achievement_date = tk.Label(root, text='')

second_achievement_title = tk.Label(root, text='')
second_image = tk.Label(root)
second_achievement_date = tk.Label(root, text='')

third_achievement_title = tk.Label(root, text='')
third_image = tk.Label(root)
third_achievement_date = tk.Label(root, text='')

achievement_entry = tk.Entry(root, textvariable=achievement_name)
achievement_submit = tk.Button(root, text='Submit Achievement', command=lambda: unlock_achievement(achievement_name.get()))

achievements_title.grid(row=0, columnspan=3)

first_achievement_title.grid(row=1, column=0)
first_image.grid(row=2, column=0)
first_achievement_date.grid(row=3, column=0)

second_achievement_title.grid(row=1, column=1)
second_image.grid(row=2, column=1)
second_achievement_date.grid(row=3, column=1)

third_achievement_title.grid(row=1, column=2)
third_image.grid(row=2, column=2)
third_achievement_date.grid(row=3, column=2)

achievement_entry.grid(row=4, columnspan=3)
achievement_submit.grid(row=5, columnspan=3)

update_images()

root.mainloop()