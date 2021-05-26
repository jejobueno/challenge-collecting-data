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
        self.postalCode = list()
        self.typeProperty = list()
        self.subtypeProperty = list()
        self.price = list()
        self.typeSale = list()
        self.subtypeSale = list()
        self.numberRooms = list()
        self.area = list()
        pass

    def extract_info(self, url: str):
        driver = webdriver.Chrome()
        # driver = webdriver.Firefox()
        driver.implicitly_wait(30)
        driver.get(url)
        soup: BeautifulSoup = BeautifulSoup(driver.page_source, 'lxml')

        # And then it's like Beautiful soup
        for elem in soup.find_all('script', attrs={"type": "text/javascript"}):
            if 'window.classified' in str(elem):
                dataStr = str(elem)

        data = re.search('{.*}', dataStr).group(0)
        jsonData = json.loads(data)

        return jsonData

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
    
    def get_info(self, jsondict):
        #print(jsondict)
        info = dict()
        properties = jsondict['property']
        # Saving the postal code (locality) of the property
        if properties['location']:
            self.postalCode.append(properties['location']['postalCode'])
        else:
            self.postalCode.append(None)
        print(self.postalCode)

        # Saving the type of the property
        if properties['type']:
            self.typeProperty.append(properties['type'])
        else:
            self.typeProperty.append(None)
        print(self.typeProperty)

        # Saving the subtype of the property
        if properties['type']:
            self.subtypeProperty.append(properties['subtype'])
        else:
            self.subtypeProperty.append(None)
        print(self.subtypeProperty) 

        # Saving the price of the property
        if jsondict['transaction']['sale']['price']:
            self.price.append(jsondict['transaction']['sale']['price'])
        else:
            self.price.append(None)
        print(self.price)

        # Saving the type of sale of the property
        if jsondict['transaction']['type']:
            self.typeSale.append(jsondict['transaction']['type'])
        else:
            self.typeSale.append(None)
        print(self.typeSale)

        # Saving the type of sale of the property
        if jsondict['transaction']['subtype']:
            self.subtypeSale.append(jsondict['transaction']['subtype'])
        else:
            self.subtypeSale.append(None)
        print(self.subtypeSale)

        # Saving the type of sale of the property
        if properties['roomCount']:
            self.numberRooms.append(properties['roomCount'])
        else:
            self.numberRooms.append(None)
        print(self.numberRooms)

        # Saving the area of the property
        if properties['netHabitableSurface']:
            self.area.append(properties['netHabitableSurface'])
        else:
            self.area.append(None)
        print(self.area)


        ### keep going searching properties ####

        info = pd.DataFrame(list(zip(self.postalCode, self.typeProperty,
                                     self.subtypeProperty, self.price, self.typeSale, self.subtypeSale,
                                     self.numberRooms, self.area)),
                            columns=['postalCode', 'type', 'subtype', 'price',
                                     'typeSale', 'subtypeSale', 'numberOfRooms',
                                     'area'])

        return info

    def create_csv(self, data):
        file_links_housing = pd.DataFrame(data)
        file_links_housing.to_csv('assets/housing-data.csv')

infograpper = InfoScrapper()
info = infograpper.extract_info('https://www.immoweb.be/en/classified/apartment/for-sale/ixelles/1050/9333411?searchId=60ad0a1ce3697')

data = infograpper.get_info(info)

infograpper.create_csv(data)