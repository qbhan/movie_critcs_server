class Movie:
    def __init__(self, num, image, title, directors, casts, genres, time, date, status):
        self.image = image
        self.title = title
        self.directors = directors
        self.casts = casts
        self.genres = genres
        self.time = time
        self.date = date
        self.num = num
        self.status = status
        self.naver_score = 0

    def set_Naver_Score(self, score):
        self.naver_score = score

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
