import requests
import json


def adjust_product_data(data):
    """
        All changes to the api response should be done here.
    """
    data = data.replace(b'null', b'"None"')
    data = data.replace(b"'", b"")
    return data

def get_data_for_gtin(gtin):
    headers = {
        'X-Cosmos-Token': 'iIjhUMG7SUSimQTGuvDY9g',
        'Content-Type': 'application/json',
        'User-Agent': 'Cosmos-API-Request'
    }
    url = f'https://api.cosmos.bluesoft.com.br/gtins/{gtin}.json'
    response = requests.get(url, headers=headers, allow_redirects=False).content
    adjusted_response = adjust_product_data(response)
    json_response = json.loads(adjusted_response)
    return json_response

