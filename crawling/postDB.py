from currentmovie import *
from premovie import *
from moviebyscore import *
from metacritic import *
from rottentomato import *
import psycopg2
from urllib.request import urlopen

current_url = urlopen("https://movie.naver.com/movie/running/current.nhn")
pre_url = urlopen("https://movie.naver.com/movie/running/premovie.nhn")
get_score_base_url = "https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20190723"
page_url = "&page="
# movies = getCurrentMovie(current_url) + getPreMovie(pre_url) + getMovieByScore(get_score_url)
current_movie = getCurrentMovie(current_url)
pre_movie = getPreMovie(pre_url)
# old_movie = getMovieByScore(get_score_url)
movies = current_movie + pre_movie
for i in range(1, 11):
    movies += getMovieByScore(urlopen(get_score_base_url + page_url + str(i)))
# print(len(current_movie))
movies = getTomato(movies)
movies = getMetascore(movies)
# print(len(movies))
try:
    # PostgreSQL로 연결
    conn_string = "host='localhost', port='5432', database='postgres', user='postgres', password='1234'"
    connection = psycopg2.connect(host='localhost', port='5432', database='week4db', user='postgres', password='1234')
    cursor = connection.cursor()
    print(connection.get_dsn_parameters(), "\n")

    # PostgreSQL insert 명령어들
    movies_clear_query = """DELETE FROM movies"""
    movies_init_sequence_query = """ALTER SEQUENCE movies_movie_id_seq RESTART WITH 1"""
    # movies_insert_query = """INSERT INTO movies (img, title, directors, casts, genres, time, date, status,
    # naver_score, synopsis_title, synopsis_content) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING
    # movie_id """
    movies_insert_query = """INSERT INTO movies(img, title, directors, casts, genres, time, date, status, naver_score, synopsis_title, synopsis_content, eng_title, rating, metascore, rottentomato, meta_url, tomato_url, trailer_url, trailer_thumbnail, shortview) select %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s WHERE NOT EXISTS (SELECT title FROM movies WHERE title = %s) RETURNING movie_id """
    genres_insert_query = """INSERT INTO movies_genres (movie_id, genre) VALUES (%s, %s)"""
    naver_insert_query = """INSERT INTO movies_critics (movie_id, name, title, score, content) VALUES (%s, %s, %s, 
    %s, %s) """
    meta_insert_query = """INSERT INTO movies_meta (movie_id, name, content, score, url) VALUES (%s, %s, %s, 
    %s, %s)"""
    tomato_insert_query = """INSERT INTO movies_tomato (movie_id, name, content, score, url) VALUES (%s, %s, %s, 
    %s, %s)"""

    # 네이버에서 현재개봉/개봉예정작 받아오기
    # current_url = urlopen("https://movie.naver.com/movie/running/current.nhn")
    # pre_url = urlopen("https://movie.naver.com/movie/running/premovie.nhn")
    # get_score_url = urlopen("https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20190721")
    # movies = getCurrentMovie(current_url) + getPreMovie(pre_url) + getMovieByScore(get_score_url)
    # movies = getPreMovie(pre_url) + getMovieByScore(get_score_url)
    # 동기화 하기 전에 movies, movies_genres 초기화
    cursor.execute(movies_clear_query)
    connection.commit()
    cursor.execute(movies_init_sequence_query)
    connection.commit()
    print("DATABASE CLEARED")

    # insert movies
    for i in range(len(movies)):
        movie_to_insert = (movies[i].image, movies[i].title, movies[i].directors, movies[i].casts, movies[i].genres,
                           movies[i].time, movies[i].date, movies[i].status, movies[i].naver_score, movies[i].syn_title, movies[i].syn_content, movies[i].eng_title, movies[i].rating, movies[i].metascore, movies[i].tomato, movies[i].meta_critic_url, movies[i].tomato_critic_url, movies[i].trailer_url, movies[i].trailer_thumbnail, movies[i].short_view, movies[i].title)
        movies[i].print_info()
        cursor.execute(movies_insert_query, movie_to_insert)
        print("MOVIE SUCCESSFULLY INSERTED")
        movie_id = cursor.fetchall()
        if not movie_id:
            continue
        movie_id = movie_id[0][0]
        print("Inserted Id : " + str(movie_id))
        connection.commit()
        # print("pass2")
        # print(movie_id, type(movie_id))
        genre_list = movies[i].genres.split(',')
        # print("pass3")
        critics_list = movies[i].naver_critic
        # print("pass4")
        # print(genre_list)
        for j in range(len(genre_list)):
            genre_to_insert = (movie_id, genre_list[j])
            cursor.execute(genres_insert_query, genre_to_insert)
            connection.commit()
        print("GENRES SUCCESSFULLY INSERTED")
        for k in range(len(critics_list)):
            critics_to_insert = (movie_id, critics_list[k][0], critics_list[k][1], critics_list[k][2], critics_list[k][3])
            # print(critics_to_insert)
            cursor.execute(naver_insert_query, critics_to_insert)
            connection.commit()
        print("CRITICS SUCCESSFULLY INSERTED")
        meta_list = movies[i].meta_critic
        for x in range(len(meta_list)):
            meta_to_insert = (movie_id, meta_list[x][0], meta_list[x][1], meta_list[x][2], meta_list[x][3])
            cursor.execute(meta_insert_query, meta_to_insert)
            connection.commit()
        print("METACRITIC SUCCESSFULLY INSERTED")
        tomato_list = movies[i].tomato_critic
        for y in range(len(tomato_list)):
            tomato_to_insert = (movie_id, tomato_list[y][0], tomato_list[y][1], tomato_list[y][2], tomato_list[y][3])
            cursor.execute(tomato_insert_query, tomato_to_insert)
            connection.commit()
        print("ROTTENTOMATO SUCCESSFULLY INSERTED")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to Database", error)
finally:
    if(connection):
        cursor.close()
        connection.close()
        print("Database connection is closed")

