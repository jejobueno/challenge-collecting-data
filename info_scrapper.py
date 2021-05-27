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
        self.hasFullyEquippedKitchen = list()
        self.kitchenType = list()
        self.isFurnished = list()
        self.fireplaceExists = list()
        self.hasTerrace = list()
        self.terraceSurface = list()
        self.hasGarden = list()
        self.gardenSurface = list()
        self.facadeCount = list()
        self.surface = list()
        self.facadeCount = list()
        self.hasSwimmingPool = list()
        self.buildingCondition = list()
        pass

    def extract_info(self, url: str):
        #print(url)
        #driver = webdriver.Chrome()
        # driver = webdriver.Firefox()
        #driver.implicitly_wait(30)
        #driver.get(url)
        page = requests.get(url)
        soup: BeautifulSoup = BeautifulSoup(page.text, 'lxml')
        print(page.status_code)
        #driver.close()

        # And then it's like Beautiful soup

        for elem in soup.find_all('script', attrs={"type": "text/javascript"}):
            if 'window.classified' in str(elem):
                dataStr = str(elem)

        data = re.search('{.*}', dataStr).group(0)
        jsonData = json.loads(data)

        return jsonData

    def scrap_links(self, urls):
        links = list()
        if isinstance(urls, str):
            link = urls
            urls = list()
            urls.append(link)

        for url in urls:
            if requests.get(url).status_code == 200:
                jsondict = self.extract_info(url)
                data = self.get_info(jsondict)
            else:
                pass
        self.create_csv(data)

    def get_info(self, jsondict):
        #print(jsondict)
        properties = jsondict['property']
        # Saving the postal code (locality) of the property
        if properties['location']:
            self.postalCode.append(properties['location']['postalCode'])
        else:
            self.postalCode.append(None)
        #print(self.postalCode)

        # Saving the type of the property
        if properties['type']:
            self.typeProperty.append(properties['type'])
        else:
            self.typeProperty.append(None)
        #print(self.typeProperty)

        # Saving the subtype of the property
        if properties['type']:
            self.subtypeProperty.append(properties['subtype'])
        else:
            self.subtypeProperty.append(None)
        #print(self.subtypeProperty)

        # Saving the price of the property
        if jsondict['transaction']['sale']['price']:
            self.price.append(jsondict['transaction']['sale']['price'])
        else:
            self.price.append(None)
        #print(self.price)

        # Saving the type of sale of the property
        if jsondict['transaction']['type']:
            self.typeSale.append(jsondict['transaction']['type'])
        else:
            self.typeSale.append(None)
        #print(self.typeSale)

        # Saving the type of sale of the property
        if jsondict['transaction']['subtype']:
            self.subtypeSale.append(jsondict['transaction']['subtype'])
        else:
            self.subtypeSale.append(None)
        #print(self.subtypeSale)

        # Saving the type of sale of the property
        if properties['roomCount']:
            self.numberRooms.append(properties['roomCount'])
        else:
            self.numberRooms.append(None)
        #print(self.numberRooms)

        # Saving the area of the property
        if properties['netHabitableSurface']:
            self.area.append(properties['netHabitableSurface'])
        else:
            self.area.append(None)
        #print(self.area)


        # Saving the kitchen type in "kitchenType"
        if 'kitchen' in jsondict['property']:
            if jsondict['property']['kitchen']:
                if 'type' in jsondict['property']['kitchen']:
                    if jsondict['property']['kitchen']['type']:
                        self.kitchenType.append(jsondict['property']['kitchen']['type'])
                        if re.search('r/HYPER_EQUIPPED/', jsondict['property']['kitchen']['type']):
                            self.hasFullyEquippedKitchen.append(1)
                        else:
                            self.hasFullyEquippedKitchen.append(0)
                    else:
                        self.kitchenType.append(None)
                        self.hasFullyEquippedKitchen.append(None)
                else:
                    self.kitchenType.append(None)
                    self.hasFullyEquippedKitchen.append(None)
            else:
                self.kitchenType.append(None)
                self.hasFullyEquippedKitchen.append(None)
        else:
            self.kitchenType.append(None)
            self.hasFullyEquippedKitchen.append(None)
        #print("hasFullEquippedKitchen", self.hasFullyEquippedKitchen)
        #print('kitchentype', self.kitchenType)

        # Saving isFurnished
        if jsondict['transaction']['sale']['isFurnished']:
            self.isFurnished.append(1)
        else:
            self.isFurnished.append(0)
        #print(self.isFurnished)

        # Saving "fireplaceExists"
        if 'fireplaceExists' in jsondict['property']:
            if jsondict['property']['fireplaceExists']:
                self.fireplaceExists.append(1)
            else:
                self.fireplaceExists.append(0)
        else:
            self.fireplaceExists.append(None)
        #print(self.fireplaceExists)

        # Saving "hasTerrace"
        if jsondict['property']['hasTerrace']:
            self.hasTerrace.append(1)
        else:
            self.hasTerrace.append(0)
        #print(self.hasTerrace)

        # Saving the terrace surface in "terraceSurface"
        if jsondict['property']['terraceSurface'] and self.hasTerrace[-1] == 1:
            self.terraceSurface.append(jsondict['property']['terraceSurface'])
        else:
            self.terraceSurface.append(None)
        #print(self.terraceSurface)

        # Saving "hasGarden"
        if jsondict['property']['hasGarden']:
            self.hasGarden.append(1)
        else:
            self.hasGarden.append(0)
        #print(self.hasGarden)

        # Saving the Garden surface in "GardenSurface"
        if jsondict['property']['gardenSurface'] and self.hasGarden[-1] == 1:
            self.gardenSurface.append(jsondict['property']['gardenSurface'])
        else:
            self.gardenSurface.append(0)
        #print(self.gardenSurface)

        # Saving the surface of the property
        if properties['land']:
            self.surface.append(properties['land']['surface'])
        else:
            self.surface.append(0)
        #print(self.surface)

        # Saving the number of facades of the property
        if properties['building']:
            if 'facadeCount' in properties['building']:
                if properties['building']['facadeCount']:
                    self.facadeCount.append(properties['building']['facadeCount'])
                else:
                    self.facadeCount.append(None)
            else:
                self.facadeCount.append(None)
        else:
            self.facadeCount.append(None)
        #print('facade', self.facadeCount)

        # Saving swimming pool in hasSwimmingPool
        if jsondict['property']['hasSwimmingPool']:
            self.hasSwimmingPool.append(1)
        else:
            self.hasSwimmingPool.append(0)
        #print(self.hasSwimmingPool)

        # Saving the State of the building in "buildingCondition"
        if properties['building']:
            if 'condition' in properties['building']:
                if jsondict['property']['building']['condition']:
                    self.buildingCondition.append(jsondict['property']['building']['condition'])
                else:
                    self.buildingCondition.append(None)
            else:
                self.buildingCondition.append(None)
        else:
            self.buildingCondition.append(None)



        ### keep going searching properties ####

        print(len(self.postalCode))
        print(len(self.typeProperty))
        print(len(self.subtypeProperty))
        print(len(self.price))
        print(len(self.typeSale))
        print(len(self.subtypeSale))
        print(len(self.numberRooms))
        print(len(self.area))
        print('hasFullyEquiped', len(self.hasFullyEquippedKitchen))
        print('kitchentype', len(self.kitchenType))
        print(len(self.isFurnished))
        print(len(self.fireplaceExists))
        print(len(self.hasTerrace))
        print(len(self.terraceSurface))
        print(len(self.hasGarden))
        print(len(self.gardenSurface))
        print(len(self.facadeCount))
        print(len(self.surface))
        print(len(self.facadeCount))
        print(len(self.hasSwimmingPool))
        print(len(self.buildingCondition))

        info = pd.DataFrame(list(zip(self.postalCode, self.typeProperty,
                                     self.subtypeProperty, self.price, self.typeSale, self.subtypeSale,
                                     self.numberRooms, self.area, self.hasFullyEquippedKitchen,
                                     self.kitchenType, self.isFurnished,
                                     self.fireplaceExists, self.hasTerrace, self.terraceSurface,
                                     self.hasGarden, self.gardenSurface, self.surface,
                                     self.facadeCount, self.hasSwimmingPool, self.buildingCondition)),
                            columns=['postalCode', 'type', 'subtype', 'price',
                                     'typeSale', 'subtypeSale', 'roomsCount',
                                     'area', 'hasFullyEquippedKitchen', 'kitchenType', 'isFurnished',
                                     'fireplaceExists', 'hasTerrace', 'terraceSurface',
                                     'hasGarden', 'gardenSurface', 'landSurface',
                                     'facadeCount', 'hasSwimmingPool', 'buildingCondition'])

        print(info)
        print(len(info))

        print(len(self.postalCode))
        if len(self.postalCode) != len(info):
            print('error')
        return info

    def create_csv(self, data):
        file_links_housing = pd.DataFrame(data)
        file_links_housing.to_csv('assets/housing-data.csv')

