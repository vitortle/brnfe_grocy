from webbrowser import Chrome
from selenium.webdriver import chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium import webdriver
import time
import requests
import shutil
import uuid
import os

import pandas as pd
from bs4 import BeautifulSoup


BASE_PATH = os.path.dirname(os.path.abspath(__file__))

def save_captcha_images(imgs_src):
    for image in imgs_src:
        res = requests.get(image, stream = True)
        file_name = os.path.join(BASE_PATH, 'img', str(uuid.uuid4())[:8]+'.png')
        if res.status_code == 200:
            with open(file_name,'wb') as f:
                shutil.copyfileobj(res.raw, f)
            print('Image sucessfully Downloaded: ',file_name)
        else:
            print('Image Couldn\'t be retrieved')

def get_captcha(browser, iframes):
# switch to captcha iframe
    browser.switch_to.frame(iframes[2])
    images = browser.find_elements_by_tag_name('img') #find_elements_by_xpath('/html/body/div/div/div[2]/div[2]/div/table/tbody/tr[1]/td[1]/div/div[1]/img')
    imgs_src = [image.get_attribute('src') for image in images]
    # images[0].click()
    save_captcha_images(imgs_src)

def scrap_data(cfe_key:str)-> str:
    options = ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors') 
    # options.add_argument("--headless")

    options.add_experimental_option("detach", True)

    browser = webdriver.Chrome(options=options)

    # go to cfe site, type the key and click the button
    browser.get('https://satsp.fazenda.sp.gov.br/COMSAT/Public/ConsultaPublica/ConsultaPublicaCfe.aspx')
    text_field = browser.find_elements_by_xpath('/html/body/div[1]/form/div[3]/div[2]/div[2]/table/tbody/tr[2]/td[2]/div[2]/div[1]/div[1]/div[1]/input')
    text_field[0].click()
    text_field[0].send_keys(cfe_key)

    # find the 3 iframes:1-Im not a robot, 3- captcha
    iframes = browser.find_elements_by_tag_name("iframe")

    # switch to not_a_robot iframe
    browser.switch_to.frame(iframes[0])
    not_a_robot = browser.find_elements_by_xpath('/html/body')
    # click on not_a_robot
    not_a_robot[0].click()

    # wait for the captcha to be solved
    input('Press enter when data is being showed!')

    #Capturing the data...
    data = browser.page_source
    browser.close()
    return data
    
def get_cfe_data(data):
    soup = BeautifulSoup(data, 'html.parser')

    date_div = soup.find('div', id='')
    date_span = date_div.find('span', id='conteudo_lblDataEmissao')

    cfeid_div = soup.find('div', id='divTelaImpressao')
    cfeid_span = cfeid_div.find('span', id='conteudo_lblNumeroCfe')
    cfeid = cfeid_span.text

    emitente_div = soup.find('div', id='DadosEmitenteContent')
    name_span = emitente_div.find('span', id='conteudo_lblNomeFantasiaEmitente')
    name = name_span.text

    address_span = emitente_div.find('span', id='conteudo_lblEnderecoEmintente')
    address = address_span.text
    
    city_span = emitente_div.find('span', id='conteudo_lblMunicipioEmitente')
    city = city_span.text

    print(f'{cfeid=}, {name=}, {address=}, {city=}')

    table = soup.find('table', {'id': 'tableItens'})
    rows = table.find_all('tr')

    keys = ['id', 'product_code', 'description', 'qtty', 'unit', 'unit_price', 'tr', 'total_price']
    invoice_items = []
    for row in rows[2::]:
        cells = row.find_all('td')
        print('='*20)

        invoice_item = {}
        if len(cells) == 2: # get line between items which keeps only the discounts
            for key, value in zip(['include', 'value'], cells):
                print(key, value.text)
                print('_'*20)
                invoice_item[key] = value.text.replace('\n','').strip()
        else: # all item
            for key, value in zip(keys, cells):
                print(value)
                print('_'*20)
                invoice_item[key] = value.text.replace('\n','').replace('X','').strip()
            
        invoice_items.append(invoice_item)


    return invoice_items

def main():
    coop_test = '35230257508426004599590005671911425513149074'
    sr_test = '35221245495694001276590008047580969276482206'

    data = scrap_data(sr_test)
    cfe_data = get_cfe_data(data)
    print(cfe_data)

    #database.save(data)

if __name__ == '__main__':
    main()