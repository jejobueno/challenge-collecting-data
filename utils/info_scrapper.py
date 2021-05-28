from time import strftime

from bs4 import BeautifulSoup
import pandas as pd
import json
import os
import re
import requests

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from typing import List, Union, Dict


class InfoScrapper:

    def __init__(self):
        """
        This method initialize the object and all the list for each
        parameter we are going to scrap. Also initializes a variable
        to count the quantity of error connections
        """
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

        # Register of connection errors
        self.connectionErrors = 0

    def scrap_links(self, urls: Union[List[str], str], fileName: str):
        """
        This method will extract all the desired information from the passed
        list of Links, and save it in a csv file with the name of the
        variable 'fileName'.

        Calls self.get_data() to extract the desired data to be save
        in the csv with self.create_csv().

        :param urls: List of urls to be passed to extract the dessired data
        can be either a list or a single String
        :param fileName: The name that will have the csv file
        :return: None
        """

        # First we check if the the urls variable passed is a string, if it is
        # a string we set this single string into a list of only one element,
        # if not we assume it is a list of string.
        if isinstance(urls, str):
            link = urls
            urls = list()
            urls.append(link)

        # Now we are going to check each url in the urls list
        for url in urls:
            page = requests.get(url)
            # We check the status to the request,
            if page.status_code == 200:
                # if the request succeeds: we make a BeautifulSoup ou of it
                soup: BeautifulSoup = BeautifulSoup(page.text, 'lxml')

                # We get the data from the BeautifulSoup and save it in our
                # attributes lists
                self.get_data(soup)

                # We print the record of connection errors and well scrapped
                # pages
                print('Connection errors:', self.connectionErrors)
                print('Scrapped pages:', len(self.price))

            else:
                # if the request doesn't succeed:
                # increment connectionErrors by one
                self.connectionErrors += 1
        self.create_csv(fileName)

    # This is a static method because it doesn't access to any
    # attribute of the class
    @staticmethod
    def extract_json_dict(soup: BeautifulSoup) -> Dict:
        """
        This method will extract the json dictionary from the 'window.classified'
        element of the soup
        :param soup: BeautifulSoup obtained from the announcement url
        :return: the dictionary with the data contained in the javascript
        element where all the information related to the house/apartment
        for sale is.
        """

        for elem in soup.find_all('script', attrs={"type": "text/javascript"}):
            if 'window.classified' in str(elem):
                dataStr = str(elem)

        data = re.search('{.*}', dataStr).group(0)
        json_data = json.loads(data)

        return json_data

    def get_data(self, soup: BeautifulSoup):
        """
        This method is going to extract first the json dictionary from
        the beautiful soup using the static method self.extract_json_dict()
        and then extract the data from some specific keys and append it to our
        attributes lists. We are looked to the patterns of where is usually
        the data for each announcement and which could be the possible error
        we could get and try to avoid them.

        :param soup: BeautifulSoup passed from self.scrap_links() method
        :return: None
        """

        # We extract the json dictionary with the needed info
        json_dict = self.extract_json_dict(soup)

        # We create a sub-dictionary out of the 'property' key
        property = json_dict['property']

        # Saving the postal code (locality) of the property
        if property['location']:
            self.postalCode.append(property['location']['postalCode'])
        else:
            # If not empty saves None
            self.postalCode.append(None)

        # Saving the type of the property
        if property['type']:
            self.typeProperty.append(property['type'])
        else:
            # If not empty saves None
            self.typeProperty.append(None)

        # Saving the subtype of the property
        if property['type']:
            self.subtypeProperty.append(property['subtype'])
        else:
            # If not empty saves None
            self.subtypeProperty.append(None)

        # Saving the price of the property
        if json_dict['transaction']['sale']['price']:
            self.price.append(json_dict['transaction']['sale']['price'])
        else:
            # If not empty saves None
            self.price.append(None)

        # Saving the type of sale of the property
        if json_dict['transaction']['type']:
            self.typeSale.append(json_dict['transaction']['type'])
        else:
            # If not empty saves None
            self.typeSale.append(None)

        # Saving the type of sale of the property
        if json_dict['transaction']['subtype']:
            self.subtypeSale.append(json_dict['transaction']['subtype'])
        else:
            # If not empty saves None
            self.subtypeSale.append(None)

        # Saving the type of sale of the property
        if property['bedroomCount']:
            self.numberRooms.append(property['bedroomCount'])
        else:
            # If not empty saves None
            self.numberRooms.append(None)

        # Saving the area of the property
        if property['netHabitableSurface']:
            self.area.append(property['netHabitableSurface'])
        else:
            # If not empty saves None
            self.area.append(None)

        # Saving the kitchen type in "kitchenType"
        # We check if there exist a kitchen key in property
        if 'kitchen' in property:
            # if exists then we check if it is 'None' or empty
            if json_dict['property']['kitchen']:
                # We check if there exist a kitchen 'type' key
                if 'type' in json_dict['property']['kitchen']:
                    # if exists then we check if it is 'None' or empty
                    if json_dict['property']['kitchen']['type']:
                        # then we save the type of Kitchen
                        self.kitchenType.append(json_dict['property']['kitchen']['type'])
                        # Now we check if it is 'HYPER_EQUIPPED'
                        if re.search('r/HYPER_EQUIPPED/', json_dict['property']['kitchen']['type']):
                            # if True we save it as a binary boolean 1 (Yes)
                            self.hasFullyEquippedKitchen.append(1)
                        else:
                            # if False we save it as a binary boolean 0 (No)
                            self.hasFullyEquippedKitchen.append(0)
                    else:
                        # for all the rest of the cases save None for empty
                        # information or information not found
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

        # Saving isFurnished
        if json_dict['transaction']['sale']['isFurnished']:
            # if True we save it as a binary boolean 1 (Yes)
            self.isFurnished.append(1)
        else:
            # if False we save it as a binary boolean 0 (No)
            self.isFurnished.append(0)

        # Saving "fireplaceExists"
        if 'fireplaceExists' in json_dict['property']:
            if json_dict['property']['fireplaceExists']:
                # if True we save it as a binary boolean 1 (Yes)
                self.fireplaceExists.append(1)
            else:
                self.fireplaceExists.append(0)
                # if False we save it as a binary boolean 0 (No)
        else:
            self.fireplaceExists.append(None)

        # Saving "hasTerrace"
        if json_dict['property']['hasTerrace']:
            # if True we save it as a binary boolean 1 (Yes)
            self.hasTerrace.append(1)
        else:
            # if False we save it as a binary boolean 0 (No)
            self.hasTerrace.append(0)

        # Saving the terrace surface in "terraceSurface"
        if json_dict['property']['terraceSurface'] and self.hasTerrace[-1] == 1:
            self.terraceSurface.append(json_dict['property']['terraceSurface'])
        else:
            # if there is no terrace save None
            self.terraceSurface.append(None)

        # Saving "hasGarden"
        if json_dict['property']['hasGarden']:
            # if True we save it as a binary boolean 1 (Yes)
            self.hasGarden.append(1)
        else:
            # if False we save it as a binary boolean 0 (No)
            self.hasGarden.append(0)

        # Saving the Garden surface in "GardenSurface"
        if json_dict['property']['gardenSurface'] and self.hasGarden[-1] == 1:
            self.gardenSurface.append(json_dict['property']['gardenSurface'])
        else:
            # if there is not garden save None
            self.gardenSurface.append(None)

        # Saving the surface of the property
        if property['land']:
            self.surface.append(property['land']['surface'])
        else:
            # if False we save it as a binary boolean 0 (No)
            self.surface.append(0)

        # Saving the number of facades of the property
        # we check if 'building' key is not empty in property dict
        if property['building']:
            # check if facadeCount exists
            if 'facadeCount' in property['building']:
                # if exists check if it is not empty
                if property['building']['facadeCount']:
                    self.facadeCount.append(property['building']['facadeCount'])
                else:
                    # if it is empty save None
                    self.facadeCount.append(None)
            else:
                # if not found saves None
                self.facadeCount.append(None)
        else:
            # if not found saves None
            self.facadeCount.append(None)

        # Saving swimming pool in hasSwimmingPool
        if json_dict['property']['hasSwimmingPool']:
            # if True we save it as a binary boolean 1 (Yes)
            self.hasSwimmingPool.append(1)
        else:
            # if False we save it as a binary boolean 0 (No)
            self.hasSwimmingPool.append(0)
        # print(self.hasSwimmingPool)

        # Saving the State of the building in "buildingCondition"
        # Check if the key 'building' is empty or not
        if property['building']:
            # then check if the 'condition' key exists
            if 'condition' in property['building']:
                # check if it is not empty
                if json_dict['property']['building']['condition']:
                    self.buildingCondition.append(json_dict['property']['building']['condition'])
                else:
                    # if empty saves None
                    self.buildingCondition.append(None)
            else:
                # if not found saves None
                self.buildingCondition.append(None)
        else:
            # if not found saves None
            self.buildingCondition.append(None)

    def create_csv(self, fileName: str):
        """
        This method will create frist a DataFrame using pandas out of the
        attributes of the InfoScrapped object. Then it saves this DataFrame
        into a csv file with the name 'fileName' into the folder '/assets'
        """

        # First we create our DataFrame
        file_links_housing = pd.DataFrame(list(zip(self.postalCode, self.typeProperty,
                                     self.subtypeProperty, self.price,
                                     self.typeSale, self.subtypeSale,
                                     self.numberRooms, self.area,
                                     self.hasFullyEquippedKitchen,
                                     self.kitchenType, self.isFurnished,
                                     self.fireplaceExists, self.hasTerrace,
                                     self.terraceSurface, self.hasGarden,
                                     self.gardenSurface, self.surface,
                                     self.facadeCount, self.hasSwimmingPool,
                                     self.buildingCondition)),
                            columns=['postalCode', 'typeProperty',
                                     'subtypeProperty', 'price',
                                     'typeSale', 'subtypeSale',
                                     'BedroomsCount', 'area',
                                     'hasFullyEquippedKitchen',
                                     'kitchenType', 'isFurnished',
                                     'fireplaceExists', 'hasTerrace',
                                     'terraceSurface', 'hasGarden',
                                     'gardenSurface', 'landSurface',
                                     'facadeCount', 'hasSwimmingPool',
                                     'buildingCondition'])

        # then we save it in our csv file
        file_links_housing.to_csv('assets/' + fileName)
