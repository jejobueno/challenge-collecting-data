# Real estate sales scraping for Belgium

##  1. Description

This project is about building a data set related to real estate sales in Belgium from scratch
by using web scraping tools in Python.

The data set should contain the common variables of interest when one is interested in real estate sales:
location, surface, price, number of rooms, amenities (equipped kitchen, terrace, garden...). It should cover all
the belgian territory, contain both apartments and houses, and count a minimum of 10 000 entries.

##  2. Our strategy
We choose to use the data from [immoweb.com](http://www.immoweb.com) which is one of the top website in the country.

##  3. Technically
The data scraping from the website uses two tools from Python: selenium and BeautifulSoup. Selenium is used in a class (PageJumper) to navigate
automatically through the results pages of the website query. The second tool is used in another class (InfoScrapper) to extract the required data for a given property from its html webpage.

##  4. Usage
Go to immoweb.com and make a query for having the URL of all the apartments for sale. Do the same for all the houses for sale. These two URLs are passed as parameter in the PageJumper class to get the list of webpage for each property. This list is then passed in the InfoScrapper that will extract the desired data and build the final file housing-data.csv file that contains all the variables required.

##  5. Contributors
Jesus Bueno, Dirk Van Winkel, Lyes Rouabah

##  6. Timeline
This project was developed during working hours from May 25th until May 28th.

##  7. Personal situation
???
