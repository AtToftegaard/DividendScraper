# -*- coding: utf-8 -*-

import urllib3
from urllib.request import urlopen
from bs4 import BeautifulSoup
from requests import get
import csv
import google

# Take ticker, return url for company-page
def getURLforPage(ticker):
    url = "http://www.reuters.com/finance/stocks/lookup?searchType=any&comSortBy=marketcap&sortBy=&dateRange=&search=" + ticker
    response = get(url)
    search_soup = BeautifulSoup(response.text, 'html.parser')
    partURL = search_soup.find('tr', class_='stripe').get('onclick')[17:-1]
    return ("http://www.reuters.com"+partURL)

    
# Take stockticker, return dividend
def findDividend(ticker):
    url = getURLforPage(ticker)
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    
    keywords = ['Yield']
    for tr in html_soup.find_all('tr'):
        string = tr.get_text()
        if any(word in string for word in keywords):
            return(string);


stockurl = "http://www.nasdaqomxnordic.com/shares/listed-companies/copenhagen"

response = get(stockurl)
stockpage_soup = BeautifulSoup(response.text, 'html.parser')
table = stockpage_soup.find('table', id = "listedCompanies")
headings = [header.get_text() for header in stockpage_soup.find('tr').find_all('th')]

yield_dict = {}
datasets= []
for row in table.find_all('tr')[1:]:
    dataset = zip(headings, (td.get_text() for td in row.find_all('td')))
    datasets.append(dataset)


for dataset in datasets:
    for field in dataset:
        if field[0] == 'Name':
            companyname = field[1]
        if field[0] == 'Symbol': 
            #print('finding for '+ field[1])
            yield_dict[companyname] = findDividend(field[1])
            
for key in yield_dict:
    print( key, yield_dict[key]) 
                
       # print ("{0:<16}: {1}".format(field[0], field[1]))






