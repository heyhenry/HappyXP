import requests

search_value = 'narute'

url = f'https://api.jikan.moe/v4/anime?q={search_value}'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    content_data = data['data']
    print(len(content_data))
