# -*- coding: utf-8 -*-

import urllib3
from urllib.request import urlopen
from bs4 import BeautifulSoup
from requests import get
import google

stockurl = "https://npinvestor.dk/aktier-og-kurslister/aktier/danmark/alle-danske-aktier"

response = get(stockurl)
stockpage_soup = BeautifulSoup(response.text, 'html.parser')

danskeAktier = stockpage_soup.find_all('div', class_="table-row-even float-columns")
stockList = []
URLlist = []

for stock in danskeAktier:
    name = stock.div.a
    name = name.text
    stockList.append(name)

for stockName in stockList:
    for url in google.search((stockName + 'Reuters'), num = 4, stop = 1, pause = 2.0):
        url.text
        if url.endswith('.CO'):
            URLlist.append(url)


#for url in google.search(stockName, num = 1, stop = 1):



# =============================================================================
# 
# url = "http://mobile.reuters.com/finance/stocks/overview/MATAS.CO"
# 
# response = get(url)
# html_soup = BeautifulSoup(response.text, 'html.parser')
#  
# div_containers = html_soup.find_all('div', class_="section-quote-detail group")
# 
# for div in div_containers:
#     string = div.text
#     if 'Dividend' in string:
#         string = " ".join(string.split())
#         print(string)
# 
# =============================================================================
