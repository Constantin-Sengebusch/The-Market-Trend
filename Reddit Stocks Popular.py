#!/usr/bin/env python
# coding: utf-8

"""

Get most discussed stocks on Reddit over the last day.

"""

#Importer Modules
import pandas as pd
import praw
from collections import Counter

# Should create your credentials
reddit = praw.Reddit(client_id='XXXXX',
                     client_secret='XXXXX',
                     password='XXXXX',
                     user_agent='XXXXX',
                     username='XXXXX')


all_stocks = pd.read_csv('Nasdaq_Stocks.csv', sep=';')
list_symbol = list(all_stocks['Symbol'])


#Get all post from Reddit day
complete_string = []

SubredditTopics = ["investing",
                   "stocks",
                   "wallstreetbets",
                   "smallstreetbets",
                   "thetagang",
                   "Superstonk",
                   "options",
                   "pennystocks",
                   "wallstreetbetsOGs"]

for x in SubredditTopics:
    subreddit = reddit.subreddit(x).top("day")
    sub_ids = []
    for submission in subreddit:
        sub_ids.append(submission.id)

    top_level_comments = []
    title = []
    selftext = []
    for sub_id in sub_ids:
        submission = reddit.submission(id = sub_id)
        title.append(submission.title) # Get submission title
        selftext.append(submission.selftext) # Get submission content
        submission.comments.replace_more(limit = None)
        for top_level_comment in submission.comments:
            top_level_comments.append(top_level_comment.body) # Get top-level comments

    complete_string += top_level_comments + title + selftext


#Compare the list with list of stock of NASDAQ
split_it = str(complete_string).split()

# Pass the split_it list to instance of Counter class.
Counter = Counter(split_it)

# most_common() produces k frequently encountered
# input values and their respective counts.
most_occur = Counter.most_common(5000)
most_occur_df = pd.DataFrame(most_occur)
search = list(most_occur_df[0])

values = pd.DataFrame([(w, list_symbol.count(w)) for w in set(list_symbol) if w in search])

df1 = most_occur_df.set_axis(['lkey','value'],axis='columns')
df2 = values.set_axis(['rkey','value'],axis='columns')

#Get the Frequency for each result
merge_df = df1.merge(df2, left_on='lkey', right_on='rkey')
merge_df = merge_df[['lkey','value_x']].set_axis(['Stock','Frequency'],axis='columns').head(10)


