from urllib.request import urlopen
import urllib.request
from bs4 import BeautifulSoup
# from currentmovie import *
from movie import *

def getMetascore(movie_list):
    meta_base_url = 'https://www.metacritic.com/movie/'
    new_movie_list = []
    for movie_info in movie_list:
        if not movie_info.eng_title:
            # return None
            continue
        if not movie_info.eng_title[-1].isdigit():
            # return None
            continue
        movie_title_list = movie_info.eng_title.split(',')
        if len(movie_title_list) == 1:
            # return None
            continue
        elif len(movie_title_list) == 2:
            eng_title = movie_title_list[-2]
        elif len(movie_title_list) == 3:
            eng_title = movie_title_list[-2][1:]
        eng_title = eng_title.replace(': ', '-')
        eng_title = eng_title.replace(' & ', '-')

        eng_title = eng_title.replace("'", "")
        eng_title = eng_title.replace("' ", "")
        eng_title = eng_title.replace("’", "")
        eng_title = eng_title.replace('"', "")
        eng_title = eng_title.replace('" ', "")
        eng_title = eng_title.replace(' ', "-")
        eng_title = eng_title.replace(' ', '')
        movie_url_1 = eng_title.lower() + '-' + movie_title_list[-1][1:]
        movie_url_2 = eng_title.lower()
        # print(movie_url_1, movie_url_2)
        # print(meta_base_url+movie_url_1)
        # print(meta_base_url+movie_url_2)
        req = urllib.request.Request(meta_base_url+movie_url_1, headers={'User-Agent': 'Mozilla/5.0'})
        used_url = None
        # print("pass1")
        try:
            # print(meta_base_url + movie_url_1)
            url = urlopen(req)
            used_url = meta_base_url+movie_url_1
            bs = BeautifulSoup(url, 'html.parser')
            body = bs.body

        except:
                req = urllib.request.Request(meta_base_url + movie_url_2, headers={'User-Agent': 'Mozilla/5.0'})
                try:
                    # print(meta_base_url + movie_url_2)
                    url = urlopen(req)
                    used_url = meta_base_url + movie_url_2
                    bs = BeautifulSoup(url, 'html.parser')
                    body = bs.body

                except:
                    body = None

        # main_content > div.movie.product.summary > div.content_under_header > div > table > tbody > tr >
        # td.maskedcenter > div > table > tbody > tr > td.gu5.maskedbg > div > div > div.ms_wrapper > table > tbody > tr
        # > td.summary_right.pad_btm1 > a.metascore_anchor > span

        review_list = []
        if body:
            try:
                score = body.find(class_="movie product summary").find(class_="content_under_header").find(class_="metascore_anchor").find('span').getText()
            except AttributeError:
                score = None

            # 대표 평론 받아오기
            try:
                reviews_body_list = body.find(class_="critic_reviews2").find_all(class_="review pad_top2 pad_btm2")
                for reviews in reviews_body_list:
                    try:
                        review_score = reviews.find(class_="score_wrap").find('div').getText()
                    except:
                        review_score = None
                    # print(review_score)
                    try:
                        review_reviewer = " ".join(reviews.find(class_="author").find('a').getText().split())
                    except:
                        review_reviewer = None
                    # print(review_reviewer)
                    try:
                        review = " ".join(reviews.find(class_="summary").find('a').getText().split())
                    except:
                        review = None
                    # print(review)
                    try:
                        review_full_url = " ".join(reviews.find(class_="summary").find('a').get('href').split())
                    except:
                        review_full_url = None
                    # print(review_full_url)
                    review_list.append((review_reviewer, review, review_score, review_full_url))
            except:
                reviews_body_list = []
            # print(reviews_list)
        else:
            score = None

        # print(review_list)
        # if score:
        #     movie_info.set_metascore(score)
        movie_info.set_metacritic(score, review_list, used_url)
        print(movie_info.metascore)
        print(movie_info.meta_critic)
        print(movie_info.meta_critic_url)
        new_movie_list.append(movie_info)
    return new_movie_list

# current_list = getCurrentMovie(urlopen("https://movie.naver.com/movie/running/current.nhn"))
# title_score_list = getMetascore(current_list)