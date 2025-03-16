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
import database.db_adapters as db_adapters
from product_api import product_api
import bestbrowser
from database import operations
from utils import return_url


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
ENV = os.environ.get('ENV')
URL = return_url(ENV)

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

def scrap_data(cfe_key:str, browser)-> str:
    if ENV == 'prod':
        
        text_field = browser.find_element(By.XPATH,'/html/body/div[1]/form/div[3]/div[2]/div[2]/table/tbody/tr[2]/td/div[2]/div[1]/div[1]/div[1]/input')
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
    
    time.sleep(2)
    
    # click on emitente
    detail_button = browser.find_element(By.ID,'conteudo_tabEmitente')
    detail_button.click()

    time.sleep(2)
    
    # Capturing the data for header...
    header_data = browser.page_source

    # click on Produtos e Servicos button
    detail_button = browser.find_element(By.ID,'conteudo_tabProdutoServico')
    detail_button.click()

    time.sleep(2)
    
    # Capturing the data for items...
    item_data = browser.page_source
    

    browser.close()

    return (header_data, item_data)

def get_cfe_header_data(data, access_key)-> dict:
    try:
        soup = BeautifulSoup(data, 'html.parser')

        key = soup.find('span', id='conteudo_lblChaveAcesso').text
        cfid = soup.find('span', id='conteudo_lblNumeroCfe').text
        date = soup.find('span', id='conteudo_lblDataEmissao').text
        
        cnpj = soup.find('span', id='conteudo_lblEmitenteDadosEmitenteCnpj').text
        state_registration_number = soup.find('span', id='conteudo_lblEmitenteDadosInscricaoEstatual').text
        municipal_registration_number = soup.find('span', id='conteudo_lblEmitenteDadosInscricaoMunicipal').text
        trade_number = soup.find('span', id='conteudo_lblEmitenteDadosNomeFantasia').text
        company_name = soup.find('span', id='conteudo_lblEmitenteDadosNome').text
        
        address = soup.find('span', id='conteudo_lblEmitenteDadosEndereco').text
        area = soup.find('span', id='conteudo_lblEmitenteDadosBairro').text
        city = soup.find('span', id='conteudo_lblEmitenteDadosMunicipio').text
        state_number = soup.find('span', id='conteudo_lblEmitenteDadosUf').text
        tax_code = soup.find('span', id='conteudo_lblEmitenteDadosCodigoRegimeTributario').text
        ISSQN_special_tax = soup.find('span', id='conteudo_lblEmitenteDadosRegimeEspecialTributacaoIssqn').text
        discount_indicator = soup.find('span', id='conteudo_lblEmitenteDadosIndicadorRateioDescontoSubtotal').text

        header = dict(
            key=key,
            cfid=cfid,
            date=date,            
            cnpj=cnpj,
            state_registration_number=state_registration_number,
            municipal_registration_number=municipal_registration_number,
            trade_number=trade_number,
            company_name=company_name,            
            address=address,
            area=area,
            city=city,
            state_number=state_number,
            tax_code=tax_code,
            ISSQN_special_tax=ISSQN_special_tax,
            discount_indicator=discount_indicator
        )

    except AttributeError as ex:
        print(ex)
    except Exception as ex:
        print(f'Unexpected exception {ex} !')
    return header

def get_cfe_item_data(data)-> dict:
    headers_list = []
    items = []
    item = {}
    soup = BeautifulSoup(data, 'html.parser')
 
    table = soup.find('table', {'id': 'conteudo_grvProdutosServicos'})

    headers = table.find_all('th')

    for header in headers:
        headers_list.append(header.text)

    rows = table.find_all('tr')
    for row in rows[1:]:
        cells = row.find_all('td')
        for key, value in zip(headers_list, cells):
            item[key] = value.text.replace('\n','')

        items.append(item)
        item = {}
    return items

def is_key_valid(access_key):
    valid = True
    if len(access_key) != 44 or not access_key.isnumeric():
        print('Chave invalida! ')
        valid = False
    return valid
    
def save_json(access_key, data):
    try: 
        with open("dump/" + access_key + ".json", "w", encoding="utf-8") as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
    except AttributeError as ex:
        print(ex)


def main():
    document_type = 'NFESAT'
    mongodb = db_adapters.MongoDatabase()
    while True:
        access_key = input('Enter the CFEid: ') if ENV == 'prod' else os.environ.get('CFEid_SAMPLE')
        if not is_key_valid(access_key):
            continue
        try:
            browser = bestbrowser.Browser().browser
            url = return_url(ENV)
            browser.get(url)
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

        cfe = cfe_header_data
        cfe['document_type'] = document_type
        cfe['items'] = cfe_item_data

        save_json(access_key, cfe)

        idh = mongodb.insert_dict(cfe)
        logger.info('Data inserted into MongoDB')
 
if __name__ == '__main__':
    main()