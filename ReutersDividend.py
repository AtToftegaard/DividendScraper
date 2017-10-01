# -*- coding: utf-8 -*-

from urllib.request import urlopen
from bs4 import BeautifulSoup
from requests import get
import csv

# Take ticker, return url for company-page
def getURLforPage(ticker):
    url = "http://www.reuters.com/finance/stocks/lookup?searchType=any&comSortBy=marketcap&sortBy=&dateRange=&search=" + ticker
    response = get(url)
    search_soup = BeautifulSoup(response.text, 'html.parser')
    partURLs = search_soup.find_all('tr', class_='stripe', attrs ={'onclick'})
    for url in partURLs:
        url = url.get('onclick')[17:-1]
        if (ticker.replace(" ", "")+'.CO') in url:
            return ('http://www.reuters.com'+url)
        else: 
            return ('Error')
    
# Take stockticker, return dividend
def findDividend(ticker):
    url = getURLforPage(ticker)
    if url == 'Error':
        return ('Error')
    else:
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
            print(companyname + ' : ' + field[1])
            yield_dict[companyname] = findDividend(field[1])
            
i = 0 
j = 0
w = csv.writer(open("output.csv", "w"))
for key, val in yield_dict.items():
    if '--' in yield_dict[key]:
        i = i+1
    else:
        j = j+1
    w.writerow([key, val])

print(i , ' missing')
print(j , ' found')
print(i/(i+j)*100,'% completion')






