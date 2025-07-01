import pandas as pd
import requests
import BeautifulSoup


web=requests.get('https://en.wikipedia.org/wiki/Main_Page')
print(web)

soup=BeautifulSoup(web.content,'html.parser')
print(soup.prettify())

