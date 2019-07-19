from urllib.request import urlopen

from bs4 import BeautifulSoup

def getCurrentMovieScore(naver_url):
    naver_base_url = 'https://movie.naver.com'
    naver_score_list = []
    naver_bs = BeautifulSoup(naver_url, 'html.parser')
    body = naver_bs.body

    target = body.find(class_="lst_detail_t1")
    print(type(target))
    list = target.find_all('li')
    ######################################################################################

    print(naver_base_url + list[0].find(class_="star").find("a").get('href'))
    score_url = urlopen(naver_base_url + list[0].find(class_="star").find("a").get('href'))
    score_bs = BeautifulSoup(score_url, 'html.parser')
    score_body = score_bs.body

    # content > div.article > div.section_group.section_group_frst > div:nth-child(4) > div > div.title_area > div
    for child in score_body.find(class_="score_special").find(class_="star_score").children:
        child.get("num6")
    # score_box = target_score.find('st_off')
    # print(score_box)

    # for n in range(len(list)):
    #     movie_url = list[n].find(class_="tit").find("a")


naver_url = urlopen("https://movie.naver.com/movie/running/current.nhn")
getCurrentMovieScore(naver_url)