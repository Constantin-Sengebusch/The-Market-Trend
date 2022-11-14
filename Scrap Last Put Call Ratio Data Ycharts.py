#!/usr/bin/env python
# coding: utf-8

"""

This algorithm aims to scrap last put/call ratio data from Ycharts.com

"""

#Importer Modules
import datetime
import requests
from bs4 import BeautifulSoup


#Ajout ligne à partir de données à jour
url = "https://ycharts.com/indicators/cboe_spx_put_call_ratio"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
page = requests.get(url, headers=headers).text

soup = BeautifulSoup(page, "lxml")

entries = []

currentMonth = datetime.datetime.now().strftime("%B")

for found_table in soup.find_all('table', class_='table'):
    if currentMonth in found_table.get_text():
        table_data = found_table.tbody.find_all("tr")

# Get the data
headings = []

for td in table_data[0].find_all("td"):
    # remove any newlines and extra spaces from left and right
    headings.append(td.text.replace('\n', ' ').strip())

put_call_ratio = [headings[0], headings[1]]