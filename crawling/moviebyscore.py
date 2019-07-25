from urllib.request import urlopen

from bs4 import BeautifulSoup

from movie import *

# from metacritic import *

def getMovieByScore(url):
    movielist = []
    naver_base_url = 'https://movie.naver.com'
    order_score_url = '/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20190723'
    bs = BeautifulSoup(url, 'html.parser')
    body = bs.body
    target = body.find(class_="list_ranking")
    list = target.find_all('td', class_="title")
    # print(list)
    no = 1
    for n in range(0, len(list)):
        # print(list[n])
        url1 = list[n].find(class_="tit5").find('a').get('href')
        movie_home_url = naver_base_url + url1
        # print(movie_home_url)
        soup = BeautifulSoup(urlopen(movie_home_url), 'html.parser')
        soup_body = soup.body
        mv_info_area = soup_body.find(class_='mv_info')

        # 영화제목
        try:
            mv_title = mv_info_area.find(class_='h_movie').find('a').getText()
        except AttributeError:
            mv_title = None
        # print(mv_title)

        mv_info_spec = mv_info_area.find(class_='info_spec').find_all('span')
        # print(mv_info_spec)

        # 장르
        try:
            mv_genre = mv_info_spec[0].find('a').getText()
        except:
            mv_genre = None
        # print(mv_genre)

        # 상영시간
        try:
            mv_time = mv_info_spec[2].getText()
        except AttributeError:
            mv_time = None
        # print(mv_time)

        # 개봉일
        try:
            mv_date_list = mv_info_spec[3].find_all('a')[-2:]
            mv_date = mv_date_list[0].getText() + mv_date_list[1].getText()
        except AttributeError:
            mv_date = None
        print(mv_date)

        # 등급
        # content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(8) > p > a:nth-child(1)
        # content > div.article > div.mv_info_area > div.mv_info > dl > dd:nth-child(8) > p
        try:
            rating = soup_body.find(class_="mv_info_area").find(class_="mv_info").find('dl').find_all('dd')[-1].find('a').getText()
        except AttributeError:
            rating = None
        # print(rating)

        # 감독
        try:
            mv_director = mv_info_area.find_all('dl')[0].find('dd').find('a').getText()
        except AttributeError:
            mv_director = None
        # print(mv_director)

        # 출연진
        try:
            mv_cast_list = mv_info_area.find_all('dl')[1].find('dd').find_all('a')
            # print(mv_cast_list)
            mv_cast = ''
            for i in range(len(mv_cast_list)):
                mv_cast += mv_cast_list[i].getText()
                if i!=(len(mv_cast_list)-1):
                    mv_cast += ', '
        except AttributeError:
            mv_cast = None
        # print(mv_cast)

        # 이미지 주소
        # content > div.article > div.mv_info_area > div.poster > a > img
        try:
            mv_img = soup_body.find(class_='mv_info_area').find(class_='poster').find('a').find('img').get('src')
        except AttributeError:
            mv_img = None
        # print(mv_img)

        # 시놉시스
        try:
            synopsis_title = soup_body.find(class_="h_tx_story").getText()
        except AttributeError:
            synopsis_title = None
        try:
            content = soup_body.find('div', class_="story_area").find('p', class_='con_tx')
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

        try:
            trailer_url = naver_base_url + soup_body.find(class_="article").find(class_="section_group section_group_frst").find_all(class_="obj_section")[3].find('li').find('a').get('href')
        except:
            trailer_url = None
        # print(trailer_url)
        try:
            trailer_thumbnail = soup_body.find(class_="article").find(class_="section_group section_group_frst").find_all(class_="obj_section")[2].find(class_="viewer_img").find('img').get('src')
        except:
            trailer_thumbnail = None

        # 평점 사이트 이동
        # movieEndTabMenu > li:nth-child(5) > a
        score_url_tail = soup_body.find(class_="end_sub_tab").find_all('li')[4].find('a').get('href')[1:]
        # print(score_url_tail)
        # print(naver_base_url + '/movie/bi/mi' + score_url_tail)
        score_url = urlopen(naver_base_url + '/movie/bi/mi' + score_url_tail)
        score_bs = BeautifulSoup(score_url, 'html.parser')
        score_body = score_bs.body

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

        # 평론가
        try:
            star_score = score_body.find(class_="score_special").find(class_="score_result")
            lis = star_score.find_all('li')
            for li in lis:
                try:
                    score = int(li.find('div', class_='star_score').find('em').get_text())
                except AttributeError:
                    score = None
                try:
                    critic_str = li.find('div', class_='score_reple').find('p').get_text()
                except AttributeError:
                    critic_str = None
                try:
                    critic_name = li.find('div', class_='score_reple').find('dd').get_text().split(' ')[1].split('\r')[
                        0]
                except AttributeError:
                    critic_name = None
                critic_content = None
                critic_list.append((critic_name, critic_str, score, critic_content))
            # whole_list.append(critic_list)
        except AttributeError:
            print("No Critics")

        year = mv_date[0:4]
        parsed_title = mv_title + '_' + year
        movie = Movie(no, mv_img, parsed_title, mv_director, mv_cast, mv_genre, mv_time, mv_date, -1, critic_list, synopsis_title,
                      content, eng_title, rating)
        no += 1
        movie.set_trailer(trailer_url, trailer_thumbnail)
        # print(movie.trailer_url)
        # print(movie.trailer_thumbnail)
        movie.set_naver_score(movie.get_score_average())
        # movie.set_metascore(getMetascore(movie))
        movielist.append(movie)
        print(movie.title)
    return movielist





# base_url = "https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20190723"
# movie_score_list = []
# for i in range(1, 2):
#     print(base_url + "&page=" + str(i))
#     movie_score_list += getMovieByScore(urlopen(base_url + "&page=" + str(i)))