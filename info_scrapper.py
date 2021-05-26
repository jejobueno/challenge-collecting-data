from time import strftime

from bs4 import BeautifulSoup
import pandas as pd
import json
import re
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class InfoScrapper:

    def __init__(self):
        pass

    def extract_info(self, url: str):
        driver = webdriver.Chrome()
        # driver = webdriver.Firefox()
        driver.implicitly_wait(30)
        driver.get(url)
        soup: BeautifulSoup = BeautifulSoup(driver.page_source, 'lxml')
        info: Dict = dict()

        # And then it's like Beautiful soup
        for elem in soup.find_all('script', attrs={"type": "text/javascript"}):
            if 'window.classified' in str(elem):
                dataStr = str(elem)

        data = re.search('{.*}', dataStr).group(0)
        jsonData = json.loads(data)

        print(jsonData)
        print(type(jsonData))
        print(jsonData['id'])
        driver.close()

        return info

    def scrap_pages(self, url: str):
        links = list()
        while True:
            print(len(links))
            page_links = self.extract_links(url)
            if page_links and len(links) < 15000:
                links += page_links
                url = self.jump_page(url)
            else:
                break
        return links


infograpper = InfoScrapper()
infograpper.extract_info('https://www.immoweb.be/en/classified/apartment/for-sale/ixelles/1050/9333411?searchId=60ad0a1ce3697')