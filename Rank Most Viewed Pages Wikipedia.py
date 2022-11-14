#!/usr/bin/env python
# coding: utf-8

"""

This algorithm aims to rank the most viewed Wikipedia pages of companies listed on the Nasdaq.

"""

#Importer Modules
import numpy as np
import datetime
import subprocess
import ast
import wikipediaapi
import pandas as pd

wiki_wiki = wikipediaapi.Wikipedia('en')
all_Stock = pd.read_csv('Nasdaq_Stocks.csv', sep=';')


list_name = list(all_Stock['Name'])[0:50]

daily_num_search = []
weekly_num_search = []

for name in list_name:

    page_py = wiki_wiki.page(name)

    if page_py.exists() == True:

        #Create the link
        startTime = datetime.datetime.now() - datetime.timedelta(days= 7)
        startTimeFormat = startTime.strftime('%Y%m%d')
        endTime = datetime.datetime.now().strftime('%Y%m%d')

        name_corp = name.replace(" ", '_')

        link = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/all-agents/{name_corp}/daily/{str(startTimeFormat)}/{str(endTime)}"

        try:

            #Get data on Wikipedia
            proc = subprocess.Popen(["curl",  "-X", "GET", link], 
                                    stdout=subprocess.PIPE)

            cadastro, err = proc.communicate()

            #Transfom bytes to dict

            byte_str = cadastro
            dict_str = byte_str.decode("UTF-8")
            data_wiki = ast.literal_eval(dict_str)

            #Get the data
            firstString = str(data_wiki.values())

            toDel = ['""',',','[',']','{','}',':','(',')','dict_values',"'"]

            for i in toDel:
                     firstString = firstString.replace(i, '')

            firstString = firstString.split()

            new_values = np.column_stack((name, firstString[97]))

            daily_num_search.extend(new_values)

            sum_values_week = int(firstString[13]) + int(firstString[27]) + int(firstString[41]) + int(firstString[55]) + int(firstString[69]) + int(firstString[83]) + int(firstString[97])

            new_values = np.column_stack((name, sum_values_week))

            weekly_num_search.extend(new_values)
        except:
            pass


#Create Dataframe
daily_num_search_df = pd.DataFrame(daily_num_search, columns = ['Name Company','Page Views'])
weekly_num_search_df = pd.DataFrame(weekly_num_search, columns = ['Name Company','Page Views'])

#Put Dataframe in form
daily_num_search_df['Page Views'] = pd.to_numeric(daily_num_search_df['Page Views'])
daily_num_search_df = daily_num_search_df.sort_values(by =['Page Views'], ascending=False)
daily_num_search_df = daily_num_search_df.head(15)

weekly_num_search_df['Page Views'] = pd.to_numeric(weekly_num_search_df['Page Views'])
weekly_num_search_df = weekly_num_search_df.sort_values(by =['Page Views'], ascending=False)
weekly_num_search_df = weekly_num_search_df.head(15)





