from urllib.request import urlopen

from bs4 import BeautifulSoup
from movie import *
# from metacritic import *
# from rottentomato import *


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

def getCurrentMovie(url):
    movielist = []
    naver_base_url = 'https://movie.naver.com'
    bs = BeautifulSoup(url, 'html.parser')
    body = bs.body

    target = body.find(class_="lst_detail_t1")
    list = target.find_all('li')
    no = 1
    for n in range(0, len(list)):
        # print("No : " + str(no))
        # 영화 포스터 이미지 주소
        img = list[n].find("img").get('src')
        # img1 = img.replace("99", "203", 1)
        img1 = replaceRight(img, "99", "203", 1)
        # resize_img = img1.replace("141", "290", 1)
        resize_img = replaceRight(img1, "141", "290", 1)
        # print(resize_img)

        # 등급
        # content > div.article > div:nth-child(1) > div.lst_wrap > ul > li:nth-child(1) > dl > dt > span
        try:
            rating = list[n].find(class_="tit").find('span').getText()
        except AttributeError:
            rating = None
        # print(rating)

        # 영화 제목
        title = list[n].find(class_="tit").find("a").text
        print(title)

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

        score_url = urlopen(naver_base_url + list[n].find(class_="star").find("a").get('href').split('#')[0])
        # print(naver_base_url + list[n].find(class_="star").find("a").get('href').split('#')[0])
        score_bs = BeautifulSoup(score_url, 'html.parser')
        score_body = score_bs.body

        # 영어 제목
        # content > div.article > div.mv_info_area > div.mv_info > strong
        try:
            eng_title = score_body.find(class_="mv_info_area").find(class_="mv_info").find('strong').getText()
            # eng_title = eng_title.replace(', ', '-')
        except AttributeError:
            eng_title = None
        # print(eng_title)

        # 기자
        critic_list = []
        try:
            report_body = score_body.find(class_="score_special").find(class_="reporter")
            report_list = report_body.find_all('li')
            for report in report_list:
                try:
                    report_name = report.find('div', class_="reporter_line").find('dl', class_="p_review").find(
                        "a").getText()
                except AttributeError:
                    report_name = None
                # print(report_name)
                try:
                    report_title = report.find('div', class_="reporter_line").find('dd').getText()
                except AttributeError:
                    report_title = None
                # print(report_title)
                try:
                    report_score = float(report.find('div', class_="re_score_grp").find('em').getText())
                except AttributeError:
                    report_score = None
                # print(report_score)
                try:
                    report_content = report.find('p', class_="tx_report").getText()
                except AttributeError:
                    report_content = None
                # print(report_content)
                critic_list.append((report_name, report_title, report_score, report_content))
        except AttributeError:
            print("No Reports")
            # critic_list.append((None, None, None, None))

        # 평론가
        try:
            star_score = score_body.find(class_="score_special").find(class_="score_result")
            lis = star_score.find_all('li')
            for li in lis:
                try:
                    score = int(li.find('div',class_='star_score').find('em').get_text())
                except AttributeError:
                    score = None
                try:
                    critic_str = li.find('div', class_='score_reple').find('p').get_text()
                except AttributeError:
                    critic_str = None
                try:
                    critic_name = li.find('div', class_='score_reple').find('dd').get_text().split(' ')[1].split('\r')[0]
                except AttributeError:
                    critic_name = None
                critic_content = None
                critic_list.append((critic_name, critic_str, score, critic_content))
            # whole_list.append(critic_list)
        except AttributeError:
            print("No Critics")
            # critic_list.append((None, None, None, None))

        # print(critic_list)

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
        # print(content)
        # print(critic_list)
        year = date[0:4]
        parsed_title = title + '_' + year
        movie = Movie(no, resize_img, parsed_title, directors, casts, genres, time, date, 0, critic_list, synopsis_title, content, eng_title, rating)
        no += 1
        # print(movie.image)
        movie.set_naver_score(movie.get_score_average())
        # movie.set_metascore(getMetascore(movie))
        # getTomato(movie)
        # movie.set_tomato(getTomato)
        movielist.append(movie)
        # print(movie.eng_title)
        # print(movie.avg_score)

    return movielist



# url = urlopen("https://movie.naver.com/movie/running/current.nhn")
# current_list = getCurrentMovie(url)
# # getTomato(current_list)
# getMetascore(current_list)