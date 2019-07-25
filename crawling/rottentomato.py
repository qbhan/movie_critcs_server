from urllib.request import urlopen
import urllib.request
# from currentmovie import *
from bs4 import BeautifulSoup
from movie import *

def getTomato(movie_list):
    tomato_base_url = 'https://www.rottentomatoes.com/m/'
    used_url = ''
    new_movie_list = []
    for movie_info in movie_list:
        if not movie_info.eng_title:
            # return None
            continue
        if not movie_info.eng_title[-1].isdigit():
            continue
            # return None
        movie_title_list = movie_info.eng_title.split(',')
        if len(movie_title_list) == 1:
            continue
            # return None
        elif len(movie_title_list) == 2:
            eng_title = movie_title_list[-2]
        elif len(movie_title_list) == 3:
            eng_title = movie_title_list[-2][1:]

        eng_title = eng_title.replace(': ', '_')
        eng_title = eng_title.replace('&', 'and')
        eng_title = eng_title.replace('...', '_')
        eng_title = eng_title.replace("'", "")
        eng_title = eng_title.replace("' ", "")
        eng_title = eng_title.replace("’", "")
        eng_title = eng_title.replace('"', "")
        eng_title = eng_title.replace('" ', "")
        eng_title = eng_title.replace(' - ', '_')
        eng_title = eng_title.replace('-', '_')
        eng_title = eng_title.replace(' ', "_")
        eng_title = eng_title.replace(' ', '')
        movie_url_1 = eng_title.lower() + '_' + movie_title_list[-1][1:]
        movie_url_2 = eng_title.lower()
        # print(movie_url_1, movie_url_2)

        req = urllib.request.Request(tomato_base_url + movie_url_1, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            # print(tomato_base_url + movie_url_1)
            url = urlopen(req)
            used_url = tomato_base_url + movie_url_1
            bs = BeautifulSoup(url, 'html.parser')
            body = bs.body

        except:
            req = urllib.request.Request(tomato_base_url + movie_url_2, headers={'User-Agent': 'Mozilla/5.0'})
            try:
                # print(tomato_base_url + movie_url_2)
                url = urlopen(req)
                used_url = tomato_base_url + movie_url_2
                bs = BeautifulSoup(url, 'html.parser')
                body = bs.body

            except:
                bs = None

        if bs:
            # 토마토지수 가져오기
            try:
                # tomato_meter_link > span.mop-ratings-wrap__percentage
                score = bs.find(class_="mop-ratings-wrap__half").find(class_="mop-ratings-wrap__percentage").getText().split()
                score = int(score[0][:-1])
            except AttributeError:
                score = None

            # 토마토 평요약 가져오기
            # topSection > div.col-sm-17.col-xs-24.score-panel-wrap > div.mop-ratings-wrap.score_panel.js-mop-ratings-wrap > section > p
            try:
                shortview = bs.find(class_="col-sm-17 col-xs-24 score-panel-wrap").find('p').getText()
            except:
                shortview = None
            # print(shortview)
        else:
            score = None
            shortview = None

        if score:
            movie_info.set_tomato(score)

        review_list = []
        review_url = None
        if bs:
            # 평론 가져오기
            review_url = used_url + '/reviews'
            # print(review_url)
            # print(review_url)
            review_list = []
            review = None
            review_reviewer = None
            review_full_url = None
            review_tomato = None
            try:
                review_body = BeautifulSoup(urlopen(review_url), 'html.parser')
                print("review opened")
                review_body_list = review_body.find(class_="review_table").find_all(class_="row review_table_row")
                print("review body opened")
                for reviews in review_body_list:
                    if reviews.find(class_="glyphicon glyphicon-star"):
                        try:
                            review = " ".join(reviews.find(class_="the_review").getText().split())
                        except:
                            review = None
                        # print(review)
                        try:
                            review_full_url = reviews.find(class_="small subtle review-link").find('a').get('href')
                        except:
                            review_full_url = None
                        # print(review_full_url)
                        try:
                            review_reviewer = reviews.find(class_="unstyled bold articleLink").getText()
                        except:
                            review_reviewer = None
                        # print(review_reviewer)
                        try:
                            if 'fresh' in reviews.find(class_="col-xs-16 review_container").find('div').get('class')[-1]:
                                review_tomato = 'fresh'
                            else:
                                review_tomato = 'rotten'
                        except:
                            review_tomato = None
                        review_list.append((review_reviewer, review, review_tomato, review_full_url))

            except:
                review_list = []

        # print(score)
        #
        # print(review_url)
        movie_info.set_rottentomato(score, review_list, review_url)
        movie_info.set_shortview(shortview)
        # print(movie_info.title)
        # print(review_list)
        print(type(movie_info.tomato))
        # print(movie_info.short_view)
        # print(movie_info.tomato)
        # print(movie_info.tomato_critic)
        # print(movie_info.tomato_critic_url)
        new_movie_list.append(movie_info)
        # print(score)
        # print(review_list)
    return new_movie_list


# current_list = getCurrentMovie(urlopen("https://movie.naver.com/movie/running/current.nhn"))
# title_score_list = getTomato(current_list)
# getOneTomato('https://www.rottentomatoes.com/m/spider_man_far_from_home_2019')
