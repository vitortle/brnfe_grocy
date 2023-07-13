import os

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium import webdriver
from dotenv import load_dotenv

load_dotenv()


class Browser:

    def __init__(self):
        
        path = os.getcwd()
        self.download_path = os.path.join(path, 'downloads')

        options = ChromeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors=yes') 
        options.add_argument('--window-size=1920,1080')
        prefs = {"download.default_directory" : self.download_path}
        # for os with no GUI
        # options.add_argument("--headless")

        options.add_experimental_option("detach", True)
        options.add_experimental_option("prefs",prefs)
        self.browser = webdriver.Chrome(options=options)

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
