from time import strftime

from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class PageJumper:

    def jump_page(self, url: str):
        if url.find('page=') > 0:
            page_number = int(url[url.find('page=') + 5:url.find('&order')])
            nextlink = url[0:url.find('page=') + 5] + str(page_number + 1) + url[url.find('&order'):]
        else:
            nextlink = url[0:url.find('BE')+3] + 'page=2' + url[url.find('&order'):]
        return nextlink

    def extract_links(self, url):
        driver = webdriver.Chrome()
        # driver = webdriver.Firefox()
        driver.implicitly_wait(30)
        driver.get(url)
        soup: BeautifulSoup = BeautifulSoup(driver.page_source, 'lxml')
        links: List = list()

        # And then it's like Beautiful soup
        for elem in soup.find_all('a', attrs={"class": "card__title-link"}):
            links.append(elem.get('href'))
        
        driver.close()
        
        return links


    def scrap_pages(self, url: str):
        links = list()
        while True:

            print(links)
            page_links = self.extract_links(url)
            if page_links or len(links)<10000:
                links += page_links
                url = self.jump_page(url)
            else:
                break
        return links

    def create_csv(self, url):
        links = self.scrap_pages(url)
        file_links_housing = pd.DataFrame(links)
        file_links_housing.to_csv(".assets/links-inmoweb.csv", index=False)




pageJumper = PageJumper()
links = pageJumper.create_csv('https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&orderBy=relevance')