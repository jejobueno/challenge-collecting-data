from time import strftime

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class PageJumper:

    def __init__(self, url):
        driver = webdriver.Chrome()
        driver.implicitly_wait(30)
        driver.get(url)

        # And then it's like Beautiful soup
        soup = BeautifulSoup(driver.page_source)
        print(soup)


pageJumper = PageJumper('https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&orderBy=relevance')
#print(pageJumper.soup)