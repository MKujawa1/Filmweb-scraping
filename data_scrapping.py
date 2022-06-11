import requests
from bs4 import BeautifulSoup as bs
import numpy as np
import pandas as pd
#Random user agent

cur_page = 1

while True:
    url = f'https://www.filmweb.pl/films/search?orderBy=popularity&descending=true&page={cur_page}'
    req = requests.get(url)
    if req.status_code == 200:
        data = bs(req.content, 'html.parser')
        movies = data.find_all('div', class_ = 'filmPreview__card')
        for movie in movies:
            try:
                title = movie.h2.text
            except:
                # print('no title')
                title = np.nan
            try:
                year = int(movie.find('div',class_ = 'filmPreview__year').text)
            except:
                # print('no year')
                year = np.nan
            try:
                rate = float(movie.find('span', class_ = 'rateBox__rate').text.replace(',','.'))
            except:
                # print('no rate')
                rate = np.nan
            try:
                pop_rate = int(movie.find('span',class_ = 'rateBox__votes rateBox__votes--count').text.replace(' ', ''))
            except:
                # print('no pop_rate')
                pop_rate = np.nan
            try:
                want_see = int(movie.find('span',class_ = 'wantToSee__count').text.replace(' ', ''))
            except:
                # print('no want_see')
                want_see = np.nan
            try:
                genres = movie.find('div',class_ = 'filmPreview__info filmPreview__info--genres')
                genre = []
                try:
                    genres = genres.find_all('a')
                    for gen in genres:
                        genre.append(gen.text)
                except:
                    genre.append(genres.a.text)  
            except:
                # print('no genre')
                genre = np.nan
            print(title,year,rate,pop_rate,want_see,genre)
        else:
            pass
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
        print(cur_page)
        cur_page += 1