import re
from urllib.request import urlopen

from bs4 import BeautifulSoup

def getCurrentMovieScore(naver_url):
    naver_base_url = 'https://movie.naver.com'
    naver_bs = BeautifulSoup(naver_url, 'html.parser')
    body = naver_bs.body
    whole_list = []
    target = body.find(class_="lst_detail_t1")
    # print(type(target))
    list = target.find_all('li')
    for n in range(len(list)):
        movie_url = urlopen(naver_base_url + list[n].find('dt', class_="tit").find("a").get('href'))
        movie_bs = BeautifulSoup(movie_url, 'html.parser')
        movie_body = movie_bs.body
        try:
            synopsis_title = movie_body.find(class_="h_tx_story").getText()
        except AttributeError:
            synopsis_title = None
        try:
            content = movie_body.find('div', class_="story_area").find('p', class_='con_tx')
            content = content.prettify(formatter="html")

            content = content.replace('&nbsp;', '')
            content = content.replace('<br/>', '')
            content = content.replace('<p class="con_tx">\n', '')
            content = content.replace('</p>', '')
            content = content.replace('&hellip;', '...')
            content = content.replace('&lsquo;', '"')
            content = content.replace('&rsquo;', '"')
            content = content.replace('&ldquo;', '"')
            content = content.replace('&rdquo;', '"')
            content = content.replace('&lt;', '<')
            content = content.replace('&gt;', '>')
        except AttributeError:
            content = None
        print(synopsis_title)
        print(content)
naver_url = urlopen("https://movie.naver.com/movie/running/current.nhn")
getCurrentMovieScore(naver_url)