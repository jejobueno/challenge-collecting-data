from utils.page_jumper import PageJumper
from pandas import *
from utils.info_scrapper import InfoScrapper

# Seen that each search page of Inmoweb has a limit of 9990 announcements,
# we are going to recollect the 11.000 samples from the houses search page
# and the apartments search page separately.
# We save the links as 'constants'
LINKS_APPARTEMENT = 'https://www.immoweb.be/en/search/apartment/for-sale?countries=BE&orderBy=relevance'
LINKS_HOUSES = 'https://www.immoweb.be/en/search/house/for-sale?countries=BE&orderBy=relevance'

# First we call our pageJumper object which will creap the search pages
# looking for the link of each announcement for houses and apartment for
# sale with it's 'scrap_pages' function.
pageJumper = PageJumper()

# We want to analyze our both constants links, getting back 11000 links of
# announcements. We are going to get 5500 links from houses and 5500 from
# apartments
links = pageJumper.scrap_pages([LINKS_HOUSES, LINKS_APPARTEMENT], 30)

# In case you feel lazy to wait to the page jumper to get the links (can be
# one hour more or less) We've prepared a csv file using the create_csv method
# of PageJumper with 11000 links of announcements:

# We charge our csv file
# data = read_csv('assets/linksInmoweb.csv')

# converting column data to list
# links = data['link'].tolist()

# Just to check ;)
print('We have', len(links), 'links in our List')

# Now we call our InfoScrapper object which is going to collect the necessarily
# data from each link and create and csv file in the './assets' folder. You only
# need to give the List of links and the name you want for the file. The
# InfoScrapper object will print each time the quantity of error connections for
# the links and also the quantity of links that have been well scrapped
infoScrapper = InfoScrapper()
infoScrapper.scrap_links(links, 'housing-data3.csv')

# Now have a sit and order a pizza. It may take up to 3 hours!
