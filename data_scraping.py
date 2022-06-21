import requests
from bs4 import BeautifulSoup as bs
import numpy as np
import pandas as pd
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

### Get random user agent 
software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
user_agents = user_agent_rotator.get_user_agents()
### Create empty dataframe
all_data = pd.DataFrame({'title':[],
                         'year':[],
                         'rate':[],
                         'pop_rate':[],
                         'want_see':[],
                         'genre': []})
### Init first page
cur_page = 1
### Loop start
while True:
    ### Get user agent
    user_agent = user_agent_rotator.get_random_user_agent()
    ### Url of page
    url = f'https://www.filmweb.pl/films/search?orderBy=popularity&descending=true&page={cur_page}'
    ### Get request 
    req = requests.get(url,headers = {'user-agent': user_agent})
    ### Check status of request
    if req.status_code == 200:
        ### Create empty list to append data
        movie_title = []
        movie_year = []
        movie_rate = []
        movie_pop_rate = []
        movie_want_see = []
        movie_genre = []
        ### Read items from page and adding to list
        data = bs(req.content, 'html.parser')
        movies = data.find_all('div', class_ = 'filmPreview__card')
        for movie in movies:
            try:
                title = movie.h2.text
                movie_title.append(title)
            except:
                # print('no title')
                title = np.nan
                movie_title.append(title)
            try:
                year = int(movie.find('div',class_ = 'filmPreview__year').text)
                movie_year.append(year)
            except:
                # print('no year')
                year = np.nan
                movie_year.append(year)
            try:
                rate = float(movie.find('span', class_ = 'rateBox__rate').text.replace(',','.'))
                movie_rate.append(rate)
            except:
                # print('no rate')
                rate = np.nan
                movie_rate.append(rate)
            try:
                pop_rate = int(movie.find('span',class_ = 'rateBox__votes rateBox__votes--count').text.replace(' ', ''))
                movie_pop_rate.append(pop_rate)
            except:
                # print('no pop_rate')
                pop_rate = np.nan
                movie_pop_rate.append(pop_rate)
            try:
                want_see = int(movie.find('span',class_ = 'wantToSee__count').text.replace(' ', ''))
                movie_want_see.append(want_see)
            except:
                # print('no want_see')
                want_see = np.nan
                movie_want_see.append(want_see)
            try:
                genres = movie.find('div',class_ = 'filmPreview__info filmPreview__info--genres')
                genre = []
                try:
                    genres = genres.find_all('a')
                    for gen in genres:
                        genre.append(gen.text)
                except:
                    genre.append(genres.a.text)
                movie_genre.append(genre)
            except:
                genre = np.nan
                movie_genre.append(genre)
            print(title,year,rate,pop_rate,want_see,genre)
        else:
            pass
        ### Append data to DataFrame
        all_data = all_data.append(pd.DataFrame({'title':movie_title,
                                                 'year':movie_year,
                                                 'rate':movie_rate,
                                                 'pop_rate':movie_pop_rate,
                                                 'want_see':movie_want_see,
                                                 'genre': movie_genre}),ignore_index = True)   
        print(cur_page)
        ### Check that the current page isn't last page
        pages = data.find('ul', class_ = 'pagination__list')
        page = pages.find_all('li',class_ = 'pagination__item')
        max_p = []
        for p in page:
            try:
                max_p.append(int(p.text))
            except:
                pass
        max_p = np.amax(max_p)
        if max_p == int(cur_page):
            break
        ### Page increament
        cur_page += 1
### Save to excel      
all_data.to_excel('data.xlsx',index=False)
### Clean Data
### Load data
data = pd.read_excel('data.xlsx')
### Remove [] and ' from genre
for i in range(len(data)):
    try:
        data['genre'][i] = data['genre'][i].replace('[','').replace(']','').replace("'",'')
    except:
        pass
### Remove nan values
keys = list(data.keys())
indexes = []
for i in range(len(data)):
    for col_n in keys:
        if pd.isna(data[col_n][i])==True:
            indexes.append(i)
indexes = list(set(indexes))

new_data = data.drop(data.index[indexes])

new_data.to_excel('new_data.xlsx',index=False)
