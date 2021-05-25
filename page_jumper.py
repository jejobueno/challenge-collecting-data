from bs4 import BeautifulSoup
import requests

class PageJumper:

    def __init__(self, url):
        r = requests.get(url)
        print(url, r.status_code)
        self.soup = BeautifulSoup(r.content, 'lxml')

        for elem in self.soup.find_all('a'):
            print('The tag element is: ', elem)

        print('loop ended')


pageJumper = PageJumper('https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&orderBy=relevance')
print(pageJumper.soup)