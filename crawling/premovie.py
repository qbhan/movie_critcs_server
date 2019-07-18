from urllib.request import urlopen

from bs4 import BeautifulSoup

from movie import *

def getPreMovie(url):

    global directorList, castList, genreList
    bs = BeautifulSoup(url, 'html.parser')
    body = bs.body

    movie_list = []

    target = body.find(class_="obj_section")
    list_date = target.find_all(class_="lst_wrap")
    no = 1
    for i in range(0, len(list_date)):
        info = list_date[i].find_all(class_="lst_detail_t1")

        for n in range(0, len(info)):

            # 영화 포스터 이미지 주소
            img = info[n].find("img").get('src')

            # 영화 제목
            title = info[n].find(class_="tit").find("a").text

            # 감독
            try:
                director = info[n].find(class_="info_txt1").find_all("dd")[1].find("span").find_all("a")
                directorList = [director.text.strip() for director in director]
                directors = ','.join(directorList)
            except IndexError:
                directors = ''

            # 출연 배우
            try:
                cast = info[n].find(class_="lst_dsc").find("dl", class_="info_txt1").find_all("dd")[2].find(
                    class_="link_txt").find_all("a")
                castList = [cast.text.strip() for cast in cast]
                casts = ','.join(castList)
            except IndexError:
                casts = ''

            info = info[n].find(class_="info_txt1").find_all("dd")[0].getText().split()

            count = 0
            genres = ""
            time = ""
            date = ""
            for j in range(len(info)):
                if count == 0:
                    if '|' not in info[j]:
                        genres += info[j]
                    else:
                        genreList = genres.split(',')
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

            movie = Movie(no, img, title, directors, casts, genres, time, date, 1)
            movie_list.append(movie)

            no += 1
    return movie_list


url = urlopen("https://movie.naver.com/movie/running/premovie.nhn")
pre_list = getPreMovie(url)
print(type(pre_list[0].directors), type(pre_list[0].casts), type(pre_list[0].genres))
# for k in range(len(pre_list)):
#     pre_list[k].print_info()
