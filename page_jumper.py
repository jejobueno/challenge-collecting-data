from time import strftime

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class PageJumper:

    def __init__(self, url):
        # driver = webdriver.Chrome()
        self.driver: webdriver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.driver.get(url)
        self.soup: BeautifulSoup = BeautifulSoup(driver.page_source)
        self.links: List = []

    def jump_page(self):
        pass

    def extract_links(self):
        # And then it's like Beautiful soup
        print(soup)
        for elem in soup.find_all('a', attrs={"class": "card__title-link"}):
            print('The link ("href") is: ', elem.get('href'))
            print('House: ', elem.get('aria-label'), "\n")


pageJumper = PageJumper('https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&orderBy=relevance')
# print(pageJumper.soup)
