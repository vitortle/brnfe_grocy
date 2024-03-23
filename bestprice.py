from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import requests
import shutil
import uuid
import os
import requests
import json
import logging
import dotenv
import sys

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from database import db_adapters
from api import product_api
import bestbrowser

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

logging.basicConfig(format='[%(levelname)s] [%(asctime)s] {%(filename)s:%(lineno)d} - %(message)s',
    handlers=[
        logging.FileHandler("logs.log"),
        logging.StreamHandler(sys.stdout)
    ],
    level=logging.INFO)

logger = logging.getLogger('__name__')
logger.setLevel(logging.INFO)
logger.propagate = True

dotenv.load_dotenv()

# Captcha functions not used
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
    images = browser.find_elements(By.TAG_NAME, 'img') #browser.find_element("xpath",'/html/body/div/div/div[2]/div[2]/div/table/tbody/tr[1]/td[1]/div/div[1]/img')
    imgs_src = [image.get_attribute('src') for image in images]
    save_captcha_images(imgs_src)


def scrap_data(cfe_key:str, browser)-> str:
    
    text_field = browser.find_element(By.XPATH,'/html/body/div[1]/form/div[3]/div[2]/div[2]/table/tbody/tr[2]/td[2]/div[2]/div[1]/div[1]/div[1]/input')
    text_field.click()
    text_field.send_keys(cfe_key)
    # find the 3 iframes:1-Im not a robot, 3- captcha
    iframes = browser.find_elements(By.TAG_NAME, "iframe")

    # switch to not_a_robot iframe
    browser.switch_to.frame(iframes[0])
    not_a_robot = browser.find_element(By.XPATH,'/html/body')
    # click on not_a_robot
    not_a_robot.click()

    # wait for the captcha to be solved
    input('Press enter when data is being showed!')

    browser.switch_to.parent_frame()

    # click on Detail button
    detail_button = browser.find_element(By.ID,'conteudo_btnDetalhe')
    detail_button.click()

    # click on emitente
    detail_button = browser.find_element(By.ID,'conteudo_tabEmitente')
    detail_button.click()
    
    # Capturing the data for header...
    header_data = browser.page_source

    # click on Produtos e Servicos button
    detail_button = browser.find_element(By.ID,'conteudo_tabProdutoServico')
    detail_button.click()
    
    # Capturing the data for items...
    item_data = browser.page_source

    browser.close()

    return (header_data, item_data)

def get_cfe_header_data(data, access_key)-> dict:
    try:
        soup = BeautifulSoup(data, 'html.parser')

        date = soup.find('span', id='conteudo_lblDataEmissao').text
        cfeid = soup.find('span', id='conteudo_lblNumeroCfe').text
        
        name = soup.find('span', id='conteudo_lblEmitenteDadosNome').text
        cnpj = soup.find('span', id='conteudo_lblEmitenteDadosEmitenteCnpj').text
        ie = soup.find('span', id='conteudo_lblEmitenteDadosInscricaoMunicipal').text
        address = soup.find('span', id='conteudo_lblEmitenteDadosEndereco').text
        city = soup.find('span', id='conteudo_lblEmitenteDadosMunicipio').text

        header = dict(cfeid=cfeid, access_key=access_key.replace(' ',''), purchase_date=date, place_name=name, address=address, city=city)
    except AttributeError as ex:
        print(ex)
    except Exception as ex:
        print(f'Unexpected exception {ex} !')
    #TODO add cnpj and ie to database
    return header

def get_cfe_item_data(data)-> dict:
    items = []
    item = {}
    soup = BeautifulSoup(data, 'html.parser')
 
    keys = ['item', 'description', 'qtty', 'unit', 'liquid_price', 'aditional_info', 'product_code', 'gtin_code',
            'ncm_code', 'Código Especificador da Substituição Tributária', 'cfop', 'unit_price', 'gross_price', 'calc_rule', 'discount',
            'Outras Despesas Acessórias', 'Rateio do Desconto Sobre Subtotal', 'Rateio do Acréscimo Sobre Subtotal',
            'Observações Fisco', 'Origem da Mercadoria', 'Tributação do ICMS', 'Cód. de Situação da Operação - Simples Nacional',
            'Alíquota Efetiva', 'icms_value', 'Código de Situação Tributária PIS', 'Valor da Base de Cálculo do PIS', 'Alíquota do PIS',
            'Quantidade Vendida PIS', 'Alíquota do PIS', 'pis_value', 
            'Valor da Base de Cálculo do PIS ST', 'Alíquota do PIS ST', 'Quantidade Vendida PIS ST', 'Alíquota do PIS ST', 'pis_st_value',
            'Código de Situação Tributária da COFINS', 'Valor da Base de Cálculo da COFINS', 'Alíquota da COFINS', 'cofins_value', 'Quantidade Vendida COFINS',	
            'Alíquota da COFINS', 'Valor da Base de Cálculo da COFINS ST', 'Alíquota da COFINS ST', 'confins_st_value', 'Quantidade Vendida COFINS ST',	
            'Alíquota da COFINS ST', 'Valor de Deduções para ISSQN', 'Valor da Base de Cálculo do ISSQN', 'Alíquota do ISSQN', 'issqn_value',	
            'Item da Lista de Serviços', 'Código do Município do Fato Gerador do ISSQN', 'Código de Tributação pelo ISSQN do Município',	
            'Natureza da Operação de ISSQN', 'Incentivo Fiscal do ISSQN', 'total_tax_value'
    ]

    table = soup.find('table', {'id': 'conteudo_grvProdutosServicos'})
    rows = table.find_all('tr')
    for row in rows[1:]:
        cells = row.find_all('td')
        for key, value in zip(keys, cells):
            item[key] = value.text.replace('\n','').replace('X','').strip()

        items.append(item)
        item = {}
    return items

def adjust_cfe_item_data(cfe_item_data)-> list[dict]:
    #keys = ['item', 'description', 'qtty', 'unit', 'product_code', 'unit_price', 'tax', 'total_price']
    keys = ['item', 'description', 'qtty', 'unit','liquid_price', 'aditional_info', 'product_code', 'gtin_code',
            'ncm_code','unit_price', 'gross_price', 'calc_rule', 'discount', 
            'icms_value', 'pis_value', 'pis_st_value', 'cofins_value', 'confins_st_value', 'issqn_value', 'total_tax_value'
    ]
    cfe_data = []
    for line in cfe_item_data:
        cfe_line = {}
        for key in keys:
            value = line[key]

            if key == 'gtin_code':
                value = value[1:] if value.startswith('0') else value

            if key in ['qtty', 'liquid_price', 'unit_price', 'gross_price', 'discount', 
                    'icms_value', 'pis_value', 'pis_st_value', 'cofins_value', 'confins_st_value', 
                    'issqn_value', 'total_tax_value'
                    ]:
                value = float(value.replace('Não Informado', '0.00').replace(',','.'))
            cfe_line[key] = value
        cfe_data.append(cfe_line)
    return cfe_data

def adjust_cfe_header_data(cfe_header_data):
    return cfe_header_data

def get_cfe_dict(cfe_key)-> dict:
    uf = cfe_key[0:2]
    aamm = cfe_key[2:6]
    cnpj = cfe_key[6:20]
    modelo = cfe_key[20:22]
    serie = cfe_key[22:31]
    cfe = cfe_key[31:37]
    aleat = cfe_key[37:43]
    dv = cfe_key[43:45]
    return dict (uf=uf, aamm=aamm, cnpj=cnpj, modelo=modelo, serie=serie, cfe=cfe, aleat=aleat, dv=dv)

def modulo11(cfe_key_dict):
    """
    Returns the modulo11 of the cfe_key
    param cfe_key_dict: dict with the cfe_key  (except the dv)
    """
    cfe_key = cfe_key_dict['uf'] + cfe_key_dict['aamm'] + cfe_key_dict['cnpj'] + cfe_key_dict['modelo'] + cfe_key_dict['serie'] + cfe_key_dict['cfe'] + cfe_key_dict['aleat']
    sum = 0
    for i, n in enumerate(cfe_key):
        sum += int(n) * (i % 8 + 2)
    dv = 11 - (sum % 11)
    if dv > 9:
        dv = 0
    return dv

def is_key_valid(access_key):
    valid = True
    if len(access_key) != 44 or not access_key.isnumeric():
        print('Chave invalida! ')
        valid = False
    return valid

def is_key_used(access_key, db):
    used = False
    if db.exists_key(access_key):
        print('Chave já foi utilizada!')
        used = True
    return used
    
def main():
    """
        Main backend:
        1- get CFE key from input.
        2- valids key and checks if its not already on the cfe_header table.
        3- logs on CFE site and scraps cfe data.
        4- adjust scraped data.
        6- insert header data on the database.
        7- iterate item data and check gtin if its on the product table
        8- if not, call product api and save data on product table.
        9- insert item data.
    """
    
    db = db_adapters.PostgresDatabase()
    while True:
        access_key = input('Enter the CFEid: ')
        if not is_key_valid(access_key) or is_key_used(access_key, db):
            continue
        try:
            browser = bestbrowser.Browser().browser
            browser.get('https://satsp.fazenda.sp.gov.br/COMSAT/Public/ConsultaPublica/ConsultaPublicaCfe.aspx')
            header_data, item_data = scrap_data(access_key, browser)
        except NoSuchElementException as ex:
            print(f'Erro.CFE não encontrado. {ex}')
            browser.close()
            continue
        except Exception as ex:
            print(f'Erro inesperado: {ex}')
            browser.close()
            continue
        
        cfe_header_data = get_cfe_header_data(header_data, access_key)
        cfe_item_data = get_cfe_item_data(item_data)

        header_data_adjusted = adjust_cfe_header_data(cfe_header_data)
        item_data_adjusted = adjust_cfe_item_data(cfe_item_data)

        idh = db.insert_header(header_data_adjusted)
        idi = db.insert_item(idh, item_data_adjusted)

        idp = db.insert_products(item_data_adjusted, product_api)
        

        print(f'Record ID {idh}, {idi} saved!')
 
if __name__ == '__main__':
    main()
