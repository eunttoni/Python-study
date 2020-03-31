import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client.dbsparta.movies

def scrap_and_insert():
    # URL을 읽어서 HTML를 받아오고,
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20200303',headers=headers)

    # HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
    soup = BeautifulSoup(data.text, 'html.parser')

    # select를 이용해서, tr들을 불러오기
    movies = soup.select('#old_content > table > tbody > tr')

    # movies (tr들) 의 반복문을 돌리기
    rank = 1
    for movie in movies:
        # movie 안에 a 가 있으면,
        a_tag = movie.select_one('td.title > div > a')
        if a_tag is not None:
            title = a_tag.text
            star = movie.select_one('td.point').text
            print(rank,title,star)
            # db.movies.insert_one({'rank':rank, 'title':title, 'star':star})
            # movies 컬렉션에 데이터 insert
            rank += 1


def find_and_print():
    all_movies = list(db.find())
    for movie in all_movies:
        print(movie['title'], movie['star'])

# 그린 북의 평점 가져오기
def find_movie():
    movie = db.find_one({'title':'그린 북'})
    print(movie['star'])

# 영화 덕구와 같은 평점인 영화 제목 뽑아오기
def find_movie_star():
    movie = db.find_one({'title': '덕구'})
    star = movie['star']
    all_movie = list(db.find({'star': star}))
    for a in all_movie:
        print(a['title'])

# 영화 덕구와 같은 평점인 영화들의 평점을 0점으로 만들기
def find_movie_star_jero():
    movie = db.find_one({'title': '덕구'})
    star = movie['star']
    all_movie = list(db.find({'star': star}))
    for a in all_movie:
        db.update_one({'title': a['title']}, {'$set': {'star': 0}})
        print(a['title'],a['star'])

