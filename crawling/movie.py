class Movie:
    def __init__(self, num, image, title, directors, casts, genres, time, date, status, critic_list, syn_title, syn_content, eng_title, rating):
        self.image = image
        self.title = title
        self.directors = directors
        self.casts = casts
        self.genres = genres
        self.time = time
        self.date = date
        self.num = num
        self.status = status
        # 네이버평론 = (이름, 제목, 점수, 내용)
        self.naver_critic = critic_list
        self.naver_score = None
        # 메타크리틱 평론
        self.metascore = None
        self.meta_critic = None
        self.meta_critic_url = None
        # 로튼토마토 평론
        self.tomato = None
        self.tomato_critic = None
        self.tomato_critic_url = None
        self.syn_title = syn_title
        self.syn_content = syn_content
        self.eng_title = eng_title
        self.rating = rating

    def set_naver_score(self, score):
        self.naver_score = score

    def set_metascore(self, score):
        self.metascore = score

    def set_metacritic(self, score, critic_list, critic_url):
        self.metascore = score
        self.meta_critic = critic_list
        self.meta_critic_url = critic_url

    def set_tomato(self, score):
        self.tomato = score

    def set_rottentomato(self, score, critic_list, critic_url):
        self.tomato = score
        self.tomato_critic = critic_list
        self.tomato_critic_url = critic_url

    def get_score_average(self):
        total_score = 0
        total_num = 0
        # for i in range(len(self.report_list)):
        #     if self.report_list[i][2]:
        #         total_score += self.report_list[i][2]
        #         total_num += 1
        for j in range(len(self.naver_critic)):
            if self.naver_critic[j][2]:
                total_score += self.naver_critic[j][2]
                total_num += 1
        if total_num:
            avg_score = round(total_score / total_num, 2)
        else:
            avg_score = float(0.00)
        return avg_score

    def print_info(self):
        print("==========================")
        print("No. ", self.num)
        if self.image:
            print("포스터 :\t", self.image)
        else:
            print("포스터 :\t 정보 없음")
        if self.title:
            print("영화 제목 : \t", self.title)
        else:
            print("영화 제목 :\t 정보 없음")
        if len(self.directors)!=0:
            print("제작 감독 : \t", self.directors)
        else:
            print("제작 감독 :\t 정보 없음")
        if len(self.casts)!=0:
            print("출연 배우 :\t", self.casts)
        else:
            print("출연 배우 :\t 정보 없음")
        if len(self.genres)!=0:
            print("장르 :\t", self.genres)
        else:
            print("장르 :\t 정보 없음")
        if len(self.time)!=0:
            print("상영 시간 :\t", self.time)
        else:
            print("상영 시간 :\t 정보 없음")
        if len(self.date)!=0:
            print("개봉일 :\t", self.date)
        else:
            print("개봉일 :\t 정보 없음")
