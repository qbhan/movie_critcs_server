from currentmovie import *
from premovie import *
import psycopg2
from urllib.request import urlopen

try:
    # PostgreSQL로 연결
    conn_string = "host='localhost', port='5432', database='postgres', user='postgres', password='1234'"
    connection = psycopg2.connect(host='localhost', port='5432', database='week4db', user='postgres', password='1234')
    cursor = connection.cursor()
    print(connection.get_dsn_parameters(), "\n")

    # PostgreSQL insert 명령어들
    movies_clear_query = """DELETE FROM movies"""
    movies_init_sequence_query = """ALTER SEQUENCE movies_movie_id_seq RESTART WITH 1"""
    movies_insert_query = """INSERT INTO movies
    (img, title, directors, casts, genres, time, date, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING movie_id"""
    genres_insert_query = """INSERT INTO movies_genres (movie_id, genre) VALUES (%s, %s)"""


    # 네이버에서 현재개봉/개봉예정작 받아오기
    current_url = urlopen("https://movie.naver.com/movie/running/current.nhn")
    pre_url = urlopen("https://movie.naver.com/movie/running/premovie.nhn")
    movies = getCurrentMovie(current_url) + getPreMovie(pre_url)

    # 동기화 하기 전에 movies, movies_genres 초기화
    cursor.execute(movies_clear_query)
    connection.commit()
    cursor.execute(movies_init_sequence_query)
    connection.commit()


    # insert movies
    for i in range(len(movies)):
        movie_to_insert = (movies[i].image, movies[i].title, movies[i].directors, movies[i].casts, movies[i].genres,
                           movies[i].time, movies[i].date, movies[i].status)
        cursor.execute(movies_insert_query, movie_to_insert)
        movie_id = cursor.fetchall()[0][0]
        connection.commit()
        # print(movie_id, type(movie_id))
        genre_list = movies[i].genres.split(',')
        # print(genre_list)
        for j in range(len(genre_list)):
            genre_to_insert = (movie_id, genre_list[j])
            cursor.execute(genres_insert_query, genre_to_insert)
            connection.commit()
            print("SUCCESSFULLY INSERTED")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to Database", error)
finally:
    if(connection):
        cursor.close()
        connection.close()
        print("Database connection is closed")

