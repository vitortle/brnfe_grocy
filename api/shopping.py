import requests
from bs4 import BeautifulSoup

import lxml.etree
import lxml.html

def get_info(gtin):
    url = "https://www.google.com/search"
    params = dict()
    params ['tbm'] = 'shop'
    params['hl'] = 'pt-br'
    params ['q'] = gtin

    response = requests.get(url, params=params)
    data = response.content
    soup = BeautifulSoup(data, 'html.parser')
    heading_objects = soup.find_all('a')

    for info in heading_objects:
        #print(str(info), type(info))
        if 'produto' in str(info):
            print(info)
            descript = info.get_text()
            print('****', descript)
            print('--------')
            break

    image = soup.find_all('img')[1]
    print(image)
    print('======')
# /html/body/div[7]/div/div[4]/div[3]/div/div[3]/div/div[2]/div/div[1]/div[1]/div[2]/span/a/div[1]/h3
    
if __name__ == '__main__':
    info = get_info(7891156001040)
    print(info)