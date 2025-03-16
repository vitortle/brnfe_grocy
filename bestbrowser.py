import os
import sys
import logging

import selenium
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class Browser:

    def __init__(self):
        
        path = os.getcwd()
        self.download_path = os.path.join(path, 'downloads')
              
        prefs = {"download.default_directory" : self.download_path}
        # for os with no GUI
        # options.add_argument("--headless")

        # options.add_experimental_option("detach", True)
        # options.add_experimental_option("prefs",prefs)
        chromedriver_path = "/usr/lib/chromium-browser/chromedriver"
        service = Service(chromedriver_path)
        try:
            # self.browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', service_args=['--verbose', '--log-path=./chrome_drv.log'], options=options)
            options = ChromeOptions()
            options.add_argument('--ignore-ssl-errors=yes')
            options.add_argument('--ignore-certificate-errors=yes')
            # options.add_argument('--window-size=1920,1080')
            self.browser = webdriver.Chrome(service=service, options=options)
        except selenium.common.exceptions.SessionNotCreatedException as ex:
            logger.error(f'Browser desatualizado. Por favor atualizar seu Chrome para a versão 115! {ex}')
            sys.exit(1)
        except Exception as ex:
            logger.error(ex)

    def get(self, url):
        self.browser.get(url)
        return self.browser
    
    def close(self):
        self.browser.close()

class Page:

    def __init_(self, browser):
        self.browser = browser

    def get_element_by_xpath(self, xpath):
        return self.browser.find_element(By.XPATH,xpath)
    
    def send_keys(self, xpath, value):
        field = self.get_element_by_xpath(xpath)
        field.send_keys(value)

    def click(self, xpath):
        element = self.get_element_by_xpath(xpath)
        element.click()

    def close_page(self):
        self.browser.close()
