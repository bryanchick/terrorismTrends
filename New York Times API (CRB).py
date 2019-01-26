#!/usr/bin/env python
# coding: utf-8

# In[14]:


import requests
import json
from config import api_key
import pandas as pd
import time

# created a list of the keywords to iterate over
kw = "Terrorism"

# created a list of begin dates to iterate over the beginning of each year
begin_dates = [20070101, 20080101, 20090101, 20100101, 20110101,
               20120101, 20130101, 20140101, 20150101, 20160101, 20170101]

# created a list of begin dates to iterate over the end of each year
end_dates = [20071231, 20081231, 20091231, 20101231, 20111231,
             20121231, 20131231, 20141231, 20151231, 20161231, 20171231]


# In[ ]:


# created an empty list to hold the responses
results = []

# jeff note: within each response, there could be a 'number of articles' parameter

# added source = revelance, to populate pg 1 with most 'revelant' articles to the keyword
for begin_date, end_date in zip(begin_dates, end_dates):

    # iterating through the first 10 pages of 'revelant' articles for each year, one keyword at a time
    for page in range(1, 11):

        try:
            url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?begin_date={}&end_date={}&q={}&sort=relevance&page={}&api-key={}'.format(begin_date, end_date,
                                                                                                                                                     kw, page, api_key)
            response = requests.get(url).json()

            # sleep requirement of 6 seconds between requests to avoid per min rate limit
            time.sleep(6)

            # printing each keyword and page it iterates through for confirmation
            print(f'{begin_date}-{end_date};  quering page #{page}...')

            # where the list of 'article' dicts begins
            for article in response['response']['docs']:

                # created column declaring the page # used to find that article
                article['page_nbr'] = page

                # jeff note: create column to declare the "hit_level" used to find that article
                # article['hits_level'] = # get the hits here

                # adds the article data created to the existing article data,
                # appends it to the empty 'results' list
                results.append(article)
        except:
            print(f'Page {page} for {kw} not found.')


# In[ ]:


# created a df from the 'records' list of dicts with article data
df = pd.DataFrame.from_records(results)

df.head()
# what is the difference in "from_records" and "for_dict"??


# In[ ]:


# created an empty list to hold the new dates
formatted_date = []
formatted_year = []
formatted_month = []

# iterate over each published date in the df 
for date in df['pub_date']:
    
    # converted all pub dates from ints to strings
    date_string = str(date)
    
    # split the date to only contain YYYY-MM-DD
    new_date = date_string[:10]
    
    # split the year and month out from the date
    new_year = date_string[:4]
    new_month = date_string[5:7]
    
    # added new date/month/year to 'formatted date/year/month' list
    formatted_date.append(new_date)
    formatted_month.append(int(new_month))
    formatted_year.append(int(new_year))
    
# added the new date/month/year to the df
df['formatted_date'] = formatted_date
df['formatted_month'] = formatted_month
df['formatted_year'] = formatted_year


# In[ ]:


# used .map() and used lambda as the function to iterate through each
# row to capture the 'main' title

# created new column 'article title'...
df['article_title'] = df['headline'].map(lambda x: x['main'])

# ...made it equal to the 'main' title for each row


# In[ ]:


new_df = pd.DataFrame({
    "Page": df['page_nbr'],
    "Year": df['formatted_year'],
    "Month": df['formatted_month'],
    "Title": df['article_title'],
    "Date": df['formatted_date'],
    "URL": df['web_url'],
    
})

new_df.head(20)


# In[ ]:


new_df.to_csv("NYT Terrorism Articles.csv")


# In[ ]:


articles_per_year = new_df.groupby(['Year','Month']).agg({"Title":"count"}).reset_index()


# In[ ]:


# import plotly.plotly as py
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from pylab import rcParams
import pylab


# style
plt.style.use('seaborn-darkgrid')
rcParams['figure.figsize'] = 12, 8


# create a color palette
palette = plt.get_cmap('Set1')

for year in articles_per_year["Year"].unique()[0:6]:

    temp = articles_per_year[articles_per_year["Year"] == year]
    x = list(temp["Month"])
    y = list(temp["Title"])
    terrorism_2007_2012 = plt.plot(x, y, label=year)


# Add legend
plt.legend(loc=2, ncol=2)

# Add titles
plt.title("From the New York Times API: Number of Articles with keyword 'Terrorism'",
          loc='right', fontsize=12, fontweight=0, color='orange')
plt.xlabel("Months")
plt.xticks()
plt.ylabel("Number Articles")
plt.show(terrorism_2007_2012)


# In[ ]:


# style
plt.style.use('seaborn-darkgrid')
rcParams['figure.figsize'] = 12, 8

# create a color palette
palette = plt.get_cmap('Set1')

for year in articles_per_year["Year"].unique()[6:11]:

    temp = articles_per_year[articles_per_year["Year"] == year]
    x = list(temp["Month"])
    y = list(temp["Title"])
    plt.plot(x, y, label=year)


# Add legend
plt.legend(loc=2, ncol=2)

# Add titles
plt.title("From the New York Times API: Number of Articles with keyword 'Terrorism'",
          loc='right', fontsize=12, fontweight=0, color='orange')
plt.xlabel("Months")

plt.ylabel("Number Articles")
plt.show()

# savefig
pylab.savefig('2012-2017.jpeg')


# In[ ]:




