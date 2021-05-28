from time import strftime

from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class PageJumper:
    """
    This object will jump from page to page getting the url of each announcment
    of each house or appartement for sale saving it in a .csv fil
    """

    def __init__(self):
        pass

    def jump_page(self, url: str):
        """
        This method takes an url of the search of appartements or houses from the 
        page inmoweb.com with the type and gives back the next page in the search.
        :return: str = url of the next page
        """
        if url.find('page=') > 0:
            page_number = int(url[url.find('page=') + 5:url.find('&order')])
            nextlink = url[0:url.find('page=') + 5] + str(page_number + 1) + url[url.find('&order'):]
        else:
            nextlink = url[0:url.find('BE') + 3] + 'page=2' + url[url.find('&order'):]
        return nextlink

    def extract_links(self, url: str):
        """
        This method will extract the links for each announcment in
        one single search page of inmoweb.
        :return: gives back the list git the links found in the page
        """
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
        """
        This method will check first if `urls` is a single url or a list of
        urls, if it is a single url is going to set it in a list. 
        Then it calls extract_links method to extract the links of the search
        page of inmoweb, once extracted it saves them in a the `link` list and
        jump to the next index of the search page with `jump_page()` method.
        It will repeat the same process for each `url` taking care of having the
        same quantity of links for each link.
        
        :return: list of all links found in the search pages of inmoweb
        with a lenght equals to `linkCount`
        """
        links = list()

        if isinstance(urls, str):
            link = urls
            urls = list()
            urls.append(link)

        linksPerLink = int(linkCount/len(urls))
        page_links = list()
        linkNumber = 0

        for url in urls:
            linkNumber += 1
            while True:
                if len(links) < linksPerLink*linkNumber:
                    page_links = self.extract_links(url)
                    if linksPerLink < 30:
                        links += page_links[0:linksPerLink]
                        url = self.jump_page(url)
                        break
                    else:
                        if len(links) + len(page_links) <= linksPerLink*linkNumber:
                            links += page_links
                            url = self.jump_page(url)
                        else:
                            links += page_links[0:linksPerLink*linkNumber-(len(page_links)+len(links))]
                            break
                else:
                    break

        return links

    def create_csv(self, url: str, linksCount: int):
        """
        This function will create a csv file from the list of links given by 
        scrap_pages method.
        """
        links = self.scrap_pages(url, linksCount)
        file_links_housing = pd.DataFrame(links, columns=['link'])
        file_links_housing.to_csv('assets/linksInmoweb.csv')

