import requests
import json

def get_data_for_gtin(gtin):
    headers = {
        'X-Cosmos-Token': 'iIjhUMG7SUSimQTGuvDY9g',
        'Content-Type': 'application/json',
        'User-Agent': 'Cosmos-API-Request'
    }
    url = f'https://api.cosmos.bluesoft.com.br/gtins/{gtin}.json'
    response = requests.get(url, headers=headers, allow_redirects=False).content
    response = response.replace(b'null', b'"None"')
    json_response = json.loads(response)
    return json_response

