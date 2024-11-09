import requests
import tkinter as tk
from PIL import Image, ImageTk

# def get_anime_cover(id):
#     url = 'https://graphql.anilist.co'

#     # GraphQL query to search for the anime by title
#     query = '''
#     query ($id: Int) {
#         Media (id: $id) {
#             id
#             title {
#                 romaji
#                 english
#                 native
#             }
#             coverImage {
#                 medium
#             }
#         }
#     }
#     '''
#     variables = {
#         'id': id
#     }

#     # send the GraphQL request
#     response = requests.post(url, json={'query': query, 'variables': variables})

#     if response.status_code == 200:
#         data = response.json()
#         if data['data']['Media']:
#             anime = data['data']['Media']
#             title = anime['title']['romaji'] or anime['title']['english'] or anime['title']['native']
#             cover_image = anime['coverImage']['medium']
#             print(f'Title: {title}')
#             print(f'ID: {id}')
#             print(f'Cover Image: {cover_image}')
#             return cover_image
#         else:
#             print(f'No anime found for title: {title}')
#     else:
#         print(f'Failed to retrieve data, status code: {response.status_code}')

# get_anime_cover(1)

# def get_anime_cover_url(id):
#     url = 'https://graphql.anilist.co'
#     query = '''
#     query ($id: Int) {
#         Media (id: $id) {
#             coverImage {
#                 medium
#             }
#         }
#     }
#     '''
#     variables = {
#         'id': id
#     }
#     response = requests.post(url, json={'query': query, 'variables': variables})
#     if response.status_code == 200:
#         data = response.json()
#         if data['data']['Media']:
#             anime = data['data']['Media']
#             cover_image_url = anime['coverImage']['medium']
#             return cover_image_url
#         else:
#             print(f'No anime found for id: {id}')
#     else:
#         print(f'Failed to retrieve data, status code: {response.status_code}')

root = tk.Tk()
root.geometry('500x500+700+200')

def show_anime_details():
    anime_title_var = 'Cowboy Bebop'
    anime_id_var = 1
    anime_cover_url = 'https://s4.anilist.co/file/anilistcdn/media/anime/cover/small/bx1-CXtrrkMpJ8Zq.png'

    anime_cover = Image.open(requests.get(anime_cover_url, stream=True).raw)
    anime_cover = ImageTk.PhotoImage(anime_cover)

    anime_title.config(text=f'Anime Title: {anime_title_var}')
    anime_id.config(text=f'ID: {anime_id_var}')
    anime_cover_image.config(image=anime_cover)
    anime_cover_image.image = anime_cover

get_anime_btn = tk.Button(root, text='Show Anime [ID: 1]', command=show_anime_details)

anime_title = tk.Label(root, text='Anime Title:')
anime_id = tk.Label(root, text='Anime ID:')
anime_cover_image = tk.Label(root)

get_anime_btn.pack()
anime_title.pack()
anime_id.pack()
anime_cover_image.pack()

root.mainloop()