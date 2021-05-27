from page_jumper import PageJumper
from pandas import *
from info_scrapper import InfoScrapper

LINKS_APPARTEMENT = 'https://www.immoweb.be/en/search/apartment/for-sale?countries=BE&orderBy=relevance'
LINKS_HOUSES = 'https://www.immoweb.be/en/search/house/for-sale?countries=BE&orderBy=relevance'

pageJumper = PageJumper()
pageJumper.create_csv([LINKS_HOUSES, LINKS_APPARTEMENT], 50)

# reading CSV file
data = read_csv('assets/linksInmoweb.csv')

# converting column data to list
links = data['link'].tolist()

infoScrapper = InfoScrapper()
infoScrapper.scrap_links(links)