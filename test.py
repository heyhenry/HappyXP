import tkinter as tk
import requests
from PIL import Image, ImageTk

def show_anime(id):
    url = 'https://graphql.anilist.co'
    query = '''
    query ($id: Int) {
      Media (id: $id) {
        id
        title {
          romaji
          english
        }
        coverImage {
          medium
        }
      }
    }
    '''
    variables = {
        'id': id
    }
    response = requests.post(url, json={'query': query, 'variables': variables})
    if response.status_code == 200:
        data = response.json()
        if data['data']['Media']:
            anime = data['data']['Media']
            title = anime['title']['romaji'] or anime['title']['english']
            cover_url = anime['coverImage']['medium']

            # anime_title_var.set(title)
            # anime_id_var.set(id)
            # anime_cover_url.set(cover_url)

            anime_title.config(f'Title: {title}')
            anime_id.config(f'ID: {id}')

            img = Image.open(requests.get(cover_url, stream=True).raw)
            img = ImageTk.PhotoImage(img)

            anime_cover.config(image=img)
            anime_cover.image = img
        else:
            print(f'No anime found for id: {id}')
    else:
        print(f'Failed to retrieve data, status code: {response.status_code}')

root = tk.Tk()
root.geometry('500x500+700+200')

anime_title_var = tk.StringVar()
anime_id_var = tk.StringVar()
anime_cover_url = tk.StringVar()

anime_btn = tk.Button(root, text='Show Anime', command=lambda: show_anime(1))

anime_title = tk.Label(root, text='Title:')
anime_id = tk.Label(root, text='ID:')
anime_cover = tk.Label(root)

anime_btn.pack()
anime_title.pack()
anime_id.pack()
anime_cover.pack()

root.mainloop()






