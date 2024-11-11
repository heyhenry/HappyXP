# api source: https://jikan.moe/

import tkinter as tk
import requests
from PIL import Image, ImageTk

def fetch_anime_by_id(anime_id):
    url = f'https://api.jikan.moe/v4/anime/{anime_id}'
    try:
        # make a get request to the api
        response = requests.get(url)
        
        # check if the request is valid/successful (status code 200)
        if response.status_code == 200:
            # parse the response as json
            data = response.json()

            # check if 'data' param is found in the json file
            if 'data' in data:
              # access the 'data' field from the json response
              anime_data = data['data']

              # directly access the information you want via anime_data
              title = anime_data['title']
              genres = ', '.join(genre['name'] for genre in anime_data['genres'])
              score = anime_data['score']
              image_url = anime_data['images']['jpg']['image_url'] or anime_data['images']['jpg']['small_image_url'] or anime_data['images']['jpg']['large_image_url']
              return [anime_id, title, genres, score, image_url]
            else:
               return None
        else:
            print(f'Failed to fetch data. Status code: {response.status_code}')
            return None
    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')
        return None

def process_anime(given_id):

  # clear any residual error messages
  anime_error_msg.config(text='')

  # check if fetch anime func returns valid info
  # if not, display error message
  if fetch_anime_by_id(given_id) is None:
    anime_error_msg.config(text='An Error Occurred. Try a Different ID.')
  else:
    # update the widgets with anime results
    anime_info = fetch_anime_by_id(given_id)

    # create the anime cover image for display
    img_url = Image.open(requests.get(anime_info[4], stream='True').raw)
    img_url = ImageTk.PhotoImage(img_url)

    anime_id.config(text=f'ID: {anime_info[0]}')
    anime_title.config(text=f'Title: {anime_info[1]}')
    anime_genres.config(text=f'Genres: {anime_info[2]}')
    anime_score.config(text=f'Score: {anime_info[3]}')
    anime_image_url.config(image=img_url)
    anime_image_url.image = img_url

root = tk.Tk()
root.geometry('500x700+700+200')

anime_id_var = tk.StringVar()
anime_title_var = tk.StringVar()
anime_genres_var = tk.StringVar()
anime_score_var = tk.StringVar()
anime_image_url_var = tk.StringVar()

enter_id = tk.Label(root, text='Enter an Anime ID:')
id_entry = tk.Entry(root, textvariable=anime_id_var)
id_submit = tk.Button(root, text='Search Anime ID', command=lambda: process_anime(anime_id_var.get()))

anime_id = tk.Label(root, text=f'ID:')
anime_title = tk.Label(root, text=f'Title:')
anime_genres = tk.Label(root, text=f'Genres:')
anime_score = tk.Label(root, text=f'Score:')
anime_image_url = tk.Label(root)
anime_error_msg = tk.Label(root, foreground='red')

enter_id.pack()
id_entry.pack()
id_submit.pack()

anime_id.pack()
anime_title.pack()
anime_genres.pack()
anime_score.pack()
anime_image_url.pack()
anime_error_msg.pack()

root.mainloop()






