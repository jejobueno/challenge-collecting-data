from bs4 import BeautifulSoup
import requests

url='https://www.immoweb.be/en/classified/house/for-sale/woluwe-saint-pierre/1150/9343689'
r = requests.get(url)
print(url, r.status_code)

soup = BeautifulSoup(r.content,'lxml')
print(soup)

