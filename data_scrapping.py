import requests
from bs4 import BeautifulSoup as bs

url = 'https://www.filmweb.pl/films/search'

req = requests.get(url)

if req.status_code == 200:
    data = bs(req.content, 'html.parser')
    movie = data.find_all('div', class_ = 'filmPreview__card')
    for i in range(10):
        title = movie[i].h2.text
        year = int(movie[i].find('div',class_ = 'filmPreview__year').text)
        rate = float(movie[i].find('span', class_ = 'rateBox__rate').text.replace(',','.'))
        pop_rate = int(movie[i].find('span',class_ = 'rateBox__votes rateBox__votes--count').text.replace(' ', ''))
        want_see = int(movie[i].find('span',class_ = 'wantToSee__count').text.replace(' ', ''))
        print(title,year,rate,pop_rate,want_see)