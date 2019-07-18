from urllib.request import urlopen

from bs4 import BeautifulSoup
from movie import *

def getCurrentMovie(url):
    movielist = []
    bs = BeautifulSoup(url, 'html.parser')
    body = bs.body

    target = body.find(class_="lst_detail_t1")
    list = target.find_all('li')
    no = 1
    for n in range(0, len(list)):
        # 영화 포스터 이미지 주소
        img = list[n].find("img").get('src')

        # 영화 제목
        title = list[n].find(class_="tit").find("a").text

        # 감독
        try:
            director = list[n].find(class_="info_txt1").find_all("dd")[1].find("span").find_all("a")
            director_list = [director.text.strip() for director in director]
            directors = ','.join(director_list)
        except IndexError:
            directors = ''

        # 출연 배우
        try:
            cast = list[n].find(class_="lst_dsc").find("dl", class_="info_txt1").find_all("dd")[2].find(
                class_="link_txt").find_all("a")
            cast_list = [cast.text.strip() for cast in cast]
            casts = ','.join(cast_list)
        except IndexError:
            casts = ''

        info = list[n].find(class_="info_txt1").find_all("dd")[0].getText().split()

        count = 0
        genres = ""
        time = ""
        date = ""
        for j in range(len(info)):
            if count == 0:
                if '|' not in info[j]:
                    genres += info[j]
                else:
                    count += 1
            elif count == 1:
                if '|' not in info[j]:
                    if '분' in info[j]:
                        time += info[j]
                    else:
                        date += info[j]
                else:
                    count += 1
            elif count == 2:
                if '|' not in info[j]:
                    date += info[j]
                else:
                    break
            else:
                break
        movie = Movie(no, img, title, directors, casts, genres, time, date, 0)
        movielist.append(movie)
        no += 1

    return movielist

url = urlopen("https://movie.naver.com/movie/running/current.nhn")
current_list = getCurrentMovie(url)
# print(type(current_list[0].directors), type(current_list[0].casts), type(current_list[0].genres))
# for i in range(len(current_list)):
#     current_list[i].print_info()
