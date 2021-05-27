from time import strftime

from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class PageJumper:

    def __init__(self):
        pass

    def jump_page(self, url: str):
        if url.find('page=') > 0:
            page_number = int(url[url.find('page=') + 5:url.find('&order')])
            nextlink = url[0:url.find('page=') + 5] + str(page_number + 1) + url[url.find('&order'):]
        else:
            nextlink = url[0:url.find('BE') + 3] + 'page=2' + url[url.find('&order'):]
        return nextlink

    def extract_links(self, url: str):
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

    def scrap_pages(self, urls: str, linkCount: int):
        links = list()

        if isinstance(urls, str):
            link = urls
            urls = list()
            urls.append(link)

        for url in urls:
            while True:
                print(len(links))
                page_links = self.extract_links(url)
                if page_links and len(links) < (linkCount*len(urls)):
                    links += page_links
                    url = self.jump_page(url)
                else:
                    break

        return links

    def create_csv(self, url: str, linksCount: int):
        links = self.scrap_pages(url, linksCount)
        file_links_housing = pd.DataFrame(links, columns=['link'])
        file_links_housing.to_csv('assets/linksInmoweb.csv')

