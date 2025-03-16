Fork of https://github.com/engrogerio/bestprice.

This project will create an integrate with Grocy app at some point.

For now, it's working to scrape the data from the Cupom Fiscal Eletronico. 

# 1 - Install the browser driver.
Make sure you have driver and browser on the same version.

## 1- Install geckodriver

$ wget https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz
$ tar xvfz geckodriver-v0.19.1-linux64.tar.gz
$ mv geckodriver ~/.local/bin

## 2- Install chromedriver
https://chromedriver.chromium.org/downloads
https://googlechromelabs.github.io/chrome-for-testing/

wget https://storage.googleapis.com/chrome-for-testing-public/121.0.6167.184/linux64/chrome-linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/bin/
export PATH="/usr/bin/chrome-linux64/:$PATH"

## 3- CFE manual 
https://www.confaz.fazenda.gov.br/legislacao/arquivo-manuais/especificacao-tecnica-de-requisitos-2_24_04.pdf