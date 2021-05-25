from bs4 import BeautifulSoup
import requests
'''

filename = "Immoweb.html"
file = open(filename, "r")
html_doc = file.read()
file.close()
html_doc
soup = BeautifulSoup(html_doc, "lxml")
with open('Immoweb.html','r') as html_file:
    content = html_file.read() 
'''

url='https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page=1&orderBy=relevance'
r = requests.get(url)
print(url, r.status_code)
soup = BeautifulSoup(r.content, "lxml")
'''
filename = "Immoweb.html"
file = open(filename, "r")
html_doc = file.read()
file.close()
html_doc
soup = BeautifulSoup(html_doc, "lxml")
with open('Immoweb.html','r') as html_file:
    content = html_file.read() 
'''
page_links = []
for elem in soup.find_all('a', attrs={"class": "card__title-link"}):
    page_links.append(elem.get('href'))
    page_links
print(page_links)
    
    
    
    