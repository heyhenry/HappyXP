import requests

def fetch_anime_by_id(anime_id):
    url = f'https://api.jikan.moe/v4/anime/{anime_id}'
    try:
        # set a GET request to the API
        response = requests.get(url)

        # check if the request was successful (status code 200)
        if response.status_code == 200:
            # parse the response as json
            data = response.json()

            # access the 'data' field from the json response using []
            # assuming the 'data' key exists
            anime_data = data['data']

            # directly access the 'title', 'genres', 'score' and 'images' using []
            title = anime_data['title']
            genres = ', '.join(poop['name'] for poop in anime_data['genres'])
            score = anime_data['score']
            image_urls = anime_data['images']['jpg']['image_url'] or anime_data['images']['webp']

            print(f'Title: {title}')
            print(f'Genres: {genres}')
            print(f'Score: {score}')
            print(f'Image URLs: {image_urls}')

        else:
            print(f'Failed to fetch data. Status code: {response.status_code}')

    except requests.exceptions.RequestException as e:
        print(f'An error occurred: {e}')

fetch_anime_by_id(1)