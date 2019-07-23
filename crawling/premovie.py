from urllib.request import urlopen

from bs4 import BeautifulSoup

from movie import *

# from metacritic import *

def replaceRight(original, old, new, count_right):
    repeat = 0
    text = original

    count_find = original.count(old)
    if count_right > count_find:  # 바꿀 횟수가 문자열에 포함된 old보다 많다면
        repeat = count_find  # 문자열에 포함된 old의 모든 개수(count_find)만큼 교체한다
    else:
        repeat = count_right  # 아니라면 입력받은 개수(count)만큼 교체한다

    for _ in range(repeat):
        find_index = text.rfind(old)  # 오른쪽부터 index를 찾기위해 rfind 사용
        text = text[:find_index] + new + text[find_index + len(old):]

    return text

def getPreMovie(url):

    bs = BeautifulSoup(url, 'html.parser')
    body = bs.body
    naver_base_url = 'https://movie.naver.com'

    movie_list = []

    target = body.find(class_="obj_section")
    list_date = target.find_all(class_="lst_wrap")
    no = 1
    for i in range(0, len(list_date)):
        info = list_date[i].find(class_="lst_detail_t1").find_all('li')
        # print(len(info))

        # for n in range(0, len(info)):
        for li in info:
            # 영화 포스터 이미지 주소
            img = li.find("img").get('src')
            # print(img)
            # img1 = img.replace("99", "203", 1)
            img1 = replaceRight(img, "99", "203", 1)
            # resize_img = img1.replace("141", "290", 1)
            resize_img = replaceRight(img1, "141", "290", 1)
            # print(resize_img)

            # 영화 제목
            main_page = li.find(class_="tit").find("a")
            # title = info[n].find(class_="tit").find("a").text
            title = main_page.text
            print(title)
            try:
                rating = li.find(class_="tit").find('span').getText()
            except AttributeError:
                rating = None
            # print(rating)

            # 감독
            try:
                director = li.find(class_="info_txt1").find_all("dd")[1].find("span").find_all("a")
                directorList = [director.text.strip() for director in director]
                directors = ','.join(directorList)
            except IndexError:
                directors = ''

            # 출연 배우
            try:
                cast = li.find(class_="lst_dsc").find("dl", class_="info_txt1").find_all("dd")[2].find(
                    class_="link_txt").find_all("a")
                castList = [cast.text.strip() for cast in cast]
                casts = ','.join(castList)
            except IndexError:
                casts = ''

            info = li.find(class_="info_txt1").find_all("dd")[0].getText().split()
            print(info)
            count = 0
            genres = ""
            time = ""
            date = ""
            # if info.count('|') == 2:
            #     g = info.find('|')
            #     for x in range(g):

            # for j in range(len(info)):
            #     if count == 0:
            #         if '|' not in info[j]:
            #             genres += info[j]
            #         else:
            #             genreList = genres.split(',')
            #             count += 1
            #     elif count == 1:
            #         if '|' not in info[j]:
            #             if '분' in info[j]:
            #                 time += info[j]
            #             else:
            #                 date += info[j]
            #         else:
            #             count += 1
            #     elif count == 2:
            #         if '|' not in info[j]:
            #             date += info[j]
            #         else:
            #             break
            #     else:
            #         break
            for j in range(len(info)):
                if count == 0:
                    if '|' not in info[j]:
                        if '분' not in info[j]:
                            genres += info[j]
                        else:
                            time += info[j]
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
            print("genres : \t" + genres)
            print("time : \t" + time)
            print("date : \t" + date)
            critic_list = []

            # movie_url = urlopen(naver_base_url + info[n].find(class_="tit").find("a").get('href'))
            movie_url = urlopen(naver_base_url + main_page.get('href'))
            movie_bs = BeautifulSoup(movie_url, 'html.parser')
            movie_body = movie_bs.body

            try:
                eng_title = movie_body.find(class_="mv_info_area").find(class_="mv_info").find('strong').getText()
                # eng_title = eng_title.replace(', ', '-')
            except AttributeError:
                eng_title = None
            # print(eng_title)


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
            # print(synopsis_title)
            # print(content)

            year = date[0:4]
            parsed_title = title + '_' + year
            movie = Movie(no, resize_img, parsed_title, directors, casts, genres, time, date, 1, critic_list, synopsis_title, content, eng_title, rating)
            # movie.set_metascore(getMetascore(movie))
            movie_list.append(movie)
            no += 1
    return movie_list


# url = urlopen("https://movie.naver.com/movie/running/premovie.nhn")
# pre_list = getPreMovie(url)
# print(type(pre_list[0].directors), type(pre_list[0].casts), type(pre_list[0].genres))
# for k in range(len(pre_list)):
#     pre_list[k].print_info()
