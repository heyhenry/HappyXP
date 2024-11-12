import requests
import random

search_value = 'narute'

url = f'https://api.jikan.moe/v4/anime?q={search_value}'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    content_data = data['data']
    print(len(content_data))
    total_results = len(content_data)
    content_data = data['data'][random.randint(0, total_results)]
    title = content_data['title']
    print(title)
