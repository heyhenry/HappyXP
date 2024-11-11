import requests

def get_anime_info(title):
    url = 'https://graphql.anilist.co'
    
    # GraphQL query to search for the anime by title
    query = '''
    query ($title: String) {
      Page {
        media (search: $title, type: ANIME) {
          id
          title {
            romaji
            english
          }
          description
          averageScore
        }
      }
    }
    '''
    
    variables = {
        'title': title
    }
    
    # Send the GraphQL request
    response = requests.post(url, json={'query': query, 'variables': variables})
    
    if response.status_code == 200:
        data = response.json()
        if data['data']['Page']['media']:
            anime = data['data']['Page']['media'][0]
            title = anime['title']['romaji'] or anime['title']['english']
            description = anime['description']
            score = anime['averageScore']
            print(f"Title: {title}")
            print(f"Score: {score}")
            print(f"Description: {description}")
        else:
            print(f"No anime found for title: {title}")
    else:
        print(f"Failed to retrieve data, status code: {response.status_code}")

# Example usage
get_anime_info("Naruto")