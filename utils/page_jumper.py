from time import strftime

from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from typing import List, Union
from typing import List, Union


class PageJumper:
    """
    This object will jump from page to page getting the url of each
     announcement of each house or apartment for sale saving it in 
     a csv file
    """

    def __init__(self):
        pass

    def jump_page(self, url: str) -> str:
        """
        This method takes an url of the search of apartments or houses from the 
        page inmoweb.com with the type and gives back the next page in the search.

        Many of the search Inmoweb urls are made in the same way.

        :return: str = url of the next page
        """
        # Firs we check if the 'page=' string is in the url.
        if url.find('page=') > 0:
            # if Trues, that means that we only have to change the page number
            # so we try to get the actual page number from the url
            page_number = int(url[url.find('page=') + 5:url.find('&order')])
            # and then we make a new url changing only the 'page' number for
            # the next one
            next_link = url[0:url.find('page=') + 5] + str(page_number + 1) \
                        + url[url.find('&order'):]
        else:
            # If there is no 'page' key in the url means that it is the first
            # page. SO we have to get back the url of the second page
            next_link = url[0:url.find('BE') + 3] + 'page=2' + url[url.find('&order'):]
        return next_link

    # This is a static method because it doesn't access to any
    # attribute of the class
    @staticmethod
    def extract_links(url: str) -> List[str]:
        """
        This method will extract the links for each announcement in
        one single search page of income.
        :return: gives back the list with the links found in the page
        """
        # We  need to use selenium to get the links of the announcements
        driver = webdriver.Chrome()
        # we live the option to change to Firefox controller
        # driver = webdriver.Firefox()
        driver.implicitly_wait(30)
        driver.get(url)

        # we make the soup out of it:
        soup: BeautifulSoup = BeautifulSoup(driver.page_source, 'lxml')
        links: List = list()

        # and then we get the links!
        for elem in soup.find_all('a', attrs={"class": "card__title-link"}):
            links.append(elem.get('href'))

        # Close the driver!
        driver.close()

        return links

    def scrap_pages(self, urls: str, linkCount: int) -> List[str]:
        """
        This method gives back a list with all the links of announcements
        found scrapping the search webpages from Inmoweb.

        It will check first if `urls` is a single url or a list of
        urls, if it is a single url is going to set it in a list. 
        Then it calls extract_links method to extract the links of the search
        page of Inmoweb, once extracted it saves them in a the `link` list and
        jump to the next index of the search page with `jump_page()` method.
        It will repeat the same process for each `url` taking care of having the
        same quantity of links for each link.
        
        :return: list of all links found in the search pages of Inmoweb
        with a length equals to `linkCount`
        """
        links = list()

        # First we check if the the urls variable passed is a string, if it is
        # a string we set this single string into a list of only one element,
        # if not we assume it is a list of string.
        if isinstance(urls, str):
            link = urls
            urls = list()
            urls.append(link)

        # This variable will help us to calculate the limits of our loop
        linksPerLink = int(linkCount / len(urls))
        # This is a counter of the url we are checking
        linkNumber = 0

        for url in urls:
            # Increase each time we check a url
            linkNumber += 1
            # We are going to get an equal quantity of link
            # from each
            while True:
                # We check first if we have enough links
                if len(links) < linksPerLink * linkNumber:
                    # if not save the 30 links (There are usually 30 per url)
                    page_links = self.extract_links(url)
                    if linksPerLink < 30:
                        # if we need less than 30 links, save a sublist
                        links += page_links[0:linksPerLink]
                        break
                    else:
                        # if not save look if we need to save the whole list
                        # of links or just a part of it
                        if len(links) + len(page_links) <= linksPerLink * linkNumber:
                            links += page_links
                            url = self.jump_page(url)
                        else:
                            # if it is just a part of it
                            links += page_links[0:linksPerLink * linkNumber - (len(page_links) + len(links))]
                            break
                else:
                    # if we already have enough
                    break

        return links

    def create_csv(self, url: str, linksCount: int):
        """
        You can call this method if you desire to run self.scrap_pages()
        and create a csv out of the list received
        :return: None
        """
        links = self.scrap_pages(url, linksCount)
        file_links_housing = pd.DataFrame(links, columns=['link'])
        file_links_housing.to_csv('assets/linksInmoweb.csv')
