import requests
import bs4

r = requests.get("https://movie.naver.com/movie/sdb/rank/rmovie.nhn")
soap = bs4.BeautifulSoup(r.text, 'html.parser')

aTags = soap.select('div.tit3 a')
for a in aTags :
    print(a.text)
    # a.text : a태그 안에 텍스트 정보 
    # a['title'] : a태그 안에 title 속성 정보
