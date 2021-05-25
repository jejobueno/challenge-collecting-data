from time import strftime

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class PageJumper:

    def __init__(self, url):
        #driver = webdriver.Chrome()
        driver = webdriver.Firefox()
        driver.implicitly_wait(30)
        driver.get(url)

        # And then it's like Beautiful soup
        soup = BeautifulSoup(driver.page_source)
        print(soup)
        for elem in soup.find_all('a', attrs={"class": "card__title-link"}):
            print('The link ("href") is: ', elem.get('href'))
            print('House: ', elem.get('aria-label'), "\n")


pageJumper = PageJumper('https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&orderBy=relevance')
#print(pageJumper.soup)