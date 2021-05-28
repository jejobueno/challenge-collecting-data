# Real estate sales web scraping for Belgium

##  1. Description

This project is about building a data set related to real estate sales in Belgium from scratch
by using [web scraping](https://en.wikipedia.org/wiki/Web_scraping) tools in Python.

The data set should contain the common variables of interest to describe and analyse real estate sales:
location, surface, price, number of rooms, amenities (equipped kitchen, terrace, garden...), see table below. It should cover all
the belgian territory, contain both apartments and houses, and count a minimum of 10 000 entries.

| Data required      | Variable name          | Possible Values             |
|------------------- |------------------------|-----------------------------|
| Locality           | postalCode             |  xxxx (four digits int)     |
| Type of Property   | type                   |  HOUSE, HOUSE_GROUP, APARTMENT, APARTMENT_GROUP|
| Subtype of property | subtype             |  (25 subtypes)     |
| Price           | price             |  price in euros (float)     |
| Type of sale           | typeSale             |  "FOR_SALE"    |
| Number of rooms           | roomsCount             |  int     |
| Area           | area             |  surface in square meters (int)     |
| Fully equipped kitchen (Yes/No)           | hasFullyEquippedKitchen|  0 or 1     |
| Type of kitchen installation           | kitchenType |  HYPER_EQUIPPED, INSTALLED, NOT_INSTALLED, SEMI_EQUIPPED, USA_HYPER_EQUIPPED, USA_INSTALLED, USA_SEMI_EQUIPPED, USA_UNINSTALLED |
| Furnished (Yes/No)            | isFurnished          |  0 or 1     |
| Open fire (Yes/No) | fireplaceExists           |  0 or 1     |
| Terrace (Yes/No)           | hasTerrace        |  0 or 1     |
|   If yes: Area           | terraceSurface      |  surface in square meters (int)     |
| Garden (Yes/No)           | hasGarden             |  0 or 1     |
|   If yes: Area            | gardenSurface        |  surface in square meters (int)     |
| Surface of the land           | landSurface      |  surface in square meters (int)     |
| Number of facades           | facadeCount        |  number of facades (int)     |
| Swimming pool (Yes/No)           | hasSwimmingPool|  0 or 1     |
| State of the building            | buildingCondition|  AS_NEW, GOOD, JUST_RENOVATED, TO_BE_DONE_UP, TO_RENOVATE, TO_RESTORE     |


##  2. Our strategy
We choose to use the data from [immoweb.com](http://www.immoweb.com) which is one of the top website in the country.


##  3. Technically
The data scraping from the website uses two tools from Python: selenium and BeautifulSoup. Selenium is used in a class (PageJumper) to navigate
automatically through the results pages of the website query. The second tool is used in another class (InfoScrapper) to extract the required data for a given property from its html webpage.


##  4. Usage
Go to immoweb.com and make a query for having the URL of all the apartments for sale. Do the same for all the houses for sale.
These two URLs are passed as parameter in the PageJumper class to get the list of webpage for each property.
This list is then passed in the InfoScrapper that will extract the desired data and build the final file housing-data.csv file that contains all the variables required.

### In details

1. The url of the apartments for sale query is passed as argument to the 'scrap_pages' function 
of the PageJumper class. This function calls two other functions:
    - 'jump_page' which allows going through enough webpages of the query (only a maximum of 30 listings appear on a single page)
    - 'extract_links' which is listing the urls of each property for sale
2. The urls of each property are saved in a file
3. Steps 1 and 2 are done again for the houses for sale query.
4. In the class InfoScrapper, the required data fields are defined, then:
   - a function called 'extract_info' uses BeautifulSoup to select a extract the fields wanted in a JSON dictionary
   - the function 'get_info' looks inside the dictionary for each field one by one while checking if the data is available or not.
   Each variable (or filed) is saved in a list.
     - finally, a function 'create_csv' used Pandas to transform the lists into a csv dataset.
   

##  5. Contributors
Jesus Bueno, Dirk Van Winkel, Lyes Rouabah

##  6. Timeline
This project was developed during working hours from May 25th until May 28th.
